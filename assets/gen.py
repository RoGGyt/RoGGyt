"""Generates the profile SVG assets. Run: python3 assets/gen.py"""
import math, random, os

OUT = os.path.dirname(os.path.abspath(__file__))
MONO = "'JetBrains Mono','Fira Code','Cascadia Code',Consolas,'Courier New',monospace"
LAV, LAV_LIGHT, LAV_DARK = "#a99fd9", "#e6e1ff", "#3d3560"


def save(name, svg):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as f:
        f.write(svg)


# ───────────────────────── header ─────────────────────────
def branch(rnd, x, y, ang, length, width, depth, out_b, out_f):
    if depth == 0 or length < 6:
        out_f.append((x, y))
        return
    x2 = x + math.cos(ang) * length
    y2 = y + math.sin(ang) * length
    cx = (x + x2) / 2 + rnd.uniform(-length, length) * 0.18
    cy = (y + y2) / 2 + rnd.uniform(-length, length) * 0.18
    out_b.append(f'<path d="M{x:.1f} {y:.1f} Q{cx:.1f} {cy:.1f} {x2:.1f} {y2:.1f}" stroke-width="{width:.2f}"/>')
    if depth <= 3:
        out_f.append((x2, y2))
    n = 2 if rnd.random() < 0.75 else 3
    for i in range(n):
        na = ang + rnd.uniform(-0.75, 0.75)
        branch(rnd, x2, y2, na, length * rnd.uniform(0.62, 0.8), max(width * 0.62, 0.6), depth - 1, out_b, out_f)


def blossoms(rnd, pts, density):
    out = []
    shades = ["#f2f2f2", "#d9d9d9", "#bdbdbd", "#9a9a9a", "#ffffff"]
    for (x, y) in pts:
        for _ in range(density):
            bx, by = x + rnd.gauss(0, 9), y + rnd.gauss(0, 7)
            r = rnd.uniform(1.6, 4.2)
            out.append(f'<circle cx="{bx:.1f}" cy="{by:.1f}" r="{r:.1f}" fill="{rnd.choice(shades)}" opacity="{rnd.uniform(.45, .95):.2f}"/>')
    return out


def tree(rnd, root_x, root_y, ang, size, depth, density):
    b, f = [], []
    branch(rnd, root_x, root_y, ang, size, 9, depth, b, f)
    return b, blossoms(rnd, f, density)


def wing(side):
    """Feathered wing pointing outward; side=-1 left, 1 right. Drawn around origin."""
    feathers = []
    for i in range(9):
        t = i / 8
        ang = math.radians(-70 + t * 85)
        length = 46 + 34 * math.sin(t * math.pi * 0.9)
        w = 7 - t * 2
        x2, y2 = math.cos(ang) * length, math.sin(ang) * length
        nx, ny = -math.sin(ang) * w, math.cos(ang) * w
        d = (f"M0 0 Q{x2*0.5+nx:.1f} {y2*0.5+ny:.1f} {x2:.1f} {y2:.1f} "
             f"Q{x2*0.5-nx:.1f} {y2*0.5-ny:.1f} 0 0Z")
        feathers.append(f'<path d="{d}" fill="url(#wg)" opacity="{0.55 + 0.45*(1-t):.2f}"/>')
    for i in range(6):  # small covert feathers
        t = i / 5
        ang = math.radians(-40 + t * 60)
        length = 22 + 6 * t
        x2, y2 = math.cos(ang) * length, math.sin(ang) * length
        nx, ny = -math.sin(ang) * 4, math.cos(ang) * 4
        d = f"M0 0 Q{x2*0.5+nx:.1f} {y2*0.5+ny:.1f} {x2:.1f} {y2:.1f} Q{x2*0.5-nx:.1f} {y2*0.5-ny:.1f} 0 0Z"
        feathers.append(f'<path d="{d}" fill="{LAV_LIGHT}" opacity=".35"/>')
    return f'<g transform="scale({side},1)">{"".join(feathers)}</g>'


