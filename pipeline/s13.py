"""short-13: The night before your polygraph: wrong or right?"""
import math
from PIL import Image, ImageDraw
from sam5 import *

VOICE = "v13.raw"; TOTAL = 37.4

def room_night(d, wall=(20, 30, 58)):
    d.rectangle((0, 0, W, 1260), fill=wall)
    d.rounded_rectangle((90, 90, 430, 470), radius=20, fill=(12, 20, 40), outline=(60, 72, 100), width=10)  # window
    d.line([(260, 90), (260, 470)], fill=(60, 72, 100), width=8); d.line([(90, 280), (430, 280)], fill=(60, 72, 100), width=8)
    d.ellipse((300, 140, 380, 220), fill=(241, 245, 249)); d.ellipse((322, 130, 402, 210), fill=(12, 20, 40))  # moon
    for x, y in [(140, 160), (200, 380), (380, 400), (160, 320)]: d.ellipse((x, y, x + 6, y + 6), fill=WHITE)

def bedroom(S, t, lt):
    d = ImageDraw.Draw(S); room_night(d)
    # bed
    d.rounded_rectangle((60, 760, 1020, 1100), radius=40, fill=(51, 65, 85))
    d.rounded_rectangle((90, 700, 360, 820), radius=40, fill=(203, 213, 225))  # pillow
    d.rounded_rectangle((300, 780, 1020, 1060), radius=50, fill=(37, 70, 140))  # blanket
    # person lying, head on pillow, phone glow
    d.ellipse((150, 640, 300, 790), fill=(222, 178, 140)); d.chord((140, 626, 310, 760), 160, 360, fill=(70, 52, 40))
    d.ellipse((230, 700, 246, 716), fill=INK)
    glow = Image.new("RGBA", S.size, (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    a = int(70 + 30 * math.sin(t * 6))
    g.polygon([(330, 640), (170, 700), (300, 800)], fill=(147, 197, 253, a)); S.alpha_composite(glow); d = ImageDraw.Draw(S)
    d.rounded_rectangle((320, 560, 420, 740), radius=16, fill=(15, 23, 42), outline=(148, 163, 184), width=4)
    d.rounded_rectangle((330, 575, 410, 725), radius=10, fill=(191, 219, 254))
    for k in range(5): d.rectangle((340, 590 + k * 26, 400 - (k % 2) * 20, 600 + k * 26), fill=(71, 85, 105))
    # nightstand + clock
    d.rectangle((790, 560, 1010, 760), fill=(41, 37, 36)); digital(d, 820, 480, "02:00", 70)

def phone43(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(15, 23, 42))
    x0, y0 = 300, 140
    d.rounded_rectangle((x0, y0, x0 + 480, y0 + 900), radius=60, fill=(2, 6, 23), outline=(100, 116, 139), width=8)
    d.rounded_rectangle((x0 + 26, y0 + 70, x0 + 454, y0 + 860), radius=30, fill=(241, 245, 249))
    d.text((x0 + 60, y0 + 100), "Polygraph forum", font=F("ExtraBold", 40), fill=INK)
    posts = ["\"What will they ask me??\"", "\"I can't sleep, test is tomorrow\"", "\"Is it normal to be this nervous?\"", "\"My story (long)...\""]
    off = (lt * 160) % 170
    for k in range(6):
        yy = y0 + 180 + k * 170 - off
        if y0 + 160 < yy < y0 + 780:
            d.rounded_rectangle((x0 + 50, yy, x0 + 430, yy + 140), radius=20, fill=WHITE, outline=(203, 213, 225), width=3)
            d.text((x0 + 76, yy + 30), posts[k % 4][:26], font=F("SemiBold", 28), fill=(51, 65, 85))
            d.rectangle((x0 + 76, yy + 84, x0 + 340, yy + 98), fill=(203, 213, 225))
    u = pop(lt / 0.5)
    r = int(120 * max(0.01, u)); cx, cy = 820, 260
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=RED)
    if r > 40: d.text((cx, cy - 8), "43", font=F("ExtraBold", int(110 * u)), fill=WHITE, anchor="mm")
    d.text((cx, cy + 150), "times", font=F("Bold", 44), fill=(248, 113, 113), anchor="mm")

def late_research(S, t, lt):
    d = ImageDraw.Draw(S); room_night(d, wall=(24, 30, 52))
    d.rectangle((0, 880, W, 1260), fill=(46, 37, 32))
    d.polygon([(160, 880), (920, 880), (880, 400), (200, 400)], fill=(30, 41, 59))
    d.rounded_rectangle((225, 425, 855, 860), radius=12, fill=(226, 232, 240))
    qs = ["What will they ask?", "Can nerves fail me?", "What if I blank?", "Night-before tips??", "What do they record?"]
    for k, q in enumerate(qs):
        if lt > k * 0.35:
            d.rounded_rectangle((250, 450 + k * 80, 830, 515 + k * 80), radius=10, fill=WHITE)
            d.text((272, 462 + k * 80), "Search: " + q, font=F("SemiBold", 30), fill=(51, 65, 85))
    d.polygon([(110, 880), (970, 880), (1000, 920), (80, 920)], fill=(71, 85, 105))
    digital(d, 760, 160, "02:14", 64)
    stamp(S, "WRONG", 540, 640, RED, (lt - 3.1) / 0.5, size=140)

def chair_spike(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(17, 26, 46))
    d.rounded_rectangle((70, 60, 1010, 440), radius=24, fill=(8, 13, 26), outline=(30, 41, 59), width=12)
    spike = min(1.6, lt * 0.8)
    wave_line(d, (300, 90, 980, 200), t, amp=.2, label=None, col=ACCENT)
    wave_line(d, (300, 200, 980, 310), t, amp=.2, spike=spike * .6, col=(167, 139, 250), phase=1)
    wave_line(d, (300, 310, 980, 420), t * 1.8, amp=.22, freq=.6, spike=spike, col=(248, 113, 113), phase=2)
    d.text((100, 120), "Breathing", font=F("SemiBold", 30), fill=ACCENT); d.text((100, 232), "Sweat (skin)", font=F("SemiBold", 30), fill=(167, 139, 250))
    d.text((100, 344), "Heart rate", font=F("SemiBold", 30), fill=(248, 113, 113))
    # chair + person with sensors
    d.rounded_rectangle((290, 560, 790, 1140), radius=60, fill=(30, 30, 36))
    d.rounded_rectangle((200, 880, 330, 940), radius=20, fill=(40, 40, 48)); d.rounded_rectangle((750, 880, 880, 940), radius=20, fill=(40, 40, 48))
    person(d, 540, 640, 1.0, shirt=(100, 116, 139)); arms_on_rests(d, 540, 640, 1.0, (100, 116, 139), (222, 178, 140))
    # tired eyes: heavy lids
    for sg in (-1, 1): d.line([(540 + sg * 26 - 14, 634), (540 + sg * 26 + 14, 634)], fill=(222, 178, 140), width=8)
    card(S, (90, 1000, 760, 1170), "Tired body", "bigger reactions", u=(lt - 0.6) / 0.4, title_size=48)

def sleep(S, t, lt):
    d = ImageDraw.Draw(S); room_night(d, wall=(18, 28, 56))
    d.rounded_rectangle((60, 760, 1020, 1100), radius=40, fill=(51, 65, 85))
    d.rounded_rectangle((90, 700, 360, 820), radius=40, fill=(203, 213, 225))
    d.rounded_rectangle((260, 760, 1020, 1060), radius=50, fill=(37, 99, 235))
    d.ellipse((150, 640, 300, 790), fill=(222, 178, 140)); d.chord((140, 626, 310, 760), 160, 360, fill=(70, 52, 40))
    d.arc((210, 700, 250, 724), 0, 180, fill=INK, width=5)  # closed eye
    for k in range(3):
        a = (lt * 1.2 + k * .33) % 1
        d.text((330 + k * 50 + a * 40, 640 - k * 60 - a * 80), "z", font=F("ExtraBold", 50 + k * 14), fill=(191, 219, 254))
    card(S, (560, 520, 1010, 680), "8 hours", "of sleep", u=lt / 0.4, icon=lambda dd, x, y: clock(dd, x, y, 40, 10, 0))
    stamp(S, "RIGHT", 560, 330, GREEN, (lt - 1.45) / 0.5, ang=8, size=130)

def med_wrong(img, t, lt):
    def top(img, t, lt):
        card(img, (90, 330, 990, 560), "Skipping your medication", "to \"stay clean\"", u=lt / 0.4,
             icon=lambda dd, x, y: badge(dd, x, y, False))
        stamp(img, "WRONG", 760, 720, RED, (lt - 3.15) / 0.5, size=110)
    sam_desk(img, t, lt, expr="serious", top=top)

def med_right(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(22, 33, 58))
    d.rounded_rectangle((230, 120, 850, 980), radius=30, fill=(241, 245, 249))  # clipboard
    d.rounded_rectangle((420, 80, 660, 160), radius=20, fill=(100, 116, 139))
    d.text((280, 200), "Pre-test form", font=F("ExtraBold", 50), fill=INK)
    d.text((280, 290), "Medications I take:", font=F("Bold", 38), fill=(51, 65, 85))
    for k, item in enumerate(["Daily prescription", "Taken as usual today"]):
        if lt > 0.6 + k * 0.9:
            badge(d, 320, 420 + k * 120, True, r=34); d.text((380, 398 + k * 120), item, font=F("SemiBold", 38), fill=INK)
    # pill bottle
    d.rounded_rectangle((690, 700, 900, 1040), radius=30, fill=(245, 177, 66)); d.rounded_rectangle((680, 650, 910, 730), radius=20, fill=WHITE)
    d.rectangle((715, 800, 875, 920), fill=WHITE); d.text((795, 860), "Rx", font=F("ExtraBold", 60), fill=INK, anchor="mm")
    card(S, (70, 1020, 770, 1185), "Take it as prescribed", "and tell the examiner", u=lt / 0.4, icon=lambda dd, x, y: badge(dd, x, y, True), title_size=42)

def breakfast(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(250, 232, 200))
    d.rectangle((0, 0, W, 700), fill=(254, 243, 199))
    d.rounded_rectangle((640, 90, 980, 520), radius=20, fill=(186, 230, 253), outline=(251, 191, 36), width=10)  # sunny window
    d.ellipse((760, 170, 880, 290), fill=(253, 224, 71))
    clock(d, 300, 230, 110, 8, 15)
    d.text((300, 370), "8:15", font=F("ExtraBold", 56), fill=(120, 53, 15), anchor="ma")
    d.rectangle((0, 700, W, 1260), fill=(180, 130, 90)); d.rectangle((0, 700, W, 730), fill=(150, 105, 70))
    d.ellipse((240, 820, 640, 1020), fill=WHITE); d.ellipse((330, 860, 450, 960), fill=(254, 249, 195)); d.ellipse((365, 885, 415, 935), fill=(251, 191, 36))
    d.rounded_rectangle((470, 860, 600, 960), radius=12, fill=(217, 160, 90))  # toast
    d.rounded_rectangle((700, 820, 840, 990), radius=20, fill=(37, 99, 235)); d.arc((820, 860, 890, 940), 270, 90, fill=(37, 99, 235), width=16)
    for k in range(3):
        a = (lt * 1.5 + k * .3) % 1; d.arc((720 + k * 35, 720 - a * 60, 760 + k * 35, 800 - a * 60), 200, 340, fill=(148, 163, 184), width=5)
    card(S, (70, 1030, 770, 1195), "Normal breakfast", "and arrive a little early", u=lt / 0.4, icon=lambda dd, x, y: badge(dd, x, y, True), title_size=44)
    stamp(S, "RIGHT", 560, 560, GREEN, (lt - 2.7) / 0.5, ang=-8, size=130)

def intro(img, t, lt):
    def top(img, t, lt):
        card(img, (160, 360, 920, 600), "Sam", "your polygraph guide", u=(lt - 0.3) / 0.4, color=BLUE, tcol=WHITE, title_size=80)
    sam_desk(img, t, lt, expr="talk", wave=lt < 2.2, top=top)

def title(img, t, lt):
    sam_close(img, t, lt, expr="talk")
    pill(img, W / 2, 300, "THE NIGHT BEFORE", bg=BLUE, size=58, u=lt / 0.4)
    pill(img, W / 2 - 190, 430, "WRONG", bg=RED, size=58, u=(lt - 1.45) / 0.3)
    pill(img, W / 2 + 200, 430, "RIGHT?", bg=GREEN, size=58, u=(lt - 2.05) / 0.3)

def cta(img, t, lt):
    def top(img, t, lt):
        card(img, (110, 340, 970, 600), "Want the full guide?", "Link in bio", u=lt / 0.4, title_size=60)
    sam_desk(img, t, lt, expr="smile", top=top)

def ill(fn, inset=True, expr="talk"):
    def f(img, t, lt):
        frame_box(img, fn, t, lt)
        if inset: sam_inset(img, t, expr)
    return f

SCENES = [
    (0.0, 5.45, ill(bedroom)),
    (5.45, 7.55, ill(phone43)),
    (7.55, 10.35, intro),
    (10.35, 13.3, title),
    (13.3, 17.35, ill(late_research)),
    (17.35, 21.4, ill(chair_spike)),
    (21.4, 23.6, ill(sleep)),
    (23.6, 27.65, med_wrong),
    (27.65, 31.1, ill(med_right)),
    (31.1, 34.6, ill(breakfast)),
    (34.6, TOTAL, cta),
]
CAPS = [
    (0.0, 1.3, "It's two a.m."),
    (1.3, 5.45, "You're still awake, reading forum posts about tomorrow's polygraph..."),
    (5.45, 7.4, "...for the forty-third time."),
    (7.55, 10.3, "Hi, I'm Sam, your polygraph guide."),
    (10.35, 13.3, "The night before your test: wrong or right?"),
    (13.3, 16.45, "Staying up late to research every possible question?"),
    (16.45, 17.3, "Wrong."),
    (17.35, 21.35, "A tired body reacts more, and that never helps an honest person."),
    (21.4, 23.6, "Getting a full night's sleep? Right."),
    (23.6, 27.6, "Skipping your usual medication to \"stay clean\"? Wrong."),
    (27.65, 31.1, "Take it as prescribed, and tell the examiner what you take."),
    (31.1, 34.6, "A normal breakfast, and arriving a little early? Right."),
    (34.6, TOTAL, "Want the full guide? Link in bio."),
]
