# Builds ../data.json and the audio packs for the English app with Azure neural voices.
#   main voice  packs/        en-US Ava HD (female)
#   second      packs2/       en-US Andrew HD (male): men in stories, role-plays and comic panels speak with it
#   variety     packsv/sonia/ en-GB Sonia (female): a British talker now and then in listening drills
# The Azure key is injected by the session's network proxy (swedencentral); nothing secret lives here.
import base64, concurrent.futures as cf, hashlib, json, os, re, subprocess, sys, tempfile, time, urllib.error, urllib.request
from content_en import UNITS, PATTERNS, PAIRS, SOUNDS, ROLES, STORIES, MOD, GLOSS_EXTRA, BOARDS

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.dirname(HERE)
URL = "https://swedencentral.tts.speech.microsoft.com/cognitiveservices/v1"
VOICES = {"avahd": ("en-US", "en-US-Ava:DragonHDLatestNeural"), "andrewhd": ("en-US", "en-US-Andrew:DragonHDLatestNeural"), "sonia": ("en-GB", "en-GB-SoniaNeural"),
          "teacher": ("tr-TR", "en-US-Ava:DragonHDLatestNeural")}   # HD voices; the teacher is Ava HD speaking Turkish (it switches to English words by itself)
FEMALE = {"Emma", "Mom", "Ms. Lee"}
AV = {"Emma": "👩", "Jack": "👨", "Mom": "👩‍🦰", "Dad": "👨‍🦱", "Leo": "👦", "Ms. Lee": "👩‍🏫", "Waiter": "🧑‍🍳", "Driver": "🧑‍✈️", "Clerk": "🧑‍💼"}
LEAD = 0.1
key = lambda t: hashlib.md5(t.encode()).hexdigest()[:10]
esc = lambda t: t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def synth(text, voice):
    lang, name = VOICES[voice]
    ssml = f"<speak version='1.0' xml:lang='{lang}'><voice name='{name}'>{esc(text)}</voice></speak>"
    req = urllib.request.Request(URL, data=ssml.encode(), headers={"Content-Type": "application/ssml+xml",
        "X-Microsoft-OutputFormat": "riff-24khz-16bit-mono-pcm", "User-Agent": "english-app", "Ocp-Apim-Subscription-Key": "proxy-injected"})
    for attempt in range(8):
        try: return urllib.request.urlopen(req, timeout=60).read()
        except urllib.error.HTTPError as e:
            if e.code in (429, 500, 502, 503, 504) and attempt < 7: time.sleep(float(e.headers.get("Retry-After") or 2 ** attempt)); continue
            raise
        except (urllib.error.URLError, TimeoutError):
            if attempt < 7: time.sleep(2 ** attempt); continue
            raise


def timings(mp3, text):
    o = subprocess.run(["ffmpeg", "-hide_banner", "-i", mp3, "-af", "silencedetect=n=-38dB:d=0.12", "-f", "null", "-"], capture_output=True, text=True).stderr
    d = re.search(r"Duration: (\d+):(\d+):([\d.]+)", o); dur = int(d[2]) * 60 + float(d[3])
    st = [float(x) for x in re.findall(r"silence_start: ([\d.-]+)", o)]; en = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", o)]
    sil = [(s, en[i] if i < len(en) else dur) for i, s in enumerate(st)]
    a = sil[0][1] if sil and sil[0][0] <= 0.05 else LEAD
    b = sil[-1][0] if sil and sil[-1][1] >= dur - 0.1 else dur
    spans, cur = [], a
    for s, e in [(s, e) for s, e in sil if s > a and e < b]: spans.append((cur, s)); cur = e
    spans.append((cur, b)); total = sum(e - s for s, e in spans) or 1e-3
    def at(x):
        for s, e in spans:
            if x <= e - s: return s + x
            x -= e - s
        return b
    wt = [max(1, sum(c.isalpha() for c in w)) + 1 for w in text.split(" ")]; W, acc, out = sum(wt), 0, []
    for w in wt:
        s0, acc = acc, acc + w
        out.append([round(at(total * s0 / W), 3), round(at(total * acc / W) - .03, 3)])
    return out


