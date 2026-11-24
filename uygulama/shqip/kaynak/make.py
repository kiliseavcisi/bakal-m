# Builds data.json and generates every clip with Meta MMS (facebook/mms-tts-sqi).
# Usage: python make.py <path-to-mms-model-dir-or-hub-id>
import hashlib, json, os, subprocess, sys, tempfile
import numpy as np, scipy.io.wavfile, torch
from transformers import VitsModel, AutoTokenizer
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from data import UNITS
from extra import UNIT_INFO, STORIES, ALPHA, YT

OUT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL = sys.argv[1] if len(sys.argv) > 1 else "facebook/mms-tts-sqi"
os.makedirs(OUT + "/audio", exist_ok=True)
model = VitsModel.from_pretrained(MODEL).eval(); tok = AutoTokenizer.from_pretrained(MODEL)
model.config.speaking_rate = 0.9; model.config.noise_scale = 0.5
made = {}

def clean(t):
    t = t.lower().replace("?", ",").replace("!", ",").replace(".", ",").replace("…", "")
    return " ".join("".join(c for c in t if c.isalpha() or c in " '-").split())

def audio(text):
    key = "m" + hashlib.md5(text.encode()).hexdigest()[:10]
    path = f"audio/{key}.mp3"
    if key not in made:
        made[key] = 1
        dst = os.path.join(OUT, path)
        if not os.path.exists(dst):
            torch.manual_seed(7)
            with torch.no_grad():
                w = model(**tok(clean(text), return_tensors="pt")).waveform[0].numpy()
            w = w / max(1e-6, float(np.abs(w).max())) * 0.9
            with tempfile.NamedTemporaryFile(suffix=".wav") as f:
                scipy.io.wavfile.write(f.name, model.config.sampling_rate, (w * 32767).astype(np.int16))
                subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f.name, "-af", "adelay=100,loudnorm=I=-16",
                                "-ac", "1", "-ar", "22050", "-b:a", "40k", dst], check=True)
    return path

units = []
for uid, title, words in UNITS:
    vid, vtitle, tips = UNIT_INFO[uid]
    units.append({"id": uid, "t": title, "video": {"url": YT + vid, "t": vtitle}, "tips": tips,
                  "w": [{"sq": sq, "tr": tr, "p": p, "a": audio(sq)} for sq, tr, p in words]})
stories = []
for s in STORIES:
    stories.append({"id": s["id"], "t": s["t"], "after": s["after"], "video": {"url": YT + s["src"][0], "t": s["src"][1]},
                    "lines": [{"who": who, "sq": sq, "tr": tr, "a": audio(sq)} for who, sq, tr in s["lines"]],
                    "q": [{"q": q, "o": o, "c": c} for q, o, c in s["q"]]})
alpha = [{"l": l, "say": say, "hint": hint, "ex": ex, "tr": tr, "d": bool(d), "a": audio(ex)} for l, say, hint, ex, tr, d in ALPHA]
alpha_video = {"url": YT + "QxxBvnhw3AA", "t": "Ders 1 · Alfabe ve telaffuz"}
json.dump({"units": units, "stories": stories, "alpha": alpha, "alphaVideo": alpha_video},
          open(os.path.join(OUT, "data.json"), "w"), ensure_ascii=False, separators=(",", ":"))
print("units", len(units), "words", sum(len(u["w"]) for u in units), "clips", len(made))
