# Regenerates every clip in ../audio with Meta's open MMS Albanian voice (facebook/mms-tts-sqi, CC BY-NC 4.0).
# Usage: python mms_tts.py   (needs torch, transformers, scipy; ffmpeg on PATH)
import json, os, subprocess, tempfile
import numpy as np, torch, scipy.io.wavfile
from transformers import VitsModel, AutoTokenizer

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
model = VitsModel.from_pretrained("facebook/mms-tts-sqi").eval()
tok = AutoTokenizer.from_pretrained("facebook/mms-tts-sqi")
model.config.speaking_rate = 0.9      # a little slower for learners
model.config.noise_scale = 0.5        # steadier pronunciation

def clean(t):
    # the model's vocabulary is lowercase letters; drop punctuation
    return " ".join(t.lower().replace("?", "").replace("!", "").replace("'", "").replace("…", "").split())

units = json.load(open(os.path.join(ROOT, "data.json")))
done = set()
for u in units:
    for w in u["w"]:
        if w["a"] in done:
            continue
        done.add(w["a"])
        text = clean(w["sq"])
        inputs = tok(text, return_tensors="pt")
        torch.manual_seed(7)
        with torch.no_grad():
            wav = model(**inputs).waveform[0].numpy()
        wav = wav / max(1e-6, float(np.abs(wav).max())) * 0.9
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            scipy.io.wavfile.write(f.name, model.config.sampling_rate, (wav * 32767).astype(np.int16))
            out = os.path.join(ROOT, w["a"])
            # pad 120 ms of silence at the start so phones don't clip the first syllable
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f.name, "-af", "adelay=120,loudnorm=I=-16",
                            "-ac", "1", "-ar", "22050", "-b:a", "48k", out], check=True)
print("ok", len(done))
