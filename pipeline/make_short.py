"""Axeligence sample YouTube Short / Reel: 'There is no lie signal'.
1080x1920, 30 fps, brand colours from axeligence.com."""
import math, os, subprocess, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter

W, H, FPS = 1080, 1920, 30
NAVY = (11, 19, 37)
BLUE = (37, 99, 235)
ACCENT = (96, 165, 250)
LIGHT = (199, 210, 254)
WHITE = (255, 255, 255)
MUTED = (148, 163, 184)
TRACK = (30, 41, 59)
FD = "/usr/share/fonts/opentype/inter/"
def F(w, s): return ImageFont.truetype(FD + f"Inter-{w}.otf", s)

OUT = os.path.dirname(os.path.abspath(__file__))
TOTAL = 19.0

# ---------- logo mark (from the site's SVG, viewBox 14 14 74 74) ----------
P1 = "M36.4 22.6Q36.6 19.6 40 19.8L47.4 20.6Q52.4 21.2 55.2 27L78.6 76.2Q80.6 80.4 76.2 80.2L64.2 79.6Q61.4 79.4 60.4 76.8Z"
P2 = "M31.4 54.8Q36.6 54.2 38.6 59.4L46.6 77Q47.4 78.8 45 79Q38 80.4 31.8 77Q22.4 72 20.6 64.6Q19.8 57 31.4 54.8Z"
def path_pts(d):
    import re
    toks = re.findall(r"[MLQZ]|-?\d+\.?\d*", d)
    pts, i, cur, cmd = [], 0, (0, 0), None
    while i < len(toks):
        t = toks[i]
        if t in "MLQZ":
            cmd = t; i += 1
            if t == "Z": break
            continue
        if cmd in "ML":
            cur = (float(toks[i]), float(toks[i+1])); pts.append(cur); i += 2
        elif cmd == "Q":
            c = (float(toks[i]), float(toks[i+1])); e = (float(toks[i+2]), float(toks[i+3])); i += 4
            for k in range(1, 9):
                u = k / 8
                pts.append(((1-u)**2*cur[0] + 2*(1-u)*u*c[0] + u*u*e[0], (1-u)**2*cur[1] + 2*(1-u)*u*c[1] + u*u*e[1]))
            cur = e
    return pts
MARK = [path_pts(P1), path_pts(P2)]
def draw_mark(img, x, y, size, color=ACCENT, alpha=1.0):
    s = size / 74
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    for poly in MARK:
        d.polygon([(x + (px-14)*s, y + (py-14)*s) for px, py in poly], fill=color + (int(255*alpha),))
    img.alpha_composite(layer)

# ---------- background: navy + soft drifting blue glow ----------
def glow(radius, strength):
    # smooth radial falloff that reaches 0 well inside the square, so no edges show
    g = Image.radial_gradient("L").resize((radius*2, radius*2), Image.BICUBIC)
    return g.point(lambda v: int(strength * max(0.0, 1 - v/128) ** 2))
G1, G2 = glow(700, 70), glow(520, 45)
def background(t):
    bg = Image.new("RGBA", (W, H), NAVY + (255,))
    blue = Image.new("RGBA", G1.size, BLUE + (255,))
    x1 = int(W*0.62 + 60*math.sin(t*0.35)) - 700; y1 = int(H*0.12 + 40*math.cos(t*0.3)) - 700
    bg.paste(blue, (x1, y1), G1)
    blue2 = Image.new("RGBA", G2.size, BLUE + (255,))
    x2 = int(W*0.15 + 50*math.cos(t*0.25)) - 520; y2 = int(H*0.92 + 30*math.sin(t*0.4)) - 520
    bg.paste(blue2, (x2, y2), G2)
    return bg

def ease(u): u = max(0.0, min(1.0, u)); return 1 - (1-u)**3

