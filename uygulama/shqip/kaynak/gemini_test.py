# Generates a few Albanian test clips with Gemini TTS. The API key is injected by the network proxy
# (Network secret for generativelanguage.googleapis.com, header x-goog-api-key); nothing secret lives here.
import base64, json, os, subprocess, sys, urllib.request
OUT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "..", "ses-ornekleri")
MODEL = sys.argv[1] if len(sys.argv) > 1 else "gemini-2.5-flash-preview-tts"
VOICES = sys.argv[2].split(",") if len(sys.argv) > 2 else ["Kore", "Puck"]
TEXTS = [("1-miremengjes", "Mirëmëngjes!"), ("4-gezohem", "Gëzohem që u njohëm."), ("6-rrush", "rrush"),
         ("8-dua-kafe", "Dua një kafe turke, ju lutem."), ("9-shqiponje", "Shqiponja fluturon mbi mal.")]
URL = f"https://generativelanguage.googleapis.com/v1beta/models/{MODEL}:generateContent"
for voice in VOICES:
    for name, text in TEXTS:
        body = {"contents": [{"parts": [{"text": f"Read aloud in standard Albanian, clearly and a little slowly, for a language learner. Say only this: {text}"}]}],
                "generationConfig": {"responseModalities": ["AUDIO"],
                                     "speechConfig": {"voiceConfig": {"prebuiltVoiceConfig": {"voiceName": voice}}}}}
        req = urllib.request.Request(URL, data=json.dumps(body).encode(), headers={"Content-Type": "application/json", "x-goog-api-key": os.environ.get("GEMINI_KEY", "placeholder")})
        r = json.load(urllib.request.urlopen(req, timeout=60))
        c = r["candidates"][0]
        if "content" not in c: print("no audio", voice, name, c.get("finishReason")); continue
        pcm = base64.b64decode(c["content"]["parts"][0]["inlineData"]["data"])
        raw = f"/tmp/gem-{voice}-{name}.pcm"; open(raw, "wb").write(pcm)
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-f", "s16le", "-ar", "24000", "-ac", "1", "-i", raw,
                        "-b:a", "64k", os.path.join(OUT, f"gemini-{voice}-{name}.mp3")], check=True)
        print("ok", voice, name)
