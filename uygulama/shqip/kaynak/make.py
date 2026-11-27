# Builds data.json and audio packs (one JSON of base64 mp3 clips per unit/story) with Meta MMS (facebook/mms-tts-sqi).
# Usage: python make.py <path-to-mms-model-dir-or-hub-id>
import base64, hashlib, json, os, subprocess, sys, tempfile
import numpy as np, scipy.io.wavfile, torch
from transformers import VitsModel, AutoTokenizer
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from data import UNITS
from extra import UNIT_INFO, STORIES, ALPHA, YT
from sezon2 import UNITS2, STORIES2, VIDEO_GROUPS
from gloss import FUNCTION
from visual import UNIT_LOOK, EXTRA_PICS, STORY_LOOK, AVATARS, FEMALE
from pairs import PAIRS
from memo import MEMO
from a2 import UNITS3
from a2_stories import STORIES3, ROLES
from freq import UNITS_F
from new_units import UNITS_N, MODULES
from v5_units import UNITS_V5, PLACE, MODULE_B1, MODULE_ROLES, ROLES2, TEXTS, GRAM2
from curriculum import MODULES_V7, TITLES, UNITS_V7, LOOK_V7, PATTERNS_V7, STORY_AFTER
MODULES = [list(M) for M in MODULES_V7]          # curriculum v7: one research-ordered spine (see curriculum.py)
try:
    from story_gloss import STORY_GLOSS
except ImportError:
    STORY_GLOSS = {}
from stories4 import STORIES4
from gram import GRAM
import csv, re
from patterns import PATTERNS, NUMBERS
from patterns2 import PATTERNS2, EXTRA_EX
from verbs import VERBS, TENSES, PRON, rows as verb_rows

OUT = os.path.dirname(HERE)
CACHE = os.path.join(HERE, ".clips"); os.makedirs(CACHE, exist_ok=True)
os.makedirs(OUT + "/packs", exist_ok=True)
MODEL = sys.argv[1] if len(sys.argv) > 1 else "facebook/mms-tts-sqi"
NO_MMS = os.environ.get("NO_MMS")       # first pass for new content: list texts, skip the MMS fallback
if not NO_MMS:
    model = VitsModel.from_pretrained(MODEL).eval(); tok = AutoTokenizer.from_pretrained(MODEL)
    model.config.speaking_rate = 0.9; model.config.noise_scale = 0.5
SAY = []
packs = {}
packs2 = {}

def clean(t):
    t = t.lower().replace("?", ",").replace("!", ",").replace(".", ",").replace("…", "")
    return " ".join("".join(c for c in t if c.isalpha() or c in " '-").split())

def clip(text):
    key = hashlib.md5(text.encode()).hexdigest()[:10]
    dst = os.path.join(CACHE, key + ".mp3")
    if not os.path.exists(dst):
        torch.manual_seed(7)
        with torch.no_grad():
            w = model(**tok(clean(text), return_tensors="pt")).waveform[0].numpy()
        w = w / max(1e-6, float(np.abs(w).max())) * 0.9
        with tempfile.NamedTemporaryFile(suffix=".wav") as f:
            scipy.io.wavfile.write(f.name, model.config.sampling_rate, (w * 32767).astype(np.int16))
            subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", f.name, "-af", "adelay=100,loudnorm=I=-16",
                            "-ac", "1", "-ar", "22050", "-b:a", "40k", dst], check=True)
    return key

GEMINI = os.path.join(HERE, ".clips-gemini")
VOICE_DIR = os.path.join(HERE, os.environ.get("VOICE_DIR", ".clips-azure-anila"))      # main voice: Azure neural "Anila" (female), azure_all.py
ALT_DIR = os.path.join(HERE, os.environ.get("ALT_DIR", ".clips-azure-ilir"))           # second voice: Azure neural "Ilir" (male); men speak with it
# Real Kosovo voices from Zani (zani_kosova.py): these clips replace the synthetic ones for both talkers
ZMAP_F = os.path.join(HERE, ".zani-map.json")
ZMAP = {t: p for t, p in (json.load(open(ZMAP_F)).items() if os.path.exists(ZMAP_F) else []) if os.path.exists(p)}
def tm(text):
    """word timings [[start, end], ...] for the main and the second voice (karaoke highlighting)"""
    if text in ZMAP: return [None, None]          # no word timings for Zani clips: the whole line lights up
    key = hashlib.md5(text.encode()).hexdigest()[:10]
    out = []
    for d in (VOICE_DIR, ALT_DIR):
        f = os.path.join(d, key + ".json")
        out.append(json.load(open(f)) if os.path.exists(f) else None)
    return out

