"""short-14: Can your boss make you take a polygraph? (US)"""
import math
from PIL import Image, ImageDraw
from sam5 import *
from s13 import ill, chair_spike

VOICE = "v14.raw"; TOTAL = 42.9

def office(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(203, 213, 225))
    d.rectangle((0, 0, W, 760), fill=(226, 232, 240))
    d.rounded_rectangle((80, 80, 420, 380), radius=12, fill=(186, 230, 253), outline=(148, 163, 184), width=8)  # window
    d.rectangle((0, 760, W, 1260), fill=(120, 113, 108)); d.rectangle((0, 760, W, 790), fill=(87, 83, 78))
    d.rounded_rectangle((90, 470, 520, 760), radius=14, fill=(30, 41, 59)); d.rectangle((280, 760, 330, 800), fill=(30, 41, 59))
    d.rounded_rectangle((115, 495, 495, 735), radius=8, fill=(96, 165, 250))
    for k in range(4): d.rectangle((140, 520 + k * 50, 470 - k * 40, 540 + k * 50), fill=(219, 234, 254))
    # mug: hot, then cold
    cold = lt > 6.3
    mc = (147, 197, 253) if cold else (220, 38, 38)
    d.rounded_rectangle((590, 830, 730, 1000), radius=18, fill=mc); d.arc((710, 870, 780, 950), 270, 90, fill=mc, width=16)
    if not cold:
        for k in range(3):
            a = (lt * 1.3 + k * .3) % 1; d.arc((605 + k * 38, 740 - a * 70, 645 + k * 38, 820 - a * 70), 200, 340, fill=(148, 163, 184), width=6)
    else:
        u = ease((lt - 6.3) / 0.4); cx, cy, r = 660, 740, 50 * u
        for k in range(3):
            a = k * math.pi / 3
            d.line([(cx - math.cos(a) * r, cy - math.sin(a) * r), (cx + math.cos(a) * r, cy + math.sin(a) * r)], fill=(59, 130, 246), width=8)
    # manager leaning in from the right
    lean = ease(lt / 1.0) * 40
    person(d, 860 - lean, 420, 1.15, shirt=(71, 85, 105), skin=(230, 190, 160), hair=(40, 40, 46))
    if lt > 1.6:
        u = ease((lt - 1.6) / 0.4)
        lay = Image.new("RGBA", S.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
        g.rounded_rectangle((130, 120 + 20 * (1 - u), 760, 400 + 20 * (1 - u)), radius=36, fill=(255, 255, 255, int(250 * u)))
        g.polygon([(640, 395), (720, 395), (740, 470)], fill=(255, 255, 255, int(250 * u)))
        g.text((170, 160), "\"Quick favour...", font=F("ExtraBold", 50), fill=INK + (int(255 * u),))
        if lt > 2.8: g.text((170, 240), "could you take a lie", font=F("Bold", 44), fill=(51, 65, 85, 255))
        if lt > 3.4: g.text((170, 300), "detector test?\"", font=F("Bold", 44), fill=(51, 65, 85, 255))
        S.alpha_composite(lay)

def myth(img, t, lt):
    sam_close(img, t, lt, expr="talk" if lt < 5.2 else "serious")
    card(img, (90, 290, 990, 540), "Any employer can make", "you take a polygraph (US)", u=(lt - 0.9) / 0.4, title_size=50)
    pill(img, W / 2, 230 - 20, "MYTH OR FACT?", bg=BLUE, size=46, u=lt / 0.3)
    stamp(img, "MYTH", 540, 470, RED, (lt - 5.3) / 0.5, size=150)

def law(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(22, 33, 58))
    d.rounded_rectangle((180, 110, 900, 960), radius=26, fill=(248, 250, 252))
    d.text((540, 180), "FEDERAL LAW (US)", font=F("ExtraBold", 40), fill=(37, 99, 235), anchor="ma")
    for k, ln in enumerate(["Employee", "Polygraph", "Protection Act"]):
        d.text((540, 260 + k * 82), ln, font=F("ExtraBold", 70), fill=INK, anchor="ma")
    d.text((540, 530), "(EPPA, 1988)", font=F("SemiBold", 40), fill=(100, 116, 139), anchor="ma")
    for k in range(5): d.rectangle((260, 620 + k * 50, 820 - (k % 3) * 90, 638 + k * 50), fill=(203, 213, 225))
    # shield
    u = pop((lt - 0.8) / 0.5); s = max(0.01, u)
    cx, cy = 780, 900
    d.polygon([(cx, cy - 110 * s), (cx + 95 * s, cy - 70 * s), (cx + 85 * s, cy + 40 * s), (cx, cy + 110 * s), (cx - 85 * s, cy + 40 * s), (cx - 95 * s, cy - 70 * s)], fill=BLUE)
    if s > .5: badge(d, cx, cy, True, r=int(46 * s))

def private_employers(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(186, 230, 253))
    d.rectangle((0, 900, W, 1260), fill=(148, 163, 184))
    d.rectangle((200, 220, 640, 900), fill=(71, 85, 105))
    for r_ in range(7):
        for c in range(4): d.rectangle((235 + c * 100, 260 + r_ * 85, 295 + c * 100, 320 + r_ * 85), fill=(253, 230, 138) if (r_ + c) % 3 else (226, 232, 240))
    d.rounded_rectangle((230, 150, 610, 220), radius=10, fill=(30, 41, 59)); d.text((420, 185), "PRIVATE COMPANY", font=F("ExtraBold", 34), fill=WHITE, anchor="mm")
    u = pop((lt - 0.4) / 0.5); s = max(0.01, u); cx, cy, r = 800, 470, 170 * s
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=WHITE, outline=RED, width=int(26 * s))
    if s > .4:
        d.rounded_rectangle((cx - 80 * s, cy - 40 * s, cx + 80 * s, cy + 50 * s), radius=int(10 * s), fill=(30, 41, 59))
        wave_line(d, (cx - 60 * s, cy - 20 * s, cx + 60 * s, cy + 30 * s), t, amp=.3, col=ACCENT)
        d.line([(cx - r * .7, cy - r * .7), (cx + r * .7, cy + r * .7)], fill=RED, width=int(26 * s))
    card(S, (70, 990, 770, 1150), "Before hiring", "or on the job", u=(lt - 3.6) / 0.3, title_size=48, icon=lambda dd, x, y: badge(dd, x, y, False))

