// Copies the web app (uygulama/shqip) into www/ as a full HTML document for the Android WebView.
const fs = require("fs"), path = require("path");
const src = path.join(__dirname, "..", "uygulama", "shqip"), out = path.join(__dirname, "www");
fs.rmSync(out, { recursive: true, force: true });
for (const d of ["packs", "packs2"]) fs.mkdirSync(path.join(out, d), { recursive: true });
let page = fs.readFileSync(path.join(src, "index.html"), "utf8").replace(/^<meta charset="utf-8">\n/, "");
const head = '<!doctype html>\n<html lang="tr">\n<head>\n<meta charset="utf-8">\n' +
  '<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">\n' +
  '<meta name="theme-color" content="#c8162f">\n' +
  '<style>[hidden]{display:none!important} :root{padding-top:env(safe-area-inset-top,0px);padding-bottom:env(safe-area-inset-bottom,0px)} body{margin:0}</style>\n';
const i = page.indexOf('<div class="app"');
page = head + page.slice(0, i) + "</head>\n<body>\n" + page.slice(i) + "\n</body>\n</html>\n";
fs.writeFileSync(path.join(out, "index.html"), page);
fs.copyFileSync(path.join(src, "data.json"), path.join(out, "data.json"));
for (const d of ["packs", "packs2"]) for (const f of fs.readdirSync(path.join(src, d))) fs.copyFileSync(path.join(src, d, f), path.join(out, d, f));
console.log("www ready:", fs.readdirSync(path.join(out, "packs")).length, "packs");
