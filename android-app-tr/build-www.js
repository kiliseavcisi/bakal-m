// Copies the translator (uygulama/perkthe) into www/ for the Android WebView. The model itself is NOT bundled:
// it is downloaded once on first use and cached, so the APK stays small.
const fs = require("fs"), path = require("path");
const src = path.join(__dirname, "..", "uygulama", "perkthe"), out = path.join(__dirname, "www");
fs.rmSync(out, { recursive: true, force: true }); fs.mkdirSync(path.join(out, "lib"), { recursive: true });
for (const f of ["index.html", "gheg.js", "worker.js"]) fs.copyFileSync(path.join(src, f), path.join(out, f));
for (const f of fs.readdirSync(path.join(src, "lib"))) fs.copyFileSync(path.join(src, "lib", f), path.join(out, "lib", f));
console.log("www ready");
