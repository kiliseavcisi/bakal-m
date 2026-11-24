# Paşa Döner: Reels

- `pasa-doner-reels.mp4`: 1080×1920, 30 fps, 15 s, H.264 + AAC. Ready to upload to Instagram/Facebook Reels.
- `kapak.jpg`: cover image ("Bugün Paşa gibi ye.").

## Flow (120 BPM, cuts land on the beat)
| Time | Scene |
|---|---|
| 0–2 s | **ACIKTIN MI?** hook |
| 2–6 s | Rotating döner on the spit + "TAZE. SICAK. BOL BOL." |
| 6–10 s | "NE YESEM?": Dürüm / Ekmek Arası / Porsiyon |
| 10–12.5 s | **BUGÜN PAŞA GİBİ YE.** |
| 12.5–15 s | Logo + "Sipariş için DM'den yaz" |

## Suggested caption
> Acıktın mı? 🔥 Şişten taze kesim, tabağa sıcak! Dürüm mü, ekmek arası mı, porsiyon mu? Karar senin. 😋
> Bugün Paşa gibi ye! 👑 Sipariş için DM'den yaz.
>
> #döner #dürüm #paşadöner #lezzet #yemek #dönerci #ekmekarası #keşfet

## Editing
The text and timing live in `reel.html` (open it in a browser to see a live preview).
To render again:
```bash
python3 music.py /tmp/music.wav
node capture.js /tmp/frames 30 15
ffmpeg -framerate 30 -i /tmp/frames/f%04d.png -i /tmp/music.wav -c:v libx264 -pix_fmt yuv420p -crf 18 \
  -c:a aac -b:a 192k -shortest -movflags +faststart pasa-doner-reels.mp4
```
The music is synthesized by `music.py` (no copyright issues). If you want, you can swap in a trending sound in the Instagram app.
