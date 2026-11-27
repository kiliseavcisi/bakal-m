"""Canlı kâğıt üstünde test (paper trading): gerçek para yok.

Şu anda oluşan fiyatlarla dürbün → alt TF ChoCh → geri test → giriş
zincirini takip eder. Kurallar backtest.py ile birebir aynıdır (strategy.py).

Telegram bildirimleri:
  ⏳ ChoCh geldi, geri test bekleniyor  (seviye, stop, planlanan hedef)
  🎯 GİRİŞ                               (giriş, stop, hedef)
  ✅ HEDEF / ❌ STOP                      (sonuç + o ana kadarki toplam istatistik)

Kapanan işlemler canli_islemler.csv dosyasına yazılır.

Kullanım:
    python canli_test.py            # çalıştır (PC açık kaldıkça)
    python canli_test.py --rapor    # şimdiye kadarki sonuçları göster
"""
from __future__ import annotations

import argparse
import csv as csvmod
import json
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import data
from bot import Telegram, csv, load_env
from pattern import detect
from strategy import (ACTIVE, CHOCH_BEKLENIYOR, GERI_TEST_BEKLENIYOR, HEDEF, POZISYONDA, STOP,
                      SURE, Params, Setup, advance_to_entry, close_trade, manage_position,
                      new_setup, risk_pct)
from structure import structure_events

log = logging.getLogger("canli")
HERE = Path(__file__).parent
STATE_FILE = HERE / "canli_state.json"
TRADES_FILE = HERE / "canli_islemler.csv"
FIELDS = ["sembol", "yon", "durbun_zamani", "giris_zamani", "giris", "stop", "hedef",
          "risk_yuzde", "sonuc", "r", "cikis_zamani"]


# ---------------------------------------------------------------- yardımcılar
def fmt(x: float) -> str:
    s = f"{x:,.8f}" if abs(x) < 1 else f"{x:,.4f}"
    return s.rstrip("0").rstrip(".")


def now_ms() -> int:
    return int(time.time() * 1000)


class Cfg:
    def __init__(self) -> None:
        self.symbols = csv("BINANCE_SYMBOLS", "ALL")
        self.top_n = int(os.getenv("TOP_N", "100"))
        self.quote = os.getenv("QUOTE", "USDT")
        self.htf = os.getenv("HTF", "4h")
        self.ltf = os.getenv("LTF", "15m")
        self.directions = {d.upper() for d in csv("DIRECTIONS", "UP,DOWN")}
        self.strict = os.getenv("STRICT_WICKS", "0") == "1"
        self.every = int(os.getenv("CHECK_EVERY_SECONDS", "60"))
        self.workers = int(os.getenv("MAX_WORKERS", "8"))
        self.tz = ZoneInfo(os.getenv("TIMEZONE", "Europe/Istanbul"))
        self.notify_choch = os.getenv("NOTIFY_CHOCH", "1") == "1"
        ltf_ms = data.INTERVAL_MS[self.ltf]
        self.p = Params(
            expire_bars=int(os.getenv("SETUP_EXPIRE_BARS", "6")),
            retest_bars=int(os.getenv("RETEST_BARS", "20")),
            touch_tol=float(os.getenv("TOUCH_TOL", "0.002")),
            stop_buffer=float(os.getenv("STOP_BUFFER", "0.002")),
            max_risk=float(os.getenv("MAX_RISK", "0.05")),
            tp_r=float(os.getenv("TP_R", "2")),
            fee=float(os.getenv("FEE", "0.001")),
            max_hold_bars=int(30 * 86_400_000 / ltf_ms),
            entry=os.getenv("ENTRY", "kapanis"),
            lb=int(os.getenv("PIVOT_LB", "5")),
            rb=int(os.getenv("PIVOT_RB", "5")),
        )

    def when(self, ms: int) -> str:
        return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).astimezone(self.tz).strftime("%d.%m %H:%M")


