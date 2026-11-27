# Curriculum v7: one spine, ordered by what the learner needs to SAY first and by how grammar is acquired.
#  - Communicative needs first (CEFR can-do): greet, talk about family, say what you do, order, tell the time.
#  - Verbs early (module 3): without a present tense there is no sentence to speak.
#  - Morphology from simple to complex (processability): jam/kam -> present -> plural/agreement -> past -> future
#    -> imperfect -> perfect -> conditional -> B1 moods. One new tense per module, never two at once.
#  - Same topic in one place (no "body" in three modules); frequent function words spread across the themes.
#  - Each module: a situation, 3-5 units, a role-play and a writing mission. Spaced recycling comes from SRS.
# (id, title, level, can-do, units, role-plays, (mission prompt, checks, model answer, Turkish))
MODULES_V7 = [
 ("m1", "Merhaba!", "A1", "Selamlaşır, kendini tanıtır, nereli olduğunu ve sayıları söylersin.",
  ["selam", "hal", "zamir", "sayi", "ulke"], ["rp-njohje"],
  ("Kendini tanıt: adın, nerelisin, kaç yaşındasın.", [["quhem|jam", "adını söyle"], ["nga", "nereli olduğunu söyle (nga)"], ["vjeç", "yaşını söyle (… vjeç)"]],
   "Përshëndetje! Unë quhem Ana. Jam nga Turqia. Jam njëzet e pesë vjeç.", "Merhaba! Benim adım Ana. Türkiye'denim. Yirmi beş yaşındayım.")),
 ("m2", "Ailem ve evim", "A1", "Aileni ve evini anlatır, sahip olduklarını söylersin.",
  ["aile", "te-afermit", "shquar", "tregues", "ev"], ["rp-mysafir"],
  ("Aileni anlat: kaç kardeşin var, annen ve baban ne iş yapıyor?", [["kam", "sahip olduklarını söyle (kam)"], ["motër|vëlla|motra|vëllezër", "kardeşlerinden bahset"], ["nëna|babai|nënë|baba", "annenden ya da babandan bahset"]],
   "Kam një vëlla dhe një motër. Nëna ime është mësuese. Babai im punon në një bankë.", "Bir erkek, bir kız kardeşim var. Annem öğretmen. Babam bir bankada çalışıyor.")),
 ("m3", "Ne yapıyorsun?", "A1", "Ne yaptığını söyler, olumsuz cümle kurar, soru sorarsın. Şimdiki zaman burada başlar.",
  ["fiil", "cumle", "pyetje", "sik3", "okul"], ["rp-klasa"],
  ("Bugün neler yapıyorsun? Üç eylem yaz, birini olumsuz yap.", [["punoj|lexoj|shkoj|ha|pi|flas|mësoj|shkruaj", "en az bir fiil kullan"], ["nuk", "bir olumsuz cümle kur (nuk)"], ["dhe|pastaj", "eylemleri bağla (dhe / pastaj)"]],
   "Sot punoj në shtëpi. Pastaj lexoj një libër. Nuk shkoj në punë.", "Bugün evde çalışıyorum. Sonra bir kitap okuyorum. İşe gitmiyorum.")),
 ("m4", "Kafede ve sofrada", "A1", "Kafede sipariş verir, ne istediğini söyler, çoğul kullanır, fiyat sorarsın.",
  ["icecek", "meyve", "faleminderit", "shumes", "sik1"], ["rp-kafe"],
  ("Garsona yaz: bir içecek ve iki yiyecek iste, fiyatını sor.", [["dua|do të doja", "ne istediğini söyle"], ["ju lutem", "lütfen de"], ["sa kushton|sa kushtojnë", "fiyat sor"]],
   "Mirëdita! Dua një kafe dhe dy byrekë, ju lutem. Sa kushtojnë?", "İyi günler! Bir kahve ve iki börek istiyorum lütfen. Ne kadar?")),
 ("m5", "Zaman ve hava", "A1", "Günü, saati, tarihi ve havayı söyler, randevu ayarlarsın.",
  ["gun", "zaman", "sira", "numrat2", "mevsim"], ["rp-randevu"],
  ("Bugünü anlat: hangi gün, saat kaç, hava nasıl?", [["e hënë|e martë|e mërkurë|e enjte|e premte|e shtunë|e diel", "günü söyle"], ["ora", "saati söyle (ora)"], ["diell|shi|ftohtë|nxehtë|borë|re", "havayı söyle"]],
   "Sot është e shtunë. Ora është dhjetë. Bën ftohtë, por ka diell.", "Bugün cumartesi. Saat on. Hava soğuk ama güneşli.")),
 ("m6", "Nasıl biri?", "A1", "İnsanları ve eşyaları sıfatlarla anlatır, karşılaştırırsın.",
  ["renk", "mbiemra", "sifat", "karakteri", "krahasim"], ["rp-shoku"],
  ("En iyi arkadaşını anlat: nasıl biri, senden farkı ne?", [["është", "olmak fiilini kullan (është)"], ["\\b(i|e) [a-zëç]+", "sıfatı i/e ile kullan"], ["më ", "karşılaştır (më … se)"]],
   "Shoqja ime quhet Ana. Ajo është e gjatë dhe shumë e sjellshme. Është më e qetë se unë.", "Arkadaşımın adı Ana. Uzun boylu ve çok kibar. Benden daha sakin.")),
 ("m7", "Dün neler oldu?", "A1", "Geçmişte olanları sırayla anlatırsın. Geçmiş zaman burada başlar.",
  ["koha-shkuar", "lidhezat", "festa", "sik4"], [],
  ("Dün ne yaptın? Üç cümle yaz ve bağla.", [["dje", "dünü söyle (dje)"], ["shkova|bëra|hëngra|piva|fola|punova|pashë|lexova|erdha|isha", "geçmiş zaman kullan"], ["kur|pasi|pastaj", "olayları bağla"]],
   "Dje shkova në punë. Pasi mbarova, hëngra me familjen. Pastaj pashë një film.", "Dün işe gittim. Bitirdikten sonra ailemle yemek yedim. Sonra bir film izledim.")),
 ("m8", "Vücut ve duygular", "A1", "Neren ağrıdığını, nasıl hissettiğini ve tepkilerini söylersin.",
  ["trupi", "doktor", "ndjenja", "sik5"], ["rp-mjek"],
  ("Doktora yaz: neren ağrıyor, nasıl hissediyorsun?", [["më dhemb|më dhembin", "ağrıyı söyle (më dhemb)"], ["kam|jam", "durumunu söyle (kam temperaturë / jam i lodhur)"], ["ndihem|frikë|mërzitur|lodhur", "nasıl hissettiğini söyle"]],
   "Mirëdita, doktor. Më dhemb koka dhe kam temperaturë. Jam shumë e lodhur.", "İyi günler doktor. Başım ağrıyor ve ateşim var. Çok yorgunum.")),
 ("m9", "Alışveriş ve tatil", "A1", "Alışveriş yapar, telefonda konuşur, tatilini anlatırsın.",
  ["pazar", "plazh", "telefoni", "sik2", "hayvan"], ["rp-pazar", "rp-telefon"],
  ("Tatilden bir kartpostal yaz: nerede, nasıl, en güzel şey ne?", [["jam në|jemi në", "nerede olduğunu söyle"], ["më ", "karşılaştırma kullan (më …)"], ["\\b(dy|tre|tri|katër|pesë) [a-zëç]+", "sayıyla çoğul kullan"]],
   "Jemi në Sarandë. Deti është më i bukur se në Durrës. Kemi dy dhoma të vogla, por plazhi është shumë afër.", "Saranda'dayız. Deniz Draç'takinden daha güzel. İki küçük odamız var ama plaj çok yakın.")),
 ("m10", "Günlük hayat", "A2", "Günlük rutinini anlatır, giyim ve yemek hakkında konuşur, kibarca hitap edersin.",
  ["rutina", "pesore", "veshje", "ushqim", "kibarlik"], ["rp-restorant"],
  ("Bir gününü anlat: ne zaman kalkıyorsun, ne yiyorsun, ne giyiyorsun?", [["zgjohem|çohem", "kalkışını söyle"], ["në orën", "saat ver (në orën …)"], ["ha|pi|vishem", "yemek ya da giyinmeden bahset"]],
   "Zgjohem në orën shtatë. Ha mëngjes me bukë dhe djathë. Pastaj vishem dhe dal nga shtëpia.", "Saat yedide uyanırım. Ekmek ve peynirle kahvaltı ederim. Sonra giyinip evden çıkarım.")),
 ("m11", "Yarın ve yolculuk", "A2", "Planlarını anlatır, yol sorar, ulaşım ve otelde idare edersin. Gelecek zaman burada başlar.",
  ["ardhme", "modale", "qyteti", "transport", "udhetim"], ["rp-taksi", "rp-hotel"],
  ("Bir tatil planı yaz: nereye, nasıl ve ne zaman gideceksin?", [["do të", "gelecek zaman kullan (do të)"], ["me autobus|me tren|me avion|me makinë|me taksi", "ulaşımı söyle (me …)"], ["duhet të|mund të", "gereklilik ya da olasılık ekle"]],
   "Verën që vjen do të shkoj në Prizren me autobus. Duhet të rezervoj një hotel të vogël.", "Gelecek yaz otobüsle Prizren'e gideceğim. Küçük bir otel ayırtmam gerekiyor.")),
 ("m12", "Eskiden", "A2", "Çocukluğunu ve eski alışkanlıklarını anlatır, o sırada olanları söylersin. Geçmiş süreklilik burada başlar.",
  ["pakryer", "koha2", "fiilet2", "shumes2", "eshdizime"], ["rp-gjyshja"],
  ("Çocukluğunu anlat: nerede yaşardın, ne yapardın?", [["isha|ishim|jetoja|jetonim", "nerede olduğunu söyle (isha / jetoja)"], ["ja\\b|je\\b|nte\\b|nim\\b", "geçmiş süreklilik kullan (-ja / -nte)"], ["çdo|gjithmonë|shpesh|dikur", "alışkanlığı belirt (çdo / dikur)"]],
   "Kur isha e vogël, jetonim në një fshat. Çdo ditë luaja me shokët dhe gjyshja tregonte përralla.", "Küçükken bir köyde yaşardık. Her gün arkadaşlarımla oynardım, büyükannem masal anlatırdı.")),
 ("m13", "İş, sağlık, boş zaman", "A2", "İşini, sağlığını ve hobilerini anlatır, alışverişte pazarlık edersin.",
  ["puna", "shendeti", "hobi", "blerje", "kundersi"], ["rp-farmaci"],
  ("Kendini bir işe tanıt: işin, deneyimin, boş zamanların.", [["punoj|jam", "işini söyle"], ["vjet|vite", "süre söyle (… vjet)"], ["më pëlqen", "hobini söyle (më pëlqen)"]],
   "Jam inxhiniere dhe punoj prej pesë vjetësh. Në kohën e lirë më pëlqen të lexoj dhe të notoj.", "Mühendisim ve beş yıldır çalışıyorum. Boş zamanımda okumayı ve yüzmeyi severim.")),
 ("m14", "Deneyim ve hayal", "A2", "Deneyimlerini ve hayallerini anlatır, kişileri ve şeyleri tarif edersin. Yakın geçmiş ve şart burada.",
  ["kryer", "kushti", "lidhore", "teknologji", "natyra"], ["rp-pushime"],
  ("Param olsaydı ne yapardım? Bir de hiç gitmediğin bir yeri yaz.", [["po të", "hayalî şart kullan (po të …)"], ["do të", "sonucu söyle (do të …)"], ["kam qenë|nuk kam", "yakın geçmiş kullan (kam …)"]],
   "Po të kisha shumë para, do të udhëtoja nëpër botë. Nuk kam qenë kurrë në Kosovë, por do të doja të shkoja.", "Çok param olsaydı dünyayı gezerdim. Hiç Kosova'da bulunmadım ama gitmek isterdim.")),
 ("m15", "Kültür ve Kosova", "A2", "Bayramları, atasözlerini ve Kosova Arnavutçasını tanırsın.",
  ["festat", "proverba", "kosova"], [],
  ("Bir bayramı anlat: ne zaman, ne yapılır, ne söylenir?", [["gëzuar|urime", "kutlama sözü kullan"], ["në|më", "zamanı söyle"], ["hamë|këndojmë|vallëzojmë|takohemi", "ne yaptığınızı söyle"]],
   "Në Bajram takohemi me familjen. Hamë baklava dhe themi: Gëzuar Bajramin!", "Bayramda ailemizle buluşuruz. Baklava yeriz ve “Bayramın kutlu olsun!” deriz.")),
 ("m16", "Anlatmak, aktarmak, tartışmak", "B1", "Geçmişi sırayla anlatır, duyduğunu aktarır, şaşkınlığını ve fikrini kibarca söylersin.",
  ["tregim", "habitore", "mendim"], ["rp-debat"],
  ("Başına gelen ilginç bir olayı anlat: önce, sonra, birden, sonunda.", [["fillimisht|më pas|pastaj", "sıralama kullan (fillimisht / më pas)"], ["papritur", "beklenmedik anı söyle (papritur)"], ["në fund|si përfundim", "sonucu söyle (në fund)"]],
   "Fillimisht shkova në stacion, por treni ishte nisur. Më pas mora një taksi. Papritur pashë një shok të vjetër. Në fund udhëtuam bashkë!", "Önce istasyona gittim ama tren kalkmıştı. Sonra bir taksiye bindim. Birden eski bir arkadaşımı gördüm. Sonunda birlikte yolculuk ettik!")),
]

