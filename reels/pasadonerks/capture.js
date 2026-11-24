// Usage: node capture.js <outdir> [fps] [duration] [only comma-separated times]
const { chromium } = require('playwright');
const path = require('path'); const fs = require('fs');
(async () => {
  const out = process.argv[2]; const fps = +(process.argv[3] || 30); const dur = +(process.argv[4] || 15);
  const only = process.argv[5] ? process.argv[5].split(',').map(Number) : null;
  fs.mkdirSync(out, { recursive: true });
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  await page.goto('file://' + path.resolve(__dirname, 'reel.html') + '#capture');
  await page.evaluate(() => window.ready);
  const times = only || Array.from({ length: Math.round(fps * dur) }, (_, i) => i / fps);
  for (let i = 0; i < times.length; i++) {
    await page.evaluate(t => window.render(t), times[i]);
    await page.screenshot({ path: path.join(out, only ? `t${times[i]}.png` : `f${String(i).padStart(4, '0')}.png`) });
  }
  await browser.close();
})();
