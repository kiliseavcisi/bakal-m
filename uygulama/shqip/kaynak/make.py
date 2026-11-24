# Builds data.json and audio packs (one JSON of base64 mp3 clips per unit/story) with Meta MMS (facebook/mms-tts-sqi).
# Usage: python make.py <path-to-mms-model-dir-or-hub-id>
import base64, hashlib, json, os, subprocess, sys, tempfile
import numpy as np, scipy.io.wavfile, torch
from transformers import VitsModel, AutoTokenizer
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from data import UNITS
from extra import UNIT_INFO, STORIES, ALPHA, YT
from sezon2 import UNITS2, STORIES2, VIDEO_GROUPS
from gloss import FUNCTION
from visual import UNIT_LOOK, EXTRA_PICS, STORY_LOOK, AVATARS

OUT = os.path.dirname(HERE)
CACHE = os.path.join(HERE, ".clips"); os.makedirs(CACHE, exist_ok=True)
os.makedirs(OUT + "/packs", exist_ok=True)
MODEL = sys.argv[1] if len(sys.argv) > 1 else "facebook/mms-tts-sqi"
model = VitsModel.from_pretrained(MODEL).eval(); tok = AutoTokenizer.from_pretrained(MODEL)
model.config.speaking_rate = 0.9; model.config.noise_scale = 0.5
packs = {}

def clean(t):
    t = t.lower().replace("?", ",").replace("!", ",").replace(".", ",").replace("…", "")
    return " ".join("".join(c for c in t if c.isalpha() or c in " '-").split())

def clip(text):
    key = hashlib.md5(text.encode()).hexdigest()[:10]
    dst = os.path.join(CACHE, key + ".mp3")
    if not os.path.exists(dst):
        torch.manual_seed(7)
        with torch.no_grad():
            w = model(**tok(clean(text), return_tensors="pt")).waveform[0].numpy()
        w = w / max(1e-6, float(np.abs(w).max())) * 0.9
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            scipy.io.wavfile.write(f.name, model.config.sampling_rate, (w * 32767).astype(np.int16))
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f.name, "-af", "adelay=100,loudnorm=I=-16",
                            "-ac", "1", "-ar", "22050", "-b:a", "40k", dst], check=True)
    return key

GEMINI = os.path.join(HERE, ".clips-gemini")
VOICE_DIR = os.path.join(HERE, os.environ.get("VOICE_DIR", ".clips-piper"))   # chosen voice: Piper "Edon"
def audio(pack, text):
    key = hashlib.md5(text.encode()).hexdigest()[:10]
    chosen = os.path.join(VOICE_DIR, key + ".mp3")
    src = chosen if os.path.exists(chosen) else os.path.join(CACHE, clip(text) + ".mp3")   # fall back to MMS
    packs.setdefault(pack, {})[key] = base64.b64encode(open(src, "rb").read()).decode()
    return pack + "#" + key

units, used_videos = [], set()
for uid, title, words in UNITS:
    vid, vtitle, tips = UNIT_INFO[uid]; used_videos.add(vid)
    units.append({"id": uid, "t": title, "season": 1, "tips": tips,
                  "ic": UNIT_LOOK[uid][0], "hue": UNIT_LOOK[uid][1],
                  "w": [{"sq": sq, "tr": tr, "p": p or EXTRA_PICS.get(sq, ""), "a": audio(uid, sq)} for sq, tr, p in words]})
for uid, title, vid, vtitle, words, tips in UNITS2:
    used_videos.add(vid)
    units.append({"id": uid, "t": title, "season": 2, "tips": tips,
                  "ic": UNIT_LOOK[uid][0], "hue": UNIT_LOOK[uid][1],
                  "w": [{"sq": sq, "tr": tr, "p": p or EXTRA_PICS.get(sq, ""), "a": audio(uid, sq)} for sq, tr, p in words]})
stories = []
for s in STORIES + STORIES2:
    used_videos.add(s["src"][0])
    stories.append({"id": s["id"], "t": s["t"], "after": s["after"],
                    "cover": STORY_LOOK.get(s["id"], "📖"),
                    "lines": [{"who": who, "av": AVATARS.get(who, ""), "sq": sq, "tr": tr, "a": audio("s-" + s["id"], sq)} for who, sq, tr in s["lines"]],
                    "q": [{"q": q, "o": o, "c": c} for q, o, c in s["q"]]})
alpha = [{"l": l, "say": say, "hint": hint, "ex": ex, "tr": tr, "d": bool(d), "a": audio("alfabe", ex)} for l, say, hint, ex, tr, d in ALPHA]
used_videos.add("QxxBvnhw3AA")

# Video library: every video in the playlist, grouped, with whether its notes were transcribed.
rows = [l.rstrip("\n").split("|", 3) for l in open(os.path.join(OUT, "..", "..", "notlar", "playlist.txt"))]
videos = []
for idx, vid, dur, title in rows:
    i = int(idx); g = next(lbl for a, b, lbl in VIDEO_GROUPS if a <= i <= b)
    videos.append({"n": i, "id": vid, "t": title.strip(), "min": round(int(dur) / 60), "g": g,
                   "notes": i <= 31, "inApp": vid in used_videos})

# Tap-to-translate dictionaries
gloss = {}
for u in units:
    for w in u["w"]:
        k = w["sq"].lower().strip("?!.… ")
        if " " not in k or k.startswith(("i ", "e ")):
            gloss.setdefault(k, w["tr"])
            if k.startswith(("i ", "e ")): gloss.setdefault(k[2:], w["tr"])
gloss.update(FUNCTION)
rev = {}
for u in units:
    for w in u["w"]:
        t = w["tr"].lower().split(" (")[0].split(",")[0].split(" / ")[0].strip("?!. ")
        if " " not in t and " " not in w["sq"].strip("?!. "): rev.setdefault(t, w["sq"].strip("?!. "))

for name, d in packs.items():
    json.dump(d, open(os.path.join(OUT, "packs", name + ".json"), "w"), separators=(",", ":"))
json.dump({"units": units, "stories": stories, "alpha": alpha, "gloss": gloss, "rev": rev}, open(os.path.join(OUT, "data.json"), "w"), ensure_ascii=False, separators=(",", ":"))
print("voice clips", len(os.listdir(VOICE_DIR)) if os.path.isdir(VOICE_DIR) else 0, "units", len(units), "words", sum(len(u["w"]) for u in units), "stories", len(stories), "packs", len(packs),
      "clips", sum(len(p) for p in packs.values()))
