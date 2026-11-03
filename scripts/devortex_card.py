"""Stand-in for scripts/devortex_card.py (missing from the repo).
Recreates the 28 Oct card layout with fonts available here (Inter + DejaVu Sans Mono)."""
import json, sys
from PIL import Image, ImageDraw, ImageFont

W = H = 1080
M = 96
BG = (0, 0, 0)
FG = (245, 245, 245)
MUTED = (150, 150, 155)
LINE = (45, 45, 48)
PANEL = (14, 14, 16)
BLUE = (88, 166, 255)
SEV = {"CRITICAL": (255, 107, 107), "HIGH": (255, 168, 76), "MEDIUM": (240, 200, 80), "INFO": (120, 180, 255)}

INTER = "/usr/share/fonts/opentype/inter/"
def f(name, size): return ImageFont.truetype(INTER + name, size)
def mono(size): return ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf", size)

def wrap(draw, text, font, width):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= width: cur = t
        else: lines.append(cur); cur = w
    lines.append(cur)
    return lines

def spaced(draw, xy, text, font, fill, track=2):
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + track
    return x

def spaced_len(draw, text, font, track=2):
    return sum(draw.textlength(c, font=font) + track for c in text) - track

def render(s, date_label, mark_path, out):
    im = Image.new("RGB", (W, H), BG)
    d = ImageDraw.Draw(im)
    mark = Image.open(mark_path).convert("RGBA")
    mark.thumbnail((72, 72))
    im.paste(mark, (M, 96), mark)
    d.text((M + 96, 114), "Devortex Solutions", font=f("Inter-SemiBold.otf", 34), fill=FG)
    df = mono(26)
    d.text((W - M - d.textlength(date_label, font=df), 120), date_label, font=df, fill=MUTED)
    d.line([(M, 204), (W - M, 204)], fill=LINE, width=2)

    lf = f("Inter-Medium.otf", 25)
    spaced(d, (M, 263), s["label"], lf, MUTED)
    sev = s["status"]; col = SEV.get(sev, FG)
    sf = f("Inter-Medium.otf", 26)
    tw = spaced_len(d, sev, sf) + 40
    bx0 = W - M - tw
    d.rectangle([bx0 - 4, 250, W - M, 298], outline=col, width=2)
    d.polygon([(bx0 + 14, 266), (bx0 + 21, 273), (bx0 + 14, 280), (bx0 + 7, 273)], fill=col)
    spaced(d, (bx0 + 30, 262), sev, sf, col)

    # headline: shrink until it fits in 2 lines
    for size in (84, 78, 72, 66, 60):
        hf = f("Inter-SemiBold.otf", size)
        lines = wrap(d, s["card_headline"], hf, W - 2 * M)
        if len(lines) <= 2: break
    y = 336
    for ln in lines:
        d.text((M, y), ln, font=hf, fill=FG); y += int(size * 1.15)
    y += 22
    sfnt = f("Inter-Regular.otf", 33)
    for ln in wrap(d, s["summary"], sfnt, W - 2 * M):
        d.text((M, y), ln, font=sfnt, fill=MUTED); y += 48

    y = max(y + 28, 660)
    rows = s["facts"][:3]; rh = 64
    d.rounded_rectangle([M, y, W - M, y + rh * len(rows)], radius=8, fill=PANEL, outline=LINE, width=2)
    kf = f("Inter-Medium.otf", 23); vf = mono(27)
    for i, (k, v) in enumerate(rows):
        ry = y + i * rh
        if i: d.line([(M, ry), (W - M, ry)], fill=LINE, width=2)
        spaced(d, (M + 28, ry + 21), k, kf, MUTED)
        d.text((M + 270, ry + 17), v, font=vf, fill=FG)
    by = y + rh * len(rows) + 48
    cf = f("Inter-SemiBold.otf", 30)
    cw = d.textlength(s["cta"], font=cf) + 64
    d.rounded_rectangle([M, by, M + cw, by + 72], radius=8, fill=BLUE)
    d.text((M + 32, by + 18), s["cta"], font=cf, fill=(5, 10, 20))
    im.save(out)

if __name__ == "__main__":
    stories, date_label, mark, outdir = sys.argv[1:5]
    for s in json.load(open(stories)):
        render(s, date_label, mark, f"{outdir}/{s['slug']}.png")
