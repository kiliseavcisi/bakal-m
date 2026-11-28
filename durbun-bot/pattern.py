"""Dürbün mum formasyonu tespiti.

Kurallar (paylaşılan görsellerden):

YÜKSELİŞ (dipte oluşur)
  1) Sıra ve renk: KIRMIZI, KIRMIZI, YEŞİL, YEŞİL.
  2) 2. ve 3. mumun gövdeleri, 1. ve 4. mumun gövdelerini YUKARI doğru ihlal
     edemez. Çizgi = min(1. mum gövde üstü, 4. mum gövde üstü).
  3) İğneler aşağı doğru taşabilir; mum boyu önemli değildir.

DÜŞÜŞ (tepede oluşur) — yükselişin tam tersi
  1) Sıra ve renk: YEŞİL, YEŞİL, KIRMIZI, KIRMIZI.
  2) 2. ve 3. mumun gövdeleri, 1. ve 4. mumun gövdelerini AŞAĞI doğru ihlal
     edemez. Çizgi = max(1. mum gövde altı, 4. mum gövde altı).
  3) İğneler yukarı doğru taşabilir.

`strict_wicks=True` verilirse ortadaki mumların iğnelerinin de çizgiyi
ihlal etmemesi şartı aranır (daha az ama daha temiz sinyal).
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional, Sequence


@dataclass(frozen=True)
class Candle:
    time: int  # açılış zamanı, ms (epoch)
    open: float
    high: float
    low: float
    close: float

    @property
    def green(self) -> bool:
        return self.close > self.open

    @property
    def red(self) -> bool:
        return self.close < self.open

    @property
    def body_top(self) -> float:
        return max(self.open, self.close)

    @property
    def body_bottom(self) -> float:
        return min(self.open, self.close)


@dataclass(frozen=True)
class Signal:
    direction: str  # "UP" veya "DOWN"
    line: float  # ihlal edilmemesi gereken gövde çizgisi
    candles: tuple  # 4 mum


def detect(candles: Sequence[Candle], strict_wicks: bool = False) -> Optional[Signal]:
    """Son 4 (kapanmış) mumda dürbün formasyonu var mı bakar."""
    if len(candles) < 4:
        return None
    c1, c2, c3, c4 = candles[-4:]

    # Yükseliş: K K Y Y
    if c1.red and c2.red and c3.green and c4.green:
        line = min(c1.body_top, c4.body_top)
        ok = c2.body_top <= line and c3.body_top <= line
        if strict_wicks:
            ok = ok and c2.high <= line and c3.high <= line
        if ok:
            return Signal("UP", line, (c1, c2, c3, c4))

    # Düşüş: Y Y K K
    if c1.green and c2.green and c3.red and c4.red:
        line = max(c1.body_bottom, c4.body_bottom)
        ok = c2.body_bottom >= line and c3.body_bottom >= line
        if strict_wicks:
            ok = ok and c2.low >= line and c3.low >= line
        if ok:
            return Signal("DOWN", line, (c1, c2, c3, c4))

    return None


def is_star(history: Sequence[Candle], sig: Signal, trend_bars: int = 10,
            long_mult: float = 1.0, small_ratio: float = 0.5) -> bool:
    """Sabah / Akşam Yıldızı şartları (dürbüne ek filtre).

    history: dürbünün 4 mumu dahil, öncesindeki mumlarla birlikte (en az
    trend_bars + 4 mum). Şartlar (yükseliş; düşüş tam tersi):
      1) Önceki trend: 1. mumun kapanışı, trend_bars mum öncesinin kapanışından düşük.
      2) 1. mum uzun: gövdesi, önceki trend_bars mumun ortalama gövdesinin
         long_mult katından büyük. 2. ve 3. mum küçük: gövdeleri 1. mumun
         small_ratio katından küçük.
      3) 4. mum, 1. mum gövdesinin ortasının üstünde kapanır.
    """
    if len(history) < trend_bars + 4:
        return False
    c1, c2, c3, c4 = sig.candles
    prev = history[-(trend_bars + 4):-4]
    body = lambda c: abs(c.close - c.open)
    b1 = body(c1)
    avg = sum(body(c) for c in prev) / len(prev)
    if b1 <= 0 or b1 < long_mult * avg:
        return False
    if body(c2) > small_ratio * b1 or body(c3) > small_ratio * b1:
        return False
    mid = (c1.open + c1.close) / 2
    if sig.direction == "UP":
        return c1.close < prev[0].close and c4.close > mid
    return c1.close > prev[0].close and c4.close < mid
