#!/usr/bin/env python3
"""Front page of the world's news for Saturday 21 November 2026.

Pure PIL drawing, no numpy, no network. Writes one 1024x1024 PNG to
$MAKEFUN_OUTPUT_DIR/entry.png (default /output/entry.png).
"""

import math
import os
from PIL import Image, ImageDraw, ImageFont

W = H = 1024
MARGIN = 20
GUTTER = 12

NAVY = (18, 33, 58)
NAVY_DK = (10, 20, 37)
CREAM = (247, 241, 227)
CREAM_DK = (233, 224, 206)
INK = (28, 33, 43)
MUTED = (96, 96, 104)
RED = (168, 46, 46)
BLUE = (32, 74, 138)
BLUE_LT = (86, 132, 196)
GOLD = (192, 148, 58)
GREEN = (52, 104, 72)

FONT_DIR = "/usr/share/fonts/truetype/dejavu"


def font(size, bold=False, serif=False):
    """Return a DejaVu font at the given pixel size."""
    if serif:
        name = "DejaVuSerif-Bold.ttf" if bold else "DejaVuSerif.ttf"
    else:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


def text_w(draw, s, f):
    box = draw.textbbox((0, 0), s, font=f)
    return box[2] - box[0]


def center(draw, s, f, cx, y, fill):
    draw.text((cx - text_w(draw, s, f) / 2, y), s, font=f, fill=fill)


def wrap(draw, s, f, max_w):
    """Greedy word wrap to a pixel width."""
    words, lines, cur = s.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if text_w(draw, trial, f) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def fit(draw, s, max_w, max_h, start=20, min_size=12, bold=False):
    """Largest font size at which s wraps inside max_w x max_h, with its lines."""
    size = start
    while size >= min_size:
        f = font(size, bold)
        lines = wrap(draw, s, f, max_w)
        line_h = int(size * 1.28)
        if len(lines) * line_h <= max_h and all(text_w(draw, ln, f) <= max_w for ln in lines):
            return f, lines, line_h
        size -= 1
    f = font(min_size, bold)
    return f, wrap(draw, s, f, max_w), int(min_size * 1.28)


def paragraph(draw, s, x, y, max_w, max_h, start, bold=False,
              fill=INK, leading=1.28, align="left", cx=None):
    f, lines, lh = fit(draw, s, max_w, max_h, start, bold=bold)
    lh = int(f.size * leading)
    for i, ln in enumerate(lines):
        if align == "center":
            center(draw, ln, f, cx if cx is not None else x + max_w / 2, y + i * lh, fill)
        else:
            draw.text((x, y + i * lh), ln, font=f, fill=fill)
    return y + len(lines) * lh


def panel(draw, box, fill=CREAM):
    """Cream card with a hairline navy rule."""
    x0, y0, x1, y1 = box
    draw.rectangle([x0, y0, x1, y1], fill=fill, outline=NAVY, width=2)
    return box


def star(draw, cx, cy, r, fill, points=5):
    """A filled five-pointed star."""
    outer, inner = r, r * 0.42
    pts = []
    for i in range(points * 2):
        ang = -math.pi / 2 + i * math.pi / points
        rr = outer if i % 2 == 0 else inner
        pts.append((cx + rr * math.cos(ang), cy + rr * math.sin(ang)))
    draw.polygon(pts, fill=fill)


def flag_eu(draw, box):
    """EU flag: blue field with twelve gold stars in a ring."""
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=BLUE, outline=NAVY, width=2)
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    r = (y1 - y0) * 0.30
    for i in range(12):
        ang = -math.pi / 2 + i * math.pi / 6
        star(draw, cx + r * math.cos(ang), cy + r * math.sin(ang), (y1 - y0) * 0.072, GOLD)