# Clearer titles where the old ones were numbered or repeated
TITLES = {
 "sik1": "Küçük ama sık: sadece, belki, hâlâ", "sik2": "İnsanlar ve şeyler: biri, kimse, her şey", "sik3": "Emirler ve günlük fiiller",
 "sik4": "Emin olmak ve bağlamak", "sik5": "Duygular ve tepkiler", "te-afermit": "Akrabalar: benim, senin",
 "sira": "Sıra sayıları: birinci, ikinci", "numrat2": "Büyük sayılar ve tarih", "natyra": "Doğa", "fiilet2": "Sık fiiller: vermek, almak, bilmek",
 "pazar": "Pazarda: ne kadar?", "blerje": "Para, kart, fatura", "shendeti": "Sağlık: nasıl hissediyorsun?", "trupi": "Vücudumuz",
 "tregim": "Miş'li geçmiş ve hikâye anlatmak", "habitore": "Hayret kipi: -mış!", "mendim": "Fikir bildirmek ve tartışmak",
 "cumle": "Olumsuz cümle: nuk, mos", "sifat": "Sıfatlar: iyi, kötü, büyük, küçük", "ardhme": "Gelecek zaman: do të",
}

# New unit: the imperfect (punoja), the tense the course never taught
UNITS_V7 = [
 ("pakryer", "Eskiden ve o sırada: punoja", "", "", [
  ["Dikur", "eskiden, bir zamanlar", "⏳"], ["punoja", "çalışıyordum / çalışırdım", "💼"], ["luaja", "oynardım / oynuyordum", "⚽"],
  ["shkoja", "giderdim / gidiyordum", "🚶"], ["isha", "idim (olmak, geçmiş)", "🧍"], ["kishte", "vardı / onun vardı", "📦"],
  ["Kur isha i vogël, luaja shumë.", "Küçükken çok oynardım.", "🧒"], ["Çdo verë shkonim në det.", "Her yaz denize giderdik.", "🏖️"],
  ["Kur erdhe, unë po haja.", "Sen geldiğinde ben yemek yiyordum.", "🍽️"], ["Ku ishe dje?", "Dün neredeydin?", "❓"],
  ["Gjyshja tregonte përralla.", "Büyükannem masallar anlatırdı.", "👵"], ["Binte shi.", "Yağmur yağıyordu.", "🌧️"],
  ["Ai fliste shumë shpejt.", "O çok hızlı konuşuyordu.", "🗣️"], ["Ishte vonë.", "Vakit geçti. / Geç olmuştu.", "🌙"]],
  ["Geçmişte <b>süren</b> ya da <b>alışkanlık</b> olan işler: punoj → puno<b>ja</b> (çalışıyordum / çalışırdım). Tek seferlik, biten iş için <b>punova</b> (çalıştım).",
   "Çekim: <b>-ja, -je, -nte, -nim, -nit, -nin</b> (punoja, punoje, punonte, punonim, punonit, punonin). Olmak: <b>isha, ishe, ishte</b>; sahip olmak: <b>kisha, kishe, kishte</b>.",
   "“O sırada …-yordum” için önüne <b>po</b>: <i>po haja</i> = yemek yiyordum (tam o anda)."]),
]
LOOK_V7 = {"pakryer": ("⏳", 28)}

