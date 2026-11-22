import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const here = dirname(fileURLToPath(import.meta.url));
const src = join(here, "entry.png");
if (!existsSync(src)) throw new Error("entry.png not found next to main.ts");
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
const srcBytes = statSync(src).size;
const destBytes = statSync(dest).size;
if (srcBytes !== destBytes) throw new Error(`copy mismatch: ${srcBytes} vs ${destBytes}`);
console.log(`entry.png copied: ${destBytes} bytes`);
