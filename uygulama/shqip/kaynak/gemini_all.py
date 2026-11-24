# Generates every app clip with Gemini TTS into kaynak/.clips-gemini/<key>.mp3 (same keys as make.py).
# Resumable: existing clips are skipped. Key comes from GEMINI_KEY (or the proxy's network secret).
import base64, hashlib, json, os, subprocess, sys, time, urllib.request, urllib.error
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
OUT = os.path.join(HERE, ".clips-gemini"); os.makedirs(OUT, exist_ok=True)
MODEL = os.environ.get("GEMINI_TTS_MODEL", "gemini-3.8-flash-tts"); VOICE = os.environ.get("GEMINI_VOICE", "Kore")
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
KEY = os.environ.get("GEMINI_KEY", "placeholder")
d = json.load(open(os.path.join(ROOT, "data.json")))
texts = [w["sq"] for u in d["units"] for w in u["w"]] + [l["sq"] for s in d["stories"] for l in s["lines"]] + [a["ex"] for a in d["alpha"]]
todo = []
for t in texts:
    k = hashlib.md5(t.encode()).hexdigest()[:10]
    if k not in [x[0] for x in todo] and not os.path.exists(os.path.join(OUT, k + ".mp3")): todo.append((k, t))
print("to generate:", len(todo), flush=True)
FILTER = ("silenceremove=start_periods=1:start_threshold=-45dB,areverse,silenceremove=start_periods=1:start_threshold=-45dB,areverse,"
          "adelay=100,loudnorm=I=-16")
fails429 = 0
for n, (k, t) in enumerate(todo, 1):
    body = {"contents": [{"parts": [{"text": f"Read aloud in standard Albanian, clearly and a little slowly, for a language learner. Say only this: {t}"}]}],
            "generationConfig": {"responseModalities": ["AUDIO"], "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": VOICE}}}}}
    for attempt in range(6):
        try:
            req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": KEY})
            r = json.load(urllib.request.urlopen(req, timeout=90)); fails429 = 0
            c = r["candidates"][0]
            if "content" not in c: print("no audio", k, t, c.get("finishReason"), flush=True); time.sleep(7); continue
            pcm = base64.b64decode(c["content"]["parts"][0]["inlineData"]["data"])
            raw = f"/tmp/gem-{k}.pcm"; open(raw, "wb").write(pcm)
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", raw, "-af", FILTER,
                            "-ac", "1", "-ar", "22050", "-b:a", "40k", os.path.join(OUT, k + ".mp3")], check=True)
            os.remove(raw); print(f"{n}/{len(todo)} ok", t, flush=True); break
        except urllib.error.HTTPError as e:
            if e.code == 429:
                fails429 += 1
                if fails429 >= 8: print("STOP: rate/daily limit reached", flush=True); sys.exit(2)
                time.sleep(60); continue
            print("HTTP", e.code, t, e.read()[:200], flush=True); time.sleep(10)
        except Exception as e:
            print("err", t, e, flush=True); time.sleep(10)
    time.sleep(7)
print("DONE", flush=True)
