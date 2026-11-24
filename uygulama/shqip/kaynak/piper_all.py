# Generates every app clip with the Piper Albanian voice "Edon" (rhasspy/piper-voices sq_AL-edon-medium)
# into kaynak/.clips-piper/<key>.mp3 (same keys as make.py). Usage: python piper_all.py <path/to/sq_AL-edon-medium.onnx>
import hashlib, json, os, subprocess, sys, tempfile, wave
from piper import PiperVoice, SynthesisConfig
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, ".clips-piper"); os.makedirs(OUT, exist_ok=True)
voice = PiperVoice.load(sys.argv[1])
cfg = SynthesisConfig(length_scale=1.1)          # a little slower for learners
d = json.load(open(os.path.join(ROOT, "data.json")))
texts = [w["sq"] for u in d["units"] for w in u["w"]] + [l["sq"] for s in d["stories"] for l in s["lines"]] + [a["ex"] for a in d["alpha"]] + [x["sq"] for p in d.get("pairs", []) for pr in p["pairs"] for x in pr]
done = 0
for t in dict.fromkeys(texts):
    k = hashlib.md5(t.encode()).hexdigest()[:10]
    dst = os.path.join(OUT, k + ".mp3")
    if os.path.exists(dst): continue
    with tempfile.NamedTemporaryFile(suffix=".wav") as f:
        with wave.open(f.name, "wb") as wf:
            voice.synthesize_wav(t.replace("…", "."), wf, syn_config=cfg)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f.name, "-af", "adelay=100,loudnorm=I=-16",
                        "-ac", "1", "-ar", "22050", "-b:a", "40k", dst], check=True)
    done += 1
print("generated", done, "total", len(os.listdir(OUT)))
