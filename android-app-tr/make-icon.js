// Renders the Përkthe launcher icon (two speech bubbles, SQ and TR) to a 512px PNG (needs Playwright's Chromium).
const { chromium } = require("playwright");
const path = require("path");
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="22" fill="#c8162f"/>
  <rect x="12" y="18" width="46" height="34" rx="9" fill="#fff"/><path d="M24 52l-6 10 14-10z" fill="#fff"/>
  <text x="35" y="42" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="17" fill="#c8162f">SQ</text>
  <rect x="42" y="48" width="46" height="34" rx="9" fill="#2a2122"/><path d="M76 82l6 10-14-10z" fill="#2a2122"/>
  <text x="65" y="72" text-anchor="middle" font-family="Arial, sans-serif" font-weight="800" font-size="17" fill="#fff">TR</text>
</svg>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 512, height: 512 } });
  await p.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
  await p.locator("svg").screenshot({ path: path.join(__dirname, "icon-512.png"), omitBackground: true });
  await b.close(); console.log("icon-512.png");
})();
