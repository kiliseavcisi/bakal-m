# Kose — Tasarım Kararları

Durum: onaylandı (renk yönü C "Qiell", geçici logo). Yazı tipi: önerilen eşleşme varsayıldı.

## Dil
- Ana dil: Arnavutça (sq)
- Ek diller: İngilizce (en), Türkçe (tr), Sırpça (sr — Latin/Kiril kararı açık)
- Para birimi: EUR, biçim `49,90 €`

## Renk (yön C — Qiell)
| Token | Değer | Kullanım |
|---|---|---|
| `--brand` | `#244aa5` | Bayrak mavisi. Butonlar, linkler, aktif durumlar |
| `--ink` | `#0e1a33` | Metin, üst duyuru bandı |
| `--ice` | `#eaf1fd` | Yumuşak zemin, ürün görsel arka planı |
| `--white` | `#ffffff` | Sayfa zemini |
| `--glow` | `linear-gradient(135deg, #244aa5, #5aa0ea)` | Sadece ana bant ışığı ve kampanya alanları |
| `--gold` | `#c9a24a` | Çok küçük vurgu (ör. "E re" rozeti) |

Kural: gradyan yalnızca hero ve kampanya bloklarında. Butonlar düz mavi.

### Anlamsal renkler (Hepsiburada disiplininden uyarlandı)
Mavi **yalnızca aksiyon** içindir (ana buton, link, aktif sekme, adet rozeti). Diğer anlamlar sabit renklerle:

| Anlam | Token | Değer | Örnek |
|---|---|---|---|
| Kazanç, bedava kargo, başarı, doğrulandı | `--ok` | `#1f7a4d` | "Kursen 25,40 €", "Falas", "I verifikuar" |
| Hata | `--err` | `#b42318` | form hataları |
| Az stok, sipariş durumu | metin `#8a4b00`, zemin `#fff4e0` | — | "Vetëm 3 copë", "Në përgatitje" |
| Favori | `--heart` | `#d6336c` | dolu kalp |
| Puan yıldızı / "E re" rozeti | `--gold` | `#c9a24a` | ★ 4,6 |

## Yazı tipi
- Başlık: Geologica (600/700)
- Metin: Onest (400/500/600)
- Gerekli alt kümeler: latin, latin-ext, cyrillic

## Logo (geçici)
- Küçük harf "kose" + çanta işareti; sap = altı nokta (bayraktaki altı yıldız)
- Admin panelinden yüklenen logo bunun yerini alır

Referans pano: `kose/tasarim/yon-tahtasi.html`
