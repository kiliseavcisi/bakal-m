"""Dürbün + ChoCh + geri test stratejisinin geçmiş veride testi.

Kurallar (yükseliş; düşüş tam tersi):
  1) Üst TF'de (4h) dürbün: 🟥🟥🟩🟩, 2-3. mum gövdesi çizgiyi ihlal etmez.
  2) Dürbün tamamlandıktan sonra en fazla EXPIRE_BARS üst TF mumu içinde
     alt TF'de (15m) yukarı ChoCh (pivot 5/5, kapanış onayı).
     Bu sürede fiyat dürbün dibinin altında kapanırsa kurulum iptal.
  3) ChoCh seviyesi H, ChoCh hareketini başlatan dip L
     (kırılan pivot ile kırılım mumu arasındaki en düşük iğne).
     Stop = L'nin %STOP_BUFFER altı. Stop mesafesi > %MAX_RISK ise işlem yok.
  4) Geri test: ChoCh'tan sonra en fazla RETEST_BARS alt TF mumu içinde
     fiyat H'ye dokunur (%TOUCH_TOL tolerans) ve mum L'nin üstünde kapanır.
     - Dokunmadan fiyat 2R yukarı kaçarsa: kaçan fırsat.
     - Dokunan mum L'nin altında kapanırsa: geçersiz.
  5) Giriş:
     "kapanis" = geri test mumunun kapanışı (bildirim bu anda gelir; gerçekçi)
     "limit"   = H seviyesine önceden konmuş limit emir
  6) Hedef = giriş + TP_R × risk. Aynı mumda hem stop hem hedef varsa STOP sayılır.
     Komisyon+kayma: işlem başına toplam %FEE fiyat olarak düşülür.

Veri: {klasör}/15m/{COIN}.parquet ve {klasör}/4h/{COIN}.parquet
(sütunlar: date, open, high, low, close). Örnek kaynak:
huggingface.co/datasets/rogerdehe/klines-binance (futures/15m, futures/4h).

Kullanım:
    python backtest.py VERI_KLASORU [--entry kapanis|limit] [--last 100] [--csv sonuc.csv]
"""
from __future__ import annotations

import argparse
import bisect
import csv as csvmod
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path

from pattern import Candle, detect
from structure import structure_events

H4 = 4 * 3600 * 1000
M15 = 15 * 60 * 1000


@dataclass
class Params:
    expire_bars: int = 6
    retest_bars: int = 20
    touch_tol: float = 0.002
    stop_buffer: float = 0.002
    max_risk: float = 0.05
    tp_r: float = 2.0
    fee: float = 0.001
    max_hold_bars: int = 30 * 96  # 30 gün
    entry: str = "kapanis"
    lb: int = 5
    rb: int = 5


@dataclass
class Trade:
    coin: str
    direction: str
    durbun_time: str
    entry_time: str
    entry: float
    stop: float
    target: float
    risk_pct: float
    result: str  # HEDEF / STOP / SURE
    r: float  # komisyon dahil R
    exit_time: str
    bars_held: int


