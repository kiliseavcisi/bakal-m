"""Voice the Kosovo (Gheg) content of the course with Zani's real Kosovo voices.

    export ZANI_API_KEY=zn_live_...
    python3 zani_kosova.py --dry-run     # list what would be voiced and the credit cost
    python3 zani_kosova.py               # generate (cached; re-running costs nothing)
    python3 make.py                      # rebuild: these clips replace the synthetic ones

Writes .zani-map.json: {albanian text: cached mp3 path}. make.py reads it.
A budget guard stops before the account runs out of credits.
"""
import json, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import zani
from a2 import UNITS3
from a2_stories import STORIES3
from v5_units import ROLES2, TEXTS

MALE, FEMALE_VOICE = "arben", "vjosa"          # arben: Kosovo male; no female Kosovo voice yet, so vjosa with dialect=kosovo
FEMALE = {"Gjyshja", "Nëna", "Ana", "Shoqja"}
items = []                                      # (text, voice)
kos = next(u for u in UNITS3 if u[0] == "kosova")
for sq, tr, p in kos[4]:
    items.append((sq, MALE))
for s in STORIES3:
    if s["id"] == "prishtina":
        items += [(sq, FEMALE_VOICE if who in FEMALE else MALE) for who, sq, tr in s["lines"]]
for r in ROLES2:
    if r["id"] == "rp-gjyshja":
        for sq, tr, opts in r["turns"]:
            items.append((sq, FEMALE_VOICE))
            items += [(o[0], MALE) for o in opts if o[2]]
for tid, *_rest in TEXTS:
    if tid == "t-dasma":
        items += [(sq, FEMALE_VOICE if who in FEMALE else MALE) for who, sq, tr in _rest[4]]
items = list(dict.fromkeys(items))
cost = sum(len(t) for t, v in items)
print(f"{len(items)} clips, {cost} characters (= credits)")
if "--dry-run" in sys.argv:
    for t, v in items: print(f"  [{v}] {t}")
    sys.exit()

MAP = os.path.join(HERE, ".zani-map.json")
done = json.load(open(MAP)) if os.path.exists(MAP) else {}
try:
    credits = zani.account().get("credits", 0)
except zani.ZaniError as e:
    print("Hata:", e.user_message); sys.exit(1)
need = sum(len(t) for t, v in items if t not in done)
print("credits:", credits, "needed:", need)
if need > credits:
    print("Kredi yetmiyor; sadece sığanlar üretilecek.")
for t, v in items:
    if t in done and os.path.exists(done[t]):
        continue
    if len(t) > credits:
        print("skip (credits):", t); continue
    try:
        done[t] = zani.speak(t, voice=v, dialect="kosovo", purpose="education", pace="medium")
        credits -= len(t)
        print("ok", v, t)
    except zani.ZaniCreditsError:
        print("Kredi bitti."); break
    except zani.ZaniError as e:
        print("Hata:", e.user_message, "|", t)
    json.dump(done, open(MAP, "w"), ensure_ascii=False, indent=0)
    time.sleep(1.1)                             # stay under 60 requests per minute
json.dump(done, open(MAP, "w"), ensure_ascii=False, indent=0)
print(len(done), "clips ready")
