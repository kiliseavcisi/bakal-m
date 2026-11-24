import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from pattern import Candle  # noqa: E402
from structure import structure_events  # noqa: E402


def series(closes):
    """Kapanışlardan basit mumlar üret (gövde = önceki kapanış -> kapanış)."""
    out, prev = [], closes[0]
    for i, c in enumerate(closes):
        o = prev
        out.append(Candle(i, o, max(o, c) + 0.1, min(o, c) - 0.1, c))
        prev = c
    return out


def leg(start, end, n):
    return [start + (end - start) * i / n for i in range(1, n + 1)]


def zigzag():
    # dalgalı yükseliş -> dalgalı düşüş (aşağı kırılımlar) -> dalgalı yükseliş (yukarı ChoCh)
    pts = [10, 14, 12, 16, 13.5,   # yükseliş, ara dip 13.5
           11, 12.5, 9, 10.5, 7,   # düşüş: 13.5 kırılır, alçalan tepeler
           9.5, 8, 11.5, 10, 14]   # yükseliş: 10.5/12.5 tepeleri kırılır
    closes = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        closes += leg(a, b, 5)
    return series(closes)


def test_choch_both_directions():
    ev = structure_events(zigzag(), lb=3, rb=3)
    kinds = [(e.direction, e.kind) for e in ev]
    assert kinds == [("UP", "BOS"), ("DOWN", "CHOCH"), ("DOWN", "BOS"),
                     ("DOWN", "BOS"), ("UP", "CHOCH"), ("UP", "BOS")]
    up = next(e for e in ev if e.direction == "UP")
    assert up.close > up.level


def test_no_lookahead():
    cs = zigzag()
    full = structure_events(cs, 3, 3)
    for e in full:  # olay, sadece o ana kadarki mumlarla da aynı şekilde bulunmalı
        partial = structure_events(cs[: e.index + 1], 3, 3)
        assert partial[-1] == e


def test_wick_vs_close():
    cs = zigzag()
    assert len(structure_events(cs, 3, 3, "wick")) >= len(structure_events(cs, 3, 3, "close"))
