# Hepsiburada mobil web — kayıttan bulgular

Kaynak: kullanıcının 25.11.2026 tarihli 41 sn ekran kaydı (mobil tarayıcı, 480×800). Görülen ekranlar: ana sayfa, ürün kartından sepete ekleme, sepet, "Alışverişi tamamla" sonrası giriş ekranı. Teslimat ve ödeme adımları kayıtta yok.

## Ana sayfa
- Üstte turuncu uygulama bandı: "Uygulamayı indir, kupon fırsatını yakala" + "Uygulamaya git".
- Logo altında "premium'u keşfet"; altında tam genişlik arama: "Ürün, kategori veya marka ara".
- Altta sabit sekme çubuğu: "Keşfet", "Listelerim", "Sepetim" (turuncu adet rozeti), "Hesabım", "Kategoriler".
- Ürün kartı: görsel, sağ üstte kalp (listeye ekle), 2 satır ad, yıldız + yorum sayısı ("4,7 (28235)"), mor taksit etiketi ("Peşin fiyatına 3 x 97 TL"), fiyat, sağ altta sepete ekle ikonu. Bazı kartlarda yeşil "Sepette %28" indirimi.
- Kampanya bantları çok renkli ve yoğun ("efsane cuma", "%15 NET İNDİRİM").

## Sepete ekleme
- Sayfadan çıkmadan üstte bildirim: yeşil tik, "Ürün sepete eklendi", turuncu "Sepete git" linki, kapat (X).

## Sepet
- Başlık "Sepetim (4 ürün)" + sağda çöp kutusu.
- Ürünler satıcıya göre gruplu ("Satıcı: Teknosa"); grup başında yeşil "Kargon bedava" ve kargo zamanı ("Yarın kargoda", "Bugün kargoda").
- Her üründe turuncu onay kutusu, varyant ("Sarı/128 GB"), taksit, kırmızı "10 günün en düşük fiyatı", yeşil "Kazancını gör 550,00 TL", üstü çizili eski fiyat + yeni fiyat, adet seçici (adet 1'de "−" yerine çöp kutusu, sınırda "maks").
- "Sıklıkla birlikte alınanlar" yatay öneri şeridi.
- Altta sabit çubuk: "SEÇİLEN ÜRÜNLER (4)", "28.182,63 TL ^" (açılır döküm), yeşil "653,17 TL kazancın var", turuncu "Alışverişi tamamla".

## Giriş / üyelik kapısı ("Alışverişi tamamla" sonrası)
- En üstte turuncu metin link: "Üye olmadan devam et →".
- Sekmeler: "Giriş yap" | "Üye ol".
- Telefon öncelikli: bayrak + "+90" alanı; numara girilene kadar gri, pasif "Giriş yap".
- İkincil: "E-posta ile giriş yap" (çerçeveli buton).
- "Sosyal hesabın ile giriş yap": Apple, Google, Facebook.
- Altta yeşil kalkan + "Güvenli alışveriş".

## Renk kullanımı
- Zemin beyaz ve açık gri. Turuncu yalnızca: logo, uygulama bandı, ana buton ("Alışverişi tamamla"), aktif sekme, adet rozeti, onay kutuları, metin linkleri ("Sepete git", "Üye olmadan devam et").
- Anlamsal renkler ayrı ve tutarlı: **yeşil** = kazanç / bedava kargo / başarı, **mor** = taksit, **kırmızı** = aciliyet ("en düşük fiyat"), **sarı** = yıldız.
- Renkli kampanya görselleri bu disiplinin dışında kalıyor ve sayfayı kalabalıklaştırıyor.

## Kose'ye alındı
| Hepsiburada | Kose uyarlaması | Neden |
|---|---|---|
| Ödeme öncesi giriş kapısı + "Üye olmadan devam et" | Kapı ekranı; **üyeliksiz devam en üstte, büyük buton** | Baymard: misafir seçeneği en görünür olmalı; Hepsiburada'da küçük metin link |
| Telefon öncelikli giriş | +383 telefon + SMS kodu, **şifresiz** | Kapıda ödemede telefon zaten doğrulanıyor |
| Giriş yap / Üye ol sekmeleri | "Hyr" / "Regjistrohu" | Aynı alışkanlık |
| Kalp ile listeye ekleme | "Të preferuarat" (favoriler) | Geri dönüş sebebi |
| Alt sekme çubuğu | Kreu · Kategoritë · Shporta · Të preferuarat · Llogaria | Mobilde başparmak erişimi |
| Üstte sepete eklendi bildirimi | Mevcut bildirim korundu, mobilde sekme çubuğunun üstünde | — |
| Sabit sepet alt çubuğu + "kazancın var" | Mobilde sabit toplam + "Kursen X €" + buton | Toplamı ve kazancı her an görünür kılar |
| Yeşil = kazanç/bedava | Yeşil anlamsal renk eklendi; mavi yalnızca aksiyon | Aynı renk disiplini |
| Yıldız + yorum sayısı kartta | Kartta ve ürün sayfasında puan | Güven |
| "Sıklıkla birlikte alınanlar" | "Blihen shpesh bashkë" sepette | Sepet tutarı |
| Adet sınırında "maks" | Stok sınırında + pasif (mevcut) | — |

## Kose'ye alınmadı
- **Taksit etiketleri:** kart ödemesi yok.
- **Satıcı gruplama:** tek satıcı.
- **Uygulama indirme bandı ve kupon bandı:** uygulama yok; dikkat dağıtıyor.
- **Yoğun kampanya bant duvarı:** sade tasarım hedefiyle çelişiyor; tek kampanya bandı yeterli.
- **"10 günün en düşük fiyatı":** fiyat geçmişi gerektirir; ileride admin panelinden.
- **Sepette onay kutularıyla ürün seçme:** tek satıcı, kapıda ödeme; karmaşa ekler.
- **Sosyal giriş:** ilk aşamada gereksiz; telefon girişi yeterli. İleride Google/Apple eklenebilir.

## Doğrulanamayanlar
- Teslimat ve ödeme adımları, kapıda ödeme seçeneği (kayıtta yok).
- Turuncunun hex kodu (ekran kaydından renk ölçümü güvenilir değil).
