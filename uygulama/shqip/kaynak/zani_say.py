"""Try Zani from the command line: turns one Albanian sentence into an audio file.

    export ZANI_API_KEY=zn_live_...            # never commit it
    python3 zani_say.py "Qysh je, shpirt?" --voice arben --dialect kosovo --out qysh.mp3
    python3 zani_say.py --account              # remaining credits
    python3 zani_say.py --voices               # available voices
"""
import argparse, shutil, sys
import zani

ap = argparse.ArgumentParser()
ap.add_argument("text", nargs="?")
ap.add_argument("--voice", default="vjosa")
ap.add_argument("--dialect", choices=sorted(zani.OPTIONS["dialect"]))
ap.add_argument("--emotion", choices=sorted(zani.OPTIONS["emotion"]))
ap.add_argument("--pace", choices=sorted(zani.OPTIONS["pace"]))
ap.add_argument("--purpose", choices=sorted(zani.OPTIONS["purpose"]))
ap.add_argument("--out", default="zani.mp3")
ap.add_argument("--account", action="store_true")
ap.add_argument("--voices", action="store_true")
a = ap.parse_args()
try:
    if a.account:
        print(zani.account()); sys.exit()
    if a.voices:
        for v in zani.voices(): print(f'{v["slug"]:10} {v["gender"]:6} {v["dialect"]:9} {v.get("description", "")[:70]}')
        sys.exit()
    if not a.text:
        ap.error("text is required")
    p = zani.speak(a.text, voice=a.voice, dialect=a.dialect, emotion=a.emotion, pace=a.pace, purpose=a.purpose)
    shutil.copyfile(p, a.out)
    print("ok:", a.out, f"({len(a.text)} karakter)")
except zani.ZaniError as e:
    print("Hata:", e.user_message, file=sys.stderr); sys.exit(1)
