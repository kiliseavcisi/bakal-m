# Verb conjugator: present, simple past (aorist), imperfect, future (do të + subjunctive).
# Persons: unë, ti, ai/ajo, ne, ju, ata
PRON = ["unë", "ti", "ai", "ne", "ju", "ata"]
TENSES = [("pr", "Şimdiki / geniş zaman"), ("ao", "Geçmiş (-dı)"), ("im", "Geçmiş süreklilik (-yordu)"), ("fu", "Gelecek (-ecek)")]

def oj(stem):  # regular -oj verbs: punoj, mësoj …
    return {"pr": [stem + "oj", stem + "on", stem + "on", stem + "ojmë", stem + "oni", stem + "ojnë"],
            "ao": [stem + "ova", stem + "ove", stem + "oi", stem + "uam", stem + "uat", stem + "uan"],
            "im": [stem + "oja", stem + "oje", stem + "onte", stem + "onim", stem + "onit", stem + "onin"],
            "fu": [stem + "oj", stem + "osh", stem + "ojë", stem + "ojmë", stem + "oni", stem + "ojnë"]}

def sp(s):
    return s.split()

VERBS = [  # (infinitive-ish headword, Turkish, forms)
 ("jam", "olmak", {"pr": sp("jam je është jemi jeni janë"), "ao": sp("qeshë qe qe qemë qetë qenë"),
                   "im": sp("isha ishe ishte ishim ishit ishin"), "fu": sp("jem jesh jetë jemi jeni jenë")}),
 ("kam", "sahip olmak", {"pr": sp("kam ke ka kemi keni kanë"), "ao": sp("pata pate pati patëm patët patën"),
                         "im": sp("kisha kishe kishte kishim kishit kishin"), "fu": sp("kem kesh ketë kemi keni kenë")}),
 ("bëj", "yapmak", {"pr": sp("bëj bën bën bëjmë bëni bëjnë"), "ao": sp("bëra bëre bëri bëmë bëtë bënë"),
                    "im": sp("bëja bëje bënte bënim bënit bënin"), "fu": sp("bëj bësh bëjë bëjmë bëni bëjnë")}),
 ("dua", "istemek, sevmek", {"pr": sp("dua do do duam doni duan"), "ao": sp("desha deshe deshi deshëm deshët deshën"),
                             "im": sp("doja doje donte donim donit donin"), "fu": sp("dua duash dojë duam doni duan")}),
 ("shkoj", "gitmek", oj("shk")),
 ("vij", "gelmek", {"pr": sp("vij vjen vjen vijmë vini vijnë"), "ao": sp("erdha erdhe erdhi erdhëm erdhët erdhën"),
                    "im": sp("vija vije vinte vinim vinit vinin"), "fu": sp("vij vish vijë vijmë vini vijnë")}),
 ("flas", "konuşmak", {"pr": sp("flas flet flet flasim flisni flasin"), "ao": sp("fola fole foli folëm folët folën"),
                       "im": sp("flisja flisje fliste flisnim flisnit flisnin"), "fu": sp("flas flasësh flasë flasim flisni flasin")}),
 ("ha", "yemek", {"pr": sp("ha ha ha hamë hani hanë"), "ao": sp("hëngra hëngre hëngri hëngrëm hëngrët hëngrën"),
                  "im": sp("haja haje hante hanim hanit hanin"), "fu": sp("ha hash hajë hamë hani hanë")}),
 ("pi", "içmek", {"pr": sp("pi pi pi pimë pini pinë"), "ao": sp("piva pive piu pimë pitë pinë"),
                  "im": sp("pija pije pinte pinim pinit pinin"), "fu": sp("pi pish pijë pimë pini pinë")}),
 ("shoh", "görmek", {"pr": sp("shoh sheh sheh shohim shihni shohin"), "ao": sp("pashë pe pa pamë patë panë"),
                     "im": sp("shihja shihje shihte shihnim shihnit shihnin"), "fu": sp("shoh shohësh shohë shohim shihni shohin")}),
 ("them", "söylemek", {"pr": sp("them thua thotë themi thoni thonë"), "ao": sp("thashë the tha thamë thatë thanë"),
                       "im": sp("thosha thoshe thoshte thoshim thoshit thoshin"), "fu": sp("them thuash thotë themi thoni thonë")}),
 ("jap", "vermek", {"pr": sp("jap jep jep japim jepni japin"), "ao": sp("dhashë dhe dha dhamë dhatë dhanë"),
                    "im": sp("jepja jepje jepte jepnim jepnit jepnin"), "fu": sp("jap japësh japë japim jepni japin")}),
 ("marr", "almak", {"pr": sp("marr merr merr marrim merrni marrin"), "ao": sp("mora more mori morëm morët morën"),
                    "im": sp("merrja merrje merrte merrnim merrnit merrnin"), "fu": sp("marr marrësh marrë marrim merrni marrin")}),
 ("di", "bilmek", {"pr": sp("di di di dimë dini dinë"), "ao": sp("dita dite diti ditëm ditët ditën"),
                   "im": sp("dija dije dinte dinim dinit dinin"), "fu": sp("di dish dijë dimë dini dinë")}),
 ("dal", "çıkmak", {"pr": sp("dal del del dalim dilni dalin"), "ao": sp("dola dole doli dolëm dolët dolën"),
                    "im": sp("dilja dilje dilte dilnim dilnit dilnin"), "fu": sp("dal dalësh dalë dalim dilni dalin")}),
 ("fle", "uyumak", {"pr": sp("fle fle fle flemë flini flenë"), "ao": sp("fjeta fjete fjeti fjetëm fjetët fjetën"),
                    "im": sp("flija flije flinte flinim flinit flinin"), "fu": sp("fle flesh flejë flemë flini flenë")}),
 ("blej", "satın almak", {"pr": sp("blej blen blen blejmë blini blejnë"), "ao": sp("bleva bleve bleu blemë bletë blenë"),
                          "im": sp("blija blije blinte blinim blinit blinin"), "fu": sp("blej blesh blejë blejmë blini blejnë")}),
 ("shes", "satmak", {"pr": sp("shes shet shet shesim shitni shesin"), "ao": sp("shita shite shiti shitëm shitët shitën"),
                     "im": sp("shisja shisje shiste shisnim shisnit shisnin"), "fu": sp("shes shesësh shesë shesim shitni shesin")}),
 ("pres", "beklemek", {"pr": sp("pres pret pret presim prisni presin"), "ao": sp("prita prite priti pritëm pritët pritën"),
                       "im": sp("prisja prisje priste prisnim prisnit prisnin"), "fu": sp("pres presësh presë presim prisni presin")}),
 ("pyes", "sormak", {"pr": sp("pyes pyet pyet pyesim pyesni pyesin"), "ao": sp("pyeta pyete pyeti pyetëm pyetët pyetën"),
                     "im": sp("pyesja pyesje pyeste pyesnim pyesnit pyesnin"), "fu": sp("pyes pyesësh pyesë pyesim pyesni pyesin")}),
 ("hap", "açmak", {"pr": sp("hap hap hap hapim hapni hapin"), "ao": sp("hapa hape hapi hapëm hapët hapën"),
                   "im": sp("hapja hapje hapte hapnim hapnit hapnin"), "fu": sp("hap hapësh hapë hapim hapni hapin")}),
 ("eci", "yürümek", {"pr": sp("eci ecën ecën ecim ecni ecin"), "ao": sp("eca ece eci ecëm ecët ecën"),
                     "im": sp("ecja ecje ecte ecnim ecnit ecnin"), "fu": sp("eci ecësh ecë ecim ecni ecin")}),
 ("luaj", "oynamak", {"pr": sp("luaj luan luan luajmë luani luajnë"), "ao": sp("luajta luajte luajti luajtëm luajtët luajtën"),
                      "im": sp("luaja luaje luante luanim luanit luanin"), "fu": sp("luaj luash luajë luajmë luani luajnë")}),
 ("shkruaj", "yazmak", {"pr": sp("shkruaj shkruan shkruan shkruajmë shkruani shkruajnë"), "ao": sp("shkrova shkrove shkroi shkruam shkruat shkruan"),
                        "im": sp("shkruaja shkruaje shkruante shkruanim shkruanit shkruanin"), "fu": sp("shkruaj shkruash shkruajë shkruajmë shkruani shkruajnë")}),
 ("rri", "durmak, oturmak", {"pr": sp("rri rri rri rrimë rrini rrinë"), "ao": sp("ndenja ndenje ndenji ndenjëm ndenjët ndenjën"),
                             "im": sp("rrija rrije rrinte rrinim rrinit rrinin"), "fu": sp("rri rrish rrijë rrimë rrini rrinë")}),
 ("hyj", "girmek", {"pr": sp("hyj hyn hyn hyjmë hyni hyjnë"), "ao": sp("hyra hyre hyri hymë hytë hynë"),
                    "im": sp("hyja hyje hynte hynim hynit hynin"), "fu": sp("hyj hysh hyjë hyjmë hyni hyjnë")}),
 ("punoj", "çalışmak", oj("pun")),
 ("mësoj", "öğrenmek", oj("mës")),
 ("lexoj", "okumak", oj("lex")),
 ("kuptoj", "anlamak", oj("kupt")),
 ("dëgjoj", "dinlemek, duymak", oj("dëgj")),
 ("jetoj", "yaşamak", oj("jet")),
]

def rows():
    """[(verb, tense, spoken text, forms with pronouns)]"""
    out = []
    for v, tr, f in VERBS:
        for t, _ in TENSES:
            forms = [("do të " if t == "fu" else "") + x for x in f[t]]
            full = [p + " " + x for p, x in zip(PRON, forms)]
            out.append((v, t, ", ".join(full), full))
    return out
