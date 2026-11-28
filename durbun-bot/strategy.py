"""Dürbün → ChoCh → geri test → giriş stratejisinin ortak kuralları.

Hem backtest.py (geçmiş veri) hem canli_test.py (canlı kâğıt üstünde işlem)
aynı fonksiyonu kullanır; böylece iki testin sonuçları karşılaştırılabilir.

Kurallar (yükseliş; düşüş tam tersi):
  1) Üst TF'de dürbün tamamlanır (pattern.detect).
  2) En fazla expire_bars üst TF mumu içinde alt TF'de aynı yönde ChoCh.
     Bu sürede fiyat dürbün dibinin altında kapanırsa iptal.
  3) H = ChoCh seviyesi, L = ChoCh hareketini başlatan dip
     (kırılan pivot ile kırılım mumu arasındaki en düşük iğne).
     Stop = L'nin %stop_buffer altı. Stop mesafesi > %max_risk ise işlem yok.
  4) En fazla retest_bars alt TF mumu içinde H'ye dokunuş (%touch_tol) ve
     mum L'nin üstünde kapanırsa giriş. Dokunmadan tp_r kadar kaçarsa: kaçtı.
  5) Giriş "kapanis" = geri test mumunun kapanışı, "limit" = H.
     Hedef = giriş + tp_r × risk (exit="hedef"), ya da hedef yok ve alt TF'de
     ters yönde yapı kırılımında çıkış (exit="choch").
"""
from __future__ import annotations

import bisect
from dataclasses import dataclass, field
from typing import List, Optional, Sequence

from pattern import Candle, Signal
from structure import StructureEvent


@dataclass
class Params:
    expire_bars: int = 6
    retest_bars: int = 20
    touch_tol: float = 0.002
    stop_buffer: float = 0.002
    max_risk: float = 0.05
    tp_r: float = 2.0
    fee: float = 0.001
    max_hold_bars: int = 30 * 96  # 15m'de 30 gün
    entry: str = "kapanis"  # ya da "limit"
    exit: str = "hedef"  # "hedef" = sabit tp_r; "choch" = ters yönde yapı kırılımında çık;
    #                      "boy" = hedef, girişten dürbün boyunun boy_kat katı
    boy_kat: float = 2.0
    yildiz: bool = False  # Sabah/Akşam Yıldızı filtresi (pattern.is_star)
    lb: int = 5
    rb: int = 5


# Aşamalar
CHOCH_BEKLENIYOR = "choch_bekleniyor"
GERI_TEST_BEKLENIYOR = "geri_test_bekleniyor"
POZISYONDA = "pozisyonda"
# Bitişler
IPTAL = "iptal"  # dürbün ucu kırıldı
CHOCH_YOK = "choch_yok"  # süre doldu
RISK_BUYUK = "risk_buyuk"
GERI_TEST_YOK = "geri_test_yok"  # dokunmadan kaçtı ya da süre doldu
GERI_TEST_BOZULDU = "geri_test_bozuldu"
HEDEF, STOP, SURE, CHOCH_CIKIS = "HEDEF", "STOP", "SURE", "CHOCH_CIKIS"
ACTIVE = {CHOCH_BEKLENIYOR, GERI_TEST_BEKLENIYOR, POZISYONDA}


@dataclass
class Setup:
    direction: str
    htf_step: int
    start: int  # dürbün tamamlanma anı (ms)
    invalid: float  # dürbün dibi/tepesi
    height: float = 0.0  # dürbün boyu: 4 mumun en yüksek iğnesi - en düşük iğnesi
    stage: str = CHOCH_BEKLENIYOR
    choch: Optional[StructureEvent] = None
    H: float = 0.0
    L: float = 0.0
    stop: float = 0.0
    entry: float = 0.0
    entry_time: int = 0
    entry_index: int = -1
    target: float = 0.0
    exit_price: float = 0.0
    exit_time: int = 0
    r: float = 0.0
    extra: dict = field(default_factory=dict)

    @property
    def up(self) -> bool:
        return self.direction == "UP"


def new_setup(sig: Signal, htf_step: int) -> Setup:
    up = sig.direction == "UP"
    return Setup(
        direction=sig.direction, htf_step=htf_step,
        start=sig.candles[-1].time + htf_step,
        invalid=min(c.low for c in sig.candles) if up else max(c.high for c in sig.candles),
        height=max(c.high for c in sig.candles) - min(c.low for c in sig.candles),
    )


