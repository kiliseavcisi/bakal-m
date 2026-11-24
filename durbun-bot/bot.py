"""Dürbün mum Telegram bildirim botu.

Kullanım:
    python bot.py              # tarayıcıyı başlatır
    python bot.py --chat-id    # bota mesaj attıktan sonra chat id'ni gösterir
    python bot.py --once       # tek tur tarar ve çıkar (cron için)
    python bot.py --test       # Telegram'a deneme mesajı yollar
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests

import data
from pattern import Signal, detect

log = logging.getLogger("durbun")
STATE_FILE = Path(__file__).with_name("state.json")


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


# ---------------------------------------------------------------- Mesaj
def fmt(x: float) -> str:
    return f"{x:,.8f}".rstrip("0").rstrip(".") if x < 1 else f"{x:,.4f}".rstrip("0").rstrip(".")


def build_message(sig: Signal, source: str, symbol: str, interval: str) -> str:
    up = sig.direction == "UP"
    head = "🟢 <b>DÜRBÜN YÜKSELİŞ</b>" if up else "🔴 <b>DÜRBÜN DÜŞÜŞ</b>"
    colors = "🟥🟥🟩🟩" if up else "🟩🟩🟥🟥"
    last = sig.candles[-1]
    t = datetime.fromtimestamp(last.time / 1000, tz=timezone.utc).strftime("%d.%m.%Y %H:%M UTC")
    rule = ("2-3. mum gövdeleri çizginin üstüne çıkmadı" if up
            else "2-3. mum gövdeleri çizginin altına inmedi")
    return (
        f"{head}\n"
        f"<b>{symbol}</b> · {interval} · {source}\n"
        f"Mumlar: {colors}\n"
        f"Gövde çizgisi: <code>{fmt(sig.line)}</code> ({rule})\n"
        f"4. mum kapanış: <code>{fmt(last.close)}</code>\n"
        f"4. mum açılış zamanı: {t}\n"
        f"\n<i>Mum boyuna sinyalden sonra bak. Yatırım tavsiyesi değildir.</i>"
    )


# ---------------------------------------------------------------- Durum
def load_state() -> dict:
    try:
        return json.loads(STATE_FILE.read_text())
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, indent=1))


# ---------------------------------------------------------------- Tarama
def watchlist() -> list[tuple[str, str]]:
    items = [("binance", s) for s in csv("BINANCE_SYMBOLS", "BTCUSDT,ETHUSDT")]
    items += [("yahoo", s) for s in csv("YAHOO_SYMBOLS")]
    return items


def scan_once(tg: Telegram, state: dict, strict: bool, directions: set[str]) -> int:
    sent = 0
    intervals = csv("INTERVALS", "1h,4h")
    for source, symbol in watchlist():
        for interval in intervals:
            key = f"{source}:{symbol}:{interval}"
            try:
                candles = data.fetch(source, symbol, interval)
            except Exception as e:  # ağ/sembol hatası bir sembolü durdurmasın
                log.warning("%s alınamadı: %s", key, e)
                continue
            sig = detect(candles, strict_wicks=strict)
            if not sig or sig.direction not in directions:
                continue
            stamp = sig.candles[-1].time
            if state.get(key) == stamp:
                continue  # bu mum için zaten bildirildi
            state[key] = stamp
            log.info("SİNYAL %s %s", key, sig.direction)
            tg.send(build_message(sig, source, symbol, interval))
            sent += 1
    save_state(state)
    return sent


def main() -> None:
    load_env()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    p = argparse.ArgumentParser(description="Dürbün mum Telegram botu")
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

    strict = os.getenv("STRICT_WICKS", "0") == "1"
    directions = {d.upper() for d in csv("DIRECTIONS", "UP,DOWN")}
    every = int(os.getenv("CHECK_EVERY_SECONDS", "60"))
    state = load_state()

    if args.once:
        scan_once(tg, state, strict, directions)
        return

    log.info("Başladı: %d sembol, periyotlar=%s, her %ds", len(watchlist()), csv("INTERVALS", "1h,4h"), every)
    if os.getenv("STARTUP_MESSAGE", "1") == "1":
        tg.send("👀 Dürbün bot başladı, formasyon taranıyor.")
    while True:
        try:
            scan_once(tg, state, strict, directions)
        except Exception:
            log.exception("Tarama hatası")
        time.sleep(every)


if __name__ == "__main__":
    main()