def audio(pack, text):
    key = hashlib.md5(text.encode()).hexdigest()[:10]
    chosen = os.path.join(VOICE_DIR, key + ".mp3")
    SAY.append(text)
    if text in ZMAP:
        b64 = base64.b64encode(open(ZMAP[text], "rb").read()).decode()
        packs.setdefault(pack, {})[key] = b64; packs2.setdefault(pack, {})[key] = b64
        return pack + "#" + key
    if NO_MMS and not (os.path.exists(chosen) and os.path.exists(os.path.join(ALT_DIR, key + ".mp3"))): return pack + "#" + key
    src = chosen if os.path.exists(chosen) else os.path.join(CACHE, clip(text) + ".mp3")   # fall back to MMS
    packs.setdefault(pack, {})[key] = base64.b64encode(open(src, "rb").read()).decode()
    alt = os.path.join(ALT_DIR, key + ".mp3")                                         # second talker (male)
    if not os.path.exists(alt): alt = os.path.join(CACHE, clip(text) + ".mp3")
    packs2.setdefault(pack, {})[key] = base64.b64encode(open(alt, "rb").read()).decode()
    return pack + "#" + key

units, used_videos = [], set()
for uid, title, words in UNITS:
    vid, vtitle, tips = UNIT_INFO[uid]; used_videos.add(vid)
    units.append({"id": uid, "t": title, "season": 1, "tips": tips,
                  "ic": UNIT_LOOK[uid][0], "hue": UNIT_LOOK[uid][1],
                  "w": [{"sq": sq, "tr": tr, "p": p or EXTRA_PICS.get(sq, ""), "a": audio(uid, sq), "k": tm(sq), "m": MEMO.get(sq)} for sq, tr, p in words]})
for uid, title, vid, vtitle, words, tips in UNITS2:
    used_videos.add(vid)
    units.append({"id": uid, "t": title, "season": 2, "tips": tips,
                  "ic": UNIT_LOOK[uid][0], "hue": UNIT_LOOK[uid][1],
                  "w": [{"sq": sq, "tr": tr, "p": p or EXTRA_PICS.get(sq, ""), "a": audio(uid, sq), "k": tm(sq), "m": MEMO.get(sq)} for sq, tr, p in words]})
for uid, title, vid, vtitle, words, tips in UNITS_F:
    units.append({"id": uid, "t": title, "season": 2, "lv": "A1", "freq": True, "tips": tips,
                  "ic": UNIT_LOOK[uid][0], "hue": UNIT_LOOK[uid][1],
                  "w": [{"sq": sq, "tr": tr, "p": p or EXTRA_PICS.get(sq, ""), "a": audio(uid, sq), "k": tm(sq), "m": MEMO.get(sq)} for sq, tr, p in words]})
for uid, title, vid, vtitle, words, tips in UNITS3:
    units.append({"id": uid, "t": title, "season": 3, "lv": "A2", "tips": tips, "kos": uid == "kosova",
                  "ic": UNIT_LOOK[uid][0], "hue": UNIT_LOOK[uid][1],
                  "w": [{"sq": sq, "tr": tr, "p": p or EXTRA_PICS.get(sq, ""), "a": audio(uid, sq), "k": tm(sq), "m": MEMO.get(sq)} for sq, tr, p in words]})
UNIT_LOOK.update(LOOK_V7)
for uid, title, vid, vtitle, words, tips in UNITS_N + UNITS_V5 + UNITS_V7:
    units.append({"id": uid, "t": title, "season": 2, "tips": tips,
                  "ic": UNIT_LOOK[uid][0], "hue": UNIT_LOOK[uid][1],
                  "w": [{"sq": sq, "tr": tr, "p": p or EXTRA_PICS.get(sq, ""), "a": audio(uid, sq), "k": tm(sq), "m": MEMO.get(sq)} for sq, tr, p in words]})
