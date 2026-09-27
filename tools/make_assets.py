"""Generates the animated SVGs of the profile README (no external resources: GitHub shows SVGs as images,
so fonts, scripts and links inside them would not load anyway). Run: python tools/make_assets.py"""
from __future__ import annotations

import math
import random
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent.parent / "assets"
SANS = "'Segoe UI', 'Helvetica Neue', Helvetica, Arial, sans-serif"
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, 'DejaVu Sans Mono', monospace"
CYAN, LAV, PINK, SKY = "#7dd3fc", "#c4b5fd", "#f0abfc", "#93c5fd"


def cloud(cx: float, cy: float, s: float) -> str:
    """A soft cumulus made of overlapping circles on a flat base."""
    parts = [(0, 0, 38), (-42, 12, 28), (44, 10, 30), (-20, -18, 30), (22, -22, 34), (-70, 22, 18), (74, 22, 20)]
    circles = "".join(f'<circle cx="{cx + dx * s:.1f}" cy="{cy + dy * s:.1f}" r="{r * s:.1f}"/>' for dx, dy, r in parts)
    base = f'<rect x="{cx - 80 * s:.1f}" y="{cy + 10 * s:.1f}" width="{160 * s:.1f}" height="{32 * s:.1f}" rx="{16 * s:.1f}"/>'
    return circles + base


def cloud_layer(y: float, scale: float, xs: list[float], width: float, dur: int, opacity: float, fill: str) -> str:
    """Clouds drifting left forever: the layer is drawn twice, one width apart, and slides by one width."""
    shapes = "".join(cloud(x, y, scale) for x in xs)
    return (f'<g fill="{fill}" opacity="{opacity}"><g>{shapes}<g transform="translate({width} 0)">{shapes}</g>'
            f'<animateTransform attributeName="transform" type="translate" from="0 0" to="{-width} 0" dur="{dur}s" repeatCount="indefinite"/>'
            f"</g></g>")


