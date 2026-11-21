// news-image-20261121 entry: sums up Saturday 21 November 2026's world news in
// one 1024x1024 PNG at $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
//
// The picture is drawn by draw_news.py (pure PIL, no network). If the grading
// container has no python3/Pillow, the same image saved beside this file is
// copied instead, so a run always produces the entry.
//
// Locally:  mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
// Node 22 runs this TypeScript as-is.

import { spawnSync } from 'node:child_process';
import { copyFileSync, existsSync } from 'node:fs';
import { dirname, join } from 'node:path';
import { fileURLToPath } from 'node:url';

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
const out = join(outDir, 'entry.png');

let ok = false;
try {
  const r = spawnSync('python3', [join(here, 'draw_news.py')], {
    cwd: here,
    env: { ...process.env, MAKEFUN_OUTPUT_DIR: outDir },
    stdio: 'inherit',
  });
  ok = r.status === 0 && existsSync(out);
} catch {
  ok = false;
}

if (!ok) {
  copyFileSync(join(here, 'entry.png'), out);
}