def header():
    W, H = 1200, 320
    rnd = random.Random(7)
    b1, f1 = tree(rnd, 1235, 330, math.radians(-128), 110, 7, 3)
    b2, f2 = tree(rnd, -40, 340, math.radians(-50), 95, 6, 3)
    petals = []
    for i in range(26):
        x0 = rnd.uniform(0, W)
        dur = rnd.uniform(9, 17)
        delay = -rnd.uniform(0, dur)
        drift = rnd.uniform(-160, 60)
        s = rnd.uniform(.6, 1.3)
        shade = rnd.choice(["#e8e8e8", "#c8c8c8", "#ffffff", LAV_LIGHT])
        petals.append(
            f'<g opacity="{rnd.uniform(.35,.9):.2f}"><g>'
            f'<animateTransform attributeName="transform" type="translate" values="{x0:.0f} -20; {x0+drift:.0f} {H+20}" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
            f'<path d="M0 0 C3 -4 8 -3 9 0 C8 3 3 4 0 0Z" fill="{shade}" transform="scale({s:.2f})">'
            f'<animateTransform attributeName="transform" type="rotate" values="0;360" dur="{rnd.uniform(3,7):.1f}s" repeatCount="indefinite" additive="sum"/></path>'
            f'</g></g>')
    name = "RoGGyt"
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<defs>
 <linearGradient id="bg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#0b0b0b"/><stop offset="1" stop-color="#000"/></linearGradient>
 <radialGradient id="glow" cx=".5" cy=".5" r=".5"><stop offset="0" stop-color="{LAV}" stop-opacity=".18"/><stop offset="1" stop-color="{LAV}" stop-opacity="0"/></radialGradient>
 <linearGradient id="wg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{LAV_LIGHT}"/><stop offset=".55" stop-color="{LAV}"/><stop offset="1" stop-color="{LAV_DARK}"/></linearGradient>
 <linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset=".7" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity=".9"/></linearGradient>
 <pattern id="grain" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="1" height="1" fill="#fff" opacity=".035"/><rect x="2" y="3" width="1" height="1" fill="#fff" opacity=".025"/></pattern>
 <style>
  .t{{font-family:{MONO};}}
  .flap{{animation:flap 4s ease-in-out infinite;transform-box:fill-box;}}
  .l{{transform-origin:100% 50%;}} .r{{transform-origin:0% 50%;}}
  @keyframes flap{{0%,100%{{transform:rotate(0deg)}}50%{{transform:rotate(-7deg)}}}}
  .r.flap{{animation-name:flapr}} @keyframes flapr{{0%,100%{{transform:rotate(0deg)}}50%{{transform:rotate(7deg)}}}}
  .blink{{animation:blink 1.1s steps(1) infinite}} @keyframes blink{{50%{{opacity:0}}}}
  .glow{{animation:pulse 5s ease-in-out infinite}} @keyframes pulse{{50%{{opacity:.55}}}}
 </style>