def tile_icon(d, kind, cx, cy):
    if kind == "gov":
        d.polygon([(cx - 70, cy - 30), (cx, cy - 75), (cx + 70, cy - 30)], fill=INK)
        for k in range(4): d.rectangle((cx - 58 + k * 36, cy - 25, cx - 44 + k * 36, cy + 45), fill=INK)
        d.rectangle((cx - 75, cy + 45, cx + 75, cy + 60), fill=INK)
    elif kind == "sec":
        d.polygon([(cx, cy - 75), (cx + 62, cy - 48), (cx + 55, cy + 25), (cx, cy + 72), (cx - 55, cy + 25), (cx - 62, cy - 48)], fill=BLUE)
    elif kind == "pharma":
        d.rounded_rectangle((cx - 80, cy - 34, cx + 80, cy + 34), radius=34, fill=(244, 63, 94)); d.rounded_rectangle((cx, cy - 34, cx + 80, cy + 34), radius=34, fill=WHITE, outline=(244, 63, 94), width=6)
    else:
        d.ellipse((cx - 55, cy - 60, cx + 35, cy + 30), outline=INK, width=14); d.line([(cx + 22, cy + 18), (cx + 70, cy + 66)], fill=INK, width=20)

def exceptions(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(22, 33, 58))
    d.text((540, 70), "The main exceptions", font=F("ExtraBold", 66), fill=WHITE, anchor="ma")
    items = [("gov", "Government jobs", 1.1), ("sec", "Security firms", 2.7), ("pharma", "Drug companies", 4.1), ("theft", "Some theft", 5.4)]
    for k, (kind, lab, t0) in enumerate(items):
        u = (lt - t0) / 0.35
        if u <= 0: continue
        x = 70 + (k % 2) * 480; y = 190 + (k // 2) * 410
        lay = Image.new("RGBA", S.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay); dy = 30 * (1 - ease(u))
        g.rounded_rectangle((x, y + dy, x + 460, y + 380 + dy), radius=30, fill=(248, 250, 252, 255))
        tile_icon(g, kind, x + 230, y + 150 + dy)
        g.text((x + 230, y + 260 + dy), lab, font=F("ExtraBold", 44), fill=INK, anchor="ma")
        if kind == "theft": g.text((x + 230, y + 314 + dy), "investigations", font=F("ExtraBold", 40), fill=INK, anchor="ma")
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * ease(u)))); S.alpha_composite(lay)
    pill(S, 540, 1030, "under strict rules", bg=AMBER, fg=INK, size=50, u=(lt - 6.2) / 0.3)

