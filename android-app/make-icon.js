// Renders the Shqiponja eagle mascot to a 512px PNG launcher icon (needs Playwright's Chromium).
const { chromium } = require("playwright");
const path = require("path");
const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="512" height="512" viewBox="0 0 100 100">
  <rect width="100" height="100" rx="22" fill="#c8162f"/>
  <g transform="translate(10 8) scale(.8)">
    <path d="M14 58c-8-10-6-24 4-30 0 10 6 16 14 18z" fill="#2a2122"/><path d="M86 58c8-10 6-24-4-30 0 10-6 16-14 18z" fill="#2a2122"/>
    <ellipse cx="50" cy="62" rx="30" ry="30" fill="#fbe3e6"/>
    <circle cx="50" cy="40" r="24" fill="#2a2122"/>
    <circle cx="41" cy="38" r="7" fill="#fff"/><circle cx="59" cy="38" r="7" fill="#fff"/>
    <circle cx="42" cy="38" r="3.4" fill="#2a2122"/><circle cx="60" cy="38" r="3.4" fill="#2a2122"/>
    <path d="M44 47h12l-6 12z" fill="#f2a516"/>
    <path d="M38 88l-4 8M50 90v8M62 88l4 8" stroke="#f2a516" stroke-width="3" stroke-linecap="round"/>
  </g></svg>`;
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 512, height: 512 } });
  await p.setContent(`<html><body style="margin:0;background:transparent">${svg}</body></html>`);
  await p.locator("svg").screenshot({ path: path.join(__dirname, "icon-512.png"), omitBackground: true });
  await b.close(); console.log("icon-512.png");
})();
