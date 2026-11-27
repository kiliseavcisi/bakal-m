"""BoS / ChoCh (piyasa yapısı kırılımı) tespiti.

TradingView'daki "BoS/ChoCh (Nephew_Sam_)" göstergesinin mantığı:
  - Pivot tepe/dip: solda `lb`, sağda `rb` mum (varsayılan 5/5).
  - Son pivot tepenin üstünde KAPANIŞ  -> yukarı kırılım.
    Önceki trend aşağıysa ChoCh (karakter değişimi), değilse BOS.
  - Son pivot dibin altında KAPANIŞ   -> aşağı kırılım (aynı mantık).
  - Her pivot yalnızca bir kez kırılabilir.
`confirm="wick"` verilirse kapanış yerine iğne (high/low) kullanılır.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Sequence

from pattern import Candle


@dataclass(frozen=True)
class StructureEvent:
    index: int  # kırılımın olduğu mumun sırası
    time: int  # o mumun açılış zamanı (ms)
    direction: str  # "UP" / "DOWN"
    kind: str  # "CHOCH" / "BOS"
    level: float  # kırılan pivot seviyesi
    close: float
    pivot_index: int = -1  # kırılan pivotun mum sırası


def _is_pivot_high(c: Sequence[Candle], p: int, lb: int, rb: int) -> bool:
    h = c[p].high
    return all(c[i].high < h for i in range(p - lb, p)) and all(
        c[i].high <= h for i in range(p + 1, p + rb + 1))


def _is_pivot_low(c: Sequence[Candle], p: int, lb: int, rb: int) -> bool:
    l = c[p].low
    return all(c[i].low > l for i in range(p - lb, p)) and all(
        c[i].low >= l for i in range(p + 1, p + rb + 1))


def structure_events(candles: Sequence[Candle], lb: int = 5, rb: int = 5,
                     confirm: str = "close") -> List[StructureEvent]:
    events: List[StructureEvent] = []
    trend = 0  # 1 yukarı, -1 aşağı, 0 belirsiz
    ph = pl = None  # [seviye, kırıldı_mı, mum_sırası]
    for j, cj in enumerate(candles):
        p = j - rb  # pivotlar ancak rb mum sonra kesinleşir
        if p >= lb:
            if _is_pivot_high(candles, p, lb, rb):
                ph = [candles[p].high, False, p]
            if _is_pivot_low(candles, p, lb, rb):
                pl = [candles[p].low, False, p]
        up_src = cj.close if confirm == "close" else cj.high
        dn_src = cj.close if confirm == "close" else cj.low
        if ph and not ph[1] and up_src > ph[0]:
            ph[1] = True
            events.append(StructureEvent(j, cj.time, "UP",
                                         "CHOCH" if trend == -1 else "BOS", ph[0], cj.close, ph[2]))
            trend = 1
        if pl and not pl[1] and dn_src < pl[0]:
            pl[1] = True
            events.append(StructureEvent(j, cj.time, "DOWN",
                                         "CHOCH" if trend == 1 else "BOS", pl[0], cj.close, pl[2]))
            trend = -1
    return events
