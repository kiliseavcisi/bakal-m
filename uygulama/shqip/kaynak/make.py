import json, os, subprocess, hashlib, sys
sys.path.insert(0, os.path.dirname(__file__))
from data import UNITS
OUT = "/home/user/bakal-m/uygulama/shqip"
os.makedirs(OUT + "/audio", exist_ok=True)
tmp = "/tmp/claude-0/tts.wav"
units, seen = [], {}
def audio(text):
    key = hashlib.md5(text.encode()).hexdigest()[:10]
    path = f"audio/{key}.mp3"
    if key not in seen:
        seen[key] = 1
        if not os.path.exists(f"{OUT}/{path}"):
            subprocess.run(["espeak-ng","-v","sq+f3","-s","115","-g","4","-w",tmp,text.replace("?","").replace("!","")],check=True)
            subprocess.run(["ffmpeg","-loglevel","error","-y","-i",tmp,"-af","volume=1.6","-ac","1","-ar","22050","-b:a","32k",f"{OUT}/{path}"],check=True)
    return path
for uid, title, words in UNITS:
    units.append({"id":uid,"t":title,"w":[{"sq":sq,"tr":tr,"p":p,"a":audio(sq)} for sq,tr,p in words]})
with open(OUT+"/data.json","w") as f: json.dump(units,f,ensure_ascii=False,separators=(",",":"))
print(len(units), sum(len(u["w"]) for u in units), len(seen))
