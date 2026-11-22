# 21 November 2026 — World News in One Image

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121)
[![make.fun rank](https://make.fun/badge/news-image-20261121/iwanr94/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121)
[![make.fun reward](https://make.fun/badge/news-image-20261121/iwanr94/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121)

A newspaper-front-page image summing up Saturday 21 November 2026:
the UK–EU landmark deal as the lead, plus a bento grid of eight more
stories — a Russian missile hitting Poland, the ICJ ruling that Myanmar
committed genocide against the Rohingya, Trump vs AI data centres,
the tech market sell-off, the first Trump–Xi–Putin Shenzhen summit,
Saudi Arabia intercepting Houthi missiles aimed at Riyadh, newly
declassified US UFO footage, and Mamdani's plan to close Rikers
Island by 2032.

## How to run

```sh
python3 draw_news.py        # renders entry.png (1024x1024, pure PIL)
MAKEFUN_OUTPUT_DIR=out node main.ts   # copies entry.png to out/entry.png
```

`main.ts` is Node 22, standard library only. It copies the image the
repository holds; the program runs twice and writes identical bytes.
