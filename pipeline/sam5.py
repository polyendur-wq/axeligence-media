"""Sam v5 renderer: Sam v3 look + full-screen illustrations that change every few seconds.
Voice drives the mouth. Usage: python3 sam5.py <spec module> stills|render
The spec module defines VOICE (raw 16 kHz mono s16le), TOTAL, SCENES [(t0, t1, fn)], CAPS [(t0, t1, text)].
"""
import math, os, sys, importlib, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
import make_short as m
import look3 as L

W, H, FPS = 1080, 1920, 30
NAVY = (11, 19, 37); NAVY2 = (17, 27, 48); BLUE = (37, 99, 235); ACCENT = (96, 165, 250)
WHITE = (255, 255, 255); MUTED = (148, 163, 184); LIGHT = (199, 210, 254)
RED = (239, 68, 68); GREEN = (34, 197, 94); AMBER = (245, 177, 66); INK = (26, 26, 32)
F = L.F

def ease(u): u = max(0.0, min(1.0, u)); return 1 - (1 - u) ** 3
def pop(u):  # overshoot pop 0..1
    u = max(0.0, min(1.0, u)); return 1 + 2.2 * (u - 1) ** 3 + 1.2 * (u - 1) ** 2 if u < 1 else 1.0

# ---------- voice envelope ----------
ENV = None
def load_env(path):
    global ENV
    a = np.frombuffer(open(path, 'rb').read(), dtype=np.int16).astype(float) / 32768
    hop = 16000 // FPS
    n = len(a) // hop
    e = np.array([np.sqrt(np.mean(a[i * hop:(i + 1) * hop] ** 2)) for i in range(n)])
    e = e / (np.percentile(e, 95) + 1e-9)
    ENV = np.clip(e, 0, 1)
def mouth_at(t):
    i = int(t * FPS)
    if ENV is None or i >= len(ENV): return 0.0
    v = ENV[i]
    return 0.0 if v < 0.12 else min(1.0, v)

# ---------- Sam parts (cached) ----------
_hc = {}
def head(size, expr, t, blink_ok=True):
    mo = mouth_at(t); q = round(mo * 5) / 5
    blink = blink_ok and (t % 3.7) < 0.12
    key = (size, expr, q, blink)
    if key not in _hc:
        _hc[key] = L.head(size, expr, mouth=(q if q > 0 else None) if expr in ("smile", "talk", "serious", "surprised") else None, blink=blink)
    return _hc[key]
_bc = {}
def body(size):
    if size not in _bc: _bc[size] = L.body(size)
    return _bc[size]

def arm_wave(img, x, y, s, t):  # open palm wave beside Sam (no single finger)
    d = ImageDraw.Draw(img)
    ang = math.sin(t * 7) * 0.25
    ex, ey = x + 40 * s, y - 120 * s
    hx, hy = ex + math.sin(ang) * 30 * s, ey - 110 * s
    d.line([(x, y), (ex, ey)], fill=(28, 29, 34), width=int(46 * s))
    d.line([(ex, ey), (hx, hy)], fill=(28, 29, 34), width=int(40 * s))
    d.ellipse((hx - 34 * s, hy - 40 * s, hx + 34 * s, hy + 30 * s), fill=L.SKIN)  # palm
    for k in range(4):
        fx = hx - 26 * s + k * 17 * s
        d.rounded_rectangle((fx - 7 * s, hy - 78 * s, fx + 7 * s, hy - 26 * s), radius=int(7 * s), fill=L.SKIN)
    d.rounded_rectangle((hx + 26 * s, hy - 40 * s, hx + 44 * s, hy - 4 * s), radius=int(8 * s), fill=L.SKIN)

