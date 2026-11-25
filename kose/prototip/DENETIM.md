# Kose Vitrin Prototipi — Bağımsız Denetim

Tarih: 2026-11-25 · Hedef: `kose/prototip/index.html`
Yöntem: axe-core (WCAG 2.1 AA + best-practice), Playwright ile 375 / 768 / 1280 / 1600 px, dokunma alanı ölçümü, uçtan uca sipariş akışı, klavye gezintisi, Impeccable detector, kod incelemesi.

## Puan

| # | Boyut | Önce | Sonra | Ana bulgu |
|---|---|---|---|---|
| 1 | Erişilebilirlik | 2 | 4 | Link içinde buton, isimsiz link, odak yönetimi yok, form hataları ekran okuyucuya bildirilmiyordu |
| 2 | Performans | 3 | 3 | Tek dosya, harici kütüphane yok; her tuşta tüm görünüm yeniden çiziliyor (prototip için kabul edilebilir) |
| 3 | Tema | 3 | 3 | Bilinçli tek (açık) tema; renkler token, ürün renkleri veri içinde |
| 4 | Responsive | 3 | 4 | Dil düğmeleri 29px, kategori linkleri 34px, "Hiq" 22px dokunma alanı |
| 5 | Uygulama bütünlüğü | 2 | 4 | Uydurma "1 000+ ürün" iddiası, başlık üstü etiket, işlevsiz footer linkleri, stok kavramı yok |
| | **Toplam** | **13/20** | **18/20** | |

## Bulgular ve yapılanlar

### P1 — Yayın öncesi şart
- **Link içinde buton (ürün kartı):** Kart bir `<a>`, hızlı ekle butonu onun içindeydi (geçersiz HTML, klavye/ekran okuyucu karışıklığı). → Kart `<article>` oldu, ürün adı linki tüm kartı kaplıyor, buton ayrı katmanda.
- **İsimsiz link (axe: link-name, serious):** Bildirim içindeki "Sepeti gör" linki gizliyken boştu. → Metin dolu, gizliyken `hidden`/`visibility:hidden`.
- **Sayfa değişiminde odak ve başlık:** Görünüm değişince odak eski yerde kalıyor, sekme başlığı hep aynıydı. → Odak yeni sayfanın başlığına gidiyor, `document.title` her görünümde güncelleniyor.
- **Form hataları:** Hatalı alanlar yalnızca renkle işaretleniyordu. → `aria-invalid`, `aria-describedby`, `required`; ilk hatalı alana odak.
- **Stok yok:** Tükenmiş ürün de satın alınabiliyordu, adet sınırsızdı. → Stok alanı, "E shitur" rozeti, pasif buton, "Vetëm 3 copë" uyarısı, sepette stok sınırı.
- **Uydurma iddia:** "Mbi 1 000 produkte" gerçek veriye dayanmıyordu. → Kaldırıldı.

### P2 — Sonraki geçişte
- **Dokunma alanları:** Dil düğmeleri 36px, kategori linkleri 40px, logo 44px, "Hiq" 40px, footer linkleri büyütüldü.
- **Sipariş adımları:** Sepet → Teslimat → Onay adım göstergesi eklendi.
- **SMS kodu:** Yapıştırma desteği, 4 hane girilince otomatik gönderim, yanlış kodda alanları temizleme, 30 sn sonra "Kodu tekrar gönder".
- **Onay sayfası:** Ürünler, teslimat adresi, telefon, toplam ve "Şimdi ne olacak" 3 adımı eklendi.
- **Koşullar:** Sipariş butonunun altında satış koşulları ve gizlilik onay metni.
- **Yardım sayfası:** Footer linkleri artık çalışıyor; 4 dilde SSS (sipariş, ödeme, teslimat, iade, evde olmama). Metinler örnek olarak işaretli.
- **Fiyat şeffaflığı:** Ürün sayfasında "Çmimi përfshin TVSH-në".
- **Ürün bulunamadı** sayfası; bilinmeyen ürün linki artık listeye düşmüyor.
- **Arama:** Kategoriye geçince arama kutusu temizleniyor; yazarken odak kaybolmuyor.
- **Tarih:** Tarayıcı Arnavutçayı desteklemediği için teslim tarihi İngilizce çıkıyordu. → 4 dil için kendi gün/ay adları.
- **Landmark:** Duyuru bandı `aside` oldu; filtre çipleri üst menüyle aynı etiketi taşımıyor.

### P3 — Cila
- Başlık üstündeki kategori etiketi (ürün sayfası) kaldırıldı; kategori zaten breadcrumb'da.
- Hareket azaltma tercihi artık her şeyi öldürmüyor, sadece hareketli dönüşümleri kapatıyor.
- Metin seçimi ve imleç rengi markaya uygun.
- Bildirim mesajı hangi ürünün (ve rengin/bedenin) eklendiğini söylüyor.

## Son ölçüm
- axe: tüm görünümlerde 4 genişlikte temiz (ana sayfa, liste, ürün, tükenmiş ürün, sepet, hatalı form, doğrulama, onay, yardım).
- Yatay taşma: 0 px, tüm genişliklerde.
- Konsol hatası: yok.
- Impeccable detector: 1 bulgu (footer alt satırı "kenara yapışık"), yanlış alarm: satırın 16px üst/alt boşluğu var.

## Açık kalanlar (prototip dışı, gerçek sistemde)
- Gerçek ürün fotoğrafları (şimdilik çizim ikon).
- Sırpça Kiril alfabesi seçeneği.
- SMS sağlayıcısı ve gerçek doğrulama; kapıda ödeme sipariş limiti; tekrar teslim almayan müşteri engeli (admin paneli).
- Kurye entegrasyonu (kurye seçilince).
- SEO: sunucu tarafı render, ürün şeması (JSON-LD), sitemap.
