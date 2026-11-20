"""short-16: The one mistake honest people make (THE ONE MISTAKE format)"""
import math
from PIL import Image, ImageDraw
from sam5 import *
from s13 import ill, chair_spike
from s15 import table_scene, speech, intro, cta

VOICE = "v16.raw"; TOTAL = 32.2

def old_box(d, cx, cy, s=1.0):
    """A small cardboard box labelled 'old stuff' = 'that old thing'."""
    d.polygon([(cx - 90 * s, cy - 40 * s), (cx + 90 * s, cy - 40 * s), (cx + 90 * s, cy + 70 * s), (cx - 90 * s, cy + 70 * s)], fill=(202, 138, 4))
    d.polygon([(cx - 90 * s, cy - 40 * s), (cx - 60 * s, cy - 80 * s), (cx + 120 * s, cy - 80 * s), (cx + 90 * s, cy - 40 * s)], fill=(234, 179, 8))
    d.rectangle((cx - 50 * s, cy - 5 * s, cx + 50 * s, cy + 35 * s), fill=(254, 249, 195))
    d.text((cx, cy + 15 * s), "old", font=F("ExtraBold", max(8, int(30 * s))), fill=(120, 53, 15), anchor="mm")

def thought(S, box, u):
    if u <= 0: return
    u = ease(u); lay = Image.new("RGBA", S.size, (0, 0, 0, 0)); g = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = box
    g.rounded_rectangle(box, radius=90, fill=(255, 255, 255, 245))
    for k, (dx, dy, r) in enumerate([(-30, 40, 26), (-70, 95, 17), (-100, 140, 11)]):
        cx = x0 + 160 + dx; cy = y1 + dy
        g.ellipse((cx - r, cy - r, cx + r, cy + r), fill=(255, 255, 255, 245))
    lay.putalpha(lay.getchannel("A").point(lambda v: int(v * u))); S.alpha_composite(lay)

def asks(S, t, lt):
    table_scene(S, t, lt, bubble=["\"Anything else", "we should know?\""], bubble_t=1.3)

def too_small(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(203, 213, 225))
    d.rectangle((0, 0, W, 120), fill=(185, 195, 207))
    person(d, 540, 760, 1.5, shirt=(100, 116, 139), skin=(230, 190, 160), hair=(92, 64, 40))
    d.rectangle((0, 1080, W, 1260), fill=(120, 113, 108))
    thought(S, (120, 120, 960, 500), lt / 0.4)
    d = ImageDraw.Draw(S)
    if lt > 0.3:
        s = 1.0 - 0.55 * ease((lt - 1.4) / 1.4)  # the box shrinks as it gets "too small"
        old_box(d, 300, 300, s)
        d.text((420, 190), "That old thing?", font=F("ExtraBold", 54), fill=INK)
    if lt > 2.3:
        d.text((420, 290), "Too small", font=F("ExtraBold", 54), fill=RED)
        d.text((420, 360), "to mention.", font=F("ExtraBold", 54), fill=RED)

def the_mistake(img, t, lt):
    sam_close(img, t, lt, expr="serious")
    pill(img, W / 2, 300, "THE ONE MISTAKE", bg=RED, size=64, u=lt / 0.35)
    pill(img, W / 2, 440, "honest people make", bg=WHITE, fg=INK, size=52, u=(lt - 0.8) / 0.3)

def who_decides(S, t, lt):
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 1260), fill=(22, 33, 58))
    # balance scale: tiny box vs a big "?"
    cx, top = 540, 330
    tilt = 0.12 * math.sin(lt * 1.6)
    d.rectangle((cx - 12, top, cx + 12, 860), fill=(148, 163, 184)); d.rounded_rectangle((cx - 150, 840, cx + 150, 890), radius=20, fill=(148, 163, 184))
    lx, ly = cx - 330 * math.cos(tilt), top + 330 * math.sin(tilt); rx, ry = cx + 330 * math.cos(tilt), top - 330 * math.sin(tilt)
    d.line([(lx, ly), (rx, ry)], fill=(203, 213, 225), width=16)
    for (x, y) in ((lx, ly), (rx, ry)):
        d.line([(x, y), (x - 90, y + 230)], fill=(148, 163, 184), width=5); d.line([(x, y), (x + 90, y + 230)], fill=(148, 163, 184), width=5)
        d.chord((x - 130, y + 170, x + 130, y + 290), 0, 180, fill=(203, 213, 225))
    old_box(d, lx, ly + 190, 0.55)
    d.text((rx, ry + 150), "?", font=F("ExtraBold", 130), fill=AMBER, anchor="mm")
    card(S, (60, 960, 760, 1180), "Deciding alone", "what's \"too small\"", u=(lt - 0.2) / 0.35, icon=lambda dd, x, y: badge(dd, x, y, False), title_size=48)

