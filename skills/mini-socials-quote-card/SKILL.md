---
name: mini-socials-quote-card
description: >-
  Turn a celebrity interview video (usually a YouTube link) into a single 4:5
  "金句 card" — a sharp screenshot frame of the speaker with the quote stacked as
  dark translucent caption bars, ONE short line each, in Traditional Chinese. This
  is the 花卷（AI版）Xiaohongshu look. TRIGGER when the user, inside
  /Users/ccl/Projects/mini-socials, pastes a 名人訪談 / interview link (or names a
  person) and wants a 金句圖 / quote card / 名人金句 image in the stacked-subtitle
  style. SKIP for: a multi-page carousel (mini-socials-carousel-pipeline), captioning
  the SOURCE video itself (mini-socials-video-caption), or pushing an already-built
  asset (mini-socials-publish-queue).
---

# mini-socials-quote-card

Make ONE 4:5 (1080×1350) still: interview frame + the 金句 laid out as stacked
dark caption bars, one line per bar, white centred CJK text. Reference look =
花卷（AI版）. Static PIL image, no video render.

## Step 1 — Find the interview (搜 名人訪談)

Take a URL if the user gives one, else search:

```bash
yt-dlp "ytsearch8:<名人 英文名> interview" --flat-playlist \
  --print "%(title)s  |  %(webpage_url)s"
```

Pick the clip with a quotable, self-contained soundbite (money / career / mindset
lines travel best — 「我曾經…」「後來我…」「第一步就係…」).

## Step 2 — Screenshot the 金句 frame (keep it SHARP)

Grab the video **at the highest resolution available** so the background photo stays
clear — a low-res source upscales into a blurry card. YouTube now 403s the DASH
fragments on the default client (SABR experiment), so pass the `player_client`
fallback or it silently drops to 360p:

```bash
yt-dlp -f "bv*[height<=1080]+ba/b[height<=1080]/18/best" -o interview.mp4 \
  --extractor-args "youtube:player_client=android,web_safari,tv" "<url>"

# native-res frame at the punchline (scrub to it, or transcribe with local whisper-cli
# via --write-auto-subs first to get exact timestamps of the good line)
ffmpeg -ss 00:03:12 -i interview.mp4 -frames:v 1 -q:v 2 frame.png
```

Pick a frame where the speaker's **head sits in the upper third** — the caption bars
are bottom-anchored and fill the lower part, so a high head keeps the face uncovered.

## Step 3 — Compose the 4:5 card

Author each line SHORT and hard-wrapped yourself (the robust way to honour the
typography gates): no orphan tail line, never split a cohesive word/term, full-width
punctuation （，。：；「」）. Output must be **Traditional Chinese** — convert any
Simplified source quote, keep HK register if you rephrase (俾, not 畀).

Edit the `LINES` list at the top of `compose.py`, then:

```bash
python3 compose.py   # frame.png -> quote_card.png
```

Key knobs (top of `compose.py`):
- `LINES` — one caption bar each; the stack is **bottom-anchored** so it never rides
  up over the speaker's head. `compose.py` prints a WARN if too many lines reach the
  head zone (< 0.42H) — trim lines or shrink `FONT_SIZE` if so.
- `CROP_X` — horizontal pan of the crop (0=left … 1=right) to keep the face centred.
- No platform chrome is drawn. The 花卷 grid's red `置頂` badge is Xiaohongshu's own
  "pinned post" UI, added by the app on your profile — never bake it into the image.

## After

- Eyeball the render: background sharp, bars clear of the head, no line re-wrapping,
  no orphan tail, punctuation full-width. Fix `LINES` / `CROP_X` and re-run if any bites.
- Write a short Cantonese caption + CTA, then push via **mini-socials-publish-queue**
  (`topic_tag` mandatory). This is a single image, not a carousel.

## Notes

- One frame + stacked bars only — the whole point is zero manual capscreen/排版
  beyond picking the line. Fully scriptable end-to-end from a link.
- Real footage / real person only — use the actual interview frame, never an AI
  render of the celebrity.