def flag_uk(draw, box):
    """Simplified Union Jack."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    draw.rectangle(box, fill=NAVY, outline=NAVY, width=2)
    t = max(2, int(h * 0.16))
    draw.line([x0, y0, x1, y1], fill=(240, 240, 238), width=t)
    draw.line([x0, y1, x1, y0], fill=(240, 240, 238), width=t)
    draw.line([x0, y0, x1, y1], fill=RED, width=max(1, t // 3))
    draw.line([x0, y1, x1, y0], fill=RED, width=max(1, t // 3))
    draw.rectangle([(x0 + x1) / 2 - t, y0, (x0 + x1) / 2 + t, y1], fill=(240, 240, 238))
    draw.rectangle([x0, (y0 + y1) / 2 - t, x1, (y0 + y1) / 2 + t], fill=(240, 240, 238))
    draw.rectangle([(x0 + x1) / 2 - t // 2, y0, (x0 + x1) / 2 + t // 2, y1], fill=RED)
    draw.rectangle([x0, (y0 + y1) / 2 - t // 2, x1, (y0 + y1) / 2 + t // 2], fill=RED)


SKIN = (226, 184, 150)
SKIN_DK = (196, 150, 116)
SLEEVE_L = (44, 86, 150)
SLEEVE_R = (150, 52, 52)


def handshake(draw, box):
    """Two forearms meeting in a clasp over a dashed divide."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    # dashed divide the hands reach across
    for yy in range(int(y0), int(y1), 18):
        draw.line([cx, yy, cx, yy + 9], fill=(150, 142, 128), width=2)
    # forearms
    lean = (y1 - y0) * 0.30
    draw.polygon([(x0 + 5, cy - lean - 26), (cx - 46, cy - 26),
                  (cx - 46, cy + 26), (x0 + 5, cy + lean + 26)], fill=SLEEVE_L)
    draw.polygon([(x1 - 5, cy - lean - 26), (cx + 46, cy - 26),
                  (cx + 46, cy + 26), (x1 - 5, cy + lean + 26)], fill=SLEEVE_R)
    # cuffs
    draw.polygon([(cx - 74, cy - 34), (cx - 54, cy - 30), (cx - 54, cy + 30), (cx - 74, cy + 34)],
                 fill=(238, 232, 216))
    draw.polygon([(cx + 74, cy - 34), (cx + 54, cy - 30), (cx + 54, cy + 30), (cx + 74, cy + 34)],
                 fill=(238, 232, 216))
    # clasped hands
    draw.rounded_rectangle([cx - 52, cy - 30, cx + 52, cy + 28], radius=16, fill=SKIN)
    draw.rounded_rectangle([cx - 52, cy - 30, cx - 4, cy + 28], radius=14, fill=SKIN_DK)
    # thumbs crossing on top
    draw.rounded_rectangle([cx - 30, cy - 42, cx + 16, cy - 22], radius=9, fill=SKIN)
    draw.rounded_rectangle([cx - 8, cy - 44, cx + 38, cy - 24], radius=9, fill=SKIN_DK)
    # finger lines
    for i in range(3):
        y = cy - 6 + i * 12
        draw.line([cx + 2, y, cx + 44, y], fill=SKIN_DK, width=1)


def banner(draw):
    """Dark masthead naming the day."""
    draw.rectangle([0, 0, W, 98], fill=NAVY)
    draw.rectangle([0, 0, W, 5], fill=GOLD)
    draw.rectangle([0, 94, W, 98], fill=GOLD)
    f_label = font(17, True)
    draw.text((26, 26), "WORLD NEWS", font=f_label, fill=GOLD)
    draw.text((26, 54), "ONE DAY IN ONE IMAGE", font=font(11, False), fill=(196, 206, 222))
    date = "21 NOVEMBER 2026"
    f_date = font(52, True)
    center(draw, date, f_date, W / 2, 20, (252, 250, 244))
    f_day = font(15, True)
    dw = text_w(draw, "SATURDAY", f_day)
    draw.text((W - 26 - dw, 30), "SATURDAY", font=f_day, fill=(236, 232, 220))
    dw2 = text_w(draw, "NEWSPAPER OF RECORD", font(11))
    draw.text((W - 26 - dw2, 56), "NEWSPAPER OF RECORD", font=font(11), fill=(150, 166, 190))


LEAD_BOX = (20, 106, 604, 498)