def clip(text, voice):
    d = os.path.join(HERE, ".clips-" + voice); os.makedirs(d, exist_ok=True)
    mp3, js = os.path.join(d, key(text) + ".mp3"), os.path.join(d, key(text) + ".json")
    if not (os.path.exists(mp3) and os.path.exists(js)):
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            f.write(synth(text, voice)); f.flush()
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f.name, "-af",
                "silenceremove=start_periods=1:start_threshold=-50dB,areverse,silenceremove=start_periods=1:start_threshold=-50dB,areverse,"
                f"adelay={int(LEAD * 1000)},apad=pad_dur=0.25,loudnorm=I=-16:TP=-1.5", "-ac", "1", "-ar", "24000", "-b:a", "56k", mp3 + ".tmp.mp3"], check=True)
        os.replace(mp3 + ".tmp.mp3", mp3); json.dump(timings(mp3, text), open(js, "w"))
    return mp3, json.load(open(js))


# ---- collect every spoken text, grouped by pack ----
WANT = {}                       # pack -> ordered texts
def audio(pack, text):
    WANT.setdefault(pack, {})[text] = 1
    return pack + "#" + key(text)
NARR = {}                       # Turkish teacher narration (Emel), main pack only
def narr(text):
    NARR[text] = 1
    return "tahta#" + key(text)
K = {}                          # text -> [main timings, second timings]
def tm(text): return K.get(text, [None, None])

def filled(x, o): return re.sub(r"\s*\([^)]*\)", "", x.replace("___", o)).replace(" .", ".").strip()

def split_blocks(text, target):
    i = text.find(target)
    if i < 0: return [[text, 0], [target, 1]]          # Turkish has no piece here (zero copula): show the idea in red
    pre, post = text[:i].strip(), text[i + len(target):].strip()
    out = [[pre, 0]] if pre else []
    out.append([target, 1])
    if post:
        if re.fullmatch(r"[.!?,…:;]+", post): out[-1][0] += post
        else: out.append([post, 0])
    return out