# Curriculum order: 14 modules (A1 = 9 stops in Albania, A2 = 5 in Kosovo), each with a can-do goal and a mission
ORDER = {uid: (mi, k) for mi, M in enumerate(MODULES) for k, uid in enumerate(M[4])}
units.sort(key=lambda u: ORDER[u["id"]])
_seen = {}
for u in units:                                       # one topic, one place: a word taught earlier is not taught again
    if u["id"] in TITLES: u["t"] = TITLES[u["id"]]
    keep = []
    for w in u["w"]:
        first = _seen.get(w["sq"])
        same = first is not None and first.split(",")[0].split("/")[0].strip().lower() == w["tr"].split(",")[0].split("/")[0].strip().lower()
        if same: continue
        _seen.setdefault(w["sq"], w["tr"]); keep.append(w)
    u["w"] = keep
for u in units:
    mi = ORDER[u["id"]][0]; u["mod"] = mi; u["lv"] = MODULES[mi][2]; u["season"] = 3 if u["lv"] == "A2" else 2
mods = [{"id": mid, "t": mt, "lv": lv, "can": can, "units": us, "roles": rs,
         "wr": {"p": wp, "chk": chk, "sq": wsq, "tr": wtr, "a": audio("gorev", wsq), "k": tm(wsq)}}
        for mid, mt, lv, can, us, rs, (wp, chk, wsq, wtr) in MODULES]
ROLES = ROLES + ROLES2
GRAM = GRAM + GRAM2
STORIES5 = [{"id": tid, "t": tt, "after": aft, "lv": lv, "cover": cov, "kind": "text", "lines": lines, "q": q} for tid, tt, aft, lv, cov, lines, q in TEXTS]
stories = []
for s in STORIES + STORIES2 + STORIES3 + STORIES4 + STORIES5:
    if "src" in s: used_videos.add(s["src"][0])
    stories.append({"id": s["id"], "t": s["t"], "after": STORY_AFTER.get(s["id"], s["after"]), "kind": s.get("kind", "story"), "lv": s.get("lv") or ("A2" if s in STORIES3 else "A1"),
                    "cover": s.get("cover") or STORY_LOOK.get(s["id"], "📖"),
                    "lines": [{"who": who, "av": AVATARS.get(who, ""), "f": who in FEMALE, "sq": sq, "tr": tr, "a": audio("s-" + s["id"], sq), "k": tm(sq)} for who, sq, tr in s["lines"]],
                    "q": [{"q": q, "o": o, "c": c} for q, o, c in s["q"]]})
alpha = [{"l": l, "say": say, "hint": hint, "ex": ex, "tr": tr, "d": bool(d), "a": audio("alfabe", ex)} for l, say, hint, ex, tr, d in ALPHA]
used_videos.add("QxxBvnhw3AA")

# Video library: every video in the playlist, grouped, with whether its notes were transcribed.
rows = [l.rstrip("\n").split("|", 3) for l in open(os.path.join(OUT, "..", "..", "notlar", "playlist.txt"))]
videos = []
for idx, vid, dur, title in rows:
    i = int(idx); g = next(lbl for a, b, lbl in VIDEO_GROUPS if a <= i <= b)
    videos.append({"n": i, "id": vid, "t": title.strip(), "min": round(int(dur) / 60), "g": g,
                   "notes": i <= 31, "inApp": vid in used_videos})

# Tap-to-translate dictionaries
gloss = {}
for u in units:
    for w in u["w"]:
        k = w["sq"].lower().strip("?!.… ")
        if " " not in k or k.startswith(("i ", "e ")):
            gloss.setdefault(k, w["tr"])
            if k.startswith(("i ", "e ")): gloss.setdefault(k[2:], w["tr"])
gloss.update(FUNCTION)
for k_, v_ in STORY_GLOSS.items(): gloss.setdefault(k_, v_)
rev = {}
for u in units:
    for w in u["w"]:
        t = w["tr"].lower().split(" (")[0].split(",")[0].split(" / ")[0].strip("?!. ")
        if " " not in t and " " not in w["sq"].strip("?!. "): rev.setdefault(t, w["sq"].strip("?!. "))

TOKR = re.compile(r"[a-zëç]+")
def look(t):
    if t in STORY_GLOSS: return STORY_GLOSS[t]
    if t in gloss: return gloss[t]
    for suf in ("ave", "ëve", "it", "in", "ës", "ën", "ja", "në", "të", "ve", "a", "i", "u", "t", "n"):
        if t.endswith(suf) and len(t) - len(suf) >= 2:
            b = t[:-len(suf)]
            for c in (b, b + "ë", b + "e"):
                if c in gloss: return gloss[c]
    return None