def text(img, xy, s, font, color, t, t0, dur=0.45, rise=40, anchor="la"):
    """Fade + rise in starting at t0."""
    u = ease((t - t0) / dur)
    if u <= 0: return
    layer = Image.new("RGBA", img.size, (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    d.text((xy[0], xy[1] + rise*(1-u)), s, font=font, fill=color + (int(255*u),), anchor=anchor)
    img.alpha_composite(layer)

def chrome(img, t, show_swipe=True):
    d = ImageDraw.Draw(img)
    draw_mark(img, 84, 150, 92)
    d.text((200, 158), "Axeligence", font=F("ExtraBold", 50), fill=WHITE)
    d.text((202, 218), "1-on-1 Polygraph Preparation & Rights Advisory", font=F("Medium", 26), fill=MUTED)
    # progress bar
    d.rounded_rectangle((84, 1700, W-84, 1708), radius=4, fill=TRACK)
    d.rounded_rectangle((84, 1700, 84 + (W-168)*min(1, t/TOTAL), 1708), radius=4, fill=BLUE)
    d.text((W-84, 1745), "axeligence.com", font=F("Medium", 34), fill=MUTED, anchor="ra")

BIG = F("ExtraBold", 132); MID = F("ExtraBold", 104); LBL = F("Bold", 44); SM = F("SemiBold", 46)

# ---------- scenes: (start, end, draw(img, t_global, t_local)) ----------
def s1(img, t, lt):  # hook
    text(img, (84, 640), "MYTH", LBL, ACCENT, lt, 0.0)
    for i, (w, y) in enumerate([("A polygraph", 720), ("detects", 870), ("lies.", 1020)]):
        text(img, (84, y), w, BIG, WHITE, lt, 0.25 + i*0.35)
    if lt > 2.3:  # strike through "lies."
        u = ease((lt-2.3)/0.35); d = ImageDraw.Draw(img)
        wl = BIG.getlength("lies"); top = 1020 + BIG.getbbox("lies")[1]; bot = 1020 + BIG.getbbox("lies")[3]
        ym = int(top + (bot - top) * 0.58)
        d.rectangle((80, ym - 7, 84 + (wl + 8)*u, ym + 7), fill=BLUE)
def s2(img, t, lt):
    text(img, (84, 640), "FACT", LBL, ACCENT, lt, 0.0)
    text(img, (84, 720), "It measures", BIG, WHITE, lt, 0.2)
    text(img, (84, 870), "stress.", BIG, ACCENT, lt, 0.55)
    text(img, (84, 1060), "Breathing. Heart rate. Sweat.", SM, MUTED, lt, 1.2)
def s3(img, t, lt):
    text(img, (84, 560), "And stress looks the same", SM, MUTED, lt, 0.0)
    text(img, (84, 620), "whatever causes it:", SM, MUTED, lt, 0.0)
    for i, (w, y) in enumerate([("Fear.", 760), ("Embarrassment.", 900), ("Anger.", 1040)]):
        text(img, (84, y), w, MID, WHITE if i != 1 else LIGHT, lt, 0.6 + i*0.55)
def s4(img, t, lt):
    text(img, (84, 700), "That's why", MID, WHITE, lt, 0.0)
    text(img, (84, 830), "honest people", MID, WHITE, lt, 0.3)
    text(img, (84, 960), "can fail.", MID, ACCENT, lt, 0.6)
def s5(img, t, lt):  # CTA, centred
    u = ease(lt/0.6)
    draw_mark(img, W/2 - 120, 560 + 40*(1-u), 240, alpha=u)
    text(img, (W/2, 900), "Know the test", MID, WHITE, lt, 0.4, anchor="ma")
    text(img, (W/2, 1030), "before you take it.", MID, ACCENT, lt, 0.7, anchor="ma")
    text(img, (W/2, 1220), "Free guide: link in bio", SM, MUTED, lt, 1.2, anchor="ma")

SCENES = [(0.0, 3.2, s1), (3.2, 6.6, s2), (6.6, 10.6, s3), (10.6, 14.2, s4), (14.2, TOTAL, s5)]
FADE = 0.25

def frame(t, idx):
    a, b, fn = SCENES[idx]
    img = background(t); chrome(img, t)
    lt = t - a
    scene = Image.new("RGBA", (W, H), (0, 0, 0, 0)); fn(scene, t, lt)
    # fade the scene out at its end (except the last)
    alpha = 1.0
    if idx < len(SCENES)-1 and t > b - FADE: alpha = max(0, (b - t)/FADE)
    if alpha < 1:
        scene.putalpha(scene.getchannel("A").point(lambda v: int(v*alpha)))
    img.alpha_composite(scene)
    return img.convert("RGB")

def render_scene(idx):
    a, b, _ = SCENES[idx]
    n = round((b - a) * FPS)
    tmp = os.path.join(OUT, f"scene{idx}.tmp.mp4"); final = os.path.join(OUT, f"scene{idx}.mp4")
    p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}",
                          "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", tmp], stdin=subprocess.PIPE)
    for k in range(n):
        p.stdin.write(frame(a + k/FPS, idx).tobytes())
    p.stdin.close(); assert p.wait() == 0
    os.replace(tmp, final)

if __name__ == "__main__":
    if sys.argv[1] == "stills":
        for t in [2.9, 5.5, 9.8, 13.6, 17.5]:
            idx = next(i for i, (a, b, _) in enumerate(SCENES) if a <= t < b)
            frame(t, idx).save(os.path.join(OUT, f"still_{t}.png"))
    else:
        for i in range(len(SCENES)): render_scene(i)
        with open(os.path.join(OUT, "list.txt"), "w") as f:
            for i in range(len(SCENES)): f.write(f"file 'scene{i}.mp4'\n")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", os.path.join(OUT, "list.txt"),
                        "-c", "copy", "-movflags", "+faststart", os.path.join(OUT, "axeligence-short-no-lie-signal.mp4")], check=True)
