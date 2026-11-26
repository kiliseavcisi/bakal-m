# Voices every text in .say.json (written by `NO_MMS=1 make.py`) with Azure neural Albanian voices.
#   python3 azure_all.py anila   -> .clips-azure-anila/<key>.mp3 + <key>.json (word timings)
#   python3 azure_all.py ilir    -> .clips-azure-ilir/...
# The subscription key is injected by the session's network proxy for this host: nothing secret lives here.
# Clips are requested as raw PCM and encoded here the same way for both voices (100 ms lead-in, loudness -16 LUFS,
# 24 kHz mono 56 kbps; Azure's long trailing silence is trimmed to 0.25 s), so the two talkers sound equally loud. Azure's REST API gives no word timings, so the
# karaoke timings are estimated: speech is found with silence detection and words share it by length.
import concurrent.futures as cf, hashlib, json, os, re, subprocess, sys, tempfile, time, urllib.error, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REGION = os.environ.get("AZURE_REGION", "swedencentral")
URL = f"https://{REGION}.tts.speech.microsoft.com/cognitiveservices/v1"
VOICES = {"anila": "sq-AL-AnilaNeural", "ilir": "sq-AL-IlirNeural"}
name = sys.argv[1] if len(sys.argv) > 1 else "anila"
VOICE = VOICES[name]
OUT = os.path.join(HERE, ".clips-azure-" + name); os.makedirs(OUT, exist_ok=True)
LEAD = 0.1


def esc(t): return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def synth(text):
    ssml = f"<speak version='1.0' xml:lang='sq-AL'><voice name='{VOICE}'>{esc(text)}</voice></speak>"
    req = urllib.request.Request(URL, data=ssml.encode("utf-8"), headers={
        "Content-Type": "application/ssml+xml", "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm",
        "User-Agent": "shqip-app", "Ocp-Apim-Subscription-Key": "proxy-injected"})
    for attempt in range(8):
        try:
            return urllib.request.urlopen(req, timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 7:
                time.sleep(float(e.headers.get("Retry-After") or 2 ** attempt)); continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if attempt < 7: time.sleep(2 ** attempt); continue
            raise


def timings(mp3, text):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", "silencedetect=n=-38dB:d=0.12", "-f", "null", "-"],
                       capture_output=True, text=True).stderr
    dur = re.search(r"Duration: (\d+):(\d+):([\d.]+)", o); dur = int(dur[2]) * 60 + float(dur[3])
    st = [float(x) for x in re.findall(r"silence_start: ([\d.-]+)", o)]
    en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", o)]
    sil = [(s, en[i] if i < len(en) else dur) for i, s in enumerate(st)]
    a = sil[0][1] if sil and sil[0][0] <= 0.05 else LEAD
    b = sil[-1][0] if sil and sil[-1][1] >= dur - 0.1 else dur
    pauses = [(s, e) for s, e in sil if s > a and e < b]
    spans, cur = [], a                                     # speech pieces between inner pauses
    for s, e in pauses: spans.append((cur, s)); cur = e
    spans.append((cur, b))
    total = sum(e - s for s, e in spans) or 1e-3
    def at(x):                                             # speech-time -> clock time, skipping pauses
        for s, e in spans:
            if x <= e - s: return s + x
            x -= e - s
        return b
    words = text.split(" ")
    wt = [max(1, sum(c.isalpha() for c in w)) + 1 for w in words]
    W, acc, out = sum(wt), 0, []
    for w in wt:
        s0, acc = acc, acc + w
        out.append([round(at(total * s0 / W), 3), round(at(total * acc / W) - .03, 3)])
    return out


def one(text):
    key = hashlib.md5(text.encode()).hexdigest()[:10]
    mp3, js = os.path.join(OUT, key + ".mp3"), os.path.join(OUT, key + ".json")
    if os.path.exists(mp3) and os.path.exists(js): return 0
    pcm = synth(text)
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        f.write(pcm); f.flush()
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f.name, "-af", "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                        f"adelay={int(LEAD * 1000)},apad=pad_dur=0.25,loudnorm=I=-16:TP=-1.5",
                        "-ac", "1", "-ar", "24000", "-b:a", "56k", mp3 + ".tmp.mp3"], check=True)
    os.replace(mp3 + ".tmp.mp3", mp3)
    json.dump(timings(mp3, text), open(js, "w"))
    return len(text)


texts = list(dict.fromkeys(json.load(open(os.path.join(HERE, ".say.json")))))
chars, done, t0 = 0, 0, time.time()
with cf.ThreadPoolExecutor(3) as ex:
    for n in ex.map(one, texts):
        chars += n; done += 1
        if done % 200 == 0: print(f"{name} {done}/{len(texts)} new chars {chars} {time.time() - t0:.0f}s", flush=True)
print(f"{name} done {len(texts)} texts, {chars} characters sent, {time.time() - t0:.0f}s", flush=True)