uidx = {u["id"]: i for i, u in enumerate(units)}
NAMES = {"ana", "artan", "artani", "arben", "arbeni", "dritan", "dritani", "besnik", "besniku", "besnike", "fatmir", "fatmiri", "mimoza", "demir", "talesin", "gjergj", "kastrioti", "mustafa", "qemal", "ataturku", "selanik", "edrene", "krujë", "krujës", "prizren", "prishtinë", "kosova", "kosovës", "turqisë", "anës"}
MISSING = set()
for st in stories:
    known = set(x for u in units[:uidx[st["after"]] + 1] for w in u["w"] for x in TOKR.findall(w["sq"].lower()))
    toks = [x for l in st["lines"] for x in TOKR.findall(l["sq"].lower())]
    unk = [t for t in dict.fromkeys(toks) if t not in known and t not in NAMES and len(t) > 1]
    pre = []
    for t in unk:
        g = look(t)
        if g: pre.append({"sq": t, "tr": g.split(";")[0], "n": toks.count(t), "a": audio("s-" + st["id"], t), "k": tm(t)})
        else: MISSING.add(t)
    st["pre"] = pre
    st["cov"] = round(sum(t in known or t in NAMES for t in toks) / max(1, len(toks)) * 100)
    st["cov2"] = round(sum(bool(t in known or t in NAMES or look(t)) for t in toks) / max(1, len(toks)) * 100)
json.dump(sorted(MISSING), open(os.path.join(HERE, ".missing_gloss.json"), "w"), ensure_ascii=False)
print("story coverage known->with pre-teach:", [(st["id"], st["cov"], st["cov2"]) for st in stories], "missing gloss", len(MISSING))

pairs = [{"id": pid, "t": lbl, "tip": tip, "pairs": [[{"sq": a, "tr": at, "a": audio("ciftler", a)}, {"sq": b, "tr": bt, "a": audio("ciftler", b)}] for (a, at), (b, bt) in prs]}
         for pid, lbl, tip, prs in PAIRS]
# Extra phrases spoken in the grammar "mirror" section
EXTRA = ["Dua të pi ujë", "Jam nga Turqia", "Jam në shkollë", "Do të vij nesër", "Nuk flas shqip", "Unë flas turqisht",
         "shtëpia ime", "vajzë e bukur", "me ty", "A je mirë?"]
extra = [{"sq": x, "a": audio("ayna", x), "k": tm(x)} for x in EXTRA]

# Role-play conversations: NPC lines and every answer option get audio
roles = [{"id": r["id"], "t": r["t"], "cover": r["cover"], "npc": r["npc"], "av": AVATARS.get(r["npc"], "🧑"), "f": r["npc"] in FEMALE, "goal": r["goal"],
          "turns": [{"sq": sq, "tr": tr, "a": audio("roller", sq), "k": tm(sq),
                     "o": [{"sq": osq, "tr": otr, "ok": bool(ok), "fb": fb, "a": audio("roller", osq), "k": tm(osq)} for osq, otr, ok, fb in opts]}
                    for sq, tr, opts in r["turns"]]} for r in ROLES]
# Grammar practice: the full correct sentence gets audio
def filled(x, o): return re.sub(r"\s*\([^)]*\)", "", x.replace("___", o)).replace(" .", ".").strip()
gram = [{"id": gid, "t": gt, "items": [dict(s=x, o=o, c=c, tr=tr, why=why, **{"full": filled(x, o[c])}, a=audio("gramer", filled(x, o[c])), k=tm(filled(x, o[c])))
         for x, o, c, tr, why in items]} for gid, gt, items in GRAM]
# Teach-first pattern lessons (rule + illustrated colour-block examples + targeted gap drills)
def split_blocks(text, target):
    # compact examples: colour the target red (1) and the rest blue (0); trailing punctuation joins the block before it
    i = text.find(target)
    if i < 0: raise SystemExit(f"pattern target {target!r} not in {text!r}")
    pre, post = text[:i].strip(), text[i + len(target):].strip()
    out = [[pre, 0]] if pre else []
    out.append([target, 1])
    if post:
        if re.fullmatch(r"[.!?,…:;]+", post): out[-1][0] += post
        else: out.append([post, 0])
    return out

