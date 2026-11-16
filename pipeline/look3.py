"""Sam look v3 (stills only): more realistic face, behind a polygraph desk."""
import math
from PIL import Image, ImageDraw, ImageFilter, ImageFont
FD = "/usr/share/fonts/opentype/inter/"
def F(w, s): return ImageFont.truetype(FD + f"Inter-{w}.otf", s)
NAVY = (11, 19, 37); BLUE = (37, 99, 235); ACCENT = (96, 165, 250); WHITE = (255, 255, 255); MUTED = (148, 163, 184)
SKIN = (233, 190, 154); SKIN_SH = (205, 158, 122); SKIN_HI = (244, 208, 176)
HAIR = (128, 128, 136); HAIR_D = (92, 92, 100); HAIR_HI = (188, 188, 196)
BEARD = (118, 112, 112); INK = (26, 26, 32); IRIS = (82, 112, 150)
SUIT = (28, 29, 34); SUIT_D = (14, 14, 18); EDGE = (70, 74, 86)
LIP_U = (164, 98, 92); LIP_L = (186, 118, 108); MOUTH = (96, 36, 40)

def poly(d, pts, cx, cy, s, fill, outline=None, width=0):
    d.polygon([(cx + x * s, cy + y * s) for x, y in pts], fill=fill, outline=outline, width=width)

def smooth(pts, n=6):
    out = []; L = len(pts)
    for i in range(L):
        p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % L], pts[(i + 2) % L]
        for k in range(n):
            t = k / n; t2, t3 = t * t, t * t * t
            out.append(tuple(0.5 * ((2 * p1[j]) + (-p0[j] + p2[j]) * t + (2 * p0[j] - 5 * p1[j] + 4 * p2[j] - p3[j]) * t2 + (-p0[j] + 3 * p1[j] - 3 * p2[j] + p3[j]) * t3) for j in (0, 1)))
    return out

FACE = smooth([(0, -255), (115, -242), (180, -195), (203, -115), (206, -30), (198, 50), (183, 118), (158, 178), (112, 230), (55, 262), (0, 270), (-55, 262), (-112, 230), (-158, 178), (-183, 118), (-198, 50), (-206, -30), (-203, -115), (-180, -195), (-115, -242)])