# ---------- shared drawing helpers ----------
def layer(): return Image.new("RGBA", (W, H), (0, 0, 0, 0))
def comp(img, lay, a=1.0):
    if a < 1: lay.putalpha(lay.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(lay)
def card(img, box, title, sub=None, color=WHITE, tcol=INK, u=1.0, icon=None, title_size=54):
    if u <= 0: return
    lay = layer(); d = ImageDraw.Draw(lay)
    x0, y0, x1, y1 = box; dy = 40 * (1 - ease(u))
    d.rounded_rectangle((x0, y0 + dy, x1, y1 + dy), radius=34, fill=color + (245,))
    tx = x0 + 40
    if icon:
        icon(d, x0 + 80, (y0 + y1) / 2 + dy); tx = x0 + 150
    d.text((tx, y0 + 34 + dy), title, font=F("ExtraBold", title_size), fill=tcol)
    if sub: d.text((tx, y0 + 34 + title_size + 18 + dy), sub, font=F("SemiBold", 38), fill=(71, 85, 105))
    comp(img, lay, ease(u))
def badge(d, cx, cy, ok, r=44):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GREEN if ok else RED)
    if ok: d.line([(cx - r * .45, cy), (cx - r * .1, cy + r * .38), (cx + r * .5, cy - r * .35)], fill=WHITE, width=int(r * .28), joint="curve")
    else:
        for sg in (1, -1): d.line([(cx - r * .4, cy - sg * r * .4), (cx + r * .4, cy + sg * r * .4)], fill=WHITE, width=int(r * .28))
def stamp(img, text, cx, cy, color, u, ang=-12, size=150):
    if u <= 0: return
    sc = pop(min(1, u * 1.6)) if u < 1 else 1
    f = F("ExtraBold", size); w = f.getlength(text) + 80; h = size + 60
    s = Image.new("RGBA", (int(w), int(h)), (0, 0, 0, 0)); d = ImageDraw.Draw(s)
    d.rounded_rectangle((6, 6, w - 6, h - 6), radius=24, outline=color + (255,), width=14)
    d.text((w / 2, h / 2), text, font=f, fill=color + (255,), anchor="mm")
    s = s.rotate(ang, expand=True, resample=Image.BICUBIC)
    s = s.resize((max(1, int(s.width * sc * (2 - min(1, u * 1.6)))), max(1, int(s.height * sc * (2 - min(1, u * 1.6))))), Image.BICUBIC)
    a = min(1, u * 3); s.putalpha(s.getchannel("A").point(lambda v: int(v * a)))
    img.alpha_composite(s, (int(cx - s.width / 2), int(cy - s.height / 2)))
