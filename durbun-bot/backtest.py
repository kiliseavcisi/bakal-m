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
from strategy import (ACTIVE, POZISYONDA, SURE, Params, advance_to_entry, close_trade,
                      manage_position, new_setup, risk_pct)
from structure import structure_events

H4 = 4 * 3600 * 1000
M15 = 15 * 60 * 1000


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
    events = structure_events(m15, p.lb, p.rb, "close")
    times = [c.time for c in m15]
    used_events: set[int] = set()
    trades: list[Trade] = []

    for i in range(3, len(h4)):
        sig = detect(h4[i - 3:i + 1])
        if not sig:
            continue
        stats["durbun"] += 1
        s = advance_to_entry(new_setup(sig, H4), m15, events, p, M15)
        if s.choch is not None and s.stage != "iptal":
            if s.choch.index in used_events:
                stats["ayni_choch"] += 1
                continue
            used_events.add(s.choch.index)
            stats["choch"] += 1
        if s.stage in ACTIVE and s.stage != POZISYONDA:
            stats["acik"] += 1  # veri bitti
            continue
        if s.stage != POZISYONDA and s.stage not in ("HEDEF", "STOP"):
            stats[s.stage] += 1
            continue
        if s.stage == POZISYONDA:
            after = m15[s.entry_index + 1:s.entry_index + 1 + p.max_hold_bars]
            manage_position(s, after, p)
            if s.stage == POZISYONDA:
                if len(after) < p.max_hold_bars:
                    stats["acik"] += 1  # veri bitti, hâlâ açık: sayma
                    continue
                close_trade(s, SURE, after[-1].close, after[-1].time, p)
        stats["islem"] += 1
        exit_i = bisect.bisect_left(times, s.exit_time)
        trades.append(Trade(coin, s.direction, fmt_t(h4[i].time), fmt_t(s.entry_time),
                            s.entry, s.stop, s.target, round(risk_pct(s), 2), s.stage,
                            round(s.r, 3), fmt_t(s.exit_time), exit_i - s.entry_index))
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
