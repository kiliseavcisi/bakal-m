"""Dürbün mum + alt zaman dilimi ChoCh onaylı Telegram bildirim botu.

Akış:
  1) Üst zaman diliminde (ör. 4h) kripto paritelerinde dürbün formasyonu aranır.
  2) Bulunan her dürbün "bekleyen kurulum" olarak saklanır.
  3) Alt zaman diliminde (ör. 15m) dürbün yönünde ChoCh oluşursa
     ✅ ONAYLI bildirim gönderilir.
  4) Belirli sayıda üst zaman dilimi mumu içinde onay gelmezse ya da fiyat
     dürbünün ucunu kapanışla geçerse kurulum iptal edilir.

Kullanım:
    python bot.py              # botu başlatır
    python bot.py --chat-id    # bota mesaj attıktan sonra chat id'ni gösterir
    python bot.py --once       # tek tur tarar ve çıkar
    python bot.py --test       # Telegram'a deneme mesajı yollar
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

import requests

import data
from pattern import Signal, detect
from structure import structure_events

log = logging.getLogger("durbun")
STATE_FILE = Path(__file__).with_name("state.json")
DEFAULT_LTF_MAP = "1d:1h,4h:15m,2h:15m,1h:5m,30m:5m,15m:1m"


# ---------------------------------------------------------------- Ayarlar
def load_env(path: Path = Path(__file__).with_name(".env")) -> None:
    """Basit .env okuyucu (ek kütüphane gerektirmez)."""
    if not path.exists():
        return
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        k, v = line.split("=", 1)
        os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))


def csv(name: str, default: str = "") -> list[str]:
    return [x.strip() for x in os.getenv(name, default).split(",") if x.strip()]


def flag(name: str, default: str = "0") -> bool:
    return os.getenv(name, default).strip() in ("1", "true", "yes", "evet")


class Config:
    def __init__(self) -> None:
        self.symbols_raw = csv("BINANCE_SYMBOLS", "ALL")
        self.quote = os.getenv("QUOTE", "USDT")
        self.top_n = int(os.getenv("TOP_N", "100"))
        self.yahoo = csv("YAHOO_SYMBOLS")
        self.intervals = csv("INTERVALS", "4h,1h")
        self.ltf_map = dict(x.split(":") for x in csv("LTF_MAP", DEFAULT_LTF_MAP))
        self.directions = {d.upper() for d in csv("DIRECTIONS", "UP,DOWN")}
        self.strict = flag("STRICT_WICKS")
        self.lb = int(os.getenv("PIVOT_LB", "5"))
        self.rb = int(os.getenv("PIVOT_RB", "5"))
        self.confirm = os.getenv("BREAKOUT_CONFIRM", "close").lower()
        self.kinds = {k.upper() for k in csv("CONFIRM_KINDS", "CHOCH")}
        self.expire_bars = int(os.getenv("SETUP_EXPIRE_BARS", "6"))
        self.invalidate = flag("INVALIDATE", "1")
        self.notify_pending = flag("NOTIFY_PENDING")
        self.every = int(os.getenv("CHECK_EVERY_SECONDS", "60"))
        self.workers = int(os.getenv("MAX_WORKERS", "8"))
        self.tz = ZoneInfo(os.getenv("TIMEZONE", "Europe/Istanbul"))
        for iv in self.intervals:
            if iv not in data.INTERVAL_MS:
                sys.exit(f"Desteklenmeyen periyot: {iv}")
            if iv not in self.ltf_map:
                sys.exit(f"{iv} için alt zaman dilimi yok. LTF_MAP'e ekle (ör. {iv}:15m)")


# ---------------------------------------------------------------- Telegram
class Telegram:
    def __init__(self, token: str, chat_ids: list[str]):
        self.base = f"https://api.telegram.org/bot{token}"
        self.chat_ids = chat_ids

    def send(self, text: str) -> None:
        for cid in self.chat_ids:
            try:
                r = requests.post(
                    f"{self.base}/sendMessage",
                    json={"chat_id": cid, "text": text, "parse_mode": "HTML",
                          "disable_web_page_preview": True},
                    timeout=15,
                )
                if not r.ok:
                    log.error("Telegram hatası (%s): %s", cid, r.text)
            except requests.RequestException as e:
                log.error("Telegram'a ulaşılamadı: %s", e)

    def print_chat_ids(self) -> None:
        r = requests.get(f"{self.base}/getUpdates", timeout=15)
        r.raise_for_status()
        seen = {}
        for u in r.json().get("result", []):
            msg = u.get("message") or u.get("channel_post") or {}
            chat = msg.get("chat")
            if chat:
                seen[chat["id"]] = chat.get("title") or chat.get("username") or chat.get("first_name")
        if not seen:
            print("Hiç mesaj yok. Önce Telegram'da bota /start yaz, sonra tekrar dene.")
        for cid, name in seen.items():
            print(f"TELEGRAM_CHAT_ID={cid}   ({name})")


# ---------------------------------------------------------------- Mesajlar
def fmt(x: float) -> str:
    s = f"{x:,.8f}" if abs(x) < 1 else f"{x:,.4f}"
    return s.rstrip("0").rstrip(".")


def tv_link(source: str, symbol: str) -> str:
    if source == "binance":
        return f"https://www.tradingview.com/chart/?symbol=BINANCE:{symbol}"
    if source == "yahoo" and symbol.endswith(".IS"):
        return f"https://www.tradingview.com/chart/?symbol=BIST:{symbol[:-3]}"
    return ""


def when(ms: int, tz) -> str:
    return datetime.fromtimestamp(ms / 1000, tz=timezone.utc).astimezone(tz).strftime("%d.%m %H:%M")


def pending_message(s: dict, cfg: Config) -> str:
    up = s["direction"] == "UP"
    return (
        f"{'🟡' if up else '🟠'} <b>DÜRBÜN {'YÜKSELİŞ' if up else 'DÜŞÜŞ'} — ChoCh bekleniyor</b>\n"
        f"<b>{s['symbol']}</b> · {s['htf']} dürbün · onay: {s['ltf']} ChoCh\n"
        f"Mumlar: {'🟥🟥🟩🟩' if up else '🟩🟩🟥🟥'}\n"
        f"Gövde çizgisi: <code>{fmt(s['line'])}</code>\n"
        f"İptal seviyesi: <code>{fmt(s['invalid'])}</code>\n"
        f"Son geçerlilik: {when(s['expires'], cfg.tz)}"
    )


def confirmed_message(s: dict, ev, cfg: Config) -> str:
    up = s["direction"] == "UP"
    link = tv_link(s["source"], s["symbol"])
    return (
        f"✅ <b>ONAYLI DÜRBÜN {'YÜKSELİŞ 🟢' if up else 'DÜŞÜŞ 🔴'}</b>\n"
        f"<b>{s['symbol']}</b> · {s['htf']} dürbün → {s['ltf']} {ev.kind}\n"
        f"Mumlar: {'🟥🟥🟩🟩' if up else '🟩🟩🟥🟥'}\n"
        f"Dürbün gövde çizgisi: <code>{fmt(s['line'])}</code>\n"
        f"{ev.kind} seviyesi: <code>{fmt(ev.level)}</code>\n"
        f"Onay mumu kapanışı: <code>{fmt(ev.close)}</code> ({when(ev.time, cfg.tz)})\n"
        f"Dürbün {'dibi' if up else 'tepesi'} (iptal): <code>{fmt(s['invalid'])}</code>\n"
        + (f"<a href=\"{link}\">TradingView'da aç</a>\n" if link else "")
        + "\n<i>Yatırım tavsiyesi değildir.</i>"
    )


# ---------------------------------------------------------------- Durum
def load_state() -> dict:
    try:
        st = json.loads(STATE_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        st = {}
    st.setdefault("scanned", {})
    st.setdefault("seen", {})
    st.setdefault("setups", {})
    return st


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=1))


# ---------------------------------------------------------------- Bot
class Scanner:
    def __init__(self, cfg: Config, tg: Telegram, state: dict):
        self.cfg, self.tg, self.state = cfg, tg, state
        self._universe: list[tuple[str, str]] = []
        self._universe_at = 0.0

    # --- sembol listesi
    def universe(self) -> list[tuple[str, str]]:
        if self._universe and time.time() - self._universe_at < 6 * 3600:
            return self._universe
        items: list[tuple[str, str]] = []
        if [s.upper() for s in self.cfg.symbols_raw] == ["ALL"]:
            try:
                items = [("binance", s) for s in data.binance_universe(self.cfg.quote, self.cfg.top_n)]
            except Exception as e:
                log.error("Binance parite listesi alınamadı: %s", e)
                return self._universe
        else:
            items = [("binance", s.upper()) for s in self.cfg.symbols_raw]
        items += [("yahoo", s) for s in self.cfg.yahoo]
        self._universe, self._universe_at = items, time.time()
        log.info("Taranacak parite sayısı: %d", len(items))
        return items

    # --- 1) üst zaman diliminde dürbün ara
    def scan_htf(self, force: bool = False) -> None:
        now = time.time() * 1000
        for iv in self.cfg.intervals:
            bucket = int(now // data.INTERVAL_MS[iv])
            if not force and self.state["scanned"].get(iv) == bucket:
                continue  # bu periyotta yeni mum kapanmadı
            syms = self.universe()
            if not syms:
                continue
            log.info("%s taraması: %d parite", iv, len(syms))
            with ThreadPoolExecutor(self.cfg.workers) as ex:
                results = list(ex.map(lambda s: self._check_durbun(s[0], s[1], iv), syms))
            found = sum(1 for r in results if r)
            log.info("%s taraması bitti, yeni dürbün: %d", iv, found)
            self.state["scanned"][iv] = bucket

    def _check_durbun(self, source: str, symbol: str, iv: str) -> bool:
        key = f"{source}:{symbol}:{iv}"
        try:
            candles = data.fetch(source, symbol, iv, limit=10)
        except Exception as e:
            log.debug("%s alınamadı: %s", key, e)
            return False
        sig = detect(candles, strict_wicks=self.cfg.strict)
        if not sig or sig.direction not in self.cfg.directions:
            return False
        last = sig.candles[-1]
        if self.state["seen"].get(key) == last.time:
            return False
        self.state["seen"][key] = last.time
        self._add_setup(source, symbol, iv, sig)
        return True

    def _add_setup(self, source: str, symbol: str, iv: str, sig: Signal) -> None:
        step = data.INTERVAL_MS[iv]
        start = sig.candles[-1].time + step  # dürbün tamamlandığı an
        up = sig.direction == "UP"
        setup = {
            "source": source, "symbol": symbol, "htf": iv, "ltf": self.cfg.ltf_map[iv],
            "direction": sig.direction, "line": sig.line,
            "invalid": min(c.low for c in sig.candles) if up else max(c.high for c in sig.candles),
            "start": start, "expires": start + self.cfg.expire_bars * step,
        }
        self.state["setups"][f"{source}:{symbol}:{iv}:{sig.candles[-1].time}"] = setup
        log.info("DÜRBÜN %s %s %s -> %s ChoCh bekleniyor", symbol, iv, sig.direction, setup["ltf"])
        if self.cfg.notify_pending:
            self.tg.send(pending_message(setup, self.cfg))

    # --- 2) alt zaman diliminde ChoCh onayı
    def check_setups(self) -> None:
        setups = self.state["setups"]
        if not setups:
            return
        with ThreadPoolExecutor(self.cfg.workers) as ex:
            outcomes = list(ex.map(lambda kv: (kv[0], self._evaluate(kv[1])), list(setups.items())))
        for key, (status, ev) in outcomes:
            s = setups[key]
            if status == "confirmed":
                log.info("ONAY %s %s %s %s", s["symbol"], s["htf"], s["ltf"], ev.kind)
                self.tg.send(confirmed_message(s, ev, self.cfg))
                del setups[key]
            elif status in ("expired", "invalid"):
                log.info("%s %s %s: %s", s["symbol"], s["htf"], s["direction"],
                         "süre doldu" if status == "expired" else "iptal (seviye kırıldı)")
                del setups[key]

    def _evaluate(self, s: dict):
        try:
            candles = data.fetch(s["source"], s["symbol"], s["ltf"], limit=500)
        except Exception as e:
            log.debug("%s %s alınamadı: %s", s["symbol"], s["ltf"], e)
            return "wait", None
        up = s["direction"] == "UP"
        events = [e for e in structure_events(candles, self.cfg.lb, self.cfg.rb, self.cfg.confirm)
                  if e.time >= s["start"]]
        hit = next((e for e in events if e.direction == s["direction"] and e.kind in self.cfg.kinds), None)
        if self.cfg.invalidate:
            for c in candles:
                if c.time < s["start"] or (hit and c.time >= hit.time):
                    continue
                if (up and c.close < s["invalid"]) or (not up and c.close > s["invalid"]):
                    return "invalid", None
        if hit:
            return "confirmed", hit
        if time.time() * 1000 >= s["expires"]:
            return "expired", None
        return "wait", None

    def tick(self, force: bool = False) -> None:
        self.scan_htf(force)
        self.check_setups()
        save_state(self.state)


def main() -> None:
    load_env()
    logging.basicConfig(level=os.getenv("LOG_LEVEL", "INFO"),
                        format="%(asctime)s %(levelname)s %(message)s")
    p = argparse.ArgumentParser(description="Dürbün mum + ChoCh Telegram botu")
    p.add_argument("--chat-id", action="store_true", help="chat id'leri listele")
    p.add_argument("--once", action="store_true", help="tek tur tara ve çık")
    p.add_argument("--test", action="store_true", help="deneme mesajı gönder")
    args = p.parse_args()

    token = os.getenv("TELEGRAM_BOT_TOKEN")
    if not token:
        sys.exit("TELEGRAM_BOT_TOKEN tanımlı değil (.env dosyasına yaz).")
    tg = Telegram(token, csv("TELEGRAM_CHAT_ID"))

    if args.chat_id:
        tg.print_chat_ids()
        return
    if not tg.chat_ids:
        sys.exit("TELEGRAM_CHAT_ID tanımlı değil. Bulmak için: python bot.py --chat-id")
    if args.test:
        tg.send("✅ Dürbün bot bağlantısı çalışıyor.")
        return

    cfg = Config()
    scanner = Scanner(cfg, tg, load_state())

    if args.once:
        scanner.tick(force=True)
        return

    log.info("Başladı: periyotlar=%s, alt TF=%s, her %ds",
             cfg.intervals, {i: cfg.ltf_map[i] for i in cfg.intervals}, cfg.every)
    if flag("STARTUP_MESSAGE", "1"):
        tg.send("👀 Dürbün + ChoCh bot başladı.\nPeriyotlar: "
                + ", ".join(f"{i}→{cfg.ltf_map[i]}" for i in cfg.intervals))
    while True:
        try:
            scanner.tick()
        except Exception:
            log.exception("Tarama hatası")
        time.sleep(cfg.every)


if __name__ == "__main__":
    main()
