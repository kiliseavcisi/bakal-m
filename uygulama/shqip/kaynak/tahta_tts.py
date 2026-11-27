# Voices the Tahta narrations (tahta_sq.py): Turkish by Ava HD, every «Albanian» word by Anila, in one clip.
#   python3 tahta_tts.py  -> .clips-tahta/<key>.mp3   (make.py packs them into packs/tahta.json and packs2/tahta.json)
# The Azure key is injected by the session's network proxy; nothing secret lives here.
import hashlib, os, re, subprocess, tempfile, time, urllib.error, urllib.request
from tahta_sq import BOARDS_SQ
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, ".clips-tahta"); os.makedirs(OUT, exist_ok=True)
URL = "https://swedencentral.tts.speech.microsoft.com/cognitiveservices/v1"
TEACHER, SQ = "en-US-Ava:DragonHDLatestNeural", "sq-AL-AnilaNeural"
esc = lambda t: t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

def ssml(text):
    parts = re.split(r"«([^»]+)»", text)          # even = Turkish, odd = Albanian
    body = "".join(f"<voice name='{SQ if i % 2 else TEACHER}'>{esc(p.strip())}</voice>" for i, p in enumerate(parts) if p.strip(" ,."))
    return f"<speak version='1.0' xml:lang='tr-TR'>{body}</speak>"

def synth(text):
    req = urllib.request.Request(URL, data=ssml(text).encode(), headers={"Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm", "User-Agent": "shqip-app", "Ocp-Apim-Subscription-Key": "proxy-injected"})
    for attempt in range(8):
        try: return urllib.request.urlopen(req, timeout=90).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 7: time.sleep(2 ** attempt); continue
            raise

n = 0
for steps in BOARDS_SQ.values():
    for say, *_ in steps:
        mp3 = os.path.join(OUT, hashlib.md5(say.encode()).hexdigest()[:10] + ".mp3")
        if os.path.exists(mp3): continue
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            f.write(synth(say)); f.flush()
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f.name, "-af",
                "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                "adelay=100,apad=pad_dur=0.25,loudnorm=I=-16:TP=-1.5", "-ac", "1", "-ar", "24000", "-b:a", "56k", mp3], check=True)
        n += 1
print("tahta clips new", n)
