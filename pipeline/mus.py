"""Original ambient bed for Axeligence shorts (no third-party samples, so no licensing issues).
Calm, slightly tense, then resolving. Chord changes land on the video's scene cuts."""
import numpy as np, sys
from scipy.signal import fftconvolve, butter, sosfilt
from scipy.io import wavfile

SR = 48000
TOTAL = float(sys.argv[2])
CUTS = [0.0] + [float(x) for x in sys.argv[3].split(",")] + [TOTAL]
HB = [float(x) for x in sys.argv[4].split(",")]
# chord tones as MIDI notes: Am, Fmaj7, C(add9), G, C(add9) resolve
CHORDS = [[57, 60, 64, 69], [53, 57, 60, 64], [48, 55, 62, 64], [55, 59, 62, 67], [48, 55, 60, 62, 64]]
BASS = [45, 41, 36, 43, 36]
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)
N = int(SR * TOTAL); t = np.arange(N) / SR
rng = np.random.default_rng(7)

def env(n, a, r):
    e = np.ones(n); A = int(a*SR); R = int(r*SR)
    e[:A] = np.linspace(0, 1, A) ** 2
    e[-R:] *= np.linspace(1, 0, R) ** 1.5
    return e

def lp(x, f, order=2):
    return sosfilt(butter(order, f, fs=SR, output="sos"), x)

pad = np.zeros(N); bass = np.zeros(N); arp = np.zeros(N); fx = np.zeros(N)
BASE_CH = CHORDS; BASE_B = BASS
CHORDS = [BASE_CH[i % 4] for i in range(len(CUTS) - 2)] + [BASE_CH[4]]
BASS = [BASE_B[i % 4] for i in range(len(CUTS) - 2)] + [BASE_B[4]]
for i, ch in enumerate(CHORDS):
    a, b = CUTS[i], CUTS[i+1]
    s0 = int(a*SR); s1 = min(N, int((b + 0.6)*SR))  # overlap into next chord
    n = s1 - s0; tt = np.arange(n) / SR
    e = env(n, 0.9, 0.9)
    for m in ch:
        f = hz(m)
        for det in (-0.12, 0.0, 0.12):  # soft detuned sines + a little 2nd harmonic
            ph = rng.uniform(0, 2*np.pi)
            v = np.sin(2*np.pi*f*(1+det/100)*tt + ph) + 0.18*np.sin(4*np.pi*f*tt + ph)
            pad[s0:s1] += 0.05 * v * e
    fb = hz(BASS[i]); bass[s0:s1] += 0.22 * np.sin(2*np.pi*fb*tt) * env(n, 0.4, 0.8)
    # gentle 8th-note pluck arpeggio from the second scene on
    if i >= 1:
        step = 60/96/2
        k = 0; tn = a
        while tn < b - 0.05:
            m = ch[[0, 2, 1, 3][k % 4] % len(ch)] + 12
            p0 = int(tn*SR); L = int(0.5*SR); p1 = min(N, p0+L); ln = p1-p0
            tp = np.arange(ln)/SR
            note = np.sin(2*np.pi*hz(m)*tp) * np.exp(-tp*9) * (0.06 if k % 4 == 0 else 0.04)
            arp[p0:p1] += note
            k += 1; tn += step
# soft riser into each cut
for c in CUTS[1:-1]:
    L = int(0.7*SR); p1 = int(c*SR); p0 = p1 - L
    noise = rng.normal(0, 1, L)
    sweep = lp(noise, 2500) * np.linspace(0, 1, L) ** 3 * 0.05
    fx[p0:p1] += sweep
# low heartbeat thump in scene 3-4 (the "stress" part), subtle
for c0, c1 in [(HB[0], HB[1])]:
    tn = c0
    while tn < c1:
        for off, amp in ((0, 0.25), (0.22, 0.14)):
            p0 = int((tn+off)*SR); L = int(0.25*SR); tp = np.arange(L)/SR
            fx[p0:p0+L] += amp * np.sin(2*np.pi*(55 - 20*tp)*tp) * np.exp(-tp*18)
        tn += 60/64  # ~64 bpm heartbeat

mix = lp(pad, 1800) + bass + lp(arp, 4000) + fx
# reverb: exponentially decaying noise IR
ir_len = int(2.2*SR); tir = np.arange(ir_len)/SR
ir = rng.normal(0, 1, ir_len) * np.exp(-tir*2.6); ir = lp(ir, 5000); ir /= np.sqrt((ir**2).sum())
wet = fftconvolve(mix, ir)[:N]
out = 0.75*mix + 0.45*wet
# stereo widen with a short delay on the wet path
L = out; R = np.concatenate([np.zeros(int(0.012*SR)), out])[:N] * 0.97 + 0.03*out
st = np.stack([L, R], 1)
st *= env(N, 0.6, 1.8)[:, None]
st /= np.abs(st).max() * 1.12
wavfile.write(sys.argv[1], SR, (st * 32767).astype(np.int16))
