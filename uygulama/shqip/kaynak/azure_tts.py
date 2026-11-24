# Regenerates every clip in ../audio with Azure neural Albanian voice.
# The key is injected by the session's network proxy for this host; nothing secret lives here.
import json, os, sys, time, urllib.request
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
URL = "https://westeurope.tts.speech.microsoft.com/cognitiveservices/v1"
VOICE = sys.argv[1] if len(sys.argv) > 1 else "sq-AL-AnilaNeural"
units = json.load(open(os.path.join(ROOT, "data.json")))
done = set()
for u in units:
    for w in u["w"]:
        if w["a"] in done: continue
        done.add(w["a"])
        text = w["sq"].replace("&", "&amp;").replace("<", "&lt;")
        ssml = (f"<speak version='1.0' xml:lang='sq-AL'><voice name='{VOICE}'>"
                f"<prosody rate='-10%'>{text}</prosody></voice></speak>")
        req = urllib.request.Request(URL, data=ssml.encode("utf-8"), headers={
            "Content-Type": "application/ssml+xml",
            "X-Microsoft-OutputFormat": "audio-24khz-48kbitrate-mono-mp3",
            "User-Agent": "shqip-app",
            "Ocp-Apim-Subscription-Key": "placeholder-replaced-by-proxy"})
        for attempt in range(4):
            try:
                data = urllib.request.urlopen(req, timeout=30).read()
                open(os.path.join(ROOT, w["a"]), "wb").write(data); break
            except Exception as e:
                if attempt == 3: raise
                time.sleep(2 ** attempt)
print("ok", len(done))
