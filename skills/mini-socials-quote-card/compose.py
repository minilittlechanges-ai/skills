#!/usr/bin/env python3
# mini-socials 金句 card — 4:5 stacked caption bars over an interview frame.
# Static image, no platform chrome. Background stays sharp if FRAME is 1080p+.
from PIL import Image, ImageDraw, ImageFont

# ---- EDIT ----
FRAME = "frame.png"           # high-res frame from Step 2 (1080p+ so it stays sharp)
OUT   = "quote_card.png"
LINES = [                     # author each line short: no orphan tail, keep terms whole
    "成日話自己專攻「被動收入」嘅人",
    "其實根本冇賺過真正嘅收入",
    "被動收入係 21 世紀最大嘅迷思",
    "一班喺 TikTok、YouTube 上",
    "得十二歲嘅細路呃你",
    "等你乖乖掏荷包",
]
CROP_X    = 0.5               # horizontal pan of the crop (0=left … 1=right) — keep the face centred
FONT_SIZE = 46
# --------------

W, H = 1080, 1350
BAR_H, GAP, BOTTOM = 92, 4, 90   # bar height, gap between bars, bottom margin


def font(size):
    for p in ("/System/Library/Fonts/STHeiti Medium.ttc",
              "/System/Library/Fonts/Supplemental/STHeiti Medium.ttc",
              "/System/Library/Fonts/PingFang.ttc"):
        try:
            return ImageFont.truetype(p, size)
        except OSError:
            continue
    return ImageFont.load_default()


# cover-fit the frame to 1080x1350 (LANCZOS; no visible upscaling if the source is 1080p+)
src = Image.open(FRAME).convert("RGB")
sc = max(W / src.width, H / src.height)
src = src.resize((round(src.width * sc), round(src.height * sc)), Image.LANCZOS)
x0 = round((src.width - W) * CROP_X)
card = src.crop((x0, 0, x0 + W, H))
d = ImageDraw.Draw(card, "RGBA")

# stacked caption bars, BOTTOM-anchored so they never ride up over the speaker's head
f = font(FONT_SIZE)
stack_h = len(LINES) * BAR_H + (len(LINES) - 1) * GAP
top = H - BOTTOM - stack_h
if top < H * 0.42:
    print(f"WARN: {len(LINES)} lines reach y={top} (< 0.42H) — may cover the head; "
          "trim lines or shrink FONT_SIZE/BAR_H, or use a frame with the head higher.")
for i, ln in enumerate(LINES):
    y = top + i * (BAR_H + GAP)
    d.rectangle([0, y, W, y + BAR_H], fill=(0, 0, 0, 150))
    b = d.textbbox((0, 0), ln, font=f)
    d.text(((W - (b[2] - b[0])) // 2, y + (BAR_H - (b[3] - b[1])) // 2 - b[1]),
           ln, font=f, fill=(255, 255, 255, 255))

card.save(OUT)
print("saved", OUT, card.size)
