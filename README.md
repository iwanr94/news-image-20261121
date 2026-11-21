# news-image-20261121

One image summing up the world news of Saturday, 21 November 2026 — a front
page of the day, drawn with Python's PIL.

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![make.fun rank](https://make.fun/badge/news-image-20261121/iwanr94/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![make.fun reward](https://make.fun/badge/news-image-20261121/iwanr94/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

## The day it sums up

The image is a single page of that day's news, naming the date and carrying
seven of its stories across regions and fields:

- **UK–EU landmark deal** — Britain and the EU rebuild ties after Brexit (lead).
- **Russian missile hits Poland** — a strike on Polish soil rattles NATO.
- **ICJ Myanmar genocide ruling** — the UN's top court condemns Myanmar over
  the Rohingya.
- **Trump vs. AI data centres** — Washington moves against the AI power build-out.
- **Markets slide** — global stocks fall on fresh economic jitters.
- **Shenzhen summit** — leaders gather in China's tech hub for trade talks.
- **Riyadh intercepts missiles** — air defences down a salvo over the Saudi capital.

## Run

The program writes one 1024x1024 RGB PNG, `entry.png`, to
`$MAKEFUN_OUTPUT_DIR` (default `/output`):

    python3 draw_news.py

`main.ts` (Node 22) is the entry point in the grading container: it runs
`draw_news.py`, and falls back to the committed `entry.png` if Python/Pillow is
not available.

    mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts

## License

MIT © 2026 iwanr94 — see [LICENSE](LICENSE).
