// Runs the translation model off the main thread. The model (Meta NLLB-200, 600M, 8-bit) is downloaded once from
// Hugging Face and then served from the browser cache, so the app works without internet afterwards.
import { pipeline, env } from "./lib/transformers.min.js";
env.backends.onnx.wasm.wasmPaths = new URL("./lib/", import.meta.url).href;
env.allowLocalModels = false;
const MODEL = "Xenova/nllb-200-distilled-600M";
let tr = null;
async function load(local) {
  if (tr) return tr;
  if (local) { env.allowLocalModels = true; env.allowRemoteModels = false; env.localModelPath = local; }
  tr = await pipeline("translation", MODEL, { dtype: "q8", progress_callback: p => postMessage({ type: "progress", p }) });
  return tr;
}
self.onmessage = async e => {
  const m = e.data;
  try {
    if (m.type === "load") { await load(m.local); postMessage({ type: "ready" }); return; }
    if (m.type === "translate") {
      const t = await load(m.local);
      const parts = m.text.split(/(?<=[.!?…])\s+|\n+/).map(s => s.trim()).filter(Boolean), out = [];
      for (const s of parts) {
        const r = await t(s, { src_lang: m.src, tgt_lang: m.tgt, max_new_tokens: 200 });
        out.push(r[0].translation_text);
        postMessage({ type: "partial", id: m.id, text: out.join(" ") });
      }
      postMessage({ type: "done", id: m.id, text: out.join(" ") });
    }
  } catch (err) { postMessage({ type: "error", id: m.id, message: String(err && err.message || err) }); }
};