def header() -> str:
    W, H = 1200, 320
    rnd = random.Random(7)
    stars = []
    for _ in range(70):
        x, y, r = rnd.uniform(10, W - 10), rnd.uniform(8, H * 0.62), rnd.choice([0.7, 0.9, 1.1, 1.4, 1.8])
        d, delay = rnd.uniform(2.2, 5.5), rnd.uniform(0, 5)
        stars.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r}" fill="#fff" opacity=".2">'
                     f'<animate attributeName="opacity" values=".15;.95;.15" dur="{d:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/></circle>')
    # a small constellation: the "web" in WolkeWeb
    nodes = [(930, 70), (1010, 48), (1085, 92), (1040, 150), (960, 132), (1125, 40), (880, 118)]
    edges = [(0, 1), (1, 2), (2, 3), (3, 4), (4, 0), (1, 5), (0, 6), (4, 6), (2, 5)]
    web = []
    for i, (a, b) in enumerate(edges):
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        length = math.hypot(x2 - x1, y2 - y1)
        web.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-opacity=".35" stroke-width="1.2"/>')
        web.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{CYAN}" stroke-width="2" stroke-linecap="round" '
                   f'stroke-dasharray="10 {length:.0f}" stroke-dashoffset="{length + 10:.0f}">'
                   f'<animate attributeName="stroke-dashoffset" values="{length + 10:.0f};0" dur="{2.4 + i * 0.35:.2f}s" begin="{i * 0.4:.1f}s" repeatCount="indefinite"/></line>')
    for i, (x, y) in enumerate(nodes):
        web.append(f'<circle cx="{x}" cy="{y}" r="3.2" fill="{LAV}"><animate attributeName="r" values="3;5;3" dur="{2.5 + i * 0.3:.1f}s" repeatCount="indefinite"/></circle>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="WolkeWeb – Self-Hosting, Sicherheit, Daten, Game-Dev">
<defs>
  <linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#070b1f"/><stop offset=".55" stop-color="#1a1b4b"/><stop offset="1" stop-color="#3b2470"/></linearGradient>
  <radialGradient id="glow" cx=".5" cy=".55" r=".5"><stop offset="0" stop-color="#6d5dfc" stop-opacity=".45"/><stop offset="1" stop-color="#6d5dfc" stop-opacity="0"/></radialGradient>
  <radialGradient id="moon" cx=".4" cy=".4" r=".6"><stop offset="0" stop-color="#fffbeb"/><stop offset="1" stop-color="#fde68a"/></radialGradient>
  <linearGradient id="title" x1="0" y1="0" x2="1200" y2="0" gradientUnits="userSpaceOnUse">
    <stop offset="0" stop-color="{CYAN}"/><stop offset=".35" stop-color="{LAV}"/><stop offset=".65" stop-color="{PINK}"/><stop offset="1" stop-color="{CYAN}"/>
    <animateTransform attributeName="gradientTransform" type="translate" values="-600 0;600 0;-600 0" dur="12s" repeatCount="indefinite"/>
  </linearGradient>
  <filter id="soft" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6"/></filter>
  <clipPath id="card"><rect width="{W}" height="{H}" rx="26"/></clipPath>
</defs>
<g clip-path="url(#card)">
  <rect width="{W}" height="{H}" fill="url(#sky)"/>
  <ellipse cx="600" cy="190" rx="520" ry="170" fill="url(#glow)"/>
  {''.join(stars)}
  <circle cx="150" cy="78" r="46" fill="#fde68a" opacity=".25" filter="url(#soft)"/>
  <circle cx="150" cy="78" r="30" fill="url(#moon)"/>
  <circle cx="162" cy="70" r="27" fill="#141541" opacity=".9"/>
  <g>{''.join(web)}</g>
  {cloud_layer(250, 1.3, [80, 470, 860], 1200, 90, .10, "#c7d2fe")}
  {cloud_layer(278, 1.0, [220, 620, 1010], 1200, 55, .16, "#e0e7ff")}
  {cloud_layer(300, 1.45, [40, 420, 780, 1120], 1200, 34, .22, "#ffffff")}
  <text x="600" y="168" text-anchor="middle" font-family="{SANS}" font-size="92" font-weight="800" letter-spacing="-1" fill="url(#title)">WolkeWeb</text>
  <text x="600" y="214" text-anchor="middle" font-family="{SANS}" font-size="22" font-weight="500" letter-spacing="3" fill="#e0e7ff" opacity="0">SELF-HOSTING · SICHERHEIT · DATEN · GAME-DEV
    <animate attributeName="opacity" from="0" to=".9" begin=".4s" dur="1.6s" fill="freeze"/>
  </text>
</g>
</svg>
'''


def typing(lines: list[str], W: int = 900, H: int = 46, size: int = 22, per_line: float = 5.0) -> str:
    """Lines type themselves, stay with a blinking cursor, and are deleted, one after the other. Each character has
    its own discrete visibility timeline, so the effect does not depend on the viewer's font width."""
    T = per_line * len(lines)

    def timeline(windows: list[tuple[float, float]]) -> str:
        """fill-opacity 1 inside the windows (seconds within the cycle), 0 elsewhere."""
        kt, vals = [0.0], ["0"]
        for a, b in windows:
            kt += [a / T, b / T]
            vals += ["1", "0"]
        kt.append(1.0)
        vals.append("0")
        return (f'<animate attributeName="fill-opacity" dur="{T:g}s" repeatCount="indefinite" calcMode="discrete" '
                f'keyTimes="{";".join(f"{k:.4f}" for k in kt)}" values="{";".join(vals)}"/>')

    parts = []
    for i, text in enumerate(lines):
        n, t0 = len(text), i * per_line
        type_d, erase_d = min(1.8, 0.07 * n), 0.5
        t_end = t0 + per_line - erase_d
        spans = []
        for k, ch in enumerate(text):
            shown = t0 + type_d * (k + 1) / n
            hidden = t_end + erase_d * (n - k) / (n + 1)        # right-most characters go first
            spans.append(f'<tspan fill-opacity="0">{escape(ch)}{timeline([(shown, hidden)])}</tspan>')
        blinks, b = [], t0 + type_d
        while b < t_end - 0.05:
            blinks.append((b, min(b + 0.5, t_end)))
            b += 1.0
        spans.append(f'<tspan fill="{CYAN}" fill-opacity="0">\u258d{timeline(blinks)}</tspan>')
        parts.append(f'<text x="{W / 2}" y="{H / 2 + size * 0.35:.1f}" text-anchor="middle" font-family="{MONO}" font-size="{size}" '
                     f'fill="{LAV}" xml:space="preserve">{"".join(spans)}</text>')
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{escape(' · '.join(lines))}">
{''.join(parts)}
</svg>
'''


def terminal() -> str:
    """Types itself line by line and starts over. Commands are revealed character by character inside the same text
    element as the prompt, so the result does not depend on the viewer's monospace font width."""
    W, H = 820, 330
    prompt = "wolke@web:~$\u00a0"
    steps = [  # (command, output lines)
        ("whoami", ["WolkeWeb · baut Software, die zu Hause läuft"]),
        ("ls werkstatt/", ["sicherheit/   spiele/   daten/   self-hosting/"]),
        ("cat philosophie.txt", ["Selbst hosten. Selbst verstehen. Selbst bauen.", "Keine fremde Cloud – die Wolke steht nur im Namen."]),
    ]
    size, lh = 16, 26

    def show(t: float) -> str:  # hidden at every loop start, visible from loop start + t
        return (f'<set attributeName="fill-opacity" to="0" begin="loop.begin"/>'
                f'<set attributeName="fill-opacity" to="1" begin="loop.begin+{t:.2f}s"/>')

    y, t, body = 84, 0.8, []
    for cmd, outs in steps:
        chars = []
        for k, ch in enumerate(cmd):
            chars.append(f'<tspan fill="#f8fafc" fill-opacity="0">{escape(ch)}{show(t + 0.35 + 0.08 * k)}</tspan>')
        body.append(f'<text x="28" y="{y}" font-family="{MONO}" font-size="{size}" xml:space="preserve">'
                    f'<tspan fill="{CYAN}" fill-opacity="0">{prompt}{show(t)}</tspan>{"".join(chars)}</text>')
        t += 0.35 + 0.08 * len(cmd) + 0.35
        for o in outs:
            y += lh
            body.append(f'<text x="28" y="{y}" font-family="{MONO}" font-size="{size}" xml:space="preserve" fill="{LAV}" fill-opacity="0">{escape(o)}{show(t)}</text>')
            t += 0.2
        y += lh + 8
        t += 0.6
    blink = (f'<set attributeName="fill-opacity" to="0" begin="loop.begin"/>'
             f'<animate attributeName="fill-opacity" values="1;1;0;0" keyTimes="0;.5;.5;1" dur="1s" begin="loop.begin+{t:.2f}s" repeatCount="8"/>')
    body.append(f'<text x="28" y="{y}" font-family="{MONO}" font-size="{size}" xml:space="preserve">'
                f'<tspan fill="{CYAN}" fill-opacity="0">{prompt}{show(t)}</tspan><tspan fill="{CYAN}" fill-opacity="0">\u2588{blink}</tspan></text>')
    total = t + 8
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Terminal: whoami – WolkeWeb baut Software, die zu Hause läuft; Werkstatt: Sicherheit, Spiele, Daten, Self-Hosting">
<defs>
  <linearGradient id="bd" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset=".5" stop-color="{LAV}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
</defs>
<rect x="1" y="1" width="{W - 2}" height="{H - 2}" rx="16" fill="#0d1117" stroke="url(#bd)" stroke-width="2"/>
<rect x="2" y="2" width="{W - 4}" height="40" rx="15" fill="#161b22"/>
<rect x="2" y="30" width="{W - 4}" height="12" fill="#161b22"/>
<circle cx="26" cy="22" r="7" fill="#ff5f57"/><circle cx="48" cy="22" r="7" fill="#febc2e"/><circle cx="70" cy="22" r="7" fill="#28c840"/>
<text x="{W / 2}" y="27" text-anchor="middle" font-family="{MONO}" font-size="13" fill="#8b949e">wolke@web: ~</text>
<rect width="0" height="0"><animate id="loop" attributeName="width" from="0" to="0" dur="{total:.1f}s" begin="0s;loop.end"/></rect>
{''.join(body)}
</svg>
'''


def card(x: float, y: float, w: float, h: float, accent: str, icon: str, title: str, lines: list[str], idx: int) -> str:
    text = "".join(f'<text x="{x + 132}" y="{y + 92 + i * 24}" font-family="{SANS}" font-size="16" fill="#c9d1d9">{escape(l)}</text>' for i, l in enumerate(lines))
    return f'''<g>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="#0d1117"/>
  <rect x="{x + 1}" y="{y + 1}" width="{w - 2}" height="{h - 2}" rx="17" fill="none" stroke="{accent}" stroke-opacity=".55" stroke-width="1.5"/>
  <rect x="{x}" y="{y}" width="{w}" height="{h}" rx="18" fill="url(#shine{idx})"/>
  <g transform="translate({x + 28} {y + 38})">{icon}</g>
  <text x="{x + 132}" y="{y + 58}" font-family="{SANS}" font-size="22" font-weight="700" fill="{accent}">{escape(title)}</text>
  {text}
</g>'''


def werkstatt() -> str:
    W, H, gap = 1000, 430, 20
    cw, ch = (W - gap) / 2, (H - gap) / 2
    lock = f'''<rect x="10" y="40" width="64" height="52" rx="10" fill="{LAV}"/>
<path d="M22 42 V26 a20 20 0 0 1 40 0 V42" fill="none" stroke="{LAV}" stroke-width="9" stroke-linecap="round">
  <animateTransform attributeName="transform" type="translate" values="0 0;0 0;0 -9;0 -9;0 0" keyTimes="0;.55;.62;.9;1" dur="4s" repeatCount="indefinite"/></path>
<circle cx="42" cy="62" r="7" fill="#0d1117"/><rect x="39" y="64" width="6" height="14" rx="3" fill="#0d1117"/>
<circle cx="42" cy="62" r="16" fill="{LAV}" opacity="0"><animate attributeName="opacity" values="0;0;.35;0" keyTimes="0;.9;.95;1" dur="4s" repeatCount="indefinite"/></circle>'''
    # a pixel flame: rows of 8-px pixels that flicker
    flame_rows = ["...#....", "..##.#..", "..####..", ".######.", ".##**##.", "##****##", "##*oo*##", ".#*oo*#.", "..####.."]
    colors = {"#": "#fb923c", "*": "#fde047", "o": "#fff7ed"}
    px = []
    rnd = random.Random(3)
    for r, row in enumerate(flame_rows):
        for c, ch_ in enumerate(row):
            if ch_ in colors:
                flick = ""
                if ch_ == "#" and r < 5:
                    flick = f'<animate attributeName="opacity" values="1;.2;1" dur="{rnd.uniform(.5, 1.1):.2f}s" repeatCount="indefinite"/>'
                px.append(f'<rect x="{10 + c * 8}" y="{18 + r * 8}" width="8" height="8" fill="{colors[ch_]}">{flick}</rect>')
    flame = f'<g><animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="1.4s" repeatCount="indefinite"/>{"".join(px)}</g>'
    pts = [(0, 70), (14, 62), (28, 66), (42, 44), (56, 50), (70, 26), (84, 32)]
    path = "M" + " L".join(f"{10 + a} {10 + b}" for a, b in pts)
    chart = f'''<rect x="6" y="6" width="92" height="84" rx="10" fill="none" stroke="{CYAN}" stroke-opacity=".25"/>
<path d="{path}" fill="none" stroke="{CYAN}" stroke-width="4" stroke-linecap="round" stroke-linejoin="round" stroke-dasharray="140" stroke-dashoffset="140">
  <animate attributeName="stroke-dashoffset" values="140;0;0;140" keyTimes="0;.45;.85;1" dur="5s" repeatCount="indefinite"/></path>
<circle cx="94" cy="42" r="5" fill="{CYAN}" opacity="0"><animate attributeName="opacity" values="0;0;1;1;0" keyTimes="0;.42;.47;.85;.9" dur="5s" repeatCount="indefinite"/></circle>'''
    leds = "".join(
        f'<rect x="{18}" y="{22 + i * 24}" width="68" height="18" rx="4" fill="#1f2937" stroke="{PINK}" stroke-opacity=".5"/>'
        f'<circle cx="{74}" cy="{31 + i * 24}" r="3.5" fill="#4ade80"><animate attributeName="opacity" values="1;.15;1" dur="{0.7 + i * 0.45:.2f}s" repeatCount="indefinite"/></circle>'
        f'<rect x="26" y="{29 + i * 24}" width="26" height="4" rx="2" fill="{PINK}" opacity=".6"/>' for i in range(3))
    server = f'''{leds}<g fill="#e0e7ff" opacity=".9"><animateTransform attributeName="transform" type="translate" values="0 0;6 0;0 0" dur="6s" repeatCount="indefinite"/>
<circle cx="52" cy="4" r="8"/><circle cx="63" cy="0" r="10"/><circle cx="74" cy="5" r="7"/><rect x="45" y="4" width="36" height="8" rx="4"/></g>'''
    cards = [
        card(0, 0, cw, ch, LAV, lock, "Zero-Knowledge", ["Verschlüsselt wird im Browser –", "der Server sieht nur Rauschen.", "Standardbibliothek statt Abhängigkeiten."], 0),
        card(cw + gap, 0, cw, ch, "#fdba74", flame, "Prozedurale Spiele", ["Roguelites in reinem Python –", "Grafik und Sound werden berechnet,", "nicht aus Dateien geladen."], 1),
        card(0, ch + gap, cw, ch, CYAN, chart, "Daten & Märkte", ["Öffentliche Daten, eigene Modelle –", "und eine ehrliche Rückrechnung,", "bevor irgendwer irgendwas glaubt."], 2),
        card(cw + gap, ch + gap, cw, ch, PINK, server, "Self-Hosting", ["Docker, Postgres, eigene VM –", "alles läuft im Heimnetz,", "mit Backups und Totmann-Schalter."], 3),
    ]
    shines = "".join(
        f'<linearGradient id="shine{i}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
        f'<stop offset=".5" stop-color="#fff" stop-opacity=".06"/><stop offset="1" stop-color="#fff" stop-opacity="0"/>'
        f'<animateTransform attributeName="gradientTransform" type="translate" values="-1 0;1 0;1 0" keyTimes="0;.35;1" dur="7s" begin="{i * 0.8:.1f}s" repeatCount="indefinite"/></linearGradient>'
        for i in range(4))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Werkstatt: Zero-Knowledge-Sicherheit, prozedurale Spiele in Python, Daten und Märkte, Self-Hosting">
<defs>{shines}</defs>
{''.join(cards)}
</svg>
'''


def footer() -> str:
    W, H = 1200, 140

    def wave(amp: float, length: float, y: float) -> str:
        pts = []
        for i in range(0, int(2 * W) + 1, 20):
            pts.append(f"{i} {y + amp * math.sin(2 * math.pi * i / length):.1f}")
        return f"M0 {H} L" + " L".join(pts) + f" L{2 * W} {H} Z"

    layers = [(10, 400, 60, 22, "url(#w1)", .55), (14, 600, 78, 16, "url(#w2)", .7), (8, 300, 96, 11, "url(#w3)", .9)]
    g = "".join(
        f'<path d="{wave(a, L, y)}" fill="{fill}" opacity="{op}"><animateTransform attributeName="transform" type="translate" from="0 0" to="{-L * round(W / L)} 0" dur="{d}s" repeatCount="indefinite"/></path>'
        for a, L, y, d, fill, op in layers)
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="Danke fürs Vorbeischauen">
<defs>
  <linearGradient id="w1" x1="0" x2="1"><stop offset="0" stop-color="{CYAN}"/><stop offset="1" stop-color="{LAV}"/></linearGradient>
  <linearGradient id="w2" x1="0" x2="1"><stop offset="0" stop-color="{LAV}"/><stop offset="1" stop-color="{PINK}"/></linearGradient>
  <linearGradient id="w3" x1="0" x2="1"><stop offset="0" stop-color="#3b2470"/><stop offset="1" stop-color="#1a1b4b"/></linearGradient>
</defs>
{g}
<text x="{W / 2}" y="{H - 18}" text-anchor="middle" font-family="{SANS}" font-size="17" font-weight="600" letter-spacing="2" fill="#e0e7ff">DANKE FÜRS VORBEISCHAUEN</text>
</svg>
'''


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    files = {
        "header.svg": header(),
        "typing.svg": typing([
            "Baut Software, die auf dem eigenen Server läuft.",
            "Zero-Knowledge: nicht mal der Server weiß Bescheid.",
            "Prozedurale Welten in reinem Python.",
            "Daten rein, Erkenntnis raus – ehrlich gemessen.",
        ]),
        "terminal.svg": terminal(),
        "werkstatt.svg": werkstatt(),
        "footer.svg": footer(),
    }
    for name, svg in files.items():
        (OUT / name).write_text(svg, encoding="utf-8")
        print(f"{name}: {len(svg.encode()) / 1024:.1f} KB")


if __name__ == "__main__":
    main()