def head(size, expr="smile", mouth=None, blink=False):
    S = 2; Wd = 700 * S; Hd = 760 * S
    im = Image.new("RGBA", (Wd, Hd), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    cx, cy, s = Wd / 2, Hd / 2 + 40 * S, S
    def P(x, y): return (cx + x * s, cy + y * s)
    def E(a, b, c, e, **kw): d.ellipse((cx + a * s, cy + b * s, cx + c * s, cy + e * s), **kw)
    d.rectangle((cx - 95 * s, cy + 150 * s, cx + 95 * s, cy + 420 * s), fill=SKIN_SH)
    for sg in (-1, 1):
        E(sg * 205 - 38, -45, sg * 205 + 38, 95, fill=SKIN)
        E(sg * 205 - 20, -25, sg * 205 + 20, 70, fill=SKIN_SH)
    poly(d, FACE, cx, cy, s, SKIN)
    fm = Image.new("L", im.size, 0); ImageDraw.Draw(fm).polygon([P(*p) for p in FACE], fill=255)
    grad = Image.linear_gradient("L").rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT).resize(im.size)
    grad = grad.point(lambda v: int(max(0, (v - 150)) * 1.4))
    from PIL import ImageChops
    sh = Image.new("RGBA", im.size, SKIN_SH + (255,)); sh.putalpha(ImageChops.multiply(fm, grad).filter(ImageFilter.GaussianBlur(10 * s)))
    im.alpha_composite(sh); d = ImageDraw.Draw(im)
    bd = Image.new("RGBA", im.size, (0, 0, 0, 0)); b = ImageDraw.Draw(bd)
    beard = smooth([(-198, 40), (-150, 95), (-95, 112), (-45, 100), (0, 98), (45, 100), (95, 112), (150, 95), (198, 40), (183, 118), (158, 178), (112, 230), (55, 262), (0, 272), (-55, 262), (-112, 230), (-158, 178), (-183, 118)], 4)
    b.polygon([P(*p) for p in beard], fill=BEARD + (205,))
    b.polygon([P(-78, 108), P(-30, 92), P(0, 98), P(30, 92), P(78, 108), P(60, 125), P(0, 118), P(-60, 125)], fill=(98, 94, 96, 235))
    bd = bd.filter(ImageFilter.GaussianBlur(2.5 * s)); im.alpha_composite(bd); d = ImageDraw.Draw(im)
    if mouth is not None and mouth > 0.04:
        o = 8 + 44 * mouth
        d.rounded_rectangle((cx - 46 * s, cy + 140 * s, cx + 46 * s, cy + (140 + o) * s), radius=int(min(22, o / 2) * s), fill=MOUTH)
        if o > 22: d.rectangle((cx - 34 * s, cy + 140 * s, cx + 34 * s, cy + 150 * s), fill=(240, 236, 230))
        d.line([P(-48, 140), P(48, 140)], fill=LIP_U, width=int(8 * s))
        d.arc((cx - 48 * s, cy + (126 + o) * s, cx + 48 * s, cy + (150 + o) * s), 20, 160, fill=LIP_L, width=int(7 * s))
    elif expr == "surprised":
        E(-30, 140, 30, 205, fill=MOUTH); d.arc((cx - 30 * s, cy + 140 * s, cx + 30 * s, cy + 205 * s), 0, 360, fill=LIP_L, width=int(7 * s))
    elif expr in ("serious", "think"):
        d.line([P(-52, 150), P(52, 146 if expr == "serious" else 140)], fill=LIP_U, width=int(11 * s))
        d.line([P(-40, 160), P(40, 160)], fill=LIP_L, width=int(8 * s))
    elif expr == "talk":
        d.rounded_rectangle((cx - 48 * s, cy + 136 * s, cx + 48 * s, cy + 186 * s), radius=int(22 * s), fill=MOUTH)
        d.rectangle((cx - 36 * s, cy + 136 * s, cx + 36 * s, cy + 150 * s), fill=(240, 236, 230))
        d.line([P(-50, 140), P(50, 140)], fill=LIP_U, width=int(8 * s))
    else:
        d.chord((cx - 62 * s, cy + 105 * s, cx + 62 * s, cy + 175 * s), 15, 165, fill=MOUTH)
        d.chord((cx - 52 * s, cy + 112 * s, cx + 52 * s, cy + 160 * s), 15, 165, fill=(240, 236, 230))
        d.arc((cx - 66 * s, cy + 100 * s, cx + 66 * s, cy + 182 * s), 15, 165, fill=LIP_L, width=int(8 * s))
        for sg in (-1, 1): d.arc((cx + sg * 70 * s - 24 * s, cy + 120 * s, cx + sg * 70 * s + 24 * s, cy + 160 * s), 250 if sg < 0 else 200, 340 if sg < 0 else 290, fill=SKIN_SH, width=int(5 * s))
    d.line([P(14, -15), P(26, 55)], fill=SKIN_SH, width=int(9 * s))
    d.arc((cx - 34 * s, cy + 45 * s, cx + 34 * s, cy + 92 * s), 10, 170, fill=SKIN_SH, width=int(8 * s))
    for sg in (-1, 1): E(sg * 20 - 9, 68, sg * 20 + 9, 82, fill=(150, 98, 82))
    E(-12, 40, 12, 60, fill=SKIN_HI)
    lift = {"surprised": 14, "smile": 0, "talk": 2, "serious": -4, "think": 0}.get(expr, 0)
    for sg in (-1, 1):
        ex, ey = sg * 85, -22
        open_ = 1.25 if expr == "surprised" else (0.8 if expr == "smile" else 1.0)
        eye = smooth([(ex - 46, ey + 2), (ex - 15, ey - 20 * open_), (ex + 22, ey - 18 * open_), (ex + 46, ey), (ex + 15, ey + 15 * open_), (ex - 20, ey + 14 * open_)], 5)
        if blink:
            d.line([P(ex - 44, ey + 4), P(ex + 44, ey + 4)], fill=INK, width=int(7 * s))
            continue
        poly(d, eye, cx, cy, s, (246, 244, 240))
        ix = 8 if expr == "think" else 0; iy = -5 if expr == "think" else 0
        mask = Image.new("L", im.size, 0); ImageDraw.Draw(mask).polygon([P(*p) for p in eye], fill=255)
        ir = Image.new("RGBA", im.size, (0, 0, 0, 0)); idr = ImageDraw.Draw(ir)
        idr.ellipse((cx + (ex - 19 + ix) * s, cy + (ey - 19 + iy) * s, cx + (ex + 19 + ix) * s, cy + (ey + 19 + iy) * s), fill=IRIS)
        idr.ellipse((cx + (ex - 9 + ix) * s, cy + (ey - 9 + iy) * s, cx + (ex + 9 + ix) * s, cy + (ey + 9 + iy) * s), fill=INK)
        idr.ellipse((cx + (ex - 1 + ix) * s, cy + (ey - 10 + iy) * s, cx + (ex + 7 + ix) * s, cy + (ey - 2 + iy) * s), fill=WHITE)
        im.paste(ir, (0, 0), Image.composite(ir.getchannel("A"), Image.new("L", im.size, 0), mask)); d = ImageDraw.Draw(im)
        d.line([P(*p) for p in eye[:16]], fill=INK, width=int(7 * s))
        d.arc((cx + (ex - 44) * s, cy + (ey - 42 - lift) * s, cx + (ex + 44) * s, cy + (ey + 4 - lift) * s), 205, 335, fill=SKIN_SH, width=int(5 * s))
        for k in range(2):
            d.line([P(ex + sg * 52, ey + 4 + k * 10), P(ex + sg * 70, ey - 4 + k * 18)], fill=SKIN_SH, width=int(4 * s))
    for sg in (-1, 1):
        rl = 16 if (expr == "think" and sg == 1) else 0
        inner = {"serious": 10, "think": 0}.get(expr, 0)
        by = -78 - lift - rl
        poly(d, [(sg * 38, by + 8 + inner), (sg * 70, by - 6), (sg * 118, by - 4), (sg * 138, by + 8), (sg * 112, by + 6), (sg * 70, by + 10), (sg * 40, by + 20 + inner)], cx, cy, s, HAIR_D)
    for sg in (-1, 1):
        x0, x1 = (sg * 85 - 66), (sg * 85 + 66)
        d.rounded_rectangle((cx + min(x0, x1) * s, cy - 62 * s, cx + max(x0, x1) * s, cy + 22 * s), radius=int(16 * s), outline=INK, width=int(8 * s))
        rf = Image.new("RGBA", im.size, (0, 0, 0, 0)); ImageDraw.Draw(rf).polygon([P(sg * 85 - 40, -55), P(sg * 85 - 20, -55), P(sg * 85 - 50, 15), P(sg * 85 - 62, 15)], fill=(255, 255, 255, 40)); im.alpha_composite(rf); d = ImageDraw.Draw(im)
        d.line([P(sg * 151, -40), P(sg * 205, -32)], fill=INK, width=int(7 * s))
    d.arc((cx - 22 * s, cy - 40 * s, cx + 22 * s, cy - 10 * s), 200, 340, fill=INK, width=int(7 * s))
    hair = smooth([(-208, -70), (-212, -150), (-170, -238), (-80, -290), (30, -298), (130, -275), (200, -215), (214, -120), (208, -70), (190, -125), (150, -175), (60, -200), (-40, -192), (-75, -205), (-120, -175), (-180, -125)], 5)
    poly(d, hair, cx, cy, s, HAIR)
    poly(d, smooth([(-75, -205), (-60, -270), (40, -292), (150, -262), (205, -195), (150, -230), (40, -250), (-40, -232)], 4), cx, cy, s, HAIR_D)
    for k in range(4):
        x = -20 + k * 55
        d.arc((cx + (x - 90) * s, cy - 290 * s, cx + (x + 90) * s, cy - 170 * s), 215, 285, fill=(158, 158, 166), width=int(4 * s))
    for sg in (-1, 1):
        poly(d, [(sg * 206, -95), (sg * 200, -5), (sg * 188, -5), (sg * 185, -100)], cx, cy, s, HAIR)
    d.arc((cx - 80 * s, cy - 160 * s, cx + 80 * s, cy - 110 * s), 200, 340, fill=SKIN_SH, width=int(4 * s))
    im = im.resize((int(700 * size), int(760 * size)), Image.LANCZOS)
    return im

