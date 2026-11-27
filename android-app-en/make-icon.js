// Renders the Köprü launcher icon (a bridge between two banks) to a 512px PNG (needs Playwright's Chromium).
const { chromium } = require("playwright");
const path = require("path");
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="22" fill="#1f5fbf"/>
  <path d="M0 70h100v30H0z" fill="#174a96"/>
  <path d="M10 66c14-30 66-30 80 0" fill="none" stroke="#fff" stroke-width="6" stroke-linecap="round"/>
  <path d="M8 66h84" stroke="#fff" stroke-width="6" stroke-linecap="round"/>
  <path d="M26 66V50M38 66V43M50 66V41M62 66V43M74 66V50" stroke="#fff" stroke-width="3.5" stroke-linecap="round"/>
  <text x="18" y="34" font-family="Arial, sans-serif" font-weight="800" font-size="15" fill="#f2a516">TR</text>
  <text x="64" y="34" font-family="Arial, sans-serif" font-weight="800" font-size="15" fill="#fff">EN</text>
</svg>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 512, height: 512 } });
  await p.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
  await p.locator("svg").screenshot({ path: path.join(__dirname, "icon-512.png"), omitBackground: true });
  await b.close(); console.log("icon-512.png");
})();
