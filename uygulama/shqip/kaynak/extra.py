# Content beyond the word lists: video links, grammar tips, stories, alphabet.
YT = "https://www.youtube.com/watch?v="

# unit id -> (video id, video title, tips[])
UNIT_INFO = {
 "selam": ("mZW4U7y6ZTY", "Ders 2/2 · Selamlaşma ve iltifatlar", [
   "<b>Mirëdita</b> sabah 10'dan güneş batana kadar kullanılır; giderken <b>Mirupafshim</b> denir.",
   "<b>Natën e mirë</b> sadece yatarken değil, akşam ayrılırken de söylenir."]),
 "hal": ("SpkgkgGYHUU", "Ders 8 · Tanışma", [
   "<b>Si je?</b> arkadaşa, <b>Si jeni?</b> büyüklere ve resmî ortamda sorulur.",
   "Cümle başındaki <b>A</b> evet/hayır sorusu yapar: <i>A flisni shqip?</i>"]),
 "zamir": ("3sRKdlS_Q3k", "Ders 5 · Fiil çekimi", [
   "Türkçede ek olan \"-im, -sin\" Arnavutçada ayrı bir fiildir: <b>jam, je, është</b>.",
   "<b>ai</b> erkek, <b>ajo</b> kadın için \"o\" demektir; fiil ikisinde de aynıdır."]),
 "aile": ("2DjhwmDb-v0", "Ders 7 · Aile fertleri", [
   "İyelik isimden sonra gelir: <b>familja ime</b> = ailem, <b>nëna ime</b> = annem.",
   "Eril isimler çoğunlukla ünsüzle, dişil isimler <b>-ë / -e</b> ile biter."]),
 "sayi": ("PwbVOS1Ptgg", "Ders 14 · Sayılar", [
   "11–19: sayı + <b>mbëdhjetë</b> (\"onun üstünde\"): <i>pesëmbëdhjetë</i> = 15.",
   "20 = <b>njëzet</b>, 40 = <b>dyzet</b>; bileşikler <b>e</b> ile bağlanır: <i>njëzet e pesë</i>."]),
 "renk": ("NBw95VPJIDM", "Ders 19 · Renkler", [
   "Sıfat isimle uyar: eril <b>i kuq</b>, dişil <b>e kuqe</b>.",
   "Arnavut bayrağı kırmızı-siyah: <i>Flamuri shqiptar është i kuq dhe i zi.</i>"]),
 "meyve": ("Oc9teZ5xKtE", "Ders 4 · Meyve, sebze, hayvanlar", [
   "<b>rr</b> kalın ve titrek okunur: <i>rrush</i> (üzüm), <i>arrë</i> (ceviz).",
   "<b>ll</b> kalın l'dir: <i>mollë</i> = elma."]),
 "hayvan": ("Oc9teZ5xKtE", "Ders 4 · Hayvanlar ve sesleri", [
   "<b>Shqipëri</b> \"kartallar ülkesi\" demektir: <i>shqiponjë</i> = kartal.",
   "<b>q</b> yumuşak ç'dir: <i>qen</i> = köpek."]),
 "gun": ("VvMquynR5oY", "Ders 15 · Haftanın günleri", [
   "Günlerin başında <b>e</b> vardır: <i>e hënë, e martë</i>.",
   "<b>nga … deri</b> = -den … -e kadar: <i>nga e hëna deri të dielën</i>."]),
 "zaman": ("hkzDkCuLDsk", "Ders 12 · Saat sorma", [
   "<b>e</b> = geçe, <b>pa</b> = var: <i>katër e çerek</i> (4'ü çeyrek geçe), <i>pesë pa çerek</i> (5'e çeyrek var).",
   "<b>gjysmë</b> = yarım: <i>tre e gjysmë</i> = üç buçuk."]),
 "mevsim": ("7BQAZrBI_x4", "Ders 24 · Mevsimler ve hava", [
   "<b>Bie shi</b> = \"yağmur düşüyor\", yani yağmur yağıyor.",
   "Gelecek zaman: <b>do të</b> + fiil: <i>Nesër do të bjerë borë.</i>"]),
 "ev": ("mUYzzBJ8mIs", "Ders 18 · Bizim evimiz", [
   "Yer bildiren kelimeler: <b>lart</b> yukarı, <b>poshtë</b> aşağı, <b>para</b> önünde, <b>prapa</b> arkasında.",
   "<b>dhoma e gjumit</b> = \"uyku odası\", yani yatak odası."]),
 "okul": ("WuK1pqYsVsY", "Ders 9 · Okulda", [
   "<b>në</b> = -de/-da: <i>në shkollë</i> okulda, <i>në shtëpi</i> evde.",
   "<b>Më pëlqen të lexoj</b> = okumayı seviyorum (hoşuma gidiyor)."]),
 "icecek": ("RzsEAgFAzEA", "Ders 21 · İçecekler", [
   "<b>me</b> = ile, -lı: <i>çaj me limon</i> limonlu çay.",
   "<b>verë</b> hem \"şarap\" hem \"yaz\" demektir; bağlamdan anlaşılır."]),
 "ulke": ("pRraYRMSOfk", "Ders 10 · Ülkeler ve diller", [
   "Dil adları <b>-isht</b> ile biter: <i>turqisht, anglisht</i>; Arnavutça ise <b>shqip</b>.",
   "<b>ndodhet në</b> = -de bulunur: <i>Tirana ndodhet në Shqipëri.</i>"]),
 "fiil": ("toHrQvtdb3w", "Ders 11 · Okuma-yazma fiilleri", [
   "<b>-oj</b> ile biten fiiller \"sen\" ve \"o\" için <b>-on</b> olur: <i>lexoj → lexon</i>.",
   "Şu anı vurgulamak için fiilden önce <b>po</b>: <i>Po lexoj</i> = şu an okuyorum."]),
 "sifat": ("qeVAH-JB6lc", "Olumlu ve olumsuz cümleler", [
   "Olumsuzluk fiilden önce <b>nuk</b> ya da <b>s'</b>: <i>Nuk jam i lodhur.</i>",
   "<b>aspak / fare</b> = hiç: <i>Nuk kam aspak durim.</i>"]),
 "cumle": ("pObAxkoIhM0", "30 gündelik kelime", [
   "<b>dua</b> hem \"istemek\" hem \"sevmek\": <i>Të dua</i> seni seviyorum, <i>Dua ujë</i> su istiyorum.",
   "Bir şeyi sevmek için <b>më pëlqen</b> kullanılır: <i>Më pëlqen kafeja.</i>"]),
}

