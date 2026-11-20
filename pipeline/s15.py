"""short-15: How long does a CBP polygraph take? (QUIZ format)"""
import math
from PIL import Image, ImageDraw
from sam5 import *
from s13 import ill, chair_spike

VOICE = "v15.raw"; TOTAL = 38.5

# ---------- shared pieces (also used by s16) ----------
def table_scene(S, t, lt, wall=(203, 213, 225), bubble=None, bubble_t=0.0, cand_bubble=None, cand_t=0.0, sheet=True):
    """Pre-test interview: examiner (left) and candidate (right) at a table."""
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=wall)
    d.rectangle((0, 0, W, 120), fill=tuple(max(0, c - 18) for c in wall))
    d.rounded_rectangle((760, 150, 1000, 390), radius=10, fill=(241, 245, 249), outline=(148, 163, 184), width=6)  # wall clock frame
    clock(d, 880, 270, 90, 9, 10 + int(lt * 2) % 60)
    person(d, 260, 520, 1.05, shirt=(30, 41, 59), skin=(214, 170, 135), hair=(60, 60, 66))   # examiner
    person(d, 820, 560, 1.05, shirt=(100, 116, 139), skin=(230, 190, 160), hair=(92, 64, 40))  # candidate
    d.rectangle((0, 900, W, 1260), fill=(120, 113, 108)); d.rounded_rectangle((60, 860, 1020, 940), radius=16, fill=(87, 70, 58))
    if sheet:
        d.polygon([(330, 870), (560, 870), (580, 905), (310, 905)], fill=(248, 250, 252))
        for k in range(3): d.line([(350 + k * 8, 880 + k * 8), (520 + k * 8, 880 + k * 8)], fill=(148, 163, 184), width=4)
    if bubble and lt > bubble_t:
        speech(S, (60, 150, 700, 400), bubble, (lt - bubble_t) / 0.35, tail=(250, 420))
    if cand_bubble and lt > cand_t:
        speech(S, (380, 170, 1020, 420), cand_bubble, (lt - cand_t) / 0.35, tail=(800, 440))

