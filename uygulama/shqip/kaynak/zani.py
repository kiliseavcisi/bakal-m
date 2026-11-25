"""Zani text-to-speech (natural Albanian voices) for the build scripts.

The app is a static page: audio is generated ahead of time here, never from browser code.
The API key is read from the ZANI_API_KEY environment variable and is never logged or written to disk by this module.

    from zani import speak
    path = speak("Qysh je?", voice="arben", dialect="kosovo")   # -> cached .mp3 path

Uses only the Python standard library.
"""
import hashlib, json, os, re, time, urllib.error, urllib.request

BASE = "https://www.tryzani.com"
MAX_CHARS = 20000            # API limit per request
SYNC_LIMIT = 900             # longer texts are queued and must be polled
REQUEST_TIMEOUT = 60         # seconds per HTTP request
POLL_EVERY = 2.5             # seconds between polls of a queued generation
POLL_MAX = 300               # give up polling after about 5 minutes
CACHE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), ".clips-zani")
OPTIONS = {
    "dialect": {"standard", "kosovo", "gheg", "tosk"},
    "emotion": {"neutral", "warm", "confident", "energetic", "calm", "empathetic", "serious", "joyful", "solemn"},
    "pace": {"slow", "medium", "medium-fast", "fast"},
    "energy": {"low", "medium", "high"},
    "purpose": {"advertisement", "audiobook", "accessibility", "social", "documentary", "meditation", "education", "news", "podcast", "narration", "character"},
    "format": {"mp3", "wav"},
}


class ZaniError(Exception):
    """Base error. `user_message` is a Turkish message safe to show to the user (the API's own messages are Albanian)."""
    user_message = "Ses üretilemedi."
    def __init__(self, message="", status=None):
        super().__init__(message or self.user_message)
        self.status = status
class ZaniConfigError(ZaniError): user_message = "ZANI_API_KEY ortam değişkeni tanımlı değil."
class ZaniBadRequest(ZaniError): user_message = "İstek geçersiz (metin, ses ya da seçenekleri kontrol et)."
class ZaniAuthError(ZaniError): user_message = "API anahtarı geçersiz ya da eksik."
class ZaniCreditsError(ZaniError): user_message = "Zani kredisi yetersiz."
class ZaniNotFound(ZaniError): user_message = "Ses ya da üretim bulunamadı."
class ZaniRateLimit(ZaniError): user_message = "Çok fazla istek: biraz sonra tekrar dene."
class ZaniServerError(ZaniError): user_message = "Zani'de geçici bir sorun var, sonra tekrar dene."
class ZaniTimeout(ZaniError): user_message = "Ses üretimi zaman aşımına uğradı."
class ZaniGenerationFailed(ZaniError): user_message = "Zani bu metni seslendiremedi."

_BY_STATUS = {400: ZaniBadRequest, 401: ZaniAuthError, 402: ZaniCreditsError, 404: ZaniNotFound, 429: ZaniRateLimit}

_sleep = time.sleep          # replaced in tests
_urlopen = urllib.request.urlopen


def _key():
    k = os.environ.get("ZANI_API_KEY", "").strip()
    if not k:
        raise ZaniConfigError()
    return k


def _request(method, path, body=None, _retried_5xx=False, _retries_429=0):
    """JSON request with auth, timeout, Retry-After on 429 and one retry on 5xx. Returns parsed JSON."""
    data = json.dumps(body).encode() if body is not None else None
    req = urllib.request.Request(BASE + path, data=data, method=method, headers={
        "Authorization": "Bearer " + _key(), "Content-Type": "application/json", "Accept": "application/json",
        "User-Agent": "shqiponja-build/1.0"})
    try:
        with _urlopen(req, timeout=REQUEST_TIMEOUT) as r:
            return json.loads(r.read().decode() or "{}")
    except urllib.error.HTTPError as e:
        status = e.code
        try:
            detail = json.loads(e.read().decode() or "{}")
        except Exception:
            detail = {}
        if status == 429 and _retries_429 < 3:
            wait = float(e.headers.get("Retry-After", "60") or 60) if e.headers else 60.0
            _sleep(wait)
            return _request(method, path, body, _retried_5xx, _retries_429 + 1)
        if status >= 500 and not _retried_5xx:
            _sleep(3)
            return _request(method, path, body, True, _retries_429)
        cls = _BY_STATUS.get(status, ZaniServerError if status >= 500 else ZaniError)
        # keep the API's (Albanian) message for logs/debugging; show cls.user_message to users
        raise cls(f"HTTP {status}: {detail.get('error', '')} {detail.get('issues', '') or ''}".strip(), status)
    except (TimeoutError, urllib.error.URLError) as e:
        raise ZaniTimeout(f"network: {e}") from e


