"""Uçtan uca akış: 4h dürbün -> 15m ChoCh -> Telegram bildirimi (ağ yok)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import bot  # noqa: E402
import data  # noqa: E402
from pattern import Candle  # noqa: E402
from test_structure import leg  # noqa: E402

H4 = data.INTERVAL_MS["4h"]
M15 = data.INTERVAL_MS["15m"]
T0 = 1_700_000_000_000 // H4 * H4


def htf():
    return [Candle(T0, 10, 10.5, 8, 8.5), Candle(T0 + H4, 8.6, 8.8, 7.5, 7.8),
            Candle(T0 + 2 * H4, 7.8, 8.4, 7.0, 8.3), Candle(T0 + 3 * H4, 8.3, 10, 8.2, 9.8)]


def ltf(start, pts):
    closes = [pts[0]]
    for a, b in zip(pts, pts[1:]):
        closes += leg(a, b, 5)
    out, prev = [], closes[0]
    for i, c in enumerate(closes):
        out.append(Candle(start + i * M15, prev, max(prev, c) + 0.02, min(prev, c) - 0.02, c))
        prev = c
    return out


class FakeTG:
    def __init__(self):
        self.msgs = []

    def send(self, t):
        self.msgs.append(t)


def run(monkeypatch, tmp_path, ltf_pts, now_ms):
    monkeypatch.setattr(bot, "STATE_FILE", tmp_path / "s.json")
    monkeypatch.setenv("BINANCE_SYMBOLS", "BTCUSDT")
    monkeypatch.setenv("INTERVALS", "4h")
    monkeypatch.setattr(bot.time, "time", lambda: now_ms / 1000)
    start = T0 + 4 * H4  # dürbün tamamlandı
    lt = ltf(start - 21 * M15, ltf_pts)  # ilk 5 nokta dürbün öncesi

    def fake_fetch(src, sym, iv, limit=20):
        return htf() if iv == "4h" else [c for c in lt if c.time + M15 <= now_ms]

    monkeypatch.setattr(data, "fetch", fake_fetch)
    tg = FakeTG()
    sc = bot.Scanner(bot.Config(), tg, bot.load_state())
    sc.tick()
    return tg, sc


# ChoCh öncesi yükseliş, dürbün sonrası test (düşüş) ve yukarı ChoCh
PTS = [9, 9.6, 9.3, 9.9, 9.5,  # dürbün öncesi
       9.8, 9.0, 9.3, 8.6,      # dürbün sonrası geri çekilme (aşağı ChoCh/BOS)
       9.1, 8.8, 9.6, 9.4, 10.2]  # yukarı ChoCh = onay


def test_confirmed(monkeypatch, tmp_path):
    tg, sc = run(monkeypatch, tmp_path, PTS, T0 + 4 * H4 + 70 * M15)
    assert len(tg.msgs) == 1 and "ONAYLI DÜRBÜN YÜKSELİŞ" in tg.msgs[0]
    assert "15m CHOCH" in tg.msgs[0]
    assert sc.state["setups"] == {}
    sc.tick()  # tekrar bildirmemeli
    assert len(tg.msgs) == 1


def test_waiting_then_invalid(monkeypatch, tmp_path):
    # dürbün dibi (7.0) altında kapanış -> iptal
    pts = [9, 9.6, 9.3, 9.9, 9.5, 9.8, 8.0, 8.4, 6.5, 7.0, 6.8, 9.6, 9.4, 10.2]
    tg, sc = run(monkeypatch, tmp_path, pts, T0 + 4 * H4 + 70 * M15)
    assert tg.msgs == [] and sc.state["setups"] == {}


def test_expired(monkeypatch, tmp_path):
    flat = [9.5, 9.6] * 7
    tg, sc = run(monkeypatch, tmp_path, flat, T0 + 4 * H4 + 7 * H4)
    assert tg.msgs == [] and sc.state["setups"] == {}
