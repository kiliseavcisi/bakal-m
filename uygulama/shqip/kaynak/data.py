# Units for the app. Each word: [albanian, turkish, picture]
# picture: emoji, "#rrggbb" color swatch, "n:<digits>" number, or "" (no picture)
UNITS = [
 ("selam","Selamlaşma",[
  ["Përshëndetje","Merhaba","👋"],["Mirëmëngjes","Günaydın","🌅"],["Mirëdita","İyi günler","☀️"],["Mirëmbrëma","İyi akşamlar","🌆"],
  ["Natën e mirë","İyi geceler","🌙"],["Mirupafshim","Hoşça kal","🙋"],["Faleminderit","Teşekkürler","🙏"],["Ju lutem","Lütfen",""],
  ["S'ka përse","Bir şey değil",""],["Më falni","Affedersiniz",""],["Shihemi nesër","Yarın görüşürüz",""],["Gjumë të ëmbël","İyi uykular","😴"]]),
 ("hal","Tanışma",[
  ["Si je?","Nasılsın?",""],["Mirë jam","İyiyim","🙂"],["Shumë mirë","Çok iyi","😄"],["Jo keq","Fena değil",""],["Po ti?","Ya sen?",""],
  ["Si quhesh?","Adın ne?",""],["Unë quhem Ana","Benim adım Ana",""],["Gëzohem që u njohëm","Tanıştığıma memnun oldum","🤝"],
  ["Nga je?","Nerelisin?",""],["Jam nga Turqia","Türkiye'denim","🇹🇷"],["Sa vjeç je?","Kaç yaşındasın?",""],["Unë jam student","Ben öğrenciyim","🎓"]]),
 ("zamir","Ben, sen, o",[
  ["unë","ben","🙋"],["ti","sen","👉"],["ai","o (erkek)","👨"],["ajo","o (kadın)","👩"],["ne","biz","👥"],["ju","siz",""],
  ["ata","onlar",""],["unë jam","ben -im",""],["ti je","sen -sin",""],["ai është","o -dir",""],["ne jemi","biz -iz",""],["ata janë","onlar -dır",""]]),
 ("aile","Aile",[
  ["familje","aile","👨‍👩‍👧‍👦"],["nënë","anne","👩"],["baba","baba","👨"],["vëlla","erkek kardeş","👦"],["motër","kız kardeş","👧"],
  ["gjysh","dede","👴"],["gjyshe","nine","👵"],["fëmijë","çocuk","🧒"],["djalë","oğlan","👦"],["vajzë","kız","👧"],
  ["burrë","adam, koca","🧔"],["grua","kadın, eş","👩"],["xhaxha","amca",""],["teze","teyze",""],["bebe","bebek","👶"]]),
 ("sayi","Sayılar",[
  ["një","bir","n:1"],["dy","iki","n:2"],["tre","üç","n:3"],["katër","dört","n:4"],["pesë","beş","n:5"],["gjashtë","altı","n:6"],
  ["shtatë","yedi","n:7"],["tetë","sekiz","n:8"],["nëntë","dokuz","n:9"],["dhjetë","on","n:10"],["njëzet","yirmi","n:20"],
  ["tridhjetë","otuz","n:30"],["dyzet","kırk","n:40"],["njëqind","yüz","n:100"],["një mijë","bin","n:1000"]]),
 ("renk","Renkler",[
  ["e bardhë","beyaz","#f5f5f5"],["e zezë","siyah","#1d1d1f"],["e kuqe","kırmızı","#d7263d"],["e verdhë","sarı","#f6c91d"],
  ["blu","mavi","#2f6fd6"],["e gjelbër","yeşil","#2e9d4f"],["portokalli","turuncu","#f08a24"],["kafe","kahverengi","#7a4a2a"],
  ["gri","gri","#8e8e93"],["rozë","pembe","#f49ac1"],["vjollcë","mor","#7b4bb7"]]),
 ("meyve","Meyveler",[
  ["mollë","elma","🍎"],["dardhë","armut","🍐"],["qershi","kiraz","🍒"],["banane","muz","🍌"],["limon","limon","🍋"],
  ["luleshtrydhe","çilek","🍓"],["portokall","portakal","🍊"],["rrush","üzüm","🍇"],["shalqi","karpuz","🍉"],["pjepër","kavun","🍈"],
  ["arrë","ceviz","🌰"],["ulli","zeytin","🫒"],["kajsi","kayısı","🍑"]]),
 ("hayvan","Hayvanlar",[
  ["shqiponjë","kartal","🦅"],["mace","kedi","🐈"],["qen","köpek","🐕"],["pulë","tavuk","🐔"],["lopë","inek","🐄"],
  ["pëllumb","güvercin","🕊️"],["lepur","tavşan","🐇"],["ujk","kurt","🐺"],["bretkosë","kurbağa","🐸"],["flutur","kelebek","🦋"],
  ["peshk","balık","🐟"],["gjarpër","yılan","🐍"],["kalë","at","🐎"],["dele","koyun","🐑"],["bilbil","bülbül","🐦"]]),
 ("gun","Günler ve aylar",[
  ["e hënë","pazartesi",""],["e martë","salı",""],["e mërkurë","çarşamba",""],["e enjte","perşembe",""],["e premte","cuma",""],
  ["e shtunë","cumartesi",""],["e diel","pazar",""],["javë","hafta","📅"],["muaj","ay","🗓️"],["vit","yıl",""],
  ["janar","ocak","❄️"],["prill","nisan","🌷"],["korrik","temmuz","🏖️"],["tetor","ekim","🍂"]]),
 ("zaman","Zaman ve saat",[
  ["sot","bugün",""],["dje","dün",""],["nesër","yarın",""],["ora","saat","🕒"],["Sa është ora?","Saat kaç?","⌚"],
  ["Ora është tre","Saat üç","🕒"],["Ora është tre e gjysmë","Saat üç buçuk","🕞"],["mëngjes","sabah","🌅"],["mbrëmje","akşam","🌆"],
  ["natë","gece","🌙"],["minutë","dakika","⏱️"],["mesnatë","gece yarısı","🕛"]]),
 ("mevsim","Mevsimler ve hava",[
  ["pranverë","ilkbahar","🌸"],["verë","yaz","🌞"],["vjeshtë","sonbahar","🍁"],["dimër","kış","⛄"],["diell","güneş","☀️"],
  ["shi","yağmur","🌧️"],["borë","kar","❄️"],["erë","rüzgâr","🌬️"],["re","bulut","☁️"],["ylber","gökkuşağı","🌈"],
  ["Bie shi","Yağmur yağıyor","🌧️"],["Është ftohtë","Hava soğuk","🥶"],["Është nxehtë","Hava sıcak","🥵"]]),
 ("ev","Ev",[
  ["shtëpi","ev","🏠"],["derë","kapı","🚪"],["dritare","pencere","🪟"],["kuzhinë","mutfak","🍳"],["banjo","banyo","🛁"],
  ["dhoma e gjumit","yatak odası","🛏️"],["kopsht","bahçe","🌳"],["tavolinë","masa",""],["karrige","sandalye","🪑"],
  ["divan","kanepe","🛋️"],["jastëk","yastık",""],["televizor","televizyon","📺"],["kompjuter","bilgisayar","💻"],["çati","çatı",""]]),
 ("okul","Okul",[
  ["shkollë","okul","🏫"],["libër","kitap","📕"],["fletore","defter","📓"],["laps","kalem","✏️"],["mësuese","öğretmen","👩‍🏫"],
  ["nxënës","öğrenci","🧑‍🎓"],["klasë","sınıf",""],["shkronjë","harf","🔤"],["fjalë","kelime",""],["letër","mektup","✉️"],
  ["Unë lexoj një libër","Bir kitap okuyorum","📖"],["Unë shkruaj një letër","Bir mektup yazıyorum","✍️"]]),
 ("icecek","Yiyecek ve içecek",[
  ["ujë","su","💧"],["çaj","çay","🍵"],["kafe","kahve","☕"],["qumësht","süt","🥛"],["birrë","bira","🍺"],["verë","şarap","🍷"],
  ["lëng portokalli","portakal suyu","🧃"],["akullore","dondurma","🍦"],["bukë","ekmek","🍞"],["supë","çorba","🍲"],
  ["peshk","balık","🐟"],["Sa kushton?","Ne kadar?","💰"],["Gëzuar!","Şerefe!","🥂"],["Ju bëftë mirë!","Afiyet olsun!","🍽️"]]),
 ("ulke","Ülkeler ve diller",[
  ["Shqipëri","Arnavutluk","🇦🇱"],["Turqi","Türkiye","🇹🇷"],["Kosovë","Kosova","🇽🇰"],["Greqi","Yunanistan","🇬🇷"],
  ["Gjermani","Almanya","🇩🇪"],["Spanjë","İspanya","🇪🇸"],["Francë","Fransa","🇫🇷"],["shqip","Arnavutça",""],
  ["turqisht","Türkçe",""],["anglisht","İngilizce",""],["Ai flet turqisht","O Türkçe konuşuyor","🗣️"],["Unë flas shqip","Arnavutça konuşuyorum","🗣️"]]),
 ("fiil","Fiiller",[
  ["ha","yemek","🍴"],["pi","içmek","🥤"],["fle","uyumak","😴"],["shkoj","gitmek","🚶"],["vij","gelmek",""],["flas","konuşmak","🗣️"],
  ["punoj","çalışmak","💼"],["vrapoj","koşmak","🏃"],["notoj","yüzmek","🏊"],["këndoj","şarkı söylemek","🎤"],["qesh","gülmek","😂"],
  ["qaj","ağlamak","😢"],["lexoj","okumak","📖"],["shkruaj","yazmak","✍️"],["dëgjoj","dinlemek","🎧"],["shoh","görmek","👀"]]),
 ("sifat","Sıfatlar ve duygular",[
  ["i mirë","iyi","👍"],["i keq","kötü","👎"],["i bukur","güzel","✨"],["i madh","büyük","🐘"],["i vogël","küçük","🐭"],
  ["i ri","yeni / genç",""],["i vjetër","eski / yaşlı",""],["i lodhur","yorgun","😩"],["i ëmbël","tatlı","🍬"],
  ["dashuri","aşk","❤️"],["lumturi","mutluluk","😊"],["shpresë","umut","🌱"]]),
 ("cumle","Kalıp cümleler",[
  ["Të dua","Seni seviyorum","❤️"],["Më pëlqen","Hoşuma gidiyor","😍"],["Nuk më pëlqen","Hoşuma gitmiyor","😒"],
  ["Dua të pi ujë","Su içmek istiyorum","💧"],["Nuk kuptoj","Anlamıyorum","🤷"],["Ç'po bën?","Ne yapıyorsun?",""],
  ["Ku po shkon?","Nereye gidiyorsun?",""],["Do të vij nesër","Yarın geleceğim",""],["Kam një shok","Bir arkadaşım var","🧑‍🤝‍🧑"],
  ["Më ka marrë malli për ty","Seni özledim","🥺"],["Gëzuar ditëlindjen!","Doğum günün kutlu olsun!","🎂"],["Më ndihmo!","Yardım et!","🆘"]]),
]