# Short readings built from the video lessons (comprehensible input).
STORIES = [
 {"id": "klasa", "t": "Sınıfta", "src": ("SpOt7IE14YY", "Ders 3 · Öğretmen-öğrenci diyaloğu"), "after": "sayi",
  "lines": [
   ["Mësuesja", "Mirëmëngjes, nxënës!", "Günaydın öğrenciler!"],
   ["Nxënësit", "Mirëmëngjes, mësuese!", "Günaydın öğretmenim!"],
   ["Mësuesja", "Sa është ora?", "Saat kaç?"],
   ["Arbeni", "Ora është tetë.", "Saat sekiz."],
   ["Mësuesja", "Sa nxënës janë në klasë?", "Sınıfta kaç öğrenci var?"],
   ["Arturi", "Në klasë janë njëzet e katër nxënës.", "Sınıfta yirmi dört öğrenci var."],
   ["Mësuesja", "Sa bëjnë katër plus tre?", "Dört artı üç kaç eder?"],
   ["Dritani", "Bëjnë shtatë.", "Yedi eder."],
   ["Mësuesja", "Po, ashtu është. Mjaft për sot!", "Evet, aynen öyle. Bugünlük yeter!"]],
  "q": [["Saat kaç?", ["Sekiz", "Yedi", "Dokuz"], 0], ["Sınıfta kaç öğrenci var?", ["24", "14", "42"], 0]]},
 {"id": "familja", "t": "Benim ailem", "src": ("2DjhwmDb-v0", "Ders 7 · Aile fertleri"), "after": "aile",
  "lines": [
   ["", "Unë quhem Ana.", "Benim adım Ana."],
   ["", "Kjo është familja ime.", "Bu benim ailem."],
   ["", "Nëna ime quhet Mimoza.", "Annemin adı Mimoza."],
   ["", "Babai im është mësues.", "Babam öğretmen."],
   ["", "Kam një vëlla dhe një motër.", "Bir erkek kardeşim ve bir kız kardeşim var."],
   ["", "Familja ime nuk është e vogël.", "Ailem küçük değil."],
   ["", "Familja ime është e madhe.", "Ailem büyük."]],
  "q": [["Ana'nın annesinin adı ne?", ["Mimoza", "Albana", "Lindita"], 0], ["Babası ne iş yapıyor?", ["Öğretmen", "Doktor", "Mühendis"], 0]]},
 {"id": "kafe", "t": "Kafede", "src": ("RzsEAgFAzEA", "Ders 21 · İçecekler"), "after": "icecek",
  "lines": [
   ["Kamerieri", "Mirëdita! Urdhëroni!", "İyi günler! Buyurun!"],
   ["Ana", "Mirëdita. Dua një çaj me limon, ju lutem.", "İyi günler. Limonlu bir çay istiyorum, lütfen."],
   ["Kamerieri", "Po ju?", "Ya siz?"],
   ["Artani", "Unë dua një kafe turke.", "Ben bir Türk kahvesi istiyorum."],
   ["Kamerieri", "Diçka tjetër?", "Başka bir şey?"],
   ["Ana", "Po, një akullore me fruta.", "Evet, meyveli bir dondurma."],
   ["Artani", "Sa kushton?", "Ne kadar?"],
   ["Kamerieri", "Pesë qind lekë.", "Beş yüz lek."],
   ["Ana", "Faleminderit! Mirupafshim!", "Teşekkürler! Hoşça kalın!"]],
  "q": [["Ana ne içiyor?", ["Limonlu çay", "Türk kahvesi", "Süt"], 0], ["Artan ne istiyor?", ["Türk kahvesi", "Bira", "Su"], 0]]},
 {"id": "qindarka", "t": "On beş kuruş", "src": ("4UNe9b-TiEY", "Ders 16 · Okuma: 15 Qindarka"), "after": "cumle",
  "lines": [
   ["", "Një djalë dhjetë vjeç hyri në një hotel.", "On yaşında bir çocuk bir otele girdi."],
   ["", "Ai u ul në një tavolinë.", "Bir masaya oturdu."],
   ["", "Kamerierja i solli një gotë ujë.", "Garson kız ona bir bardak su getirdi."],
   ["Djali", "Sa kushton një akullore me fruta?", "Meyveli bir dondurma ne kadar?"],
   ["Kamerierja", "Pesëdhjetë qindarka.", "Elli kuruş."],
   ["", "Djali numëroi monedhat.", "Çocuk bozuk paralarını saydı."],
   ["Djali", "Po një akullore e thjeshtë?", "Peki sade bir dondurma?"],
   ["Kamerierja", "Tridhjetë e pesë qindarka!", "Otuz beş kuruş!"],
   ["", "Djali hëngri akulloren, pagoi dhe doli.", "Çocuk dondurmasını yedi, ödedi ve çıktı."],
   ["", "Pranë pjatës ishin pesëmbëdhjetë qindarka.", "Tabağın yanında on beş kuruş vardı."],
   ["", "Ishin bakshish për kamerieren.", "Garson kıza bahşişti."]],
  "q": [["Çocuk kaç yaşında?", ["On", "On beş", "Beş"], 0], ["Tabağın yanında ne vardı?", ["15 kuruş bahşiş", "Bir mektup", "Dondurma"], 0]]},
]

