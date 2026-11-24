# Dürbün Mum + ChoCh Telegram Botu

Binance'teki kripto paritelerini tarar. Üst zaman diliminde **dürbün mum** formasyonu bulunca alt zaman diliminde **ChoCh** onayı bekler. Onay gelince Telegram'a bildirim yollar.

## Akış

1. **Dürbün:** Üst zaman diliminde (ör. 4h) formasyon aranır. Tarama her yeni mum kapanışında bir kez yapılır.
2. **Bekleme:** Bulunan dürbün kaydedilir ve alt zaman dilimi (ör. 15m) her dakika kontrol edilir.
3. **Onay:** Dürbün tamamlandıktan sonra alt zaman diliminde aynı yönde ChoCh olursa ✅ **ONAYLI** bildirimi gider.
   - Yükseliş dürbünü için yukarı ChoCh: alt zaman dilimi önce aşağı dönmüş olmalı, sonra son tepe kapanışla kırılmalı.
4. **İptal:** Şu iki durumda bildirim gitmez:
   - `SETUP_EXPIRE_BARS` üst zaman dilimi mumu içinde ChoCh gelmezse.
   - Fiyat dürbünün dibinin altında (düşüşte tepesinin üstünde) kapanırsa.

ChoCh mantığı TradingView'daki **BoS/ChoCh (Nephew_Sam_)** göstergesinin ekrandaki ayarlarıyla aynı:
- Pivot lb = 5, Pivot rb = 5.
- Kırılım kapanışla onaylanır.
- Trend aşağıyken son pivot tepenin üstünde kapanış = yukarı ChoCh. Trend zaten yukarıysa = BOS.

| Üst TF | Alt TF (varsayılan) |
|---|---|
| 1d | 1h |
| 4h | 15m |
| 1h | 5m |
| 15m | 1m |

Bunları `.env` dosyasındaki `LTF_MAP` ile değiştirebilirsin.

## Formasyon kuralları

| | Yükseliş (dipte) | Düşüş (tepede) |
|---|---|---|
| Renk sırası | 🟥 🟥 🟩 🟩 | 🟩 🟩 🟥 🟥 |
| Çizgi | 1. ve 4. mumun gövde **üstlerinden** alçak olanı | 1. ve 4. mumun gövde **altlarından** yüksek olanı |
| Şart | 2. ve 3. mumun gövdesi çizginin **üstüne çıkamaz** | 2. ve 3. mumun gövdesi çizginin **altına inemez** |
| İğneler | Aşağı taşabilir | Yukarı taşabilir |

- Mumların boyuna bakılmaz. Sadece renk sırası ve gövde ihlali önemlidir.
- `STRICT_WICKS=1` yaparsan ortadaki mumların iğneleri de çizgiyi geçemez.
- Sadece **kapanmış** mumlara bakılır. Aynı sinyal iki kez gönderilmez (`state.json`).
- `BINANCE_SYMBOLS=ALL` yaparsan hacme göre ilk `TOP_N` USDT paritesi taranır. Stabil coinler ve kaldıraçlı tokenler hariç tutulur.
- Dürbün bulunduğu an da haber almak istersen `NOTIFY_PENDING=1` yap.

## Kurulum

1. Telegram'da **@BotFather**'a `/newbot` yaz. Sana verdiği token'ı al.
2. Kurulumu yap:
   ```bash
   cd durbun-bot
   pip install -r requirements.txt        # BIST için ayrıca: pip install yfinance
   cp .env.example .env                    # token'ı ve sembolleri yaz
   ```
3. Kendi botuna Telegram'dan `/start` yaz. Sonra şunu çalıştır:
   ```bash
   python bot.py --chat-id
   ```
   Çıkan `TELEGRAM_CHAT_ID=...` satırını `.env` dosyasına ekle. Grup ya da kanal da kullanabilirsin: botu ekle, bir mesaj at ve aynı komutu çalıştır.
4. Bağlantıyı dene, sonra botu başlat:
   ```bash
   python bot.py --test
   python bot.py
   ```

`python bot.py --once` tek tur tarayıp kapanır. cron ile kullanmak için uygundur.

## Sürekli çalıştırma

Botun 7/24 çalışması için sürekli açık duran bir bilgisayar gerekir. Bu bir VPS, Raspberry Pi ya da kapanmayan bir PC olabilir. Örnek:
```bash
nohup python bot.py > bot.log 2>&1 &
```

> Not: Binance bazı ülkelerden ve bulut sunucularından API erişimine izin vermiyor. Hata alırsan başka bir sunucu dene.

## Testler
```bash
pip install pytest && pytest -q tests
```

*Bu bot sadece formasyonu tespit eder. Yatırım tavsiyesi değildir.*
