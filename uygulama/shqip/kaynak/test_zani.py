"""Tests for zani.py with a mocked network.  Run:  python3 -m unittest test_zani -v   (from uygulama/shqip/kaynak)"""
import io, json, os, sys, tempfile, unittest, urllib.error
from email.message import Message
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import zani


class Resp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): self.close()


def http_error(code, body=None, headers=None):
    h = Message()
    for k, v in (headers or {}).items(): h[k] = v
    return urllib.error.HTTPError("https://x", code, "err", h, io.BytesIO(json.dumps(body or {"error": "gabim"}).encode()))


class FakeNet:
    """Queue of responses: dict -> JSON body, bytes -> raw body, Exception -> raised."""
    def __init__(self, *responses):
        self.responses, self.calls = list(responses), []
    def __call__(self, req, timeout=None):
        self.calls.append((req.get_method(), req.full_url, req.data, dict(req.header_items()), timeout))
        r = self.responses.pop(0)
        if isinstance(r, Exception): raise r
        return Resp(r if isinstance(r, bytes) else json.dumps(r).encode())


class ZaniTest(unittest.TestCase):
    def setUp(self):
        os.environ["ZANI_API_KEY"] = "zn_live_test"
        self.tmp = tempfile.mkdtemp()
        self.sleeps = []
        zani._sleep = self.sleeps.append
    def tearDown(self):
        zani._urlopen = __import__("urllib.request").request.urlopen
    def use(self, *responses):
        net = FakeNet(*responses); zani._urlopen = net; return net

    def test_sync_generation_downloads_and_caches(self):
        net = self.use({"id": "g1", "status": "completed", "audioUrl": "https://cdn/a.mp3"}, b"MP3DATA")
        p = zani.speak("Qysh je?", voice="arben", dialect="kosovo", cache_dir=self.tmp)
        self.assertEqual(open(p, "rb").read(), b"MP3DATA")
        method, url, data, headers, timeout = net.calls[0]
        self.assertEqual((method, url), ("POST", "https://www.tryzani.com/v1/text-to-speech"))
        self.assertEqual(json.loads(data), {"text": "Qysh je?", "voice": "arben", "dialect": "kosovo", "format": "mp3"})
        self.assertEqual(headers["Authorization"], "Bearer zn_live_test")
        self.assertEqual(timeout, 60)
        # same text + options: served from cache, no request
        self.use()
        self.assertEqual(zani.speak("Qysh je?", voice="arben", dialect="kosovo", cache_dir=self.tmp), p)

    def test_queued_generation_is_polled(self):
        net = self.use({"id": "g2", "status": "queued", "audioUrl": None}, {"id": "g2", "status": "processing"},
                       {"id": "g2", "status": "completed", "audioUrl": "https://cdn/b.mp3"}, b"LONG")
        p = zani.speak("a" * 1000, voice="vjosa", cache_dir=self.tmp)
        self.assertEqual(open(p, "rb").read(), b"LONG")
        self.assertEqual([c[1] for c in net.calls[1:3]], ["https://www.tryzani.com/v1/generations/g2"] * 2)
        self.assertEqual(self.sleeps, [zani.POLL_EVERY, zani.POLL_EVERY])

    def test_429_waits_for_retry_after(self):
        self.use(http_error(429, headers={"Retry-After": "60"}), {"id": "g3", "status": "completed", "audioUrl": "https://cdn/x.mp3"}, b"OK")
        zani.speak("Mirë", voice="vjosa", cache_dir=self.tmp)
        self.assertEqual(self.sleeps, [60.0])

    def test_5xx_retried_once_then_raises(self):
        self.use(http_error(502), {"id": "g4", "status": "completed", "audioUrl": "https://cdn/x.mp3"}, b"OK")
        zani.speak("Po", voice="vjosa", cache_dir=self.tmp)
        self.use(http_error(500), http_error(502))
        with self.assertRaises(zani.ZaniServerError):
            zani.speak("Jo", voice="vjosa", cache_dir=self.tmp)

    def test_typed_errors(self):
        for code, cls in [(400, zani.ZaniBadRequest), (401, zani.ZaniAuthError), (402, zani.ZaniCreditsError), (404, zani.ZaniNotFound)]:
            self.use(http_error(code))
            with self.assertRaises(cls) as cm:
                zani.speak(f"tekst {code}", voice="vjosa", cache_dir=self.tmp)
            self.assertEqual(cm.exception.status, code)
            self.assertTrue(cm.exception.user_message)

    def test_failed_generation(self):
        self.use({"id": "g5", "status": "failed", "error": "gabim"})
        with self.assertRaises(zani.ZaniGenerationFailed):
            zani.speak("Diçka", voice="vjosa", cache_dir=self.tmp)

    def test_missing_key(self):
        del os.environ["ZANI_API_KEY"]
        self.use()
        with self.assertRaises(zani.ZaniConfigError):
            zani.speak("Tung", voice="vjosa", cache_dir=self.tmp)

    def test_validation(self):
        self.use()
        with self.assertRaises(zani.ZaniBadRequest): zani.speak("  ", voice="vjosa", cache_dir=self.tmp)
        with self.assertRaises(zani.ZaniBadRequest): zani.speak("Tung", voice="vjosa", dialect="xx", cache_dir=self.tmp)

    def test_split_on_sentences(self):
        text = " ".join(["Kjo është një fjali e gjatë."] * 1000)       # ~29000 chars
        parts = zani.split_text(text)
        self.assertGreater(len(parts), 1)
        self.assertTrue(all(len(p) <= zani.MAX_CHARS for p in parts))
        self.assertTrue(all(p.endswith(".") for p in parts))
        self.assertEqual(" ".join(parts), text)

    def test_long_text_makes_several_requests(self):
        text = " ".join(["Fjali."] * 4000)                              # ~28000 chars -> 2 chunks
        n = len(zani.split_text(text))
        resp = []
        for i in range(n): resp += [{"id": f"q{i}", "status": "queued"}, {"id": f"q{i}", "status": "completed", "audioUrl": "https://cdn/x.mp3"}, b"P%d" % i]
        self.use(*resp)
        p = zani.speak(text, voice="vjosa", cache_dir=self.tmp)
        self.assertEqual(open(p, "rb").read(), b"".join(b"P%d" % i for i in range(n)))


if __name__ == "__main__":
    unittest.main()