ALPHA = [
 ["a","a","Ankara'daki a","ari","ayı",""],["b","b","","bukë","ekmek",""],["c","ts","tsunami'deki ts","cili","hangisi","d"],
 ["ç","ç","","çaj","çay",""],["d","d","","derë","kapı",""],["dh","İng. this","dil dişlerin arasında","dhe","ve","d"],
 ["e","e","","emër","isim",""],["ë","ı ile ö arası","kelime sonunda yutulur","një","bir","d"],["f","f","","fjalë","kelime",""],
 ["g","g","","gur","taş",""],["gj","yumuşak c","","gjuhë","dil","d"],["h","h","","hallë","hala",""],["i","i","","ishull","ada",""],
 ["j","y","Türkçedeki y","ju","siz","d"],["k","k","","kush","kim",""],["l","ince l","","lule","çiçek",""],
 ["ll","kalın l","\"oldu\"daki l","llambë","lamba","d"],["m","m","","motër","kız kardeş",""],["n","n","","nënë","anne",""],
 ["nj","ny","İspanyolca ñ","njeri","insan","d"],["o","o","","orë","saat",""],["p","p","","pi","içmek",""],
 ["q","yumuşak ç","dil damağa yakın","qen","köpek","d"],["r","r","","rri","kalmak",""],["rr","titrek r","dil titreşir","rrugë","yol","d"],
 ["s","s","","sot","bugün",""],["sh","ş","","shumë","çok","d"],["t","t","","tre","üç",""],["th","İng. think","dil dişlerin arasında","thua","söylersin","d"],
 ["u","u","","ujë","su",""],["v","v","","vëlla","erkek kardeş",""],["x","dz","","xixë","kıvılcım","d"],["xh","c","Türkçedeki c","xhami","cami","d"],
 ["y","ü","Türkçedeki ü","yll","yıldız","d"],["z","z","","zemër","kalp",""],["zh","j","Türkçedeki j","zhurmë","gürültü","d"],
]