def build():
    units = []
    for uid, t, ic, hue, tips, words in UNITS:
        units.append({"id": uid, "t": t, "season": 1, "tips": tips, "ic": ic, "hue": hue, "mod": 0, "lv": "A1",
                      "w": [{"sq": en, "tr": tr, "p": p, "a": audio(uid, en), "k": tm(en), "m": None} for en, tr, p in words]})
    pats = []
    for p in PATTERNS:
        exs = []
        for who, mood, sc, en, tr, ent, trt in p["ex"]:
            exs.append({"who": who, "mood": mood, "scene": sc, "trb": split_blocks(tr, trt), "sqb": split_blocks(en, ent), "sq": en, "tr": tr, "a": audio("kalip", en), "k": tm(en)})
        drills = [dict(s=x, o=o, c=0, tr=tr, why=why, full=filled(x, o[0]), a=audio("kalip", filled(x, o[0])), k=tm(filled(x, o[0]))) for x, o, tr, why in p["drills"]]
        board = [{"t": say, "rows": rows, "clear": clear, "a": narr(say), "en": [{"sq": e, "tr": "", "a": audio("kalip", e), "k": tm(e)} for e in ens]}
                 for say, rows, ens, clear in BOARDS.get(p["id"], [])]
        pats.append({"id": p["id"], "unit": p["unit"], "t": p["t"], "rule": p["rule"], "ex": exs, "drills": drills, "builder": False, "board": board})
    stories = []
    for s in STORIES:
        pid = "s-" + s["id"]
        stories.append({"id": s["id"], "t": s["t"], "after": s["after"], "kind": "story", "lv": "A1", "cover": s["cover"], "scene": s["scene"],
                        "lines": [{"who": w, "av": AV.get(w, "🧑"), "f": w in FEMALE, "sq": en, "tr": tr, "a": audio(pid, en), "k": tm(en)} for w, en, tr in s["lines"]],
                        "q": [{"q": q, "o": o, "c": c} for q, o, c in s["q"]], "pre": [], "cov": 100, "cov2": 100})
    pairs = [{"id": i, "t": t, "tip": tip, "pairs": [[{"sq": a, "tr": at, "a": audio("ciftler", a)}, {"sq": b, "tr": bt, "a": audio("ciftler", b)}] for (a, at), (b, bt) in ps]}
             for i, t, tip, ps in PAIRS]
    alpha = [{"l": l, "say": "", "hint": hint, "ex": ex, "tr": tr, "d": d, "a": audio("sounds", word)} for l, word, hint, ex, tr, d in SOUNDS]
    roles = []
    for r in ROLES:
        roles.append({"id": r["id"], "t": r["t"], "cover": r["cover"], "npc": r["npc"], "av": AV.get(r["npc"], "🧑"), "f": r["npc"] in FEMALE, "goal": r["goal"],
                      "turns": [{"sq": q, "tr": qt, "a": audio("roller", q), "k": tm(q),
                                 "o": [{"sq": o, "tr": ot, "ok": ok, "fb": fb, "a": audio("roller", o), "k": tm(o)} for o, ot, ok, fb in opts]} for q, qt, opts in r["turns"]]})
    wr = dict(MOD["wr"]); wr["a"] = audio("roller", wr["sq"]); wr["k"] = tm(wr["sq"])
    mods = [dict(MOD, wr=wr)]
    gloss, rev = dict(GLOSS_EXTRA), {}
    for _, _, _, _, _, words in UNITS:
        for en, tr, _ in words:
            if " " not in en.strip(".!?"): gloss.setdefault(en.lower().strip(".!?"), tr); rev.setdefault(tr.split(",")[0].strip().lower(), en)
    return {"units": units, "stories": stories, "alpha": alpha, "gloss": gloss, "rev": rev, "pairs": pairs, "extra": [], "roles": roles,
            "conj": None, "gram": [], "freq": [], "mods": mods, "pats": pats, "nums": []}


data = build()
texts = list(dict.fromkeys(t for p in WANT.values() for t in p))
print("texts", len(texts), "chars", sum(map(len, texts)), flush=True)
jobs = [(t, v) for v in ("avahd", "andrewhd", "sonia") for t in texts] + [(t, "teacher") for t in NARR]
with cf.ThreadPoolExecutor(3) as ex:
    res = dict(zip(jobs, ex.map(lambda j: clip(*j), jobs)))
for t in texts: K[t] = [res[(t, "avahd")][1], res[(t, "andrewhd")][1]]
data = build()                  # again, now with timings
dirs = {"avahd": "packs", "andrewhd": "packs2", "sonia": os.path.join("packsv", "sonia")}
for v, d in dirs.items():
    os.makedirs(os.path.join(OUT, d), exist_ok=True)
    for pack, ts in WANT.items():
        json.dump({key(t): base64.b64encode(open(res[(t, v)][0], "rb").read()).decode() for t in ts},
                  open(os.path.join(OUT, d, pack + ".json"), "w"), separators=(",", ":"))
if NARR:
    json.dump({key(t): base64.b64encode(open(res[(t, "teacher")][0], "rb").read()).decode() for t in NARR},
              open(os.path.join(OUT, "packs", "tahta.json"), "w"), separators=(",", ":"))
    import shutil; shutil.copy(os.path.join(OUT, "packs", "tahta.json"), os.path.join(OUT, "packs2", "tahta.json"))   # same teacher in both talkers
json.dump(data, open(os.path.join(OUT, "data.json"), "w"), ensure_ascii=False, separators=(",", ":"))
print("units", len(data["units"]), "words", sum(len(u["w"]) for u in data["units"]), "pats", len(data["pats"]), "stories", len(data["stories"]), "packs", len(WANT))
