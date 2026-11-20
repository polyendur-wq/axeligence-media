"""Covers for short-15/16 in the cover.py style (big topic text + Sam surprised at the desk)."""
import math
from PIL import Image, ImageDraw
import make_short as m
from make_short import F, W, H, WHITE, ACCENT, BLUE, draw_mark
import look3 as L3
RED = (239, 68, 68); AMBER = (245, 177, 66)

def cover(kicker, lines, accent_idx, out, kbg=BLUE, kfg=WHITE, fixed=None):
    img = m.background(0.8); d = ImageDraw.Draw(img)
    draw_mark(img, 70, 300, 70); d.text((160, 312), "Axeligence", font=F("ExtraBold", 44), fill=WHITE)
    f = F("ExtraBold", 50); tw = f.getlength(kicker)
    d.rounded_rectangle((70, 410, 70 + tw + 60, 490), radius=40, fill=kbg); d.text((100, 423), kicker, font=f, fill=kfg)
    y = 525
    for i, ln in enumerate(lines):
        size = fixed or (150 if len(ln) <= 11 else 122)
        d.text((64, y), ln, font=F("ExtraBold", size), fill=ACCENT if i in accent_idx else WHITE)
        y += int(size * 1.08)
    body = L3.body(0.7); head = L3.head(0.55, "surprised"); cx = 720
    img.alpha_composite(body, (cx - body.width // 2, 1300)); img.alpha_composite(head, (cx - head.width // 2, 1030))
    d = ImageDraw.Draw(img)
    d.rectangle((0, 1560, W, H), fill=(46, 37, 32)); d.rectangle((0, 1560, W, 1578), fill=(70, 56, 46))
    d.rounded_rectangle((60, 1470, 400, 1575), radius=14, fill=(20, 22, 28)); d.rectangle((60, 1470, 400, 1486), fill=(40, 44, 54))
    for k in range(5): d.ellipse((90 + k * 58, 1515, 118 + k * 58, 1543), fill=(60, 64, 76))
    d.ellipse((345, 1512, 370, 1537), fill=(34, 197, 94))
    pts = [(80 + i * 6, 1450 - 18 * math.sin(i * 0.5) * (2.2 if 22 < i < 30 else 0.7)) for i in range(52)]
    d.line(pts, fill=RED, width=6)
    img.convert("RGB").save(out, quality=92)

if __name__ == "__main__":
    cover("QUICK QUIZ", ["HOW LONG IS", "A CBP", "POLYGRAPH?"], [2], "cover-15-cbp-quiz.jpg", kbg=AMBER, kfg=(26, 26, 32))
    cover("THE ONE MISTAKE", ["\"IT'S TOO", "SMALL TO", "MENTION\""], [2], "cover-16-one-mistake.jpg", kbg=RED, fixed=118)