</defs>
<rect width="{W}" height="{H}" fill="url(#bg)"/>
<g stroke="#5c5c5c" fill="none" stroke-linecap="round">{"".join(b2)}</g><g>{"".join(f2)}</g>
<g stroke="#6e6e6e" fill="none" stroke-linecap="round">{"".join(b1)}</g><g>{"".join(f1)}</g>
<ellipse class="glow" cx="600" cy="150" rx="330" ry="120" fill="url(#glow)"/>
<g transform="translate(372 132) scale(1.55)"><g class="flap l">{wing(-1)}</g></g>
<g transform="translate(828 132) scale(1.55)"><g class="flap r">{wing(1)}</g></g>
<text class="t" x="600" y="166" text-anchor="middle" font-size="64" font-weight="700" fill="#f0f0f0" letter-spacing="6">{name}</text>
<text class="t" x="600" y="206" text-anchor="middle" font-size="15" fill="#8a8a8a" letter-spacing="4">GAME DEV · WEB · ROBLOX · BLENDER</text>
<text class="t" x="600" y="244" text-anchor="middle" font-size="14" fill="{LAV}">&gt; building things in the dark<tspan class="blink">_</tspan></text>
{"".join(petals)}
<rect width="{W}" height="{H}" fill="url(#grain)"/>
<rect width="{W}" height="{H}" fill="url(#fade)"/>
</svg>'''


# ───────────────────────── terminal ─────────────────────────
def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def terminal():
    W = 860
    lines = [
        ("cmd", "whoami"),
        ("out", [("RoGGyt", "#f0f0f0"), (" — 18 y.o. developer", "#9a9a9a")]),
        ("cmd", "cat about.txt"),
        ("out", [("делаю игры на Roblox, сайты и 3D в Blender", "#c9c9c9")]),
        ("out", [("люблю тёмные интерфейсы, анимации и ночные коммиты", "#c9c9c9")]),
        ("cmd", "ls ~/projects"),
        ("out", [("slime-lab/   ", LAV), ("pet-rng/   ", LAV), ("pitbike-stunt/   ", LAV), ("kege-site/", LAV)]),
        ("cmd", "cat stack.json"),
        ("out", [('{ "lang": ', "#8a8a8a"), ('["luau", "ts", "js", "python"]', "#e6e6e6"), (', "tools": ', "#8a8a8a"), ('["roblox studio", "blender", "git"]', "#e6e6e6"), (" }", "#8a8a8a")]),
        ("cmd", "echo $STATUS"),
        ("out", [("open to collabs & commissions  ", "#c9c9c9"), ("♥", LAV)]),
    ]
    y0, lh, cw = 76, 27, 9.6
    t = 0.6
    body = []
    for i, (kind, content) in enumerate(lines):
        y = y0 + i * lh
        cid = f"c{i}"
        if kind == "cmd":
            text = content
            n = len(text) + 2
            dur = max(0.35, len(text) * 0.07)
            body.append(f'<clipPath id="{cid}"><rect x="40" y="{y-18}" height="26" width="0"><animate attributeName="width" from="0" to="{40 + n*cw + 20:.0f}" begin="{t:.2f}s" dur="{dur:.2f}s" fill="freeze" calcMode="discrete" values="{";".join(str(int(40+k*cw+cw)) for k in range(n+1))}"/></rect></clipPath>')
            body.append(f'<text x="40" y="{y}" clip-path="url(#{cid})"><tspan fill="{LAV}">❯ </tspan><tspan fill="#f0f0f0">{esc(text)}</tspan></text>')
            t += dur + 0.35
        else:
            spans = "".join(f'<tspan fill="{c}">{esc(s)}</tspan>' for s, c in content)
            body.append(f'<text x="40" y="{y}" opacity="0">{spans}<animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".25s" fill="freeze"/></text>')
            t += 0.25
    yc = y0 + len(lines) * lh
    body.append(f'<text x="40" y="{yc}" opacity="0"><tspan fill="{LAV}">❯ </tspan><tspan class="blink" fill="#f0f0f0">█</tspan><animate attributeName="opacity" from="0" to="1" begin="{t:.2f}s" dur=".1s" fill="freeze"/></text>')
    H = yc + 34
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>text{{font-family:{MONO};font-size:15px;white-space:pre}} .blink{{animation:b 1s steps(1) infinite}} @keyframes b{{50%{{opacity:0}}}}</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="12" fill="#0b0b0b" stroke="#262626"/>
<path d="M1 13a12 12 0 0 1 12-12h{W-26}a12 12 0 0 1 12 12v23H1z" fill="#141414"/>
<line x1="1" y1="36" x2="{W-1}" y2="36" stroke="#262626"/>
<circle cx="24" cy="19" r="5.5" fill="#3a3a3a"/><circle cx="43" cy="19" r="5.5" fill="#3a3a3a"/><circle cx="62" cy="19" r="5.5" fill="{LAV}" opacity=".8"/>
<text x="{W/2}" y="24" text-anchor="middle" fill="#6e6e6e" style="font-size:12px">roggyt@sakura: ~</text>
{"".join(body)}
</svg>'''


# ───────────────────────── project cards ─────────────────────────
def card(title, desc, tags, status, progress, icon):
    W, H = 420, 170
    tag_svg, x = [], 22
    for tg in tags:
        w = len(tg) * 7.4 + 18
        tag_svg.append(f'<rect x="{x:.0f}" y="122" width="{w:.0f}" height="24" rx="12" fill="#161616" stroke="#2c2c2c"/><text x="{x + w/2:.0f}" y="138" text-anchor="middle" fill="#9a9a9a" font-size="12">{esc(tg)}</text>')
        x += w + 8
    desc_lines = []
    words, line = desc.split(), ""
    for wd in words:
        if len(line) + len(wd) + 1 > 46:
            desc_lines.append(line)
            line = wd
        else:
            line = (line + " " + wd).strip()
    desc_lines.append(line)
    desc_svg = "".join(f'<text x="22" y="{78 + i*20}" fill="#9a9a9a" font-size="13">{esc(l)}</text>' for i, l in enumerate(desc_lines[:2]))
    bar = max(128 * progress, 4)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}">