def advance_to_entry(s: Setup, m15: Sequence[Candle], events: Sequence[StructureEvent],
                     p: Params, step_ms: int) -> Setup:
    """Kurulumu giriş anına kadar ilerletir (ya da bitirir/bekletir).

    m15: kapanmış alt TF mumları; events: bu mumlar üzerinde structure_events.
    Veri yetmezse kurulum bekleme aşamasında kalır.
    """
    up = s.up
    last_time = m15[-1].time if m15 else 0
    times = [c.time for c in m15]
    expires = s.start + p.expire_bars * s.htf_step

    # 2) ChoCh
    ev = None
    for e in events:
        if e.time < s.start or e.kind != "CHOCH":
            continue
        if e.time >= expires:
            break
        if e.direction == s.direction:
            ev = e
            break
    a = bisect.bisect_left(times, s.start)
    stop_at = ev.index if ev else len(m15)
    for x in range(a, stop_at):
        if (m15[x].close < s.invalid) if up else (m15[x].close > s.invalid):
            s.stage = IPTAL
            return s
    if ev is None:
        s.stage = CHOCH_YOK if last_time + step_ms >= expires else CHOCH_BEKLENIYOR
        return s
    s.choch = ev

    # 3) seviyeler
    s.H = ev.level
    seg = m15[ev.pivot_index:ev.index + 1]
    s.L = min(c.low for c in seg) if up else max(c.high for c in seg)
    s.stop = s.L * (1 - p.stop_buffer) if up else s.L * (1 + p.stop_buffer)
    if abs(s.H - s.stop) / s.H > p.max_risk:
        s.stage = RISK_BUYUK
        return s

    # 4) geri test
    end = ev.index + 1 + p.retest_bars
    for n in range(ev.index + 1, min(end, len(m15))):
        c = m15[n]
        touched = c.low <= s.H * (1 + p.touch_tol) if up else c.high >= s.H * (1 - p.touch_tol)
        if not touched:
            runaway = (c.high >= s.H + p.tp_r * (s.H - s.stop)) if up else \
                      (c.low <= s.H - p.tp_r * (s.stop - s.H))
            if runaway:
                s.stage = GERI_TEST_YOK
                return s
            continue
        if (c.close <= s.L) if up else (c.close >= s.L):
            s.stage = GERI_TEST_BOZULDU
            return s
        s.entry = c.close if p.entry == "kapanis" else s.H
        risk = (s.entry - s.stop) if up else (s.stop - s.entry)
        if risk <= 0 or risk / s.entry > p.max_risk:
            s.stage = RISK_BUYUK
            return s
        dist = p.boy_kat * s.height if p.exit == "boy" else p.tp_r * risk
        s.target = s.entry + dist if up else s.entry - dist
        s.entry_time, s.entry_index = c.time, n
        s.stage = POZISYONDA
        # limit girişte dokunuş mumunda stop görülmüşse anında stop
        if p.entry == "limit" and ((c.low <= s.stop) if up else (c.high >= s.stop)):
            close_trade(s, STOP, s.stop, c.time, p)
        return s
    s.stage = GERI_TEST_YOK if len(m15) >= end else GERI_TEST_BEKLENIYOR
    return s


def close_trade(s: Setup, result: str, price: float, t: int, p: Params) -> None:
    risk = (s.entry - s.stop) if s.up else (s.stop - s.entry)
    move = (price - s.entry) if s.up else (s.entry - price)
    s.stage, s.exit_price, s.exit_time = result, price, t
    s.r = (move - p.fee * s.entry) / risk


def manage_position(s: Setup, candles: Sequence[Candle], p: Params) -> Setup:
    """Pozisyondaki kurulumu verilen (girişten SONRAKİ) mumlarla ilerletir.
    Aynı mumda hem stop hem hedef varsa STOP sayılır."""
    for c in candles:
        if s.stage != POZISYONDA:
            break
        if (c.low <= s.stop) if s.up else (c.high >= s.stop):
            close_trade(s, STOP, s.stop, c.time, p)
        elif (c.high >= s.target) if s.up else (c.low <= s.target):
            close_trade(s, HEDEF, s.target, c.time, p)
    return s


def manage_choch_exit(s: Setup, candles: Sequence[Candle], opposite_times: set, p: Params) -> Setup:
    """Hedefsiz çıkış: stop yerinde kalır; alt TF'de ters yönde ChoCh/BOS
    oluşan mumun kapanışında işlemden çıkılır."""
    for c in candles:
        if s.stage != POZISYONDA:
            break
        if (c.low <= s.stop) if s.up else (c.high >= s.stop):
            close_trade(s, STOP, s.stop, c.time, p)
        elif c.time in opposite_times:
            close_trade(s, CHOCH_CIKIS, c.close, c.time, p)
    return s


def mfe_r(s: Setup, candles: Sequence[Candle]) -> float:
    """Girişten sonra, stop olana kadar fiyatın lehte gittiği en uzak mesafe (R)."""
    risk = abs(s.entry - s.stop)
    best = 0.0
    for c in candles:
        if (c.low <= s.stop) if s.up else (c.high >= s.stop):
            break
        best = max(best, ((c.high - s.entry) if s.up else (s.entry - c.low)) / risk)
    return best


def risk_pct(s: Setup) -> float:
    return 100 * abs(s.entry - s.stop) / s.entry if s.entry else 0.0


def chunk_after(m15: List[Candle], t: int) -> List[Candle]:
    """t zamanından sonra açılan mumlar."""
    i = bisect.bisect_right([c.time for c in m15], t)
    return m15[i:]