def rights(S, t, lt):
    chair_spike(S, t, 0.0)
    d = ImageDraw.Draw(S)
    d.rectangle((0, 0, W, 470), fill=(17, 26, 46))
    card(S, (90, 60, 990, 230), "Written notice", "before the test", u=(lt - 0.8) / 0.35, icon=lambda dd, x, y: badge(dd, x, y, True), title_size=52)
    card(S, (90, 260, 990, 430), "You can stop the test", None, u=(lt - 2.0) / 0.35, icon=lambda dd, x, y: badge(dd, x, y, True), title_size=52)

def disclaimer(img, t, lt):
    sam_close(img, t, lt, expr="serious")
    pill(img, W / 2, 300, "General information", bg=(51, 65, 85), size=50, u=lt / 0.3)
    pill(img, W / 2, 420, "not legal advice (US)", bg=(51, 65, 85), size=50, u=(lt - 0.6) / 0.3)

def intro(img, t, lt):
    def top(img, t, lt):
        card(img, (160, 360, 920, 600), "Sam", "your polygraph guide", u=(lt - 0.3) / 0.4, color=BLUE, tcol=WHITE, title_size=80)
    sam_desk(img, t, lt, expr="talk", wave=lt < 2.2, top=top)

def cta(img, t, lt):
    def top(img, t, lt):
        card(img, (110, 340, 970, 600), "Want the full guide?", "Link in bio", u=lt / 0.4, title_size=60)
    sam_desk(img, t, lt, expr="smile", top=top)

SCENES = [
    (0.0, 8.4, ill(office)),
    (8.4, 11.1, intro),
    (11.1, 17.35, myth),
    (17.35, 20.6, ill(law)),
    (20.6, 26.4, ill(private_employers)),
    (26.4, 33.9, ill(exceptions)),
    (33.9, 37.75, ill(rights)),
    (37.75, 40.45, disclaimer),
    (40.45, TOTAL, cta),
]
CAPS = [
    (0.0, 2.9, "Monday morning. Your manager leans over:"),
    (2.9, 6.2, "\"Quick favour... could you take a lie detector test?\""),
    (6.2, 8.35, "Your coffee goes cold."),
    (8.4, 11.05, "Hi, I'm Sam, your polygraph guide."),
    (11.1, 16.35, "Myth or fact? In the US, any employer can make you take a polygraph."),
    (16.35, 17.3, "Myth."),
    (17.35, 20.6, "A federal law, the Employee Polygraph Protection Act,"),
    (20.6, 24.15, "bars most private employers from using lie detector tests,"),
    (24.15, 26.35, "before hiring or on the job."),
    (26.4, 30.4, "The main exceptions: government jobs, security firms,"),
    (30.4, 33.85, "drug companies, and some theft investigations, under strict rules."),
    (33.9, 37.7, "And even then, you get written notice, and you can stop the test."),
    (37.75, 40.4, "This is general information, not legal advice."),
    (40.45, TOTAL, "Want the full guide? Link in bio."),
]
