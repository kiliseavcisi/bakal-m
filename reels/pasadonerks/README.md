# PașaDöner (pasadonerks.com): Reels

- `pasadoner-reels.mp4`: 1080×1920, 30 fps, 20 s, H.264 + AAC; ready for Instagram/Facebook Reels.
- `kapak.jpg`: cover (the DoneRoll L + Ajran, 4€ offer).

All photos, the logo, product names, offers and contact details come from **pasadonerks.com** (Albanian).

| Time | Scene |
|---|---|
| 0–2.5 s | Logo + "Gjithmonë e freskët!" |
| 2.5–7 s | DoneRoll / Chickn'Buk / Iskender |
| 7–14 s | OFERTAT: Chickn'Buk + Ajran 4€ · DoneRoll L + Ajran 4€ · DoneRoll XL + Ajran 5€ |
| 14–16.5 s | Beef Plate · Chicken Plate · PasaFRIES · Big MIX Meal |
| 16.5–20 s | "Gjith' e gatuar vetëm për ty!" · +383 45 10 20 32 · @pasadonerks |

## Suggested caption (Albanian)
> Gjithmonë e freskët! 🔥 Chickn'Buk + Ajran veç 4€, DoneRoll L + Ajran veç 4€, DoneRoll XL + Ajran veç 5€.
> Gjith' e gatuar vetëm për ty! 📞 +383 45 10 20 32
>
> #pasadoner #doner #prishtina #kosova #doneroll #iskender #ajran

## Editing / rendering again
Text and timing live in `reel.html`; images are in `assets/`.
```bash
python3 music.py /tmp/music.wav
node capture.js /tmp/frames 30 20
ffmpeg -framerate 30 -i /tmp/frames/f%04d.png -i /tmp/music.wav -c:v libx264 -pix_fmt yuv420p -crf 18 \
  -c:a aac -b:a 192k -shortest -movflags +faststart pasadoner-reels.mp4
```
The music is synthesized by `music.py` (royalty‑free).