def lead(draw):
    """The day's lead story: the UK and the EU shake hands."""
    x0, y0, x1, y1 = LEAD_BOX
    panel(draw, LEAD_BOX)

    f_kick = font(15, True)
    draw.text((x0 + 16, y0 + 12), "LEAD STORY", font=f_kick, fill=RED)
    kw = text_w(draw, "LEAD STORY", f_kick)
    draw.line([x0 + 22 + kw, y0 + 22, x1 - 16, y0 + 22], fill=(206, 196, 176), width=2)

    f_head = font(44, True, serif=True)
    draw.text((x0 + 16, y0 + 36), "UK\u2013EU", font=f_head, fill=NAVY)
    draw.text((x0 + 16, y0 + 86), "LANDMARK DEAL", font=f_head, fill=NAVY)

    paragraph(draw, "Britain and the EU rebuild ties after Brexit",
              x0 + 16, y0 + 146, x1 - x0 - 32, 62, 24, fill=MUTED)

    # picture area
    px0, py0, px1, py1 = x0 + 16, y0 + 216, x1 - 16, y1 - 16
    draw.rectangle([px0, py0, px1, py1], fill=(238, 231, 214))
    draw.rectangle([px0, py0, px1, py1], outline=(208, 198, 178), width=1)
    flag_eu(draw, (px0 + 14, py0 + 12, px0 + 90, py0 + 62))
    flag_uk(draw, (px1 - 90, py0 + 12, px1 - 14, py0 + 62))
    f_tag = font(13, True)
    draw.text((px0 + 98, py0 + 18), "EUROPEAN UNION", font=f_tag, fill=BLUE)
    tw = text_w(draw, "UNITED KINGDOM", f_tag)
    draw.text((px1 - 98 - tw, py0 + 18), "UNITED KINGDOM", font=f_tag, fill=NAVY)
    handshake(draw, (px0 + 34, py0 + 86, px1 - 34, py1 - 12))


# ---------------------------------------------------------------------------
# Secondary cards
# ---------------------------------------------------------------------------

def story_card(draw, box, kicker, head, caption, icon_fn, accent=RED):
    """A cream card: kicker, headline, illustration, one-line caption."""
    x0, y0, x1, y1 = box
    w, h = x1 - x0, y1 - y0
    panel(draw, box)
    f_k = font(12, True)
    draw.text((x0 + 12, y0 + 9), kicker, font=f_k, fill=accent)
    kw = text_w(draw, kicker, f_k)
    draw.line([x0 + 17 + kw, y0 + 16, x1 - 12, y0 + 16], fill=(210, 200, 180), width=1)
    head_h = int(h * 0.36)
    f_h, lines, lh = fit(draw, head, w - 24, head_h, start=25, min_size=13, bold=True)
    y = y0 + 25
    for ln in lines:
        draw.text((x0 + 12, y), ln, font=f_h, fill=NAVY)
        y += lh
    cap_top = y1 - int(h * 0.20)
    iy1 = max(y + 30, cap_top - 6)
    icon_fn(draw, (x0 + 12, y + 4, x1 - 12, iy1))
    paragraph(draw, caption, x0 + 12, cap_top, w - 24, int(h * 0.18), 12, fill=MUTED)