# ---------------------------------------------------------------- durum
def load_state() -> dict:
    try:
        st = json.loads(STATE_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        st = {}
    st.setdefault("started_at", now_ms())
    st.setdefault("bucket", None)
    st.setdefault("setups", {})
    st.setdefault("used_choch", [])
    return st


def save_state(st: dict) -> None:
    st["used_choch"] = st["used_choch"][-2000:]
    STATE_FILE.write_text(json.dumps(st, indent=1))


def to_dict(s: Setup) -> dict:
    d = asdict(s)
    d.pop("choch")
    return d


def from_dict(d: dict) -> Setup:
    return Setup(**{k: v for k, v in d.items() if k in Setup.__dataclass_fields__})


def read_trades() -> list[dict]:
    if not TRADES_FILE.exists():
        return []
    with open(TRADES_FILE, encoding="utf-8") as f:
        return list(csvmod.DictReader(f))


def stats_line() -> str:
    rows = read_trades()
    if not rows:
        return "Henüz kapanan işlem yok."
    n = len(rows)
    w = sum(r["sonuc"] == HEDEF for r in rows)
    tot = sum(float(r["r"]) for r in rows)
    return f"Toplam {n} işlem · Hedef {w} · Stop {n - w} · Başarı %{100 * w / n:.1f} · {tot:+.2f}R"


# ---------------------------------------------------------------- mesajlar
def tv(symbol: str) -> str:
    return f"<a href=\"https://www.tradingview.com/chart/?symbol=BINANCE:{symbol}\">grafik</a>"


def msg_choch(rec: dict, s: Setup, cfg: Cfg) -> str:
    up = s.up
    plan_risk = abs(s.H - s.stop)
    plan_tp = s.H + cfg.p.tp_r * plan_risk if up else s.H - cfg.p.tp_r * plan_risk
    return (f"⏳ <b>{rec['symbol']}</b> {'YÜKSELİŞ' if up else 'DÜŞÜŞ'} · {cfg.htf} dürbün → {cfg.ltf} ChoCh\n"
            f"Geri test bekleniyor: <code>{fmt(s.H)}</code>\n"
            f"Stop: <code>{fmt(s.stop)}</code> · Hedef ≈ <code>{fmt(plan_tp)}</code> ({cfg.p.tp_r:g}R)\n"
            f"{tv(rec['symbol'])} · <i>kâğıt üstünde test</i>")


def msg_entry(rec: dict, s: Setup, cfg: Cfg) -> str:
    up = s.up
    return (f"🎯 <b>GİRİŞ — {rec['symbol']} {'LONG 🟢' if up else 'SHORT 🔴'}</b>\n"
            f"{cfg.htf} dürbün → {cfg.ltf} ChoCh → geri test ({cfg.when(s.entry_time)})\n"
            f"Giriş: <code>{fmt(s.entry)}</code>\n"
            f"Stop: <code>{fmt(s.stop)}</code> (−%{risk_pct(s):.2f})\n"
            f"Hedef: <code>{fmt(s.target)}</code> ({cfg.p.tp_r:g}R)\n"
            f"{tv(rec['symbol'])} · <i>kâğıt üstünde test, gerçek işlem değil</i>")


def msg_result(rec: dict, s: Setup, cfg: Cfg) -> str:
    icon = {"HEDEF": "✅ HEDEF", "STOP": "❌ STOP", "SURE": "⌛ SÜRE DOLDU"}[s.stage]
    return (f"{icon} — <b>{rec['symbol']}</b> {'LONG' if s.up else 'SHORT'} · {s.r:+.2f}R\n"
            f"Giriş <code>{fmt(s.entry)}</code> → çıkış <code>{fmt(s.exit_price)}</code> ({cfg.when(s.exit_time)})\n"
            f"📊 {stats_line()}")


# ---------------------------------------------------------------- motor
class Live:
    def __init__(self, cfg: Cfg, tg: Telegram, st: dict):
        self.cfg, self.tg, self.st = cfg, tg, st
        self._uni: list[str] = []
        self._uni_at = 0.0

    def universe(self) -> list[str]:
        if self._uni and time.time() - self._uni_at < 6 * 3600:
            return self._uni
        if [s.upper() for s in self.cfg.symbols] == ["ALL"]:
            try:
                self._uni = data.binance_universe(self.cfg.quote, self.cfg.top_n)
            except Exception as e:
                log.error("Parite listesi alınamadı: %s", e)
                return self._uni
        else:
            self._uni = [s.upper() for s in self.cfg.symbols]
        self._uni_at = time.time()
        log.info("Taranan parite: %d", len(self._uni))
        return self._uni

    # 1) dürbün taraması
    def scan(self) -> None:
        step = data.INTERVAL_MS[self.cfg.htf]
        bucket = now_ms() // step
        if self.st["bucket"] == bucket:
            return
        # ilk çalıştırmada henüz süresi dolmamış dürbünleri de al
        look = self.cfg.p.expire_bars if self.st["bucket"] is None else 1
        syms = self.universe()
        if not syms:
            return
        with ThreadPoolExecutor(self.cfg.workers) as ex:
            found = sum(ex.map(lambda s: self._scan_symbol(s, look), syms))
        log.info("%s taraması: %d parite, yeni dürbün %d", self.cfg.htf, len(syms), found)
        self.st["bucket"] = bucket

    def _scan_symbol(self, symbol: str, look: int) -> int:
        try:
            h = data.fetch("binance", symbol, self.cfg.htf, limit=look + 4)
        except Exception as e:
            log.debug("%s alınamadı: %s", symbol, e)
            return 0
        step = data.INTERVAL_MS[self.cfg.htf]
        n = 0
        for end in range(max(4, len(h) - look + 1), len(h) + 1):
            sig = detect(h[end - 4:end], strict_wicks=self.cfg.strict)
            if not sig or sig.direction not in self.cfg.directions:
                continue
            key = f"{symbol}:{sig.candles[-1].time}"
            if key in self.st["setups"]:
                continue
            s = new_setup(sig, step)
            self.st["setups"][key] = {"symbol": symbol, "durbun": sig.candles[-1].time,
                                      "notified": [], "last": 0, "setup": to_dict(s)}
            log.info("DÜRBÜN %s %s %s", symbol, self.cfg.htf, sig.direction)
            n += 1
        return n

    # 2) kurulumları ilerlet
    def update(self) -> None:
        items = list(self.st["setups"].items())
        if not items:
            return
        with ThreadPoolExecutor(self.cfg.workers) as ex:
            results = list(ex.map(self._fetch_ltf, [rec["symbol"] for _, rec in items]))
        for (key, rec), candles in zip(items, results):
            if candles is None:
                continue
            try:
                self._step(key, rec, candles)
            except Exception:
                log.exception("%s işlenemedi", key)

    def _fetch_ltf(self, symbol: str):
        try:
            return data.fetch("binance", symbol, self.cfg.ltf, limit=1000)
        except Exception as e:
            log.debug("%s %s alınamadı: %s", symbol, self.cfg.ltf, e)
            return None

    def _step(self, key: str, rec: dict, m: list) -> None:
        p, cfg = self.cfg.p, self.cfg
        s = from_dict(rec["setup"])
        ltf_ms = data.INTERVAL_MS[cfg.ltf]

        if s.stage != POZISYONDA:
            base = Setup(direction=s.direction, htf_step=s.htf_step, start=s.start, invalid=s.invalid)
            s = advance_to_entry(base, m, structure_events(m, p.lb, p.rb, "close"), p, ltf_ms)
            if s.choch is not None:
                ck = f"{rec['symbol']}:{s.choch.time}:{s.direction}"
                if ck in self.st["used_choch"] and "choch" not in rec["notified"]:
                    del self.st["setups"][key]  # aynı ChoCh başka dürbünle zaten takipte
                    return
                if ck not in self.st["used_choch"]:
                    self.st["used_choch"].append(ck)
                if s.stage in (GERI_TEST_BEKLENIYOR, POZISYONDA) and "choch" not in rec["notified"]:
                    rec["notified"].append("choch")
                    if cfg.notify_choch and s.stage == GERI_TEST_BEKLENIYOR:
                        self.tg.send(msg_choch(rec, s, cfg))
            if s.stage == POZISYONDA:
                if s.entry_time < self.st["started_at"]:
                    log.info("%s: giriş bot başlamadan önce olmuş, sayılmadı", key)
                    del self.st["setups"][key]
                    return
                self.tg.send(msg_entry(rec, s, cfg))
                rec["last"] = s.entry_time
                if p.entry == "limit":
                    pass  # limitte giriş mumu stop kontrolü advance_to_entry içinde yapıldı
            elif s.stage not in ACTIVE and s.stage not in (HEDEF, STOP):
                log.info("%s bitti: %s", key, s.stage)
                del self.st["setups"][key]
                return

        if s.stage == POZISYONDA:
            new = [c for c in m if c.time > rec["last"]]
            manage_position(s, new, p)
            if new:
                rec["last"] = new[-1].time
            if s.stage == POZISYONDA and now_ms() - s.entry_time > p.max_hold_bars * ltf_ms and m:
                close_trade(s, SURE, m[-1].close, m[-1].time, p)

        if s.stage in (HEDEF, STOP, SURE):
            self._record(rec, s)
            self.tg.send(msg_result(rec, s, cfg))
            del self.st["setups"][key]
            return
        rec["setup"] = to_dict(s)

    def _record(self, rec: dict, s: Setup) -> None:
        new = not TRADES_FILE.exists()
        with open(TRADES_FILE, "a", newline="", encoding="utf-8") as f:
            w = csvmod.writer(f)
            if new:
                w.writerow(FIELDS)
            w.writerow([rec["symbol"], s.direction, self.cfg.when(rec["durbun"]), self.cfg.when(s.entry_time),
                        s.entry, s.stop, s.target, round(risk_pct(s), 2), s.stage, round(s.r, 3),
                        self.cfg.when(s.exit_time)])

    def tick(self) -> None:
        self.scan()
        self.update()
        save_state(self.st)

    def summary(self) -> str:
        by = {}
        for rec in self.st["setups"].values():
            by[rec["setup"]["stage"]] = by.get(rec["setup"]["stage"], 0) + 1
        names = {CHOCH_BEKLENIYOR: "ChoCh bekleyen", GERI_TEST_BEKLENIYOR: "geri test bekleyen",
                 POZISYONDA: "açık pozisyon"}
        return ", ".join(f"{v} {names.get(k, k)}" for k, v in by.items()) or "takipte kurulum yok"


def main() -> None:
    load_env()
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"), format="%(asctime)s %(levelname)s %(message)s")
    ap = argparse.ArgumentParser(description="Dürbün + ChoCh canlı kâğıt üstünde test")
    ap.add_argument("--rapor", action="store_true", help="kapanan işlemlerin özeti")
    ap.add_argument("--once", action="store_true", help="tek tur çalış ve çık")
    args = ap.parse_args()

    if args.rapor:
        print(stats_line())
        for d, name in (("UP", "Yükseliş"), ("DOWN", "Düşüş")):
            rows = [r for r in read_trades() if r["yon"] == d]
            if rows:
                w = sum(r["sonuc"] == HEDEF for r in rows)
                print(f"  {name}: {len(rows)} işlem, başarı %{100 * w / len(rows):.1f}, "
                      f"{sum(float(r['r']) for r in rows):+.2f}R")
        return

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    chats = csv("TELEGRAM_CHAT_ID")
    if not token or not chats:
        sys.exit("TELEGRAM_BOT_TOKEN ve TELEGRAM_CHAT_ID .env dosyasında olmalı (bkz. README).")
    cfg = Cfg()
    tg = Telegram(token, chats)
    live = Live(cfg, tg, load_state())

    if args.once:
        live.tick()
        print(live.summary())
        return

    tg.send(f"🧪 Canlı kâğıt üstünde test başladı\n{cfg.htf} dürbün → {cfg.ltf} ChoCh → geri test · "
            f"giriş: {cfg.p.entry} · hedef {cfg.p.tp_r:g}R\n📊 {stats_line()}")
    while True:
        try:
            live.tick()
        except Exception:
            log.exception("Tur hatası")
        time.sleep(cfg.every)


if __name__ == "__main__":
    main()