def _download(url):
    try:
        with _urlopen(urllib.request.Request(url, headers={"User-Agent": "shqiponja-build/1.0"}), timeout=REQUEST_TIMEOUT) as r:
            return r.read()
    except (TimeoutError, urllib.error.URLError) as e:
        raise ZaniTimeout(f"download: {e}") from e


def split_text(text, limit=MAX_CHARS):
    """Split on sentence boundaries into chunks of at most `limit` characters."""
    text = text.strip()
    if len(text) <= limit:
        return [text]
    parts, cur = [], ""
    for sent in re.split(r"(?<=[.!?…])\s+", text):
        while len(sent) > limit:                         # a single huge sentence: hard cut on spaces
            cut = sent.rfind(" ", 0, limit) if " " in sent[:limit] else limit
            parts.append(sent[:cut].strip()); sent = sent[cut:].strip()
        if cur and len(cur) + 1 + len(sent) > limit:
            parts.append(cur); cur = sent
        else:
            cur = (cur + " " + sent).strip()
    if cur:
        parts.append(cur)
    return parts


def _validate(text, opts):
    if not isinstance(text, str) or not text.strip():
        raise ZaniBadRequest("text is empty")
    for k, v in opts.items():
        if v is not None and k in OPTIONS and v not in OPTIONS[k]:
            raise ZaniBadRequest(f"invalid {k}: {v}")


def _generate(text, voice, opts):
    body = {"text": text, "voice": voice, **{k: v for k, v in opts.items() if v is not None}}
    g = _request("POST", "/v1/text-to-speech", body)
    t0 = time.monotonic()
    while g.get("status") in ("queued", "processing"):
        if time.monotonic() - t0 > POLL_MAX:
            raise ZaniTimeout(f"generation {g.get('id')} still {g.get('status')}")
        _sleep(POLL_EVERY)
        g = _request("GET", f"/v1/generations/{g['id']}")
    if g.get("status") != "completed" or not g.get("audioUrl"):
        raise ZaniGenerationFailed(f"generation {g.get('id')}: {g.get('status')} {g.get('error') or ''}".strip())
    return _download(g["audioUrl"])


def cache_key(text, voice, opts):
    blob = json.dumps({"t": text, "v": voice, **{k: v for k, v in sorted(opts.items()) if v is not None}}, ensure_ascii=False, sort_keys=True)
    return hashlib.md5(blob.encode()).hexdigest()[:16]


def speak(text, voice, dialect=None, emotion=None, pace=None, energy=None, purpose=None, personality=None, format="mp3", cache_dir=CACHE_DIR):
    """Albanian text -> path of a cached audio file. Identical (text, voice, options) never cost credits twice."""
    opts = {"dialect": dialect, "emotion": emotion, "pace": pace, "energy": energy, "purpose": purpose, "personality": personality, "format": format}
    _validate(text, opts)
    if personality and len(personality) > 240:
        raise ZaniBadRequest("personality is longer than 240 characters")
    os.makedirs(cache_dir, exist_ok=True)
    path = os.path.join(cache_dir, cache_key(text, voice, opts) + "." + format)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        return path
    audio = b"".join(_generate(chunk, voice, opts) for chunk in split_text(text))   # mp3 frames concatenate cleanly
    tmp = path + ".part"
    with open(tmp, "wb") as f:
        f.write(audio)
    os.replace(tmp, path)
    return path


def account():
    """{credits, plan, status}"""
    return _request("GET", "/v1/account")


def voices():
    return _request("GET", "/v1/voices").get("voices", [])