def icon_missile(draw, box):
    """A missile streaking down to a red impact star."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    # smoke trail
    for i in range(5):
        r = 5 + i * 2
        draw.ellipse([x1 - 26 - i * 10 - r, y0 + 8 + i * 8 - r,
                      x1 - 26 - i * 10 + r, y0 + 8 + i * 8 + r],
                     fill=(214, 206, 190))
    # body: a tail fin at top-right, nose at lower-left
    tipx, tipy = cx - 22, cy + 26
    backx, backy = cx + 26, cy - 26
    draw.line([backx, backy, tipx, tipy], fill=NAVY, width=13)
    draw.line([backx, backy, tipx, tipy], fill=(126, 138, 158), width=7)
    draw.polygon([(tipx - 4, tipy + 4), (tipx + 8, tipy - 8),
                  (tipx + 2, tipy + 14)], fill=RED)
    draw.polygon([(backx - 14, backy - 4), (backx + 6, backy + 14),
                  (backx + 14, backy - 14)], fill=RED)
    # impact burst at lower left
    star(draw, cx - 46, cy + 40, 22, (222, 126, 44), points=6)
    star(draw, cx - 46, cy + 40, 11, (250, 214, 120), points=6)


def icon_gavel(draw, box):
    """A judge's gavel above its block."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    # block
    draw.rounded_rectangle([cx - 40, cy + 26, cx + 40, cy + 44], radius=5, fill=(120, 92, 56))
    draw.rounded_rectangle([cx - 40, cy + 26, cx + 40, cy + 32], radius=4, fill=(150, 116, 74))
    # head
    draw.rounded_rectangle([cx - 34, cy - 46, cx + 6, cy - 8], radius=7, fill=(150, 116, 74))
    draw.rounded_rectangle([cx - 34, cy - 46, cx + 6, cy - 38], radius=4, fill=(178, 140, 92))
    # handle
    draw.line([cx - 4, cy - 26, cx + 44, cy + 6], fill=(120, 92, 56), width=11)
    draw.line([cx - 4, cy - 26, cx + 44, cy + 6], fill=(162, 126, 82), width=6)
    # motion arc
    draw.arc([cx - 54, cy - 58, cx + 30, cy + 18], start=200, end=310, fill=NAVY, width=2)


def icon_datacenter(draw, box):
    """Two server racks, one with a lightning bolt: AI's power draw."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
    rw, rh = 34, 13
    for side in (-1, 1):
        rx = cx + side * 38
        for i in range(3):
            ry = cy - 26 + i * 16
            draw.rectangle([rx - rw, ry, rx + rw, ry + rh], fill=NAVY,
                           outline=(70, 90, 120), width=1)
            draw.rectangle([rx - rw + 4, ry + 4, rx - rw + 10, ry + 9], fill=GREEN)
            draw.rectangle([rx - rw + 14, ry + 4, rx - rw + 20, ry + 9], fill=GOLD)
    # lightning bolt between the racks
    bolt = [(cx + 6, cy - 30), (cx - 10, cy + 2), (cx + 2, cy + 2),
            (cx - 8, cy + 30), (cx + 14, cy - 6), (cx + 2, cy - 6)]
    draw.polygon(bolt, fill=(222, 178, 48))


def icon_chart_down(draw, box):
    """Axes with a falling line and an arrow."""
    x0, y0, x1, y1 = box
    ox, oy = x0 + 12, y1 - 14
    tx, ty = x1 - 14, y0 + 10
    draw.line([ox, y0 + 6, ox, oy], fill=NAVY, width=2)
    draw.line([ox, oy, x1 - 8, oy], fill=NAVY, width=2)
    pts = [(ox + 6, y0 + 26), (ox + 46, y0 + 40), (ox + 80, y0 + 34),
           (ox + 118, y0 + 62), (tx - 6, oy - 8)]
    for i in range(len(pts) - 1):
        draw.line([pts[i], pts[i + 1]], fill=RED, width=4)
    ex, ey = pts[-1]
    draw.polygon([(ex + 8, ey + 6), (ex - 6, ey + 8), (ex, ey - 10)], fill=RED)
    for i, p in enumerate(pts[:-1]):
        draw.ellipse([p[0] - 3, p[1] - 3, p[0] + 3, p[1] + 3], fill=RED)


def icon_summit(draw, box):
    """A round table with three seated delegates."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2, (y0 + y1) / 2 + 8
    draw.ellipse([cx - 58, cy - 20, cx + 58, cy + 22], fill=(206, 196, 176),
                 outline=NAVY, width=2)
    draw.ellipse([cx - 58, cy - 26, cx + 58, cy + 10], fill=CREAM_DK,
                 outline=NAVY, width=2)
    for ang, col in ((-1.6, BLUE), (1.57, RED), (3.1, GREEN)):
        sx = cx + int(34 * (1 if ang < 3 else -1)) if abs(ang) < 3 else cx
        px = cx + int(46 * __import__("math").cos(ang))
        py = cy - 34 + int(10 * __import__("math").sin(ang))
        draw.ellipse([px - 7, py - 7, px + 7, py + 7], fill=SKIN)
        draw.polygon([(px - 10, py + 4), (px + 10, py + 4),
                      (px + 7, py + 20), (px - 7, py + 20)], fill=col)


