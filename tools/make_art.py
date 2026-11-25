"""
Redraws the artwork: Seshan's avatar (docs/seshan.svg), the PetriPath icon (docs/icon.svg and its PNGs)
and the Android launcher icon layers. Needs:  pip install resvg-py
Run from the repository root:  python tools/make_art.py
"""
import math, random, os
random.seed(11)
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "docs")

# ───────────────────────── Seshan avatar (MacConkey plate, Kirby–Bauer discs) ─────────────────────────
C, R = 210, 196
zones = [(104, 126, 44, "MEM"), (318, 108, 38, "IPM"), (78, 250, 34, "CAZ")]
cols = []
tries = 0
while len(cols) < 48 and tries < 8000:
    tries += 1
    a = random.uniform(0, 2 * math.pi); rad = random.uniform(36, 182)
    x, y = C + rad * math.cos(a), C + rad * math.sin(a)
    r = random.choice([3, 3.5, 4, 4.5, 5, 5.5, 6, 7])
    if rad + r > R - 4: continue
    if any(math.hypot(x - zx, y - zy) < zr + r + 3 for zx, zy, zr, _ in zones): continue
    if any(math.hypot(x - cx, y - cy) < r + cr + 2 for cx, cy, cr, _ in cols): continue
    cols.append((x, y, r, random.random() < 0.2))
col_svg = []
for i, (x, y, r, pale) in enumerate(cols):
    d = 0.25 + 0.03 * i
    if pale:
        col_svg.append(f'<circle class="col" style="animation-delay:{d:.2f}s" cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#FFF2F7" stroke="#EFA5C4" stroke-width="1"/>')
    else:
        col_svg.append(f'<g class="col" style="animation-delay:{d:.2f}s"><circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" fill="#DD3477"/>'
                       f'<circle cx="{x - r*.32:.1f}" cy="{y - r*.32:.1f}" r="{r*.34:.1f}" fill="#FF9FC6" opacity=".85"/></g>')
zone_svg = []
for zx, zy, zr, lab in zones:
    zone_svg.append(f'<g><circle class="zone" cx="{zx}" cy="{zy}" r="{zr}" fill="#FFF6FA" opacity=".8"/>'
                    f'<circle cx="{zx}" cy="{zy}" r="{zr}" fill="none" stroke="#FFFFFF" stroke-opacity=".75" stroke-width="1.5"/>'
                    f'<circle cx="{zx}" cy="{zy}" r="12.5" fill="#FFFFFF" stroke="#E9B3CA" stroke-width="1.2"/>'
                    f'<text x="{zx}" y="{zy + 3.2}" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="8.6" font-weight="700" fill="#8C2152">{lab}</text></g>')

SKIN, SKIN_SH, SKIN_HI = "#8E5C3C", "#76492E", "#A06B49"
HAIR, HAIR_HI = "#16121C", "#3A3347"
SUIT, SUIT_SH, SUIT_HI, LAPEL = "#2E5AD6", "#2246AE", "#4A74EE", "#2650C2"
SHIRT, SHIRT_SH = "#F7F8FC", "#D9DEEA"

avatar = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 420 420" role="img" aria-labelledby="t d">
<title id="t">Dr Seshan Sivasankar</title>
<desc id="d">Illustrated avatar of Seshan in a royal-blue suit, pointing, inside a MacConkey agar plate with pink Klebsiella-like colonies and meropenem, imipenem and ceftazidime discs with zones of inhibition.</desc>
<style>
.col{{transform-box:fill-box;transform-origin:center;animation:grow 1.1s cubic-bezier(.2,.9,.25,1.25) both}}
@keyframes grow{{from{{transform:scale(0)}}to{{transform:scale(1)}}}}
.zone{{transform-box:fill-box;transform-origin:center;animation:zone 7s ease-in-out infinite}}
@keyframes zone{{0%,100%{{transform:scale(1)}}50%{{transform:scale(1.05)}}}}
.eyes{{transform-box:fill-box;transform-origin:center;animation:blink 5.5s infinite}}
@keyframes blink{{0%,93%,100%{{transform:scaleY(1)}}95.5%{{transform:scaleY(.1)}}}}
.arm{{transform-origin:298px 356px;animation:point 3.4s ease-in-out infinite}}
@keyframes point{{0%,100%{{transform:rotate(0deg)}}50%{{transform:rotate(-4deg)}}}}
.float{{animation:float 7s ease-in-out infinite}}
.float.b{{animation-duration:9s;animation-direction:reverse}}
@keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-7px)}}}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}}}
</style>
<defs>
  <radialGradient id="agar" cx="46%" cy="40%" r="62%">
    <stop offset="0" stop-color="#FFE6F0"/><stop offset=".55" stop-color="#FFBCD5"/><stop offset="1" stop-color="#EE76A6"/>
  </radialGradient>
  <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0" stop-color="#FFFFFF" stop-opacity=".95"/><stop offset=".5" stop-color="#E9DDFF" stop-opacity=".55"/><stop offset="1" stop-color="#FFFFFF" stop-opacity=".9"/>
  </linearGradient>
  <clipPath id="plate"><circle cx="{C}" cy="{C}" r="{R}"/></clipPath>