def load(path: Path) -> list[Candle]:
    import pandas as pd
    df = pd.read_parquet(path, columns=["date", "open", "high", "low", "close"])
    ts = (df["date"].astype("int64") // 10**6).tolist()
    if ts and ts[0] < 10**11:  # saniye/mikrosaniye farklılıkları
        ts = (df["date"].astype("int64") // 10**3).tolist()
    return [Candle(t, o, h, l, c) for t, o, h, l, c in
            zip(ts, df["open"], df["high"], df["low"], df["close"])]


def fmt_t(ms: int) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).strftime("%Y-%m-%d %H:%M")


def simulate(coin: str, h4: list[Candle], m15: list[Candle], p: Params, stats: dict) -> list[Trade]:
    times = [c.time for c in m15]
    events = [e for e in structure_events(m15, p.lb, p.rb, "close") if e.kind == "CHOCH"]
    ev_times = [e.time for e in events]
    used_events: set[int] = set()
    trades: list[Trade] = []

    for i in range(3, len(h4)):
        sig = detect(h4[i - 3:i + 1])
        if not sig:
            continue
        stats["durbun"] += 1
        up = sig.direction == "UP"
        start = h4[i].time + H4
        expires = start + p.expire_bars * H4
        invalid = min(c.low for c in sig.candles) if up else max(c.high for c in sig.candles)

        # 2) ChoCh bul
        k = bisect.bisect_left(ev_times, start)
        ev = None
        while k < len(events) and events[k].time < expires:
            if events[k].direction == sig.direction:
                ev = events[k]
                break
            k += 1
        if ev is None:
            stats["choch_yok"] += 1
            continue
        a = bisect.bisect_left(times, start)
        if any((m15[x].close < invalid) if up else (m15[x].close > invalid) for x in range(a, ev.index)):
            stats["iptal"] += 1
            continue
        if ev.index in used_events:
            stats["ayni_choch"] += 1
            continue
        used_events.add(ev.index)
        stats["choch"] += 1

        # 3) seviyeler
        H = ev.level
        seg = m15[ev.pivot_index:ev.index + 1]
        L = min(c.low for c in seg) if up else max(c.high for c in seg)
        stop = L * (1 - p.stop_buffer) if up else L * (1 + p.stop_buffer)
        if abs(H - stop) / H > p.max_risk:
            stats["risk_buyuk"] += 1
            continue

        # 4) geri test
        entry_i = None
        entry = None
        for n in range(ev.index + 1, min(ev.index + 1 + p.retest_bars, len(m15))):
            c = m15[n]
            touched = c.low <= H * (1 + p.touch_tol) if up else c.high >= H * (1 - p.touch_tol)
            if not touched:
                runaway = c.high >= H + p.tp_r * (H - stop) if up else c.low <= H - p.tp_r * (stop - H)
                if runaway:
                    break
                continue
            if (c.close <= L) if up else (c.close >= L):
                stats["geri_test_bozuldu"] += 1
                entry_i = -1
                break
            entry_i = n
            entry = c.close if p.entry == "kapanis" else H
            break
        if entry_i is None:
            stats["geri_test_yok"] += 1
            continue
        if entry_i == -1:
            continue
        risk = (entry - stop) if up else (stop - entry)
        if risk <= 0 or risk / entry > p.max_risk:
            stats["risk_buyuk"] += 1
            continue
        target = entry + p.tp_r * risk if up else entry - p.tp_r * risk

        # 5) sonuç
        result, exit_price, exit_i = "SURE", None, None
        first = entry_i if p.entry == "limit" else entry_i + 1
        for n in range(first, min(entry_i + 1 + p.max_hold_bars, len(m15))):
            c = m15[n]
            hit_stop = c.low <= stop if up else c.high >= stop
            hit_tp = (c.high >= target if up else c.low <= target) and n > entry_i
            if hit_stop:
                result, exit_price, exit_i = "STOP", stop, n
                break
            if hit_tp:
                result, exit_price, exit_i = "HEDEF", target, n
                break
        if exit_i is None:
            exit_i = min(entry_i + p.max_hold_bars, len(m15) - 1)
            exit_price = m15[exit_i].close
            if exit_i == len(m15) - 1 and exit_i < entry_i + p.max_hold_bars:
                stats["acik"] += 1
                continue  # veri bitti, hâlâ açık: sayma
        move = (exit_price - entry) if up else (entry - exit_price)
        r = (move - p.fee * entry) / risk
        stats["islem"] += 1
        trades.append(Trade(coin, sig.direction, fmt_t(h4[i].time), fmt_t(m15[entry_i].time),
                            entry, stop, target, round(100 * risk / entry, 2), result,
                            round(r, 3), fmt_t(m15[exit_i].time), exit_i - entry_i))
    return trades


def summarize(trades: list[Trade], title: str) -> None:
    n = len(trades)
    if not n:
        print(f"\n{title}: işlem yok")
        return
    wins = sum(t.result == "HEDEF" for t in trades)
    stops = sum(t.result == "STOP" for t in trades)
    other = n - wins - stops
    rs = [t.r for t in trades]
    eq = peak = dd = 0.0
    streak = max_streak = 0
    for t in trades:
        eq += t.r
        peak = max(peak, eq)
        dd = min(dd, eq - peak)
        streak = streak + 1 if t.r < 0 else 0
        max_streak = max(max_streak, streak)
    gross_w = sum(r for r in rs if r > 0)
    gross_l = -sum(r for r in rs if r < 0)
    print(f"\n=== {title} ===")
    print(f"İşlem: {n} | Hedef: {wins} | Stop: {stops} | Süre doldu: {other}")
    print(f"Başarı oranı: %{100 * wins / n:.1f}")
    print(f"Toplam: {sum(rs):+.1f}R | İşlem başı ortalama: {sum(rs) / n:+.3f}R")
    print(f"Profit factor: {gross_w / gross_l:.2f}" if gross_l else "Profit factor: ∞")
    print(f"En uzun stop serisi: {max_streak} | En büyük düşüş: {dd:.1f}R")
    print(f"Ortalama stop mesafesi: %{sum(t.risk_pct for t in trades) / n:.2f}")
    for d in ("UP", "DOWN"):
        sub = [t for t in trades if t.direction == d]
        if sub:
            w = sum(t.result == "HEDEF" for t in sub)
            print(f"  {'Yükseliş' if d == 'UP' else 'Düşüş'}: {len(sub)} işlem, başarı %{100 * w / len(sub):.1f}, "
                  f"toplam {sum(t.r for t in sub):+.1f}R")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("data_dir")
    ap.add_argument("--entry", default="kapanis", choices=["kapanis", "limit"])
    ap.add_argument("--tp", type=float, default=2.0, help="hedef (R)")
    ap.add_argument("--last", type=int, default=100, help="özet için son N işlem")
    ap.add_argument("--csv", help="tüm işlemleri CSV'ye yaz")
    ap.add_argument("--coins", help="virgülle; boşsa klasördeki hepsi")
    args = ap.parse_args()

    p = Params(entry=args.entry, tp_r=args.tp)
    root = Path(args.data_dir)
    coins = args.coins.split(",") if args.coins else sorted(f.stem for f in (root / "15m").glob("*.parquet"))
    stats = dict.fromkeys(["durbun", "choch_yok", "iptal", "ayni_choch", "choch", "risk_buyuk",
                           "geri_test_yok", "geri_test_bozuldu", "acik", "islem"], 0)
    trades: list[Trade] = []
    for coin in coins:
        h4, m15 = load(root / "4h" / f"{coin}.parquet"), load(root / "15m" / f"{coin}.parquet")
        t = simulate(coin, h4, m15, p, stats)
        print(f"{coin}: {len(t)} işlem")
        trades += t
    trades.sort(key=lambda t: t.entry_time)

    print("\nHuni:", ", ".join(f"{k}={v}" for k, v in stats.items()))
    print(f"Giriş: {p.entry} | Hedef: {p.tp_r}R | Başabaş başarı oranı ≈ %{100 / (1 + p.tp_r):.1f} (komisyon hariç)")
    summarize(trades[-args.last:], f"SON {args.last} İŞLEM")
    summarize(trades, "TÜM İŞLEMLER")
    by_year: dict[str, list[Trade]] = {}
    for t in trades:
        by_year.setdefault(t.entry_time[:4], []).append(t)
    print("\nYıllara göre:")
    for y, ts in sorted(by_year.items()):
        w = sum(t.result == "HEDEF" for t in ts)
        print(f"  {y}: {len(ts):4d} işlem, başarı %{100 * w / len(ts):5.1f}, toplam {sum(t.r for t in ts):+7.1f}R")
    if args.csv:
        with open(args.csv, "w", newline="", encoding="utf-8") as f:
            w = csvmod.DictWriter(f, fieldnames=list(asdict(trades[0]).keys()))
            w.writeheader()
            w.writerows(asdict(t) for t in trades)
        print(f"\nCSV: {args.csv}")


if __name__ == "__main__":
    main()
