# scheduled-posts

Media repo for the daily Devortex cybersecurity post. Same layout as
`zallomah/sentry-ops-media`, so the daily routine can point at either one.

## Layout

- `brand/` — Devortex mark (white and on-black PNGs)
- `scripts/devortex_card.py` — renders the 1080×1080 story cards
- `img/YYYY-MM-DD/<slug>.png` — rendered cards, one folder per day (created on first run)
- `log.csv` — created on first run; one row per run: date, the 5 headlines, the pick or `skip`,
  channels, post links. Checked each day so a story isn't posted twice.

## Rendering cards

```
python3 scripts/devortex_card.py <stories.json> "03 NOV 2026" brand/devortex-mark-white.png img/2026-11-03
```

Each story in the JSON needs: `slug`, `label`, `status` (CRITICAL, HIGH,
MEDIUM or INFO), `card_headline`, `summary`, `facts` (up to 3 `[key, value]`
pairs) and `cta`. Requires Pillow.

The script uses Inter and DejaVu Sans Mono from the system fonts, as a
stand-in for the brand fonts. If brand font files are added to `brand/`,
update the font paths at the top of the script.

## Image links

Images are referenced by commit, so a link never changes after posting:

```
https://raw.githubusercontent.com/zallomah/scheduled-posts/<commit SHA>/<path>
```

The repo must stay public for these links to load.
