# Generates app clips with the Albanian Kokoro model "llafazani/kokoro-shqip" (Apache-2.0; voices Agon, Dardan).
# Uses the kokoro package (PyPI) for inference and its own small Albanian grapheme-to-phoneme rules below.
# Usage: python kokoro_all.py <model_dir> <voice> [--samples]
#   model_dir holds config.json, kokoro-shqip.pth and voices/<voice>.pt (downloaded from Hugging Face).
import hashlib, json, os, re, subprocess, sys, tempfile, unicodedata, wave
import numpy as np, torch
from kokoro import KModel

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
MODEL_DIR, VOICE = sys.argv[1], sys.argv[2]
SAMPLES = "--samples" in sys.argv

# --- Albanian spelling -> IPA. Albanian is written almost phonemically, so plain rules are enough.
DIGRAPHS = {"xh": "dʒ", "gj": "ɟ", "nj": "ɲ", "sh": "ʃ", "zh": "ʒ", "th": "θ", "dh": "ð", "ll": "ɫ", "rr": "r"}
LETTERS = {"a": "a", "b": "b", "c": "ts", "ç": "tʃ", "d": "d", "e": "ɛ", "ë": "ə", "f": "f", "g": "ɡ", "h": "h", "i": "i",
           "j": "j", "k": "k", "l": "l", "m": "m", "n": "n", "o": "ɔ", "p": "p", "q": "c", "r": "ɾ", "s": "s", "t": "t",
           "u": "u", "v": "v", "x": "dz", "y": "y", "z": "z", "â": "a", "ê": "ɛ", "î": "i", "ô": "ɔ", "û": "u"}   # circumflex: Gheg (Kosovo) nasal vowels
KEEP = set(",.!?;:")

def g2p(text):
    t = unicodedata.normalize("NFC", text).lower().replace("’", "'")
    t = re.sub(r"(?<=\w)'(?=\w)", "", t).replace("'", " ").replace("…", ".").replace(" – ", ", ").replace("-", " ")
    out, i = [], 0
    while i < len(t):
        two = t[i:i + 2]
        if two in DIGRAPHS: out.append(DIGRAPHS[two]); i += 2; continue
        ch = t[i]
        out.append(LETTERS.get(ch, ch if (ch in KEEP or ch == " ") else ""))
        i += 1
    ph = re.sub(r"\s+", " ", "".join(out)).strip()
    if ph and ph[-1] not in ".!?": ph += "."          # a closing stop gives short words a clean ending
    return ph

model = KModel(config=os.path.join(MODEL_DIR, "config.json"),
               model=os.path.join(MODEL_DIR, "kokoro-shqip.pth")).eval()
vocab = model.vocab
pack = torch.load(os.path.join(MODEL_DIR, "voices", VOICE + ".pt"), weights_only=True)
SPEED = {"agon": 0.78 * 1.154, "dardan": 0.78 * 1.168, "pf_dora": 0.66, "if_sara": 0.68, "af_heart": 0.62}.get(VOICE, 0.9) * 0.92   # natural pace, a little slower for learners
FILTER = "adelay=100,apad=pad_dur=0.12,loudnorm=I=-16"     # silence is trimmed in numpy so word timings stay exact
LEAD = 0.1                                                  # seconds added in front by adelay

def word_times(text, ph, dur, spf, offset):
    """Start/end (s) of each space-separated word of text, from the model's per-phoneme durations."""
    times, i, t = [], 0, float(dur[0])
    for wd in text.split(" "):
        n_ph = len("".join(c for c in g2p(wd) if c in vocab or c == " ").rstrip(".").split(" ")) if wd.strip() else 0
        start = None
        for k in range(n_ph):
            while i < len(ph) and ph[i] == " ": t += float(dur[1 + i]); i += 1
            if start is None: start = t
            while i < len(ph) and ph[i] != " ": t += float(dur[1 + i]); i += 1
        if start is None: start = t
        times.append([round(max(0.0, start * spf / 24000 - offset) + LEAD, 3), round(max(0.0, t * spf / 24000 - offset) + LEAD, 3)])
    return times

def synth(text, dst):
    ph = "".join(c for c in g2p(text) if c in vocab or c == " ")
    with torch.no_grad():
        o = model(ph, pack[min(len(ph), len(pack)) - 1], SPEED, return_output=True)
    audio = o.audio.numpy(); dur = o.pred_dur.numpy()
    spf = len(audio) / dur.sum()
    loud = np.nonzero(np.abs(audio) > 10 ** (-45 / 20))[0]
    a, b = (loud[0], loud[-1] + 1) if len(loud) else (0, len(audio))
    times = word_times(text, ph, dur, spf, a / 24000)
    audio = audio[a:b]
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        with wave.open(f.name, "wb") as w:
            w.setnchannels(1); w.setsampwidth(2); w.setframerate(24000)
            w.writeframes((np.clip(audio, -1, 1) * 32767).astype(np.int16).tobytes())
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f.name, "-af", FILTER, "-ac", "1", "-ar", "22050",
                        "-b:a", "48k" if SAMPLES else "40k", dst], check=True)
    json.dump(times, open(dst[:-4] + ".json", "w"))

if SAMPLES:
    out = os.path.join(ROOT, "..", "ses-ornekleri")
    for name, text in [("1-miremengjes", "Mirëmëngjes!"), ("4-gezohem", "Gëzohem që u njohëm."), ("6-rrush", "rrush"),
                       ("8-dua-kafe", "Dua një kafe turke, ju lutem."), ("9-shqiponje", "Shqiponja fluturon mbi mal.")]:
        synth(text, os.path.join(out, f"kokoro-{VOICE}-{name}.mp3")); print("ok", name)
    sys.exit()

OUT = os.path.join(HERE, ".clips-kokoro-" + VOICE); os.makedirs(OUT, exist_ok=True)
d = json.load(open(os.path.join(ROOT, "data.json")))
SAYF = os.path.join(HERE, ".say.json")
texts = (json.load(open(SAYF)) if os.path.exists(SAYF) else []) + ([w["sq"] for u in d["units"] for w in u["w"]] + [l["sq"] for s in d["stories"] for l in s["lines"]] +
         [a["ex"] for a in d["alpha"]] + [x["sq"] for p in d.get("pairs", []) for pr in p["pairs"] for x in pr] + [x["sq"] for x in d.get("extra", [])])
n = 0
for t in dict.fromkeys(texts):
    dst = os.path.join(OUT, hashlib.md5(t.encode()).hexdigest()[:10] + ".mp3")
    if not os.path.exists(dst[:-4] + ".json"): synth(t, dst); n += 1
print("generated", n, "total", len([f for f in os.listdir(OUT) if f.endswith(".mp3")]))