def icon_shield(draw, box):
    """A shield deflecting incoming missiles: an intercepted salvo."""
    x0, y0, x1, y1 = box
    cx, cy = (x0 + x1) / 2 - 16, (y0 + y1) / 2
    # shield
    sh = [(cx - 26, cy - 30), (cx + 26, cy - 30), (cx + 26, cy + 4),
          (cx, cy + 30), (cx - 26, cy + 4)]
    draw.polygon(sh, fill=BLUE, outline=NAVY)
    draw.line([cx, cy - 22, cx, cy + 20], fill=(196, 214, 236), width=3)
    draw.line([cx - 16, cy - 6, cx + 16, cy - 6], fill=(196, 214, 236), width=3)
    # incoming missiles from the right, stopped short
    for i, yy in enumerate((cy - 24, cy, cy + 24)):
        sx, sy = x1 - 22, yy
        draw.line([sx, sy, sx - 30, sy], fill=RED, width=4)
        draw.polygon([(sx - 30, sy - 5), (sx - 30, sy + 5), (sx - 40, sy)], fill=RED)
        star(draw, sx - 34, sy, 5, (250, 200, 90), points=4)


# ---------------------------------------------------------------------------
# Layout of the day's seven stories
# ---------------------------------------------------------------------------

LEAD = LEAD_BOX                      # UK-EU deal (left, tall)
POLAND = (612, 106, 1004, 498)       # Russian missile hits Poland (right)
ROW_A_Y = (506, 744)                 # three across
ROW_B_Y = (752, 1004)                # two wide


def draw_all(draw):
    banner(draw)
    lead(draw)

    # right column top: the strike on Poland
    story_card(draw, POLAND, "EUROPE",
               "Russian Missile Hits Poland",
               "A strike on Polish soil rattles NATO.",
               icon_missile, accent=RED)

    # bottom band, top row of three
    ay0, ay1 = ROW_A_Y
    story_card(draw, (20, ay0, 340, ay1), "JUSTICE",
               "ICJ Genocide Ruling",
               "UN court condemns Myanmar over the Rohingya.",
               icon_gavel, accent=BLUE)
    story_card(draw, (352, ay0, 672, ay1), "TECHNOLOGY",
               "Trump v. AI Data Centres",
               "Washington moves against the AI power build-out.",
               icon_datacenter, accent=GREEN)
    story_card(draw, (684, ay0, 1004, ay1), "MARKETS",
               "Markets Slide",
               "Global stocks fall on fresh economic jitters.",
               icon_chart_down, accent=RED)

    # bottom band, row of two
    by0, by1 = ROW_B_Y
    story_card(draw, (20, by0, 506, by1), "ASIA",
               "Shenzhen Summit",
               "Leaders gather in China's tech hub for trade talks.",
               icon_summit, accent=BLUE)
    story_card(draw, (518, by0, 1004, by1), "MIDDLE EAST",
               "Riyadh Intercepts Missiles",
               "Air defences down a salvo over the Saudi capital.",
               icon_shield, accent=RED)

    # footer rule + dateline
    draw.line([20, 1012, W - 20, 1012], fill=NAVY, width=2)
    f = font(11, True)
    draw.text((20, 1014 - 2), "THE WORLD, SATURDAY 21 NOVEMBER 2026", font=f, fill=NAVY)
    tag = "ALL EVENTS OF THE DAY, ONE PAGE"
    draw.text((W - 20 - text_w(draw, tag, f), 1012), tag, font=f, fill=MUTED)


def main():
    img = Image.new("RGB", (W, H), CREAM)
    draw = ImageDraw.Draw(img)
    draw_all(draw)
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    img.save(path, "PNG", optimize=True)
    print(f"wrote {path} {os.path.getsize(path)} bytes")


if __name__ == "__main__":
    main()