def body(size):
    L = Image.new("RGBA", (1120, 900), (0, 0, 0, 0)); d = ImageDraw.Draw(L)
    d.rounded_rectangle((150, 120, 970, 1200), radius=240, fill=SUIT, outline=EDGE, width=6)
    d.polygon([(450, 115), (670, 115), (560, 450)], fill=(244, 246, 250))
    d.polygon([(425, 120), (560, 450), (495, 600), (360, 160)], fill=SUIT_D, outline=EDGE)
    d.polygon([(695, 120), (560, 450), (625, 600), (760, 160)], fill=SUIT_D, outline=EDGE)
    d.polygon([(468, 110), (520, 200), (560, 132)], fill=WHITE); d.polygon([(652, 110), (600, 200), (560, 132)], fill=WHITE)
    d.polygon([(536, 145), (584, 145), (575, 185), (545, 185)], fill=BLUE)
    d.polygon([(545, 185), (575, 185), (594, 420), (560, 455), (526, 420)], fill=BLUE)
    bx, by = 690, 190
    d.rounded_rectangle((bx + 40, by - 20, bx + 80, by + 10), radius=6, fill=(148, 163, 184))
    d.rounded_rectangle((bx, by, bx + 120, by + 160), radius=12, fill=WHITE)
    d.rectangle((bx + 16, by + 20, bx + 104, by + 80), fill=(203, 213, 225)); d.ellipse((bx + 44, by + 26, bx + 76, by + 58), fill=(148, 163, 184)); d.chord((bx + 34, by + 52, bx + 86, by + 100), 180, 360, fill=(148, 163, 184))
    d.rectangle((bx + 16, by + 96, bx + 104, by + 108), fill=BLUE); d.rectangle((bx + 16, by + 120, bx + 80, by + 130), fill=MUTED)
    return L.resize((int(1120 * size), int(900 * size)), Image.LANCZOS)