def speech(S, box, lines, u, tail):
    if u <= 0: return
    u = ease(u); x0, y0, x1, y1 = box; dy = 20 * (1 - u)
    lay = Image.new("RGBA", S.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
    g.rounded_rectangle((x0, y0 + dy, x1, y1 + dy), radius=36, fill=(255, 255, 255, 250))
    cx = (x0 + x1) / 2
    g.polygon([(tail[0] - 40, y1 - 4 + dy), (tail[0] + 40, y1 - 4 + dy), (tail[0], tail[1] + dy)], fill=(255, 255, 255, 250))
    n = len(lines); lh = 62
    for k, ln in enumerate(lines):
        g.text((cx, (y0 + y1) / 2 - lh * n / 2 + k * lh + dy), ln, font=F("ExtraBold" if k == 0 else "Bold", 48), fill=INK + (255,), anchor="ma")
    lay.putalpha(lay.getchannel("A").point(lambda v: int(v * u))); S.alpha_composite(lay)

def chip(S, x, y, num, text, u, col=BLUE):
    if u <= 0: return
    u = ease(u); lay = Image.new("RGBA", S.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay); dy = 24 * (1 - u)
    g.rounded_rectangle((x, y + dy, x + 920, y + 120 + dy), radius=30, fill=(248, 250, 252, 255))
    g.ellipse((x + 22, y + 18 + dy, x + 106, y + 102 + dy), fill=col + (255,))
    g.text((x + 64, y + 60 + dy), num, font=F("ExtraBold", 50), fill=WHITE, anchor="mm")
    g.text((x + 130, y + 32 + dy), text, font=F("ExtraBold", 48), fill=INK + (255,))
    lay.putalpha(lay.getchannel("A").point(lambda v: int(v * u))); S.alpha_composite(lay)

def intro(img, t, lt):
    def top(img, t, lt):
        card(img, (160, 360, 920, 600), "Sam", "your polygraph guide", u=(lt - 0.3) / 0.4, color=BLUE, tcol=WHITE, title_size=80)
    sam_desk(img, t, lt, expr="talk", wave=lt < 2.2, top=top)

def cta(img, t, lt):
    def top(img, t, lt):
        card(img, (110, 340, 970, 600), "Want the full guide?", "Link in bio", u=lt / 0.4, title_size=60)
    sam_desk(img, t, lt, expr="smile", top=top)

# ---------- short-15 scenes ----------
def tomorrow(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(254, 243, 199))
    d.rectangle((0, 860, W, 1260), fill=(180, 130, 90)); d.rectangle((0, 860, W, 890), fill=(150, 105, 70))
    # wall calendar
    d.rounded_rectangle((120, 110, 600, 700), radius=24, fill=WHITE, outline=(203, 213, 225), width=6)
    d.rounded_rectangle((120, 110, 600, 230), radius=24, fill=RED); d.rectangle((120, 200, 600, 230), fill=RED)
    d.text((360, 140), "TOMORROW", font=F("ExtraBold", 56), fill=WHITE, anchor="ma")
    for r in range(4):
        for c in range(5):
            x, y = 160 + c * 86, 270 + r * 100
            d.rounded_rectangle((x, y, x + 66, y + 74), radius=10, fill=(241, 245, 249))
    u = pop((lt - 0.4) / 0.5); s = max(0.01, u)
    d.ellipse((332 - 70 * s, 470 - 64 * s, 332 + 112 * s, 470 + 120 * s), outline=BLUE, width=max(1, int(12 * s)))
    if s > .6:
        d.rounded_rectangle((150, 610, 570, 680), radius=14, fill=(219, 234, 254))
        d.text((360, 645), "CBP polygraph", font=F("ExtraBold", 42), fill=(30, 58, 138), anchor="mm")
    # person at the table, coffee, looking at calendar
    person(d, 800, 560, 1.05, shirt=(71, 85, 105), skin=(214, 170, 135), hair=(40, 40, 46))
    d.rounded_rectangle((560, 900, 1040, 960), radius=14, fill=(120, 80, 50))
    d.rounded_rectangle((620, 800, 720, 900), radius=14, fill=BLUE); d.arc((700, 825, 750, 875), 270, 90, fill=BLUE, width=12)
    for k in range(3):
        a = (lt * 1.4 + k * .3) % 1; d.arc((630 + k * 28, 730 - a * 50, 660 + k * 28, 790 - a * 50), 200, 340, fill=(148, 163, 184), width=5)
    if lt > 2.3: pill(S, 540, 1040, "QUICK GUESS", bg=AMBER, fg=INK, size=58, u=(lt - 2.3) / 0.3)

def quiz_opts(S, lt, times, reveal=None):
    opts = [("A", "20 minutes"), ("B", "1 hour"), ("C", "About 4 hours")]
    for k, (L_, txt) in enumerate(opts):
        u = (lt - times[k]) / 0.3
        if u <= 0: continue
        y = 330 + k * 200
        col = BLUE
        if reveal is not None and lt > reveal:
            col = GREEN if L_ == "C" else (100, 116, 139)
        chip(S, 80, y, L_, txt, u, col=col)
        if reveal is not None and lt > reveal:
            d = ImageDraw.Draw(S); badge(d, 920, y + 60, L_ == "C", r=40)

def quiz(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(22, 33, 58))
    pill(S, 540, 60, "QUICK QUIZ", bg=AMBER, fg=INK, size=60, u=lt / 0.3)
    d = ImageDraw.Draw(S)
    d.text((540, 210), "How long does it take?", font=F("ExtraBold", 60), fill=WHITE, anchor="ma")
    quiz_opts(S, lt, [1.2, 2.2, 3.8])
    # countdown ring
    cx, cy, r = 540, 1050, 95
    frac = max(0, min(1, (lt - 0.6) / 4.6))
    d = ImageDraw.Draw(S)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(51, 65, 85), width=18)
    d.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * (1 - frac), fill=AMBER, width=18)
    d.text((cx, cy), str(max(0, 5 - int(lt))), font=F("ExtraBold", 80), fill=WHITE, anchor="mm")