</defs>

<!-- plate -->
<circle cx="{C}" cy="{C}" r="{R + 8}" fill="none" stroke="url(#glass)" stroke-width="10"/>
<circle cx="{C}" cy="{C}" r="{R}" fill="url(#agar)"/>
<g clip-path="url(#plate)">
  {"".join(zone_svg)}
  {"".join(col_svg)}

  <!-- body -->
  <path d="M40 420C48 360 70 330 118 312C145 302 168 296 186 292L210 398L214 420Z" fill="{SUIT}"/>
  <path d="M380 420C372 360 350 330 302 312C275 302 252 296 234 292L210 398L206 420Z" fill="{SUIT}"/>
  <path d="M40 420C48 360 70 330 118 312L126 332C88 348 68 378 64 420Z" fill="{SUIT_SH}"/>
  <path d="M302 312C340 326 362 350 372 392L360 394C352 362 334 340 296 328Z" fill="{SUIT_HI}" opacity=".7"/>
  <path d="M186 292L234 292L210 398Z" fill="{SHIRT}"/>
  <path d="M210 302L218 324L210 396L202 324Z" fill="{SHIRT_SH}" opacity=".3"/>
  <path d="M186 292L166 320L183 333L172 347L210 398L195 330Z" fill="{LAPEL}" stroke="{SUIT_HI}" stroke-width="1.4" stroke-linejoin="round"/>
  <path d="M234 292L254 320L237 333L248 347L210 398L225 330Z" fill="{LAPEL}" stroke="{SUIT_HI}" stroke-width="1.4" stroke-linejoin="round"/>
  <circle cx="210" cy="405" r="4.2" fill="{SUIT_SH}" stroke="#1A3A92" stroke-width="1"/>
  <!-- neck and collar -->
  <path d="M192 258L228 258L233 298Q210 312 187 298Z" fill="{SKIN_SH}"/>
  <path d="M186 292L198 318L210 300Z" fill="{SHIRT}" stroke="{SHIRT_SH}" stroke-width="1.2" stroke-linejoin="round"/>
  <path d="M234 292L222 318L210 300Z" fill="{SHIRT}" stroke="{SHIRT_SH}" stroke-width="1.2" stroke-linejoin="round"/>
</g>

<!-- head -->
<ellipse cx="157" cy="212" rx="10" ry="15" fill="{SKIN_SH}"/><ellipse cx="159" cy="212" rx="5" ry="8" fill="#6A3F26"/>
<ellipse cx="263" cy="212" rx="10" ry="15" fill="{SKIN_SH}"/><ellipse cx="261" cy="212" rx="5" ry="8" fill="#6A3F26"/>
<path d="M160 196C160 160 182 142 210 142C238 142 260 160 260 196C260 232 248 258 226 268C216 273 204 273 194 268C172 258 160 232 160 196Z" fill="{SKIN}"/>
<path d="M238 152C254 164 262 186 260 206C258 236 246 258 226 268C240 250 247 228 246 204C245 182 242 166 238 152Z" fill="{SKIN_SH}" opacity=".55"/>
<path d="M176 160C186 150 198 146 210 146C200 152 188 158 182 170Z" fill="{SKIN_HI}" opacity=".5"/>
<!-- hair: short sides, swept-up quiff -->
<path d="M157 202C150 172 154 148 170 134C182 122 196 115 212 115C230 113 248 120 259 134C270 148 268 174 263 202C259 186 253 172 245 165C236 157 224 153 210 153C194 153 181 158 173 168C165 178 160 190 157 202Z" fill="{HAIR}"/>
<path d="M178 132C188 106 220 96 246 106C258 111 262 120 260 130C250 120 236 117 222 120C208 123 196 128 186 140Z" fill="{HAIR}"/>
<path d="M196 118C208 106 228 102 244 108C232 110 220 114 210 121C204 125 199 128 194 132Z" fill="{HAIR_HI}" opacity=".75"/>
<path d="M160 188L167 186L168 210L162 206Z" fill="{HAIR}"/><path d="M260 188L253 186L252 210L258 206Z" fill="{HAIR}"/>
<!-- face -->
<path d="M177 186Q189 179 201 184" fill="none" stroke="#1A141F" stroke-width="4.6" stroke-linecap="round"/>
<path d="M219 184Q231 179 243 186" fill="none" stroke="#1A141F" stroke-width="4.6" stroke-linecap="round"/>
<g class="eyes">
  <ellipse cx="190" cy="203" rx="6.2" ry="7.2" fill="#1B1418"/><ellipse cx="230" cy="203" rx="6.2" ry="7.2" fill="#1B1418"/>
  <circle cx="192.2" cy="200.2" r="2.1" fill="#FFFFFF"/><circle cx="232.2" cy="200.2" r="2.1" fill="#FFFFFF"/>
