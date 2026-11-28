import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pattern import Candle, detect  # noqa: E402


def c(o, h, l, cl, t=0):
    return Candle(t, o, h, l, cl)


def test_bullish_valid():
    cs = [c(10, 10.5, 8, 8.5), c(8.6, 8.8, 7.5, 7.8), c(7.8, 8.4, 7.0, 8.3), c(8.3, 10, 8.2, 9.8)]
    s = detect(cs)
    assert s and s.direction == "UP" and s.line == 9.8


def test_bullish_middle_body_violates_up():
    # 3. mum gövdesi 4. mumun gövde üstünü aşıyor
    cs = [c(10, 10.5, 8, 8.5), c(8.6, 8.8, 7.5, 7.8), c(7.8, 9.5, 7.0, 9.4), c(8.3, 9.2, 8.2, 9.0)]
    assert detect(cs) is None


def test_bullish_wick_down_ok_strict_wick_up_fails():
    cs = [c(10, 10.5, 8, 8.5), c(8.6, 9.9, 6.0, 7.8), c(7.8, 8.4, 7.0, 8.3), c(8.3, 10, 8.2, 9.8)]
    assert detect(cs).direction == "UP"
    assert detect(cs, strict_wicks=True) is None


def test_wrong_colors():
    cs = [c(10, 10.5, 8, 8.5), c(7.8, 8.8, 7.5, 8.6), c(7.8, 8.4, 7.0, 8.3), c(8.3, 10, 8.2, 9.8)]
    assert detect(cs) is None


def test_bearish_valid():
    cs = [c(8, 10, 7.9, 9.5), c(9.4, 10.6, 9.3, 10.4), c(10.4, 10.8, 9.6, 9.7), c(9.7, 9.8, 7.5, 7.8)]
    s = detect(cs)
    assert s and s.direction == "DOWN" and s.line == 8


def test_bearish_middle_violates_down():
    cs = [c(8, 10, 7.9, 9.5), c(9.4, 10.6, 9.3, 10.4), c(10.4, 10.8, 7.0, 7.5), c(9.7, 9.8, 7.5, 7.8)]
    assert detect(cs) is None


def _trend_down(n=10, start=20.0):
    return [c(start - i * 0.5, start - i * 0.5 + 0.2, start - i * 0.5 - 0.7, start - i * 0.5 - 0.5) for i in range(n)]


def test_morning_star_filter():
    from pattern import is_star
    prev = _trend_down()  # 20 -> 15 düşüş, gövdeler 0.5
    durbun = [c(15, 15.1, 13.4, 13.5), c(13.5, 13.6, 13.0, 13.2), c(13.2, 13.7, 13.1, 13.4), c(13.4, 14.9, 13.3, 14.8)]
    s = detect(durbun)
    assert s and s.direction == "UP"
    assert is_star(prev + durbun, s)
    # 4. mum 1. mumun gövde ortasının (14.25) altında kapanırsa yıldız değil
    weak = durbun[:3] + [c(13.4, 14.2, 13.3, 14.1)]
    s2 = detect(weak)
    assert s2 and not is_star(prev + weak, s2)
    # önceki trend yukarıysa yıldız değil
    up_prev = [c(5 + i * 0.5, 5.7 + i * 0.5, 4.9 + i * 0.5, 5.5 + i * 0.5) for i in range(10)]
    assert not is_star(up_prev + durbun, s)