def expand_ex(e):
    if isinstance(e[3], list): return e
    who, mood, sc, sq, tr, sqt, trt = e
    return (who, mood, sc, split_blocks(tr, trt), split_blocks(sq, sqt), sq, tr)

pats = []
for P_ in PATTERNS + PATTERNS2 + PATTERNS_V7:
    P_["ex"] = [expand_ex(e) for e in P_["ex"] + EXTRA_EX.get(P_["id"], [])]
    exs = [{"who": who, "mood": mood, "scene": sc, "trb": trb, "sqb": sqb, "sq": sq, "tr": tr, "a": audio("kalip", sq), "k": tm(sq)}
           for who, mood, sc, trb, sqb, sq, tr in P_["ex"]]
    drills = [dict(s=x, o=o, c=0, tr=tr, why=why, full=filled(x, o[0]), a=audio("kalip", filled(x, o[0])), k=tm(filled(x, o[0])))
              for x, o, tr, why in P_["drills"]]
    pats.append({"id": P_["id"], "unit": P_["unit"], "t": P_["t"], "rule": P_["rule"], "ex": exs, "drills": drills, "builder": P_.get("builder", False)})
nums = [{"n": n, "sq": t, "a": audio("numra", t), "k": tm(t)} for n, t in NUMBERS]
# Verb conjugator: one clip per tense row (all six persons), word timings let each form light up
conj = {"pron": PRON, "tenses": TENSES, "verbs": []}
by = {}
for v, t, text, full in verb_rows():
    by.setdefault(v, {})[t] = {"f": full, "a": audio("fiiller", text), "k": tm(text)}
for v, tr, _ in VERBS:
    conj["verbs"].append({"v": v, "tr": tr, "t": by[v]})

# Frequency list (OpenSubtitles Albanian, hermitdave/FrequencyWords, CC BY-SA 4.0): top 2000 forms, for the coverage meter
FREQF = os.path.join(HERE, "freq_sq_2000.txt")
FREQ = [l.split()[0] for l in open(FREQF)] if os.path.exists(FREQF) else []

# Minimal pairs in two more voices (Dardan, Sara) so ear training hears four talkers
pair_texts = [x["sq"] for p in pairs for pr in p["pairs"] for x in pr]
json.dump(pair_texts, open(os.path.join(HERE, ".pairs.json"), "w"), ensure_ascii=False)
for v in ("dardan", "if_sara"):
    d_ = os.path.join(HERE, ".clips-kokoro-" + v); out = {}
    for t in pair_texts:
        k = hashlib.md5(t.encode()).hexdigest()[:10]; f = os.path.join(d_, k + ".mp3")
        if os.path.exists(f): out[k] = base64.b64encode(open(f, "rb").read()).decode()
    if out:
        os.makedirs(os.path.join(OUT, "packsv", v), exist_ok=True)
        json.dump(out, open(os.path.join(OUT, "packsv", v, "ciftler.json"), "w"), separators=(",", ":"))

# Sheet for a native speaker to check every sentence in the course
with open(os.path.join(OUT, "..", "..", "notlar", "icerik-kontrol.csv"), "w", newline="") as f:
    wr = csv.writer(f); wr.writerow(["Bölüm", "Arnavutça", "Türkçe", "Doğru mu? (E/H)", "Düzeltme / not"])
    for u in units:
        for w in u["w"]: wr.writerow(["Ünite: " + u["t"], w["sq"], w["tr"], "", ""])
    for s_ in stories:
        for l in s_["lines"]: wr.writerow(["Hikâye: " + s_["t"], l["sq"], l["tr"], "", ""])
    for r in roles:
        for t in r["turns"]:
            wr.writerow(["Konuşma: " + r["t"], t["sq"], t["tr"], "", ""])
            for o in t["o"]: wr.writerow(["Konuşma: " + r["t"] + (" (doğru cevap)" if o["ok"] else " (yanlış seçenek)"), o["sq"], o["tr"], "", ""])
    for g in gram:
        for it in g["items"]: wr.writerow(["Gramer: " + g["t"], it["full"], it["tr"], "", ""])
    for v in conj["verbs"]:
        for t, row in v["t"].items(): wr.writerow(["Fiil: " + v["v"] + " (" + t + ")", ", ".join(row["f"]), v["tr"], "", ""])

