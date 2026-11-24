# Dürbün Mum Telegram Botu

Seçtiğin kripto paraları ve hisseleri tarar. **Dürbün mum** formasyonu oluşunca Telegram'a bildirim yollar.

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