def pill(img, cx, y, text, bg=BLUE, fg=WHITE, size=56, u=1.0):
    if u <= 0: return
    lay = layer(); d = ImageDraw.Draw(lay); f = F("ExtraBold", size)
    w = f.getlength(text) + 90; dy = 30 * (1 - ease(u))
    d.rounded_rectangle((cx - w / 2, y + dy, cx + w / 2, y + size + 50 + dy), radius=(size + 50) // 2, fill=bg + (255,))
    d.text((cx, y + (size + 50) / 2 + dy), text, font=f, fill=fg, anchor="mm")
    comp(img, lay, ease(u))
def clock(d, cx, cy, r, hh, mm, face=(241, 245, 249), ink=INK):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=face, outline=(51, 65, 85), width=max(3, r // 10))
    for k in range(12):
        a = k / 12 * 2 * math.pi
        d.line([(cx + math.sin(a) * r * .8, cy - math.cos(a) * r * .8), (cx + math.sin(a) * r * .9, cy - math.cos(a) * r * .9)], fill=ink, width=max(2, r // 18))
    am = mm / 60 * 2 * math.pi; ah = (hh % 12 + mm / 60) / 12 * 2 * math.pi
    d.line([(cx, cy), (cx + math.sin(ah) * r * .5, cy - math.cos(ah) * r * .5)], fill=ink, width=max(3, r // 9))
    d.line([(cx, cy), (cx + math.sin(am) * r * .75, cy - math.cos(am) * r * .75)], fill=ink, width=max(2, r // 13))
def digital(d, x, y, text, size=64, col=(248, 113, 113)):
    f = F("ExtraBold", size); w = f.getlength(text)
    d.rounded_rectangle((x - 20, y - 14, x + w + 20, y + size + 18), radius=14, fill=(12, 12, 16))
    d.text((x, y), text, font=f, fill=col)
def person(d, cx, cy, s=1.0, shirt=(148, 163, 184), skin=(222, 178, 140), hair=(70, 52, 40), pose="sit"):
    """Generic flat person (not Sam), head centre at (cx, cy)."""
    d.rounded_rectangle((cx - 120 * s, cy + 70 * s, cx + 120 * s, cy + 400 * s), radius=int(90 * s), fill=shirt)  # torso
    d.rectangle((cx - 28 * s, cy + 40 * s, cx + 28 * s, cy + 90 * s), fill=skin)  # neck
    d.ellipse((cx - 70 * s, cy - 80 * s, cx + 70 * s, cy + 80 * s), fill=skin)
    d.chord((cx - 74 * s, cy - 92 * s, cx + 74 * s, cy + 40 * s), 180, 360, fill=hair)
    for sg in (-1, 1):
        d.ellipse((cx + sg * 26 * s - 8 * s, cy - 8 * s, cx + sg * 26 * s + 8 * s, cy + 8 * s), fill=INK)
    d.arc((cx - 24 * s, cy + 20 * s, cx + 24 * s, cy + 46 * s), 20, 160, fill=(150, 90, 80), width=int(5 * s))
def arms_on_rests(d, cx, cy, s, shirt, skin, sensors=True):
    for sg in (-1, 1):
        sx = cx + sg * 118 * s
        d.line([(sx, cy + 120 * s), (sx + sg * 30 * s, cy + 300 * s), (sx + sg * 120 * s, cy + 340 * s)], fill=shirt, width=int(56 * s), joint="curve")
        hx = sx + sg * 150 * s; hy = cy + 345 * s
        d.ellipse((hx - 34 * s, hy - 26 * s, hx + 34 * s, hy + 26 * s), fill=skin)
        if sensors:
            for k in range(2):
                fx = hx + sg * (-10 + k * 22) * s
                d.rounded_rectangle((fx - 9 * s, hy - 36 * s, fx + 9 * s, hy - 12 * s), radius=int(4 * s), fill=(96, 165, 250))
            d.line([(hx, hy - 30 * s), (hx + sg * 70 * s, hy + 120 * s)], fill=(120, 128, 140), width=int(5 * s))
    if sensors:  # blood-pressure cuff on the right upper arm + two chest bands
        d.rounded_rectangle((cx + 100 * s, cy + 150 * s, cx + 170 * s, cy + 220 * s), radius=int(14 * s), fill=(30, 58, 138))
        for yy in (190, 270):
            d.rounded_rectangle((cx - 122 * s, cy + yy * s, cx + 122 * s, cy + (yy + 22) * s), radius=int(10 * s), fill=(51, 65, 85))
def wave_line(d, box, t, amp=0.25, freq=0.33, spike=0.0, col=ACCENT, phase=0, label=None):
    x0, y0, x1, y1 = box; mid = (y0 + y1) / 2; h = (y1 - y0)
    pts = []
    for i in range(121):
        x = x0 + (x1 - x0) * i / 120
        v = math.sin(i * freq + t * 4 + phase)
        if spike and i > 70: v *= 1 + spike * (1 + math.sin(i * 1.7))
        pts.append((x, mid + h * amp * v))
    d.line(pts, fill=col, width=6)
    if label: d.text((x0, y0 - 10), label, font=F("SemiBold", 30), fill=col)

# ---------- backgrounds ----------
def bg(t, top=(14, 24, 46), bottom=NAVY):
    img = Image.new("RGBA", (W, H), NAVY + (255,))
    g = Image.linear_gradient("L").resize((W, H))
    c = Image.new("RGBA", (W, H), top + (255,)); img.paste(c, (0, 0), g.point(lambda v: 255 - v))
    return img
def frame_box(img, draw_fn, t, lt, zoom=0.04):
    """Full-screen illustration in the scene area with a slow push-in."""
    S = Image.new("RGBA", (W, 1260), (0, 0, 0, 0)); draw_fn(S, t, lt)
    c0 = S.getpixel((4, 4)); c1 = S.getpixel((4, 1255))
    if c0[3] == 255: ImageDraw.Draw(img).rectangle((0, 0, W, 280), fill=c0)
    if c1[3] == 255: ImageDraw.Draw(img).rectangle((0, 1520, W, H), fill=c1)
    z = 1 + zoom * min(1, lt / 4)
    S2 = S.resize((int(W * z), int(1260 * z)), Image.BICUBIC)
    S2 = S2.crop(((S2.width - W) // 2, (S2.height - 1260) // 2, (S2.width - W) // 2 + W, (S2.height - 1260) // 2 + 1260))
    img.alpha_composite(S2, (0, 270))
def sam_inset(img, t, expr="talk"):
    cx, cy, r = 905, 1385, 128
    lay = layer(); d = ImageDraw.Draw(lay)
    d.ellipse((cx - r - 8, cy - r - 8, cx + r + 8, cy + r + 8), fill=ACCENT + (255,))
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=NAVY2 + (255,))
    hd = head(0.42, expr, t); bd = body(0.5)
    inner = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
    inner.alpha_composite(bd, (r - bd.width // 2, int(r * 1.22)))
    inner.alpha_composite(hd, (r - hd.width // 2, int(r * 0.05)))
    mask = Image.new("L", (2 * r, 2 * r), 0); ImageDraw.Draw(mask).ellipse((0, 0, 2 * r - 1, 2 * r - 1), fill=255)
    lay.paste(inner, (cx - r, cy - r), Image.composite(inner.getchannel("A"), Image.new("L", inner.size, 0), mask))
    img.alpha_composite(lay)

# ---------- Sam shots ----------
_desk = {}
def desk_bg():
    if "d" in _desk: return _desk["d"]
    P = Image.new("RGBA", (W, 1260), (0, 0, 0, 0)); d = ImageDraw.Draw(P)
    yb = 900
    d.polygon([(0, yb), (W, yb), (W, 1260), (0, 1260)], fill=(46, 37, 32)); d.rectangle((0, yb, W, yb + 18), fill=(70, 56, 46))
    d.rounded_rectangle((60, yb - 95, 370, yb + 5), radius=14, fill=(20, 22, 28)); d.rectangle((60, yb - 95, 370, yb - 80), fill=(40, 44, 54))
    for k in range(5): d.ellipse((85 + k * 55, yb - 55, 110 + k * 55, yb - 30), fill=(60, 64, 76))
    d.ellipse((320, yb - 60, 342, yb - 38), fill=(34, 197, 94))
    d.polygon([(700, yb + 5), (1010, yb + 5), (980, yb - 185), (730, yb - 185)], fill=(51, 65, 85)); d.polygon([(670, yb + 5), (1040, yb + 5), (1050, yb + 25), (660, yb + 25)], fill=(71, 85, 105))
    m.draw_mark(P, 830, yb - 125, 50)
    d.line([(110, yb + 5), (90, yb + 120), (200, yb + 230)], fill=(120, 128, 140), width=9)
    d.line([(170, yb + 5), (230, yb + 140), (390, yb + 200)], fill=(120, 128, 140), width=9)
    d.rounded_rectangle((170, yb + 210, 240, yb + 260), radius=10, fill=(148, 163, 184))
    d.rounded_rectangle((500, yb + 90, 780, yb + 170), radius=26, fill=(30, 58, 138))
    _desk["d"] = P; return P
def sam_desk(img, t, lt, expr="talk", wave=False, screen=True, top=None):
    S = Image.new("RGBA", (W, 1260), (0, 0, 0, 0)); d = ImageDraw.Draw(S)
    if screen:
        L.chart_screen(d, (90, 60, 990, 400), t=t * 2)
    bd = body(0.82); hd = head(0.6, expr, t)
    S.alpha_composite(bd, (W // 2 - bd.width // 2, 640))
    S.alpha_composite(hd, (W // 2 - hd.width // 2, 330))
    if wave: arm_wave(S, W // 2 + 200, 820, 1.0, t)
    S.alpha_composite(desk_bg())
    img.alpha_composite(S, (0, 270))
    if top: top(img, t, lt)
def sam_close(img, t, lt, expr="talk"):
    S = Image.new("RGBA", (W, 1260), (0, 0, 0, 0))
    g = Image.radial_gradient("L").resize((1600, 1600)).point(lambda v: int(120 * max(0, 1 - v / 128) ** 1.5))
    S.paste(Image.new("RGBA", (1600, 1600), BLUE + (255,)), (W // 2 - 800, -350), g)
    bd = body(1.35); hd = head(1.02, expr, t)
    S.alpha_composite(bd, (W // 2 - bd.width // 2, 905))
    S.alpha_composite(hd, (W // 2 - hd.width // 2, 300))
    img.alpha_composite(S, (0, 270))

# ---------- captions + chrome ----------
def captions(img, t, CAPS):
    for a, b, txt in CAPS:
        if a <= t < b:
            lay = layer(); d = ImageDraw.Draw(lay); f = F("Bold", 44)
            words = txt.split(); lines = []; cur = ""
            for w_ in words:
                if f.getlength(cur + " " + w_) > 900: lines.append(cur); cur = w_
                else: cur = (cur + " " + w_).strip()
            lines.append(cur)
            y = 1540 - 30 * (len(lines) - 1)
            hgt = 62 * len(lines) + 34
            maxw = max(f.getlength(l) for l in lines)
            d.rounded_rectangle((W / 2 - maxw / 2 - 30, y - 18, W / 2 + maxw / 2 + 30, y - 18 + hgt), radius=22, fill=(8, 12, 24, 215))
            for k, l in enumerate(lines): d.text((W / 2, y + k * 62), l, font=f, fill=WHITE, anchor="ma")
            img.alpha_composite(lay)
def chrome(img, t):
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 205), fill=NAVY); d.rectangle((0, 1670, W, H), fill=NAVY)
    m.draw_mark(img, 60, 70, 76)
    d.text((158, 76), "Axeligence", font=F("ExtraBold", 44), fill=WHITE)
    d.text((160, 128), "1-on-1 Polygraph Preparation & Rights Advisory", font=F("Medium", 24), fill=MUTED)
    d.rounded_rectangle((60, 1690, W - 60, 1698), radius=4, fill=(30, 41, 59))
    d.rounded_rectangle((60, 1690, 60 + (W - 120) * min(1, t / m.TOTAL), 1698), radius=4, fill=BLUE)
    d.text((W - 60, 1730), "axeligence.com", font=F("Medium", 32), fill=MUTED, anchor="ra")

def frame(spec, t):
    img = bg(t)
    for a, b, fn in spec.SCENES:
        if a <= t < b:
            fn(img, t, t - a)
            # quick white flash-fade at each cut for energy
            if t - a < 0.12 and a > 0:
                fl = Image.new("RGBA", (W, H), (255, 255, 255, int(70 * (1 - (t - a) / 0.12)))); img.alpha_composite(fl)
            break
    captions(img, t, spec.CAPS); chrome(img, t)
    return img.convert("RGB")

if __name__ == "__main__":
    spec = importlib.import_module(sys.argv[1]); load_env(spec.VOICE); m.TOTAL = spec.TOTAL
    out = sys.argv[1]
    if sys.argv[2] == "stills":
        ts = [float(x) for x in sys.argv[3].split(",")]
        ims = [frame(spec, t).resize((270, 480)) for t in ts]
        sheet = Image.new("RGB", (270 * len(ims), 480))
        for i, im in enumerate(ims): sheet.paste(im, (i * 270, 0))
        sheet.save(out + "_stills.png")
    elif sys.argv[2] == "one":
        frame(spec, float(sys.argv[3])).save(out + "_one.png")
    else:
        n = int(spec.TOTAL * FPS)
        tmp = out + "_video.tmp.mp4"
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                              "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
        for k in range(n): p.stdin.write(frame(spec, k / FPS).tobytes())
        p.stdin.close(); assert p.wait() == 0
        os.replace(tmp, out + "_video.mp4")
