# mini-socials-quote-card

A Claude Code skill: turn a celebrity interview video (usually a YouTube link) into
a single **4:5 「金句 card」** — a sharp screenshot frame of the speaker with the quote
stacked as dark caption bars, one short line each, in Traditional Chinese.

This is the 花卷（AI版）Xiaohongshu look, fully scriptable end-to-end from a link:
zero manual capscreen / 排版 beyond picking the line.

## Files

- `SKILL.md` — the skill (3 steps: search → screenshot the 金句 frame → compose).
- `compose.py` — the PIL composer. Edit `LINES` at the top, run `python3 compose.py`.

## Quick use

```bash
# 1. get a sharp frame at the punchline
yt-dlp -f "bv*[height<=1080]+ba/b[height<=1080]/18/best" -o interview.mp4 \
  --extractor-args "youtube:player_client=android,web_safari,tv" "<url>"
ffmpeg -ss 00:03:12 -i interview.mp4 -frames:v 1 -q:v 2 frame.png

# 2. edit LINES in compose.py, then
python3 compose.py            # frame.png -> quote_card.png
```

Requires `yt-dlp`, `ffmpeg`, and Python `Pillow`.

## Design rules baked in

- **No platform chrome** — the red `置頂` badge is Xiaohongshu's own "pinned post" UI,
  never baked into the image.
- **Sharp background** — pull the highest-res frame; the composer LANCZOS-fits it.
- **Head stays clear** — caption bars are bottom-anchored; a WARN fires if too many
  lines reach the head zone.
- **Traditional Chinese**, full-width punctuation, no orphan tail line, no split terms.