# Illustrations: Twemoji SVGs (graphics CC BY 4.0, Twitter, Inc. and contributors) for every emoji the course uses
TWEMOJI = os.environ.get("TWEMOJI_DIR", "/tmp/claude-0/twemoji/package")
def emoji_list(txt):
    out, cur = [], ""
    for ch in txt:
        if cur and (ch in "\u200d\ufe0f\u20e3" or 0x1F3FB <= ord(ch) <= 0x1F3FF or cur.endswith("\u200d") or (0x1F1E6 <= ord(ch) <= 0x1F1FF and len(cur) == 1 and 0x1F1E6 <= ord(cur) <= 0x1F1FF)):
            cur += ch
        else:
            if cur: out.append(cur)
            cur = ch
    if cur: out.append(cur)
    return [e for e in out if not e.isspace()]
def twemoji(e):
    cps = [f"{ord(c):x}" for c in e]
    for name in ("-".join(cps), "-".join(c for c in cps if c != "fe0f")):
        f = os.path.join(TWEMOJI, name + ".svg")
        if os.path.exists(f): return open(f).read()
    return None
icons, missing = {}, []
wanted = set()
for u in units:
    wanted.update(emoji_list(u["ic"]))
    for w in u["w"]:
        if w["p"] and not w["p"].startswith(("#", "n:", "cal:", "sym:")): wanted.update(emoji_list(w["p"]))
for s_ in stories: wanted.update(emoji_list(s_["cover"]))
for r in roles: wanted.update(emoji_list(r["cover"] + r["av"]))
wanted.update(emoji_list("🚶🫴🍽️🥤😴🗣️👀👂✍️📖🏃🏊🎤😂😢🚪🔒🤲🛍️🏷️💼🧠⏳❓💡🤔🤝🏁✅💭⏰🚿👕💇⚽🏆😞✋🪑"))
wanted.update(emoji_list("🔢✏️💡🃏🧩📊📋🪧💬🚌🌦️🧾📰💌🇹🇷🎞️❤️😴🔀✍️🗣️🎯⏱️🧠🔁🎧👉📆👪🔗💪🧩📖😮💭🕌🎤📓🎵🧬🏅⚡🧭🎞️👄🎬📝▶️🎶🧥🎼🪕😄😂🧸📰🚪⛲🌳🪑🏮🌉🗿🌾🏛️🗼🏰🚩⚓🛶⛵🐟🪝🧺🏠🌴⛪🌅🏡🐄🌻🪵🛖🐓🌲🍯🌄🦅🕌🧿🍵🧶⚖️🪔🏺🧵🥁🪞🕰️🗝️👨‍👩‍👧✈️💼✨🌱🌿👂⏱️🎯🎙️🗣️"))
wanted.update(emoji_list("🗺️✏️🧠📈🎧🤸🎯🏛️✍️🔁🕌🌉⛰️⛏️🇽🇰🎙️📒🪞🤝📜💡⚠️🏰🏛️🏟️🧱🪟📚🇦🇱🪨🏖️🔥"))
for e in sorted(wanted):
    svg = twemoji(e)
    if svg: icons[e] = svg
    else: missing.append(e)
json.dump(icons, open(os.path.join(OUT, "icons.json"), "w"), ensure_ascii=False, separators=(",", ":"))
print("icons", len(icons), "missing", missing)

for name, d in packs.items():
    json.dump(d, open(os.path.join(OUT, "packs", name + ".json"), "w"), separators=(",", ":"))
os.makedirs(os.path.join(OUT, "packs2"), exist_ok=True)
for name, d in packs2.items():
    json.dump(d, open(os.path.join(OUT, "packs2", name + ".json"), "w"), separators=(",", ":"))

json.dump({"units": units, "stories": stories, "alpha": alpha, "gloss": gloss, "rev": rev, "pairs": pairs, "extra": extra, "roles": roles, "conj": conj, "gram": gram, "freq": FREQ, "mods": mods, "pats": pats, "nums": nums}, open(os.path.join(OUT, "data.json"), "w"), ensure_ascii=False, separators=(",", ":"))
json.dump(list(dict.fromkeys(SAY)), open(os.path.join(HERE, ".say.json"), "w"), ensure_ascii=False)
print("voice clips", len(os.listdir(VOICE_DIR)) if os.path.isdir(VOICE_DIR) else 0, "units", len(units), "words", sum(len(u["w"]) for u in units), "stories", len(stories), "packs", len(packs),
      "clips", sum(len(p) for p in packs.values()))