def chart_screen(d, box, t=1.3):
    x0, y0, x1, y1 = box
    d.rounded_rectangle((x0 - 16, y0 - 16, x1 + 16, y1 + 16), radius=28, fill=(30, 41, 59))
    d.rounded_rectangle((x0, y0, x1, y1), radius=16, fill=(8, 13, 26))
    for gx in range(int(x0) + 60, int(x1), 60): d.line([(gx, y0 + 6), (gx, y1 - 6)], fill=(20, 30, 52), width=2)
    cols = [ACCENT, (167, 139, 250), (125, 211, 252)]; names = ["Breathing", "Sweat (skin)", "Heart rate"]
    hgt = (y1 - y0) / 3
    for r in range(3):
        yy = y0 + hgt * (r + 0.5)
        pts = [(x0 + 220 + (x1 - x0 - 250) * i / 90, yy + hgt * 0.24 * math.sin(i * 0.33 * (1 + 0.25 * r) + t + r)) for i in range(91)]
        d.line(pts, fill=cols[r], width=5)
        d.text((x0 + 24, yy - 18), names[r], font=F("SemiBold", 32), fill=cols[r])

def desk_scene(expr="smile"):
    P = Image.new("RGBA", (1080, 1350), (13, 22, 42, 255)); d = ImageDraw.Draw(P)
    chart_screen(d, (70, 90, 1010, 520))
    hd = head(0.6, expr); bd = body(0.82)
    P.alpha_composite(bd, (540 - bd.width // 2, 800))
    P.alpha_composite(hd, (540 - hd.width // 2, 495))
    d = ImageDraw.Draw(P)
    d.polygon([(0, 1060), (1080, 1060), (1080, 1350), (0, 1350)], fill=(46, 37, 32))
    d.rectangle((0, 1060, 1080, 1078), fill=(70, 56, 46))
    d.rounded_rectangle((90, 975, 400, 1075), radius=14, fill=(20, 22, 28)); d.rectangle((90, 975, 400, 990), fill=(40, 44, 54))
    for k in range(5): d.ellipse((115 + k * 55, 1020, 140 + k * 55, 1045), fill=(60, 64, 76))
    d.ellipse((350, 1015, 372, 1037), fill=(34, 197, 94))
    d.polygon([(690, 1065), (990, 1065), (960, 880), (720, 880)], fill=(51, 65, 85)); d.polygon([(660, 1065), (1020, 1065), (1030, 1085), (650, 1085)], fill=(71, 85, 105))
    draw_mark(P, 815, 940, 50)
    d.line([(140, 1075), (120, 1180), (230, 1290)], fill=(120, 128, 140), width=9)
    d.line([(200, 1075), (260, 1200), (420, 1260)], fill=(120, 128, 140), width=9)
    d.line([(260, 1075), (380, 1160), (560, 1180)], fill=(30, 58, 138), width=12)
    d.rounded_rectangle((200, 1270, 270, 1320), radius=10, fill=(148, 163, 184))
    d.rounded_rectangle((400, 1240, 470, 1290), radius=10, fill=(148, 163, 184))
    d.rounded_rectangle((540, 1150, 820, 1230), radius=26, fill=(30, 58, 138))
    d.line([(560, 1170), (800, 1170)], fill=(59, 89, 170), width=6)
    return P

def draw_mark(img, x, y, size, color=ACCENT):
    import make_short as m
    m.draw_mark(img, x, y, size, color)