def answer(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(22, 33, 58))
    pill(S, 540, 60, "THE ANSWER", bg=GREEN, size=60, u=lt / 0.3)
    quiz_opts(S, lt + 10, [0, 0, 0], reveal=10.3)
    # big clock sweeping four hours
    d = ImageDraw.Draw(S); cx, cy, r = 540, 1030, 150
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(241, 245, 249))
    sw = 120 * ease((lt - 0.6) / 2.2)  # 4 of 12 hours = 120 degrees
    if sw > 1: d.pieslice((cx - r + 12, cy - r + 12, cx + r - 12, cy + r - 12), -90, -90 + sw, fill=(134, 239, 172))
    for k in range(12):
        a = k / 12 * 2 * math.pi
        d.line([(cx + math.sin(a) * r * .8, cy - math.cos(a) * r * .8), (cx + math.sin(a) * r * .92, cy - math.cos(a) * r * .92)], fill=INK, width=6)
    a = math.radians(sw); d.line([(cx, cy), (cx + math.sin(a) * r * .6, cy - math.cos(a) * r * .6)], fill=INK, width=12)
    d.ellipse((cx - 12, cy - 12, cx + 12, cy + 12), fill=INK)
    if lt > 2.0: d.text((200, 990), "average,", font=F("Bold", 40), fill=LIGHT, anchor="ma"); d.text((200, 1040), "says CBP", font=F("Bold", 40), fill=LIGHT, anchor="ma")

