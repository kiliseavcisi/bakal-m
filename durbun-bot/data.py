"""Mum verisi kaynakları: Binance (kripto) ve Yahoo Finance (BIST vb.)."""
from __future__ import annotations

import time
from typing import List

import os

import requests

from pattern import Candle

def _base() -> str:
    return os.getenv("BINANCE_BASE", "https://api.binance.com").rstrip("/")

STABLES = {"USDC", "FDUSD", "TUSD", "BUSD", "USDP", "DAI", "EUR", "EURI", "AEUR",
           "USDE", "XUSD", "USD1", "BFUSD", "PAXG", "WBTC", "WBETH"}

INTERVAL_MS = {
    "1m": 60_000, "5m": 300_000, "15m": 900_000, "30m": 1_800_000,
    "1h": 3_600_000, "2h": 7_200_000, "4h": 14_400_000,
    "1d": 86_400_000, "1w": 604_800_000,
}

# Yahoo'nun interval adları
YF_INTERVAL = {"1m": "1m", "5m": "5m", "15m": "15m", "30m": "30m",
               "1h": "60m", "1d": "1d", "1w": "1wk"}
YF_PERIOD = {"1m": "5d", "5m": "5d", "15m": "1mo", "30m": "1mo",
             "1h": "3mo", "1d": "1y", "1w": "5y"}


def _now_ms() -> int:
    return int(time.time() * 1000)


def _only_closed(candles: List[Candle], interval: str) -> List[Candle]:
    """Henüz kapanmamış son mumu at."""
    step = INTERVAL_MS[interval]
    now = _now_ms()
    return [c for c in candles if c.time + step <= now]


def binance_universe(quote: str = "USDT", top_n: int = 100) -> List[str]:
    """İşlem gören QUOTE paritelerini 24s hacme göre sırala, ilk top_n'i al."""
    info = requests.get(f"{_base()}/api/v3/exchangeInfo",
                        params={"permissions": "SPOT"}, timeout=30).json()
    ok = set()
    for s in info["symbols"]:
        base = s["baseAsset"]
        if (s["status"] == "TRADING" and s["quoteAsset"] == quote
                and base not in STABLES
                and not base.endswith(("UP", "DOWN", "BULL", "BEAR"))):
            ok.add(s["symbol"])
    tickers = requests.get(f"{_base()}/api/v3/ticker/24hr", timeout=30).json()
    vols = sorted(((float(t["quoteVolume"]), t["symbol"]) for t in tickers
                   if t["symbol"] in ok), reverse=True)
    return [s for _, s in vols[:top_n]]


def fetch_binance(symbol: str, interval: str, limit: int = 20) -> List[Candle]:
    r = requests.get(
        f"{_base()}/api/v3/klines",
        params={"symbol": symbol.upper(), "interval": interval, "limit": limit},
        timeout=15,
    )
    r.raise_for_status()
    candles = [
        Candle(int(k[0]), float(k[1]), float(k[2]), float(k[3]), float(k[4]))
        for k in r.json()
    ]
    return _only_closed(candles, interval)


def fetch_yahoo(symbol: str, interval: str, limit: int = 20) -> List[Candle]:
    try:
        import yfinance as yf
    except ImportError as e:  # pragma: no cover
        raise RuntimeError("Yahoo kaynağı için: pip install yfinance") from e
    if interval not in YF_INTERVAL:
        raise ValueError(f"Yahoo bu periyodu desteklemiyor: {interval}")
    df = yf.Ticker(symbol).history(
        period=YF_PERIOD[interval], interval=YF_INTERVAL[interval], auto_adjust=False
    )
    candles = [
        Candle(int(ts.timestamp() * 1000), float(row.Open), float(row.High),
               float(row.Low), float(row.Close))
        for ts, row in df.tail(limit).iterrows()
    ]
    return _only_closed(candles, interval)


def fetch(source: str, symbol: str, interval: str, limit: int = 20) -> List[Candle]:
    if source == "binance":
        return fetch_binance(symbol, interval, limit)
    if source == "yahoo":
        return fetch_yahoo(symbol, interval, limit)
    raise ValueError(f"Bilinmeyen kaynak: {source}")
