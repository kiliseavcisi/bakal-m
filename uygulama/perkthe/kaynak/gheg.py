# Gheg (Kosovo) -> standard Albanian, before the translation model (which was trained on standard Albanian).
# Same rules are ported to the app (gheg.js). Word lists are small on purpose: the frequent spoken forms.
import re
WORDS = {  # Gheg form -> standard
 "jom": "jam", "jena": "jemi", "jeni": "jeni", "âsht": "është", "asht": "është", "ësht": "është", "o": "është",
 "kom": "kam", "kena": "kemi", "kanë": "kanë", "qysh": "si", "qka": "çfarë", "çka": "çfarë", "qa": "çfarë", "tash": "tani", "tashti": "tani",
 "du": "dua", "don": "do", "dojm": "duam", "nji": "një", "ni": "një", "shpi": "shtëpi", "shpija": "shtëpia", "shpinë": "shtëpinë",
 "nana": "nëna", "nanë": "nënë", "fmi": "fëmijë", "fmija": "fëmija", "fmit": "fëmijët", "vlla": "vëlla", "vllau": "vëllai", "vllaznit": "vëllezërit",
 "kqyr": "shiko", "shif": "shiko", "qat": "atë", "qaj": "ai", "qajo": "ajo", "qata": "ata", "qato": "ato", "qitu": "këtu", "qaty": "aty",
 "krejt": "gjithçka", "shum": "shumë", "mir": "mirë", "zemer": "zemër", "veq": "vetëm", "veç": "vetëm", "hala": "akoma", "kurgjo": "asgjë",
 "kerkush": "askush", "kush": "kush", "najsen": "diçka", "najkush": "dikush", "bre": "", "more": "", "a": "a", "po": "po", "jo": "jo",
 "gjithqka": "gjithçka", "mos": "mos", "s'kom": "nuk kam", "s'jom": "nuk jam", "n'": "në", "t'": "të", "m'": "më", "s'": "nuk",
}
PART = {  # Gheg short participle -> (standard participle, 1st person verb for "me"/"kam me")
 "shku": ("shkuar", "shkoj"), "fol": ("folur", "flas"), "pa": ("parë", "shoh"), "ba": ("bërë", "bëj"), "bo": ("bërë", "bëj"),
 "ardh": ("ardhur", "vij"), "ardhë": ("ardhur", "vij"), "pi": ("pirë", "pi"), "punu": ("punuar", "punoj"), "ngrë": ("ngrënë", "ha"),
 "kanë": ("qenë", "jem"), "ble": ("blerë", "blej"), "thanë": ("thënë", "them"), "dalë": ("dalë", "dal"), "dal": ("dalë", "dal"),
 "hy": ("hyrë", "hyj"), "fjet": ("fjetur", "fle"), "lexu": ("lexuar", "lexoj"), "msu": ("mësuar", "mësoj"), "mësu": ("mësuar", "mësoj"),
 "ndihmu": ("ndihmuar", "ndihmoj"), "telefonu": ("telefonuar", "telefonoj"), "pritë": ("pritur", "pres"), "pri": ("pritur", "pres"),
 "rregullu": ("rregulluar", "rregulloj"), "ndejt": ("ndenjur", "rri"), "lujt": ("luajtur", "luaj"), "luejt": ("luajtur", "luaj"),
 "shkru": ("shkruar", "shkruaj"), "mendu": ("menduar", "mendoj"), "dashtë": ("dashur", "dua"), "dasht": ("dashur", "dua"), "marrë": ("marrë", "marr"),
 "dhanë": ("dhënë", "jap"), "fitu": ("fituar", "fitoj"), "harru": ("harruar", "harroj"), "kthy": ("kthyer", "kthej"), "ecë": ("ecur", "eci"),
}
IRR = {  # subjunctive: unë, ti, ai, ne, ju, ata
 "vij": "vij vish vijë vijmë vini vijnë", "flas": "flas flasësh flasë flasim flisni flasin", "shoh": "shoh shohësh shohë shohim shihni shohin",
 "bëj": "bëj bësh bëjë bëjmë bëni bëjnë", "ha": "ha hash hajë hamë hani hanë", "pi": "pi pish pijë pimë pini pinë", "jem": "jem jesh jetë jemi jeni jenë",
 "blej": "blej blesh blejë blejmë blini blejnë", "pres": "pres presësh presë presim prisni presin", "dal": "dal dalësh dalë dalim dilni dalin",
 "fle": "fle flesh flejë flemë flini flenë", "dua": "dua duash dojë duam doni duan", "marr": "marr marrësh marrë marrim merrni marrin",
 "jap": "jap japësh japë japim jepni japin", "rri": "rri rrish rrijë rrimë rrini rrinë", "luaj": "luaj luash luajë luajmë luani luajnë",
 "shkruaj": "shkruaj shkruash shkruajë shkruajmë shkruani shkruajnë", "kthej": "kthej kthesh kthejë kthejmë ktheni kthejnë",
 "eci": "eci ecësh ecë ecim ecni ecin", "hyj": "hyj hysh hyjë hyjmë hyni hyjnë", "them": "them thuash thotë themi thoni thonë"}
