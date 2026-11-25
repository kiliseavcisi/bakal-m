# Grammar practice with an explanation after every answer (metalinguistic feedback).
# Each item: (sentence with ___, options, index of correct option, Turkish meaning, why)
GRAM = [
 ("cins", "Belirli isim: -i / -u / -a", [
  ("___ është i madh. (libër)", ["Libri", "Libra", "Librat"], 0, "Kitap büyük.", "<b>libër</b> eril; belirli hâli <b>-i</b> alır: libr<b>i</b>."),
  ("___ është e bukur. (vajzë)", ["Vajza", "Vajzi", "Vajzu"], 0, "Kız güzel.", "<b>vajzë</b> dişil (-ë ile biter); belirli hâli <b>-a</b>: vajz<b>a</b>."),
  ("___ është këtu. (mik)", ["Miku", "Mika", "Miki"], 0, "Arkadaş burada.", "<b>-k, -g, -h</b> ile biten eril isimler <b>-u</b> alır: mik<b>u</b>, zog<b>u</b>."),
  ("___ ka lule. (shtëpi)", ["Shtëpia", "Shtëpiu", "Shtëpii"], 0, "Evde çiçek var.", "<b>shtëpi</b> dişil; <b>-i</b> ile biten dişiller <b>-a</b> alır: shtëpi<b>a</b>."),
  ("___ është i ri. (djalë)", ["Djali", "Djala", "Djalu"], 0, "Oğlan genç.", "<b>djalë</b> eril; sondaki ë düşer, <b>-i</b> gelir: djal<b>i</b>."),
  ("___ është e kuqe. (lule)", ["Lulja", "Lulei", "Lulu"], 0, "Çiçek kırmızı.", "<b>-e</b> ile biten dişiller <b>-ja</b> alır: lul<b>ja</b>.")]),
 ("sifat", "Sıfat uyumu: i / e / të", [
  ("një djalë ___ mirë", ["i", "e", "të"], 0, "iyi bir oğlan", "Eril tekil isimden sonra sıfat <b>i</b> alır."),
  ("një vajzë ___ mirë", ["e", "i", "të"], 0, "iyi bir kız", "Dişil tekil isimden sonra sıfat <b>e</b> alır."),
  ("djem ___ mirë", ["të", "i", "e"], 0, "iyi oğlanlar", "Çoğul isimden sonra sıfat <b>të</b> alır."),
  ("Shtëpia është e ___ .", ["madhe", "madh", "mëdhenj"], 0, "Ev büyük.", "Dişil isimle sıfatın kendisi de değişebilir: i madh → e <b>madhe</b>."),
  ("Libri është ___ vjetër.", ["i", "e", "të"], 0, "Kitap eski.", "<b>libri</b> eril, “olmak”tan sonra da uyum sürer: <b>i</b> vjetër."),
  ("Kafja është ___ nxehtë.", ["e", "i", "të"], 0, "Kahve sıcak.", "<b>kafe</b> dişil: <b>e</b> nxehtë.")]),
 ("iyelik", "İyelik: im / ime, yt / jote", [
  ("libri ___ (benim)", ["im", "ime", "imi"], 0, "benim kitabım", "Eril isimle <b>im</b>; dişil isimle <b>ime</b>."),
  ("shtëpia ___ (benim)", ["ime", "im", "imë"], 0, "benim evim", "Dişil isim (shtëpia) → <b>ime</b>."),
  ("vëllai ___ (senin)", ["yt", "jote", "tënd"], 0, "senin erkek kardeşin", "Eril isimle <b>yt</b>, dişil isimle <b>jote</b>."),
  ("motra ___ (senin)", ["jote", "yt", "juaj"], 0, "senin kız kardeşin", "Dişil isim (motra) → <b>jote</b>."),
  ("familja ___ (bizim)", ["jonë", "ynë", "jonë e"], 0, "bizim ailemiz", "Bizim: eril <b>ynë</b>, dişil <b>jonë</b>."),
  ("babai ___ (onun – kadının)", ["i saj", "e saj", "i tij"], 0, "onun (kadının) babası", "Kadının: <b>i/e saj</b>; erkeğin: <b>i/e tij</b>. Eril isimle <b>i</b>.")]),
 ("zamir", "Kısa zamirler: më, të, e, i", [
  ("___ pëlqen kafja. (bana)", ["Më", "Të", "E"], 0, "Kahve hoşuma gidiyor.", "<b>më</b> = bana/beni; fiilin <b>önüne</b> gelir."),
  ("___ dua shumë. (seni)", ["Të", "Më", "I"], 0, "Seni çok seviyorum.", "<b>të</b> = seni/sana."),
  ("Nuk ___ di. (onu)", ["e", "i", "më"], 0, "Onu bilmiyorum.", "<b>e</b> = onu (belirtme). Olumsuzlukta <b>nuk</b>tan sonra, fiilden önce."),
  ("___ jap një libër Anës. (ona)", ["I", "E", "Të"], 0, "Ana'ya bir kitap veriyorum.", "<b>i</b> = ona (yönelme). Arnavutçada isim olsa bile kısa zamir tekrar edilir."),
  ("___ ndihmo, të lutem! (bize)", ["Na", "Ju", "Më"], 0, "Bize yardım et lütfen!", "<b>na</b> = bizi/bize."),
  ("___ falënderoj shumë. (size)", ["Ju", "Na", "I"], 0, "Size çok teşekkür ederim.", "<b>ju</b> = sizi/size.")]),
 ("hal", "Haller: -it, -in, -ës, -ën", [
  ("Kjo është shtëpia e ___ . (djali – kimin?)", ["djalit", "djali", "djalin"], 0, "Bu oğlanın evi.", "Tamlayan hâli: eril <b>-it</b>. Türkçedeki <b>-ın</b> gibi ama isim arkada: shtëpia e djal<b>it</b>."),
  ("Shoh ___ . (vajza – kimi?)", ["vajzën", "vajzës", "vajza"], 0, "Kızı görüyorum.", "Belirtme hâli: dişil <b>-ën</b>, eril <b>-in</b>. Türkçedeki <b>-ı</b>."),
  ("Ia jap librin ___ . (djali – kime?)", ["djalit", "djalin", "djali"], 0, "Kitabı oğlana veriyorum.", "Yönelme hâli: eril <b>-it</b>, dişil <b>-ës</b>. Türkçedeki <b>-a</b>."),
  ("Lexoj ___ . (libri – neyi?)", ["librin", "librit", "libri"], 0, "Kitabı okuyorum.", "Belirtme hâli eril: <b>-in</b>: libr<b>in</b>."),
  ("Emri i ___ është Ana. (motra – kimin?)", ["motrës", "motrën", "motra"], 0, "Kız kardeşin adı Ana.", "Tamlayan hâli dişil: <b>-ës</b>: motr<b>ës</b>."),
  ("Vij nga ___ . (shkolla – nereden?)", ["shkolla", "shkollën", "shkollës"], 0, "Okuldan geliyorum.", "<b>nga</b> edatı yalın hâl ister: nga shkoll<b>a</b>. Ama <b>prej</b> tamlayan ister: prej shkoll<b>ës</b>.")]),
 ("koha", "Geçmiş: -dı mı, -yordu mu?", [
  ("Dje ___ në Tiranë. (shkoj)", ["shkova", "shkoja", "shkoj"], 0, "Dün Tiran'a gittim.", "Tek seferlik, bitmiş olay → <b>-dı</b> geçmişi: shkov<b>a</b>."),
  ("Kur isha i vogël, ___ çdo ditë në park. (luaj)", ["luaja", "luajta", "luaj"], 0, "Küçükken her gün parkta oynardım.", "Alışkanlık (çdo ditë) → <b>-yordu/-ırdı</b>: luaj<b>a</b>."),
  ("___ në telefon kur ai erdhi. (flas)", ["Flisja", "Fola", "Flas"], 0, "O geldiğinde telefonda konuşuyordum.", "Arka planda süren eylem → <b>flisja</b>; araya giren olay → <b>erdhi</b>."),
  ("Vitin e kaluar ___ një makinë. (blej)", ["bleva", "blija", "blej"], 0, "Geçen yıl bir araba aldım.", "Bitmiş tek olay → <b>bleva</b>."),
  ("Ai ___ shumë i lodhur. (jam – durum)", ["ishte", "qe", "është"], 0, "Çok yorgundu.", "Geçmişteki durum ve tasvir için genellikle <b>ishte</b> (isha) kullanılır."),
  ("Mbrëmë ___ një film të mirë. (shoh)", ["pashë", "shihja", "shoh"], 0, "Dün akşam güzel bir film izledim.", "Bitmiş olay → <b>pashë</b> (shoh fiili düzensiz).")]),
 ("dilek", "“të” kipi ve emir", [
  ("Dua ___ shkoj në shtëpi.", ["të", "do", "me"], 0, "Eve gitmek istiyorum.", "Standart Arnavutçada mastar yok: <b>dua të</b> + çekimli fiil."),
  ("Duhet të ___ (ti) më shumë.", ["punosh", "punoj", "punon"], 0, "Daha çok çalışman lazım.", "<b>të</b>'den sonra dilek kipi: ti → punos<b>h</b> (punon değil)."),
  ("Mund të ___ (ai) nesër.", ["vijë", "vjen", "vij"], 0, "Yarın gelebilir.", "Dilek kipinde 3. tekil şahıs <b>-ë</b> ile biter: vij<b>ë</b>, punoj<b>ë</b>."),
  ("___ këtu! (eja – siz)", ["Ejani", "Eja", "Vini"], 0, "Buraya gelin!", "Çoğul/kibar emir <b>-ni</b>: Eja → Eja<b>ni</b>."),
  ("___ harro! (unutma)", ["Mos", "Nuk", "S'"], 0, "Unutma!", "Olumsuz emir ve yasakta <b>mos</b>; olumsuz bildirimde <b>nuk</b>."),
  ("Nuk ___ flas italisht.", ["di të", "dua", "mund"], 0, "İtalyanca konuşmayı bilmiyorum.", "<b>di të</b> + fiil = …mayı bilmek. (mund të = …ebilmek)")]),
 ("olumsuz", "nuk, s', mos, as", [
  ("___ kam kohë.", ["Nuk", "Mos", "As"], 0, "Vaktim yok.", "Normal olumsuz cümle: <b>nuk</b> (konuşmada kısaca <b>s'</b>: S'kam kohë)."),
  ("___ u shqetëso!", ["Mos", "Nuk", "Jo"], 0, "Endişelenme!", "Emirde olumsuzluk: <b>mos</b>."),
  ("Nuk erdhi ___ .", ["askush", "dikush", "kush"], 0, "Kimse gelmedi.", "Olumsuz cümlede <b>askush</b> (hiç kimse), <b>asgjë</b> (hiçbir şey) — Türkçedeki gibi çift olumsuz."),
  ("Nuk kam ___ pyetje.", ["asnjë", "ndonjë", "çdo"], 0, "Hiç sorum yok.", "Olumsuzda <b>asnjë</b>; soruda <b>ndonjë</b>: A ke ndonjë pyetje?"),
  ("___ ti, ___ unë.", ["As … as", "Nuk … nuk", "Mos … mos"], 0, "Ne sen ne ben.", "“ne … ne” = <b>as … as</b>."),
  ("A je i lodhur? — ___ , jam mirë.", ["Jo", "Nuk", "Mos"], 0, "Yorgun musun? — Hayır, iyiyim.", "Tek başına “hayır” = <b>jo</b>. <b>nuk</b> her zaman fiilden önce gelir.")]),
]