def mostly_talk(S, t, lt):
    table_scene(S, t, lt, bubble=["Let me explain", "how today works."], bubble_t=0.3, sheet=True)
    # time bar: talking vs sensors
    lay = Image.new("RGBA", S.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
    u = ease((lt - 1.6) / 0.6)
    if u > 0:
        g.rounded_rectangle((60, 990, 740, 1200), radius=26, fill=(15, 23, 42, 240))
        g.rounded_rectangle((100, 1030, 100 + 420 * u, 1100), radius=16, fill=GREEN + (255,))
        g.rounded_rectangle((100 + 420 * u + 10, 1030, 100 + 420 * u + 10 + 150 * u, 1100), radius=16, fill=ACCENT + (255,))
        g.text((110, 1120), "Talking", font=F("ExtraBold", 40), fill=(134, 239, 172, 255))
        g.text((100 + 420 * u + 4, 1120), "Sensors", font=F("ExtraBold", 40), fill=ACCENT + (255,))
        S.alpha_composite(lay)

def step1_title(img, t, lt):
    sam_close(img, t, lt, expr="talk")
    pill(img, W / 2, 300, "STEP 1", bg=BLUE, size=60, u=lt / 0.3)
    pill(img, W / 2, 430, "Pre-test interview", bg=WHITE, fg=INK, size=60, u=(lt - 0.4) / 0.3)

def pretest(S, t, lt):
    table_scene(S, t, lt, sheet=True)
    d = ImageDraw.Draw(S)
    lay_items = [("Explains everything", 0.2), ("Goes over every", 1.6)]
    for k, (txt, t0) in enumerate(lay_items):
        u = (lt - t0) / 0.35
        if u <= 0: continue
        card(S, (60, 150 + k * 190, 1020, 310 + k * 190), txt, "question with you" if k == 1 else None, u=u,
             icon=lambda dd, x, y: badge(dd, x, y, True), title_size=50)
    d = ImageDraw.Draw(S)
    card(S, (60, 990, 760, 1150), "Pre-test interview", None, u=(lt - 0.1) / 0.3, color=BLUE, tcol=WHITE, title_size=50)

def rounds(S, t, lt):
    chair_spike(S, t, 0.0)
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 470), fill=(17, 26, 46))
    d.text((540, 40), "STEP 2  ·  Short rounds", font=F("ExtraBold", 56), fill=WHITE, anchor="ma")
    for k in range(3):
        u = (lt - (0.5 + k * 0.9)) / 0.3
        if u <= 0: continue
        x = 90 + k * 310
        lay = Image.new("RGBA", S.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
        g.rounded_rectangle((x, 150, x + 280, 420), radius=26, fill=(248, 250, 252, 255))
        g.text((x + 140, 175), f"Round {k + 1}", font=F("ExtraBold", 44), fill=INK + (255,), anchor="ma")
        for q in range(3):
            badge(g, x + 60, 270 + q * 52, True, r=18); g.rectangle((x + 95, 262 + q * 52, x + 240, 278 + q * 52), fill=(148, 163, 184, 255))
        lay.putalpha(lay.getchannel("A").point(lambda v: int(v * ease(u)))); S.alpha_composite(lay)
    card(S, (60, 1000, 750, 1170), "Same questions,", "asked more than once", u=(lt - 2.4) / 0.35, title_size=50)

def review(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(226, 232, 240))
    d.rectangle((0, 0, W, 90), fill=(30, 41, 59)); d.text((540, 20), "STEP 3  ·  Quality review", font=F("ExtraBold", 50), fill=WHITE, anchor="ma")
    # chart printout on the table
    d.rectangle((0, 820, W, 1260), fill=(120, 113, 108)); d.rounded_rectangle((60, 780, 1020, 860), radius=16, fill=(87, 70, 58))
    for k, x in enumerate((200, 540, 880)):
        person(d, x, 470, 0.95, shirt=[(30, 41, 59), (51, 65, 85), (71, 85, 105)][k], skin=[(214, 170, 135), (180, 130, 100), (236, 200, 170)][k], hair=[(80, 80, 86), (30, 30, 34), (150, 150, 150)][k])
    d.rectangle((0, 820, W, 1260), fill=(120, 113, 108)); d.rounded_rectangle((60, 780, 1020, 860), radius=16, fill=(87, 70, 58))
    d.rounded_rectangle((120, 870, 700, 1010), radius=10, fill=(248, 250, 252))
    wave_line(d, (150, 880, 670, 940), 1.0, amp=.25, col=ACCENT); wave_line(d, (150, 935, 670, 995), 2.0, amp=.25, col=(248, 113, 113))
    # magnifier
    u = pop((lt - 0.6) / 0.5); s = max(0.01, u)
    cx, cy = 560, 930
    d.ellipse((cx - 70 * s, cy - 70 * s, cx + 70 * s, cy + 70 * s), outline=INK, width=max(1, int(14 * s)))
    d.line([(cx + 50 * s, cy + 50 * s), (cx + 110 * s, cy + 110 * s)], fill=INK, width=max(1, int(20 * s)))
    card(S, (60, 120, 1020, 290), "Senior examiners review", "before any decision", u=(lt - 1.2) / 0.35, color=BLUE, tcol=WHITE, title_size=50)

def comments(img, t, lt):
    def top(img, t, lt):
        card(img, (110, 340, 970, 560), "Did you guess right?", "Tell me in the comments", u=lt / 0.35, title_size=58)
        if lt > 0.8:
            lay = layer(); g = ImageDraw.Draw(lay); u = ease((lt - 0.8) / 0.3)
            cx, cy = 870, 640
            g.rounded_rectangle((cx - 90, cy - 60, cx + 90, cy + 50), radius=30, fill=AMBER + (255,))
            g.polygon([(cx - 40, cy + 45), (cx - 10, cy + 45), (cx - 50, cy + 90)], fill=AMBER + (255,))
            for k in range(3): g.ellipse((cx - 50 + k * 40 - 10, cy - 15, cx - 50 + k * 40 + 10, cy + 5), fill=INK + (255,))
            comp(img, lay, u)
    sam_desk(img, t, lt, expr="smile", top=top)

SCENES = [
    (0.0, 3.2, ill(tomorrow)),
    (3.2, 8.45, ill(quiz)),
    (8.45, 11.05, intro),
    (11.05, 14.85, ill(answer)),
    (14.85, 18.3, ill(mostly_talk)),
    (18.3, 20.35, step1_title),
    (20.35, 24.2, ill(pretest)),
    (24.2, 28.7, ill(rounds)),
    (28.7, 33.0, ill(review)),
    (33.0, 35.4, comments),
    (35.4, TOTAL, cta),
]
CAPS = [
    (0.0, 2.25, "Your CBP polygraph is tomorrow."),
    (2.25, 4.3, "Quick guess: how long will it take?"),
    (4.3, 6.85, "Twenty minutes? One hour? Or..."),
    (6.85, 8.4, "...about four hours?"),
    (8.45, 11.0, "Hi, I'm Sam, your polygraph guide."),
    (11.05, 14.85, "The answer: about four hours, on average, says CBP."),
    (14.85, 18.3, "And most of it isn't on the sensors. It's talking."),
    (18.3, 20.35, "First, a pre-test interview."),
    (20.35, 24.2, "The examiner explains everything and goes over every question with you."),
    (24.2, 26.2, "Then short rounds on the sensors,"),
    (26.2, 28.7, "with the same questions asked more than once."),
    (28.7, 32.9, "After that, senior examiners review the exam before any decision."),
    (33.0, 35.4, "Did you guess right? Tell me in the comments."),
    (35.4, TOTAL, "Want the full guide? Link in bio."),
]