</g>
<path d="M210 207C207 218 205 226 212 229C216 230 219 228 220 226" fill="none" stroke="#6A3F26" stroke-width="2.6" stroke-linecap="round"/>
<ellipse cx="180" cy="231" rx="9" ry="5" fill="#B36A4B" opacity=".35"/><ellipse cx="240" cy="231" rx="9" ry="5" fill="#B36A4B" opacity=".35"/>
<path d="M192 241Q210 257 228 241Q210 249 192 241Z" fill="#FFFFFF" stroke="#4B2216" stroke-width="2.6" stroke-linejoin="round"/>

<!-- pointing arm: the hand breaks out of the plate -->
<g class="arm">
  <path d="M298 356L349 284" stroke="#1F40A0" stroke-width="39" stroke-linecap="round"/>
  <path d="M298 356L349 284" stroke="{SUIT}" stroke-width="34" stroke-linecap="round"/>
  <path d="M306 344L344 290" stroke="{SUIT_HI}" stroke-width="5" stroke-linecap="round" opacity=".55"/>
  <path d="M336 278L358 293" stroke="{SHIRT}" stroke-width="9" stroke-linecap="round"/>
  <ellipse cx="354" cy="266" rx="16.5" ry="14.5" fill="{SKIN}"/>
  <rect x="358" y="254" width="46" height="11.5" rx="5.75" fill="{SKIN}"/>
  <rect x="343" y="232" width="11.5" height="27" rx="5.75" fill="{SKIN}"/>
  <path d="M344 270Q355 275 366 270M345 278Q355 282 365 277" fill="none" stroke="{SKIN_SH}" stroke-width="2" stroke-linecap="round"/>
</g>

<!-- drifting microbes -->
<g transform="translate(52 52) rotate(-28)"><g class="float">
  <rect x="-24" y="-9" width="48" height="18" rx="9" fill="#FF4F9A"/><rect x="-18" y="-5" width="20" height="5" rx="2.5" fill="#FFB3D3" opacity=".8"/>
  <path d="M24 0C32 -7 38 7 46 0S60 -7 66 0" fill="none" stroke="#FF4F9A" stroke-width="2.4" stroke-linecap="round"/>
</g></g>
<g transform="translate(378 44)"><g class="float b">
  <path d="M0 -17L14.7 -8.5L14.7 8.5L0 17L-14.7 8.5L-14.7 -8.5Z" fill="#8F6BFF"/>
  <rect x="-3.5" y="17" width="7" height="18" rx="2" fill="#8F6BFF"/>
  <path d="M-3.5 35L-13 46M3.5 35L13 46M0 35L0 47" stroke="#8F6BFF" stroke-width="2.6" stroke-linecap="round"/>
</g></g>
<g transform="translate(40 380)"><g class="float">
  <circle r="19" fill="none" stroke="#2FC7D3" stroke-width="5"/>
  <path d="M-13.4 -13.4A19 19 0 0 1 13.4 -13.4" fill="none" stroke="#9BE03A" stroke-width="6" stroke-linecap="round"/>
  <text y="4" text-anchor="middle" font-family="Arial, Helvetica, sans-serif" font-size="8.5" font-weight="700" fill="#2FC7D3">mcr-1</text>
