#!/usr/bin/env python3
"""Draw the 21 November 2026 world news in one 1024x1024 image.

Bento-grid newspaper front page: dark navy banner naming the day,
one large lead panel (UK-EU deal) and 8 story cells covering all 9
verified stories of Saturday 21 November 2026. Pure PIL, no network.
Writes entry.png next to this script.
"""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
NAVY = (13, 16, 48)
NAVY2 = (24, 32, 74)
CREAM = (246, 239, 221)
PAPER = (255, 253, 246)
INK = (28, 28, 28)
GOLD = (201, 162, 39)
RED = (166, 58, 46)
BLUE = (46, 90, 138)
SKY = (120, 165, 205)
GREEN = (74, 120, 74)
GREY = (120, 118, 110)

_FONT_DIRS = [
    "/usr/share/fonts/truetype/dejavu",
    "/usr/share/fonts/dejavu",
    "/usr/share/fonts/truetype",
]


def _load(name, size):
    for d in _FONT_DIRS:
        p = os.path.join(d, name)
        if os.path.exists(p):
            try:
                return ImageFont.truetype(p, size)
            except Exception:
                pass
    return ImageFont.load_default(size)


def F(size, bold=False):
    return _load("DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf", size)


def wrap(d, text, font, max_w):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if d.textlength(t, font=font) <= max_w:
            cur = t
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def text_c(d, cx, y, s, size, fill, bold=False):
    f = F(size, bold)
    w = d.textlength(s, font=f)
    d.text((cx - w / 2, y), s, fill=fill, font=f)
    return y + size + 4


def text_block(d, cx, y, s, size, fill, bold, max_w, leading=None):
    f = F(size, bold)
    lines = wrap(d, s, f, max_w)
    lh = leading if leading else size + 5
    for ln in lines:
        w = d.textlength(ln, font=f)
        d.text((cx - w / 2, y), ln, fill=fill, font=f)
        y += lh
    return y


def panel(d, box, fill=PAPER, outline=NAVY, width=2):
    d.rounded_rectangle(box, radius=10, fill=fill, outline=outline, width=width)


img = Image.new("RGB", (W, H), CREAM)
d = ImageDraw.Draw(img)