<style>text{{font-family:{MONO}}} .p{{animation:p 2.4s ease-in-out infinite}} @keyframes p{{50%{{opacity:.35}}}} .bar{{transform-box:fill-box;transform-origin:0 50%;animation:g 1.6s ease-out both}} @keyframes g{{from{{transform:scaleX(0)}}}}</style>
<rect x="1" y="1" width="{W-2}" height="{H-2}" rx="14" fill="#0b0b0b" stroke="#262626"/>
<text x="22" y="44" font-size="20" fill="{LAV}">✦</text>
<text x="54" y="44" fill="#f0f0f0" font-size="18" font-weight="700">{esc(title)}</text>
<circle class="p" cx="{W-150}" cy="38" r="4" fill="{LAV}"/>
<text x="{W-140}" y="43" fill="{LAV}" font-size="12">{esc(status)}</text>
{desc_svg}
<rect x="{W-150}" y="54" width="128" height="4" rx="2" fill="#1f1f1f"/>
<rect class="bar" x="{W-150}" y="54" width="{bar:.0f}" height="4" rx="2" fill="{LAV}"/>
{"".join(tag_svg)}
</svg>'''


# ───────────────────────── pixel heart with wings ─────────────────────────
HEART = [
    ".XX...XX.",
    "XWWX.XLLX",
    "XWLLXLLLX",
    "XLLLLLLLX",
    ".XLLLLLX.",
    "..XLLLX..",
    "...XLX...",
    "....X....",
]
WING = [
    "........XX",
    "......XXWX",
    "....XXWWLX",
    "..XXWWLLX.",
    ".XWWLLLX..",
    "XWWLLX....",
    ".XXLX.....",
    "...X......",
]


def pixels(grid, ox, oy, s, flip=False):
    col = {"X": "#d9d9d9", "W": "#ffffff", "L": LAV}
    out = []
    for r, row in enumerate(grid):
        row = row[::-1] if flip else row
        for c, ch in enumerate(row):
            if ch != ".":
                out.append(f'<rect x="{ox + c*s}" y="{oy + r*s}" width="{s}" height="{s}" fill="{col[ch]}"/>')
    return "".join(out)


def heart():
    s = 6
    W, H = 300, 70
    hx = W / 2 - 9 * s / 2
    hy = 10
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" shape-rendering="crispEdges">
<style>
 .beat{{animation:beat 1.6s ease-in-out infinite;transform-origin:150px 34px}}
 @keyframes beat{{0%,40%,100%{{transform:scale(1)}}15%{{transform:scale(1.14)}}28%{{transform:scale(1.04)}}}}
 .wl{{animation:wl 2.4s ease-in-out infinite;transform-origin:100px 30px}} @keyframes wl{{50%{{transform:translateY(-3px) rotate(-4deg)}}}}
 .wr{{animation:wr 2.4s ease-in-out infinite;transform-origin:200px 30px}} @keyframes wr{{50%{{transform:translateY(-3px) rotate(4deg)}}}}
</style>
<g class="wl">{pixels(WING, hx - 10*s - 8, hy - 4, s, flip=False)}</g>
<g class="wr">{pixels(WING, hx + 9*s + 8, hy - 4, s, flip=True)}</g>
<g class="beat">{pixels(HEART, hx, hy, s)}</g>
</svg>'''


if __name__ == "__main__":
    save("header.svg", header())
    save("terminal.svg", terminal())
    save("heart.svg", heart())
    save("card-slime-lab.svg", card("Slime Lab", "симулятор сбора слаймов для Roblox — для детей, яркий и залипательный", ["roblox", "luau", "simulator"], "in dev", .6, "🧪"))
    save("card-pet-rng.svg", card("Pet RNG", "крути петов, они копают монеты, открывай локации и качай радиальное дерево апгрейдов", ["roblox", "luau", "rng"], "designing", .25, "🎲"))
    save("card-pitbike.svg", card("Pitbike Stunt", "реалистичная стант-игра на питбайке с упором на вилли", ["roblox", "blender", "physics"], "concept", .15, "🏍"))
    save("card-kege.svg", card("КЕГЭ тренажёр", "сайт для подготовки к ЕГЭ по информатике в терминальном стиле", ["web", "js", "ui"], "in dev", .5, "⌨"))
    print("ok")
