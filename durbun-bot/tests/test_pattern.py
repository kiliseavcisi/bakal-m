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