PATTERNS_V7 = [
 {"id": "p-pakryer", "unit": "pakryer", "t": "-ıyordum / -ırdım → -ja (punoja)",
  "rule": "Türkçede geçmişte süren işi <b>-ıyordum</b>, alışkanlığı <b>-ırdım</b> ile söyleriz. Arnavutçada ikisi de tek biçim: puno<b>ja</b>. Tek seferlik ve biten iş ise <b>punova</b> (çalıştım). Kendine sor: bir kere mi oldu, yoksa sürüyor ya da tekrarlanıyor muydu?",
  "ex": [("Talesi", "happy", "fshat", "Kur isha i vogël, luaja çdo ditë.", "Küçükken her gün oynardım.", "luaja", "oynardım"),
         ("Nëna", "neutral", "familja", "Çdo verë shkonim në det.", "Her yaz denize giderdik.", "shkonim", "giderdik"),
         ("Ana", "surprised", "familja", "Kur erdhe, unë po haja.", "Sen geldiğinde ben yemek yiyordum.", "po haja", "yiyordum"),
         ("Artani", "neutral", "rruga", "Binte shi dhe ishte ftohtë.", "Yağmur yağıyordu ve soğuktu.", "Binte", "yağıyordu"),
         ("Arbeni", "happy", "familja", "Gjyshja tregonte përralla.", "Büyükannem masallar anlatırdı.", "tregonte", "anlatırdı")],
  "drills": [("Kur isha fëmijë, ___ futboll çdo ditë. (oynardım)", ["luaja", "luajta", "luaj"], "Çocukken her gün futbol oynardım.", "alışkanlık → <b>-ja</b>"),
             ("Dje ___ në Tiranë. (bir kere gittim)", ["shkova", "shkoja", "shkoj"], "Dün Tiran'a gittim.", "tek seferlik → <b>shkova</b>"),
             ("Kur ti erdhe, unë ___ një libër. (okuyordum)", ["po lexoja", "lexova", "lexoj"], "Sen geldiğinde bir kitap okuyordum.", "o sırada süren → <b>po lexoja</b>"),
             ("Ku ___ dje? (sen)", ["ishe", "isha", "ishte"], "Dün neredeydin?", "sen → <b>ishe</b>"),
             ("Gjyshi ___ shumë histori. (anlatırdı)", ["tregonte", "tregoi", "tregon"], "Dedem çok hikâye anlatırdı.", "o + alışkanlık → <b>-nte</b>")]},
]

# Stories whose text needs a tense taught later move behind that tense
STORY_AFTER = {"qindarka": "koha-shkuar", "talesi": "sik4", "t-dyqanet": "festa"}