def goes_over(S, t, lt):
    table_scene(S, t, lt, sheet=True)
    for k, (txt, t0) in enumerate([("Question 1", 0.6), ("Question 2", 1.3), ("Question 3", 2.0)]):
        u = (lt - t0) / 0.3
        if u <= 0: continue
        card(S, (60, 140 + k * 150, 640, 270 + k * 150), txt, None, u=u, icon=lambda dd, x, y: badge(dd, x, y, True), title_size=46)
    card(S, (60, 990, 760, 1150), "Pre-test interview", None, u=lt / 0.3, color=BLUE, tcol=WHITE, title_size=50)

def the_moment(S, t, lt):
    table_scene(S, t, lt, cand_bubble=["\"One more thing", "I should mention...\""], cand_t=0.2)
    pill(S, 420, 1000, "THE MOMENT TO SAY IT", bg=GREEN, size=50, u=(lt - 0.6) / 0.3)

def on_mind(S, t, lt):
    chair_spike(S, t, 0.0)
    d = ImageDraw.Draw(S); d.rectangle((0, 0, W, 470), fill=(17, 26, 46))
    thought(S, (140, 60, 940, 420), lt / 0.4)
    d = ImageDraw.Draw(S)
    if lt > 0.3:
        old_box(d, 330, 250, 0.9 + 0.06 * math.sin(lt * 5))
        d.text((480, 170), "Still on", font=F("ExtraBold", 58), fill=INK)
        d.text((480, 250), "my mind...", font=F("ExtraBold", 58), fill=INK)
    card(S, (60, 1000, 760, 1170), "When that question", "comes up", u=(lt - 1.2) / 0.35, title_size=48)

def say_ask(S, t, lt):
    table_scene(S, t, lt, sheet=True)
    d = ImageDraw.Draw(S)
    card(S, (60, 150, 1020, 320), "Say it in the interview", None, u=(lt - 0.1) / 0.35, icon=lambda dd, x, y: badge(dd, x, y, True), title_size=52)
    card(S, (60, 350, 1020, 540), "Ask about any question", "you're not sure of", u=(lt - 1.5) / 0.35, icon=lambda dd, x, y: badge(dd, x, y, True), title_size=52)

SCENES = [
    (0.0, 3.0, ill(asks)),
    (3.0, 6.85, ill(too_small)),
    (6.85, 9.6, intro),
    (9.6, 12.3, the_mistake),
    (12.3, 15.4, ill(who_decides)),
    (15.4, 19.4, ill(goes_over)),
    (19.4, 21.45, ill(the_moment)),
    (21.45, 25.1, ill(on_mind)),
    (25.1, 29.1, ill(say_ask)),
    (29.1, TOTAL, cta),
]
CAPS = [
    (0.0, 3.0, "The examiner asks: \"Anything else we should know?\""),
    (3.0, 4.95, "And you think... that old thing?"),
    (4.95, 6.85, "Too small to mention."),
    (6.85, 9.55, "Hi, I'm Sam, your polygraph guide."),
    (9.6, 12.3, "That's the one mistake honest people make:"),
    (12.3, 15.4, "deciding on their own what's too small to mention."),
    (15.4, 19.4, "In the pre-test interview, the examiner goes over every question with you."),
    (19.4, 21.45, "That's the moment to bring things up."),
    (21.45, 25.1, "Something you hold back can stay on your mind when that question comes."),
    (25.1, 26.55, "So say it in the interview,"),
    (26.55, 29.1, "and ask about any question you're not sure of."),
    (29.1, TOTAL, "Want the full guide? Link in bio."),
]