IRR = {k: v.split() for k, v in IRR.items()}
PERSON = {"kam": 0, "kom": 0, "ke": 1, "ka": 2, "kemi": 3, "kena": 3, "keni": 4, "kanë": 5}
def conj(lemma, aux, refl=False):
    """subjunctive form after 'do të' for the person of the Gheg auxiliary (kam/ke/ka me ...); -oj verbs fully, others 1st person"""
    p = PERSON.get(aux, 0)
    if lemma in IRR and not refl: return IRR[lemma][p]
    if lemma.endswith("oj"):
        st = lemma[:-2]
        if refl: return st + ["ohem", "ohesh", "ohet", "ohemi", "oheni", "ohen"][p]
        return st + ["oj", "osh", "ojë", "ojmë", "oni", "ojnë"][p]
    return lemma
FEM_END = ("a", "ja")
MASC_A = {"fëmija", "fmija", "baba", "xhaxha", "daja", "kolega"}
def gheg_to_standard(text):
    t = re.sub(r"\b([nNtTmMsS])['’]\s*", lambda m: (lambda r: r.capitalize() if m.group(1).isupper() else r)({"n": "në ", "t": "të ", "m": "më ", "s": "nuk "}[m.group(1).lower()]), text)
    toks = re.findall(r"\w+|[^\w\s]+|\s+", t)
    words = [w for w in toks]
    out = []
    i = 0
    def nxt(k):  # next non-space token index
        while k < len(words) and words[k].isspace(): k += 1
        return k
    while i < len(words):
        w = words[i]; lw = w.lower()
        # "kam/ke/ka me + participle" -> "do të + verb";  "me + participle" (infinitive) -> "të + verb"
        if lw in ("kam", "kom", "ke", "ka", "kemi", "kena", "keni", "kanë") and (j := nxt(i + 1)) < len(words) and words[j].lower() == "me":
            k = nxt(j + 1); u = ""
            if k < len(words) and words[k].lower() == "u": u = "u "; k = nxt(k + 1)
            if k < len(words) and words[k].lower() in PART:
                v = conj(PART[words[k].lower()][1], lw, bool(u))
                out.append(("Do" if w[0].isupper() else "do") + " të " + ("" if u and v.endswith(("ohet", "ohen", "ohem", "ohesh")) else u) + v); i = k + 1; continue
        if lw == "me" and (k := nxt(i + 1)) < len(words):
            u = ""; kk = k
            if words[kk].lower() == "të": u = "të "; kk = nxt(kk + 1)
            if kk < len(words) and words[kk].lower() == "u": u += "u "; kk = nxt(kk + 1)
            if kk < len(words) and words[kk].lower() in PART:
                out.append("të " + u + PART[words[kk].lower()][1]); i = kk + 1; continue
        # perfect "kam pa" -> "kam parë"
        if lw in PART and out and re.sub(r"\s", "", "".join(out[-2:])).lower().endswith(("kam", "ke", "ka", "kemi", "keni", "kanë", "kisha", "kishte", "e", "i")):
            prev = [x for x in out if not x.isspace()]
            if prev and prev[-1].lower() in ("kam", "ke", "ka", "kemi", "keni", "kanë", "kisha", "kishte", "kom"):
                out.append(PART[lw][0]); i += 1; continue
        if lw == "jem" or lw == "jeme":   # possessive: nana jem -> nëna ime, djali jem -> djali im
            prev = [x for x in out if not x.isspace()]
            fem = prev and prev[-1].lower().endswith(FEM_END) and prev[-1].lower() not in MASC_A
            out.append("ime" if fem else "im"); i += 1; continue
        if lw in WORDS:
            r = WORDS[lw]
            out.append((r[:1].upper() + r[1:]) if w[0].isupper() and r else r); i += 1; continue
        out.append(w); i += 1
    return re.sub(r"\s+", " ", "".join(out)).replace(" ,", ",").replace(" .", ".").replace(" ?", "?").replace(" !", "!").strip()

if __name__ == "__main__":
    for g in ["Qysh je, a je mirë?", "Çka po bën tash?", "Kam me shku n'shpi.", "Du me t'pa nesër.", "S'po du me fol.", "Nana jem âsht n'Prishtinë.",
              "Ku ke kanë dje?", "Hajde me pi nji kafe.", "A po vjen me ne?", "Mos u mërzit, krejt kanë me u rregullu.", "Qa po don?", "Fmija jem po fle.",
              "Kqyr qat vajzë!", "E kam pa n'treg.", "Sot s'kom kohë, nesër po."]:
        print(g, "->", gheg_to_standard(g))