</g></g>
</svg>'''
open(f"{OUT}/seshan.svg", "w").write(avatar)

# ───────────────────────── App icon: a Petri dish whose colonies grow into a path ─────────────────────────
DISH = dict(cx=54, cy=54, r=26, sw=4.4)
AGAR_R = 24
ZONE = (44, 41.5, 7.2, 3.3)
COLS = [(41.5, 66, 3.7, "#C8FF5E"), (50.5, 59, 3.3, "#C8FF5E"), (59, 51.8, 2.9, "#7FF6FF"), (66.5, 45.6, 2.5, "#7FF6FF")]
ARROW = [(75.5, 36.5), (66.2, 37.6), (74.4, 45.8)]

def fg_svg(scale, mono=False):
    s = lambda v: f"{v * scale:.2f}"
    w = "#FFFFFF"
    out = [f'<circle cx="{s(54)}" cy="{s(54)}" r="{s(AGAR_R)}" fill="{w}" fill-opacity=".16"/>',
           f'<circle cx="{s(ZONE[0])}" cy="{s(ZONE[1])}" r="{s(ZONE[2])}" fill="{w}" fill-opacity=".3"/>',
           f'<circle cx="{s(ZONE[0])}" cy="{s(ZONE[1])}" r="{s(ZONE[3])}" fill="{w}"/>',
           f'<circle cx="{s(54)}" cy="{s(54)}" r="{s(26)}" fill="none" stroke="{w}" stroke-width="{s(4.4)}"/>']
    for x, y, r, c in COLS:
        out.append(f'<circle cx="{s(x)}" cy="{s(y)}" r="{s(r)}" fill="{w if mono else c}"/>')
    out.append('<path d="M' + " L".join(f"{s(x)} {s(y)}" for x, y in ARROW) + ' Z" fill="#FFFFFF" stroke="#FFFFFF" stroke-width="' + s(1.2) + '" stroke-linejoin="round"/>')
    return "".join(out)

BG = '<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#6A3BF0"/><stop offset=".55" stop-color="#B13DD0"/><stop offset="1" stop-color="#FF4F9A"/></linearGradient></defs>'
icon = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">{BG}<rect width="512" height="512" rx="116" fill="url(#g)"/><g>{fg_svg(512/108)}</g></svg>'
mask = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512">{BG}<rect width="512" height="512" fill="url(#g)"/><g>{fg_svg(512/108)}</g></svg>'
open(f"{OUT}/icon.svg", "w").write(icon)

import resvg_py
def png(svg_text, size, path):
    data = resvg_py.svg_to_bytes(svg_string=svg_text, width=size, height=size)
    open(path, "wb").write(bytes(data))
png(icon, 192, f"{OUT}/icon-192.png"); png(icon, 512, f"{OUT}/icon-512.png")
png(mask, 512, f"{OUT}/icon-maskable-512.png"); png(mask, 180, f"{OUT}/apple-touch-icon.png")
png(avatar, 840, os.path.join(ROOT, "avatar_preview.png"))

# Android adaptive-icon layers (108dp canvas), same geometry
def circle_path(cx, cy, r):
    return f"M{cx - r:.2f},{cy:.2f}a{r:.2f},{r:.2f} 0 1,0 {2*r:.2f},0a{r:.2f},{r:.2f} 0 1,0 {-2*r:.2f},0"
def vector(mono):
    p = ['<?xml version="1.0" encoding="utf-8"?>',
         '<vector xmlns:android="http://schemas.android.com/apk/res/android" android:width="108dp" android:height="108dp" android:viewportWidth="108" android:viewportHeight="108">',
         f'  <path android:fillColor="#FFFFFF" android:fillAlpha="0.16" android:pathData="{circle_path(54, 54, AGAR_R)}"/>',
         f'  <path android:fillColor="#FFFFFF" android:fillAlpha="0.3" android:pathData="{circle_path(ZONE[0], ZONE[1], ZONE[2])}"/>',
         f'  <path android:fillColor="#FFFFFF" android:pathData="{circle_path(ZONE[0], ZONE[1], ZONE[3])}"/>',
         f'  <path android:strokeColor="#FFFFFF" android:strokeWidth="4.4" android:fillColor="#00000000" android:pathData="{circle_path(54, 54, 26)}"/>']
    for x, y, r, c in COLS:
        p.append(f'  <path android:fillColor="{"#FFFFFF" if mono else c}" android:pathData="{circle_path(x, y, r)}"/>')
    p.append('  <path android:fillColor="#FFFFFF" android:pathData="M' + " L".join(f"{x},{y}" for x, y in ARROW) + ' Z"/>')
    p.append('</vector>')
    return "\n".join(p) + "\n"
res = os.path.join(ROOT, "android", "app", "src", "main", "res")
os.makedirs(f"{res}/drawable", exist_ok=True)
open(f"{res}/drawable/ic_launcher_foreground.xml", "w").write(vector(False))
open(f"{res}/drawable/ic_launcher_monochrome.xml", "w").write(vector(True))
print("ok:", len(cols), "colonies")