# ---- banner: the day, named large ----
d.rectangle([0, 0, W, 96], fill=NAVY)
d.rectangle([0, 96, W, 102], fill=GOLD)
text_c(d, W // 2, 14, "21 NOVEMBER 2026", 44, (255, 255, 255), bold=True)
text_c(d, W // 2, 66, "W O R L D   N E W S", 16, GOLD, bold=True)


# ---- lead panel: UK-EU landmark deal ----
panel(d, [16, 108, 1008, 356])
text_c(d, W // 2, 122, "UK\u2013EU LANDMARK DEAL", 34, NAVY, bold=True)
text_c(d, W // 2, 164, "Britain and the EU rebuild ties after Brexit", 18, INK)
# divide line the handshake bridges
for yy in range(206, 344, 14):
    d.line([(512, yy), (512, yy + 8)], fill=GREY, width=3)
# EU stars circle (left)
d.ellipse([98, 220, 202, 324], fill=BLUE, outline=NAVY, width=2)
import math as _m
for i in range(12):
    a = -_m.pi / 2 + i * _m.pi / 6
    sx = 150 + 36 * _m.cos(a)
    sy = 272 + 36 * _m.sin(a)
    d.ellipse([sx - 5, sy - 5, sx + 5, sy + 5], fill=GOLD)
text_c(d, 150, 330, "EU", 14, NAVY, bold=True)
# Union Jack hint (right)
jx0, jy0, jx1, jy1 = 822, 232, 946, 312
d.rectangle([jx0, jy0, jx1, jy1], fill=(30, 60, 130), outline=NAVY, width=2)
d.line([(jx0, jy0), (jx1, jy1)], fill=(255, 255, 255), width=12)
d.line([(jx0, jy1), (jx1, jy0)], fill=(255, 255, 255), width=12)
d.line([(jx0, jy0), (jx1, jy1)], fill=(200, 40, 40), width=5)
d.line([(jx0, jy1), (jx1, jy0)], fill=(200, 40, 40), width=5)
d.rectangle([(jx0 + jx1) // 2 - 10, jy0, (jx0 + jx1) // 2 + 10, jy1], fill=(255, 255, 255))
d.rectangle([jx0, (jy0 + jy1) // 2 - 10, jx1, (jy0 + jy1) // 2 + 10], fill=(255, 255, 255))
d.rectangle([(jx0 + jx1) // 2 - 4, jy0, (jx0 + jx1) // 2 + 4, jy1], fill=(200, 40, 40))
d.rectangle([jx0, (jy0 + jy1) // 2 - 4, jx1, (jy0 + jy1) // 2 + 4], fill=(200, 40, 40))
text_c(d, 884, 330, "UK", 14, NAVY, bold=True)
# handshake: two sleeves meeting in clasped hands
d.line([(300, 306), (500, 276)], fill=NAVY2, width=48)
d.line([(724, 306), (524, 276)], fill=RED, width=48)
d.rounded_rectangle([468, 252, 556, 300], radius=16, fill=(222, 184, 138), outline=(170, 130, 90), width=2)
d.rounded_rectangle([492, 258, 556, 294], radius=12, fill=(205, 168, 122))
for fy in (266, 276, 286):
    d.line([(500, fy), (548, fy)], fill=(170, 130, 90), width=2)


# ---- story grid: 2 rows x 4 cells, all 8 remaining stories ----
CELL_W, CELL_H, GAP = 239, 308, 12
COL_X = [16, 267, 518, 769]
ROW_Y = [368, 688]


def cell(x, y, accent, title, sub, draw):
    panel(d, [x, y, x + CELL_W, y + CELL_H])
    d.rectangle([x + 10, y, x + CELL_W - 10, y + 6], fill=accent)
    cx, cy = x + CELL_W // 2, y + 82
    draw(cx, cy)
    ty = text_block(d, cx, y + 158, title, 21, NAVY, True, CELL_W - 24, leading=25)
    text_block(d, cx, ty + 6, sub, 15, INK, False, CELL_W - 24, leading=19)


def pic_missile(cx, cy):
    d.line([(cx - 80, cy + 56), (cx - 40, cy + 44), (cx, cy + 58), (cx + 40, cy + 46), (cx + 80, cy + 56)], fill=GREY, width=3)
    for i, r in enumerate((4, 6, 8, 10, 12)):
        t = i / 4
        px = cx - 70 + t * 70
        py = cy + 42 - t * 52 + 8 * _m.sin(t * 3)
        d.ellipse([px - r, py - r, px + r, py + r], fill=GOLD if i % 2 else (230, 120, 40))
    d.polygon([(cx + 8, cy - 12), (cx + 52, cy - 52), (cx + 62, cy - 40), (cx + 22, cy + 4)], fill=RED)
    d.polygon([(cx + 52, cy - 52), (cx + 62, cy - 40), (cx + 58, cy - 30)], fill=(255, 255, 255))


def pic_scales(cx, cy):
    d.line([(cx, cy - 52), (cx, cy + 48)], fill=NAVY, width=6)
    d.line([(cx - 56, cy - 44), (cx + 56, cy - 44)], fill=NAVY, width=5)
    d.ellipse([cx - 8, cy - 60, cx + 8, cy - 44], fill=GOLD)
    for sx in (cx - 56, cx + 56):
        d.line([(sx, cy - 44), (sx, cy - 8)], fill=NAVY, width=3)
        d.pieslice([sx - 30, cy - 8, sx + 30, cy + 22], 0, 180, fill=GOLD, outline=NAVY)
        d.line([(sx - 30, cy + 7), (sx + 30, cy + 7)], fill=NAVY, width=2)
    d.rectangle([cx - 26, cy + 48, cx + 26, cy + 54], fill=NAVY)


def pic_datacentre(cx, cy):
    d.rectangle([cx - 58, cy - 42, cx + 58, cy + 52], fill=NAVY2, outline=NAVY, width=2)
    for r in range(3):
        for c in range(4):
            d.rectangle([cx - 44 + c * 24, cy - 28 + r * 22, cx - 30 + c * 24, cy - 14 + r * 22], fill=SKY)
    ox, oy, r = cx + 34, cy + 30, 30
    pts = []
    for i in range(8):
        a = _m.pi / 8 + i * _m.pi / 4
        pts.append((ox + r * _m.cos(a), oy + r * _m.sin(a)))
    d.polygon(pts, fill=RED, outline=(255, 255, 255), width=2)
    d.rectangle([ox - 16, oy - 4, ox + 16, oy + 4], fill=(255, 255, 255))


def pic_markets(cx, cy):
    d.line([(cx - 70, cy + 50), (cx - 70, cy - 50)], fill=INK, width=3)
    d.line([(cx - 70, cy + 50), (cx + 75, cy + 50)], fill=INK, width=3)
    for bx, bh in ((-52, 26), (-18, 18), (16, 10)):
        d.rectangle([cx + bx, cy + 50 - bh, cx + bx + 22, cy + 50], fill=GREY)
    d.line([(cx - 62, cy - 38), (cx - 20, cy - 8), (cx + 18, cy - 22), (cx + 62, cy + 28)], fill=RED, width=6)
    d.polygon([(cx + 62, cy + 28), (cx + 44, cy + 22), (cx + 58, cy + 44)], fill=RED)


cell(COL_X[0], ROW_Y[0], RED, "MISSILE HITS POLAND", "Russian strike reaches Poland", pic_missile)
cell(COL_X[1], ROW_Y[0], GOLD, "MYANMAR GENOCIDE RULING", "ICJ: Myanmar committed genocide", pic_scales)
cell(COL_X[2], ROW_Y[0], BLUE, "TRUMP vs AI DATA CENTRES", "Trump threatens tax on AI centres abroad", pic_datacentre)
cell(COL_X[3], ROW_Y[0], RED, "MARKETS SLIDE", "Tech sell-off; Anthropic shares slide", pic_markets)


def pic_summit(cx, cy):
    d.line([(cx - 78, cy + 48), (cx + 78, cy + 48)], fill=INK, width=4)
    for px, col in ((cx - 52, RED), (cx, BLUE), (cx + 52, GOLD)):
        d.line([(px, cy - 46), (px, cy + 48)], fill=INK, width=4)
        d.rectangle([px, cy - 46, px + 36, cy - 26], fill=col, outline=NAVY, width=1)
        d.rectangle([px, cy - 36, px + 36, cy - 26], fill=(255, 255, 255))


def pic_shield(cx, cy):
    for bx, bw, bh in ((-72, 34, 34), (-30, 28, 48), (6, 34, 40), (46, 26, 30)):
        d.rectangle([cx + bx, cy + 52 - bh, cx + bx + bw, cy + 52], fill=NAVY2)
        for wy in range(cy + 52 - bh + 8, cy + 48, 12):
            d.rectangle([cx + bx + 6, wy, cx + bx + 12, wy + 6], fill=SKY)
    d.polygon([(cx, cy - 52), (cx + 42, cy - 34), (cx + 42, cy + 2), (cx, cy + 30), (cx - 42, cy + 2), (cx - 42, cy - 34)], fill=BLUE, outline=GOLD, width=3)
    d.line([(cx - 18, cy - 8), (cx - 4, cy + 8), (cx + 22, cy - 22)], fill=(255, 255, 255), width=5)


def pic_ufo(cx, cy):
    for sx, sy in ((cx - 72, cy - 42), (cx + 70, cy - 48), (cx + 78, cy + 8), (cx - 76, cy + 20)):
        d.ellipse([sx - 3, sy - 3, sx + 3, sy + 3], fill=GOLD)
    d.polygon([(cx - 26, cy + 12), (cx + 26, cy + 12), (cx + 52, cy + 52), (cx - 52, cy + 52)], fill=(240, 220, 130))
    d.ellipse([cx - 58, cy - 18, cx + 58, cy + 12], fill=(150, 150, 155), outline=NAVY, width=2)
    d.pieslice([cx - 26, cy - 44, cx + 26, cy - 8], 180, 360, fill=SKY, outline=NAVY)
    for lx in (cx - 34, cx, cx + 34):
        d.ellipse([lx - 5, cy - 6, lx + 5, cy + 4], fill=GOLD)


def pic_rikers(cx, cy):
    d.rectangle([cx - 62, cy - 48, cx + 62, cy + 52], outline=NAVY, width=3)
    for bx in range(cx - 48, cx + 52, 20):
        d.line([(bx, cy - 48), (bx, cy + 52)], fill=INK, width=6)
    d.rectangle([cx - 62, cy - 48, cx + 62, cy - 38], fill=NAVY)
    d.rectangle([cx - 62, cy + 42, cx + 62, cy + 52], fill=NAVY)
    d.rounded_rectangle([cx - 16, cy + 2, cx + 16, cy + 26], radius=4, fill=GOLD, outline=NAVY, width=2)
    d.arc([cx - 10, cy - 12, cx + 10, cy + 6], 180, 360, fill=NAVY, width=4)


cell(COL_X[0], ROW_Y[1], GOLD, "SHENZHEN SUMMIT", "Trump, Xi, Putin: first three-way summit", pic_summit)
cell(COL_X[1], ROW_Y[1], BLUE, "RIYADH INTERCEPTS MISSILES", "Saudi intercepts Houthi missiles", pic_shield)
cell(COL_X[2], ROW_Y[1], SKY, "UFO FOOTAGE DECLASSIFIED", "US declassifies more UFO footage", pic_ufo)
cell(COL_X[3], ROW_Y[1], NAVY, "RIKERS TO CLOSE BY 2032", "Mamdani: close Rikers Island by 2032", pic_rikers)

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")
img.save(out_path)
print("saved", out_path, img.size, img.mode, os.path.getsize(out_path), "bytes")
