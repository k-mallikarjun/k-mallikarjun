#!/usr/bin/env python3
"""Builds assets/domains.svg: a rotating 3D dice (pure SVG/SMIL, no scripts) listing the six domains."""
import math
W, H = 1200, 380
cx, cy, S = 330, 205, 82
N_FR, DUR = 120, 18

DOMAINS = [("HEALTHCARE", "#00f0ff"), ("FINANCIAL", "#ff2bd6"), ("TELECOM", "#8a2be2"),
           ("BANKING", "#00f0ff"), ("INSURANCE", "#ff2bd6"), ("E-COMMERCE", "#8a2be2")]
# face: normal, U (right), V (up), with U x V = N
FACES = [((0,0,1),(1,0,0),(0,1,0)), ((0,0,-1),(-1,0,0),(0,1,0)), ((1,0,0),(0,0,-1),(0,1,0)),
         ((-1,0,0),(0,0,1),(0,1,0)), ((0,1,0),(1,0,0),(0,0,-1)), ((0,-1,0),(1,0,0),(0,0,1))]

def rot(v, ax, ay):
    x, y, z = v
    x, z = x*math.cos(ay) + z*math.sin(ay), -x*math.sin(ay) + z*math.cos(ay)      # Ry
    y, z = y*math.cos(ax) - z*math.sin(ax), y*math.sin(ax) + z*math.cos(ax)      # Rx
    return (x, y, z)
def add(a, b, s=1): return tuple(p + s*q for p, q in zip(a, b))

def angles(t):
    return 0.85*math.sin(2*math.pi*t + 0.6), 4*math.pi*t

face_svg = ""
for fi, ((N, U, V), (name, col)) in enumerate(zip(FACES, DOMAINS)):
    pts, ops, tr, rt, sk, sc = [], [], [], [], [], []
    prev_ang = None
    for f in range(N_FR + 1):
        ax, ay = angles(f / N_FR)
        n, u, v = rot(N, ax, ay), rot(U, ax, ay), rot(V, ax, ay)
        corners = []
        for su, sv in ((-1,-1),(1,-1),(1,1),(-1,1)):
            P = add(add(n, u, su), v, sv)
            corners.append(f"{cx+S*P[0]:.1f},{cy-S*P[1]:.1f}")
        pts.append(" ".join(corners))
        nz = n[2]
        ops.append(f"{min(1, max(0, nz*4))*(0.72+0.28*nz):.3f}")
        # affine for text in local px (u right, v down)
        a, b, c, d = u[0], -u[1], -v[0], v[1]
        e, g = cx + S*S/S*n[0]*1.0, cy - S*n[1]
        sx = math.hypot(a, b)
        if sx < 1e-3: sx, th = 1e-3, (prev_ang if prev_ang is not None else 0)
        else:
            th = math.degrees(math.atan2(b, a))
            if prev_ang is not None:
                while th - prev_ang > 180: th -= 360
                while th - prev_ang < -180: th += 360
        prev_ang = th
        ux, uy = a/sx, b/sx
        sy = c*(-uy) + d*ux
        if abs(sy) < 0.02: sy = 0.02 if sy >= 0 else -0.02
        k = (c*ux + d*uy) / sy
        tr.append(f"{e:.2f} {g:.2f}"); rt.append(f"{th:.2f}")
        sk.append(f"{math.degrees(math.atan(k)):.2f}"); sc.append(f"{sx:.4f} {sy:.4f}")
    def anim(typ, vals): return f'<animateTransform attributeName="transform" type="{typ}" values="{";".join(vals)}" dur="{DUR}s" repeatCount="indefinite"/>'
    label = name.replace("-", "&#8209;")
    face_svg += f'''<g>
<animate attributeName="opacity" values="{";".join(ops)}" dur="{DUR}s" repeatCount="indefinite"/>
<polygon fill="#0d0d28" stroke="{col}" stroke-width="3" stroke-linejoin="round" filter="url(#glow)">
<animate attributeName="points" values="{";".join(pts)}" dur="{DUR}s" repeatCount="indefinite"/></polygon>
<g>{anim("translate", tr)}<g>{anim("rotate", rt)}<g>{anim("skewX", sk)}<g>{anim("scale", sc)}
<text x="0" y="-26" text-anchor="middle" class="dn">DOMAIN 0{fi+1}</text>
<text x="0" y="12" text-anchor="middle" class="dt" fill="{col}">{label}</text>
<rect x="-40" y="26" width="80" height="3" rx="1.5" fill="{col}"/>
</g></g></g></g></g>
'''

legend = ""
for i, (name, col) in enumerate(DOMAINS):
    x = 640 + (i % 2) * 270
    y = 150 + (i // 2) * 62
    legend += (f'<rect x="{x}" y="{y}" width="250" height="46" rx="12" fill="#0b0b22" stroke="{col}" stroke-width="1.8"/>'
               f'<circle cx="{x+24}" cy="{y+23}" r="6" fill="{col}" filter="url(#glow)"><animate attributeName="opacity" values="1;.35;1" dur="{2+i*.3:.1f}s" repeatCount="indefinite"/></circle>'
               f'<text x="{x+42}" y="{y+29}" class="lg">{name.title()}</text>')

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Rotating dice listing the domains: healthcare, financial, telecom, banking, insurance and e-commerce">
<defs>
<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#07071a"/><stop offset=".6" stop-color="#120a2b"/><stop offset="1" stop-color="#0a1428"/></linearGradient>
<linearGradient id="neon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#00f0ff"/><stop offset="1" stop-color="#ff2bd6"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#00f0ff" stroke-opacity=".07"/></pattern>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
<style>
.h{{font:700 13px 'Courier New',monospace;fill:#ff2bd6;letter-spacing:4px}}
.t{{font:800 34px 'Segoe UI',Arial,sans-serif;fill:url(#neon)}}
.s{{font:500 16px 'Segoe UI',Arial,sans-serif;fill:#cfefff}}
.lg{{font:700 19px 'Segoe UI',Arial,sans-serif;fill:#fff}}
.dn{{font:700 10px 'Courier New',monospace;fill:#8fe9ff;letter-spacing:3px}}
.dt{{font:800 19px 'Segoe UI',Arial,sans-serif;letter-spacing:.5px}}
</style></defs>
<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/><rect width="{W}" height="{H}" rx="18" fill="url(#grid)"/>
<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="17" fill="none" stroke="url(#neon)" stroke-width="3" filter="url(#glow)"/>
<circle cx="{cx}" cy="{cy}" r="170" fill="#8a2be2" opacity=".14" filter="url(#glow)"/>
<text x="640" y="58" class="h">// DOMAINS</text>
<text x="640" y="104" class="t">Industries I've built for</text>
<text x="640" y="132" class="s">Regulated, high-scale, always-on systems across six domains.</text>
{legend}
{face_svg}
</svg>'''
open("assets/domains.svg", "w").write(svg)
print("domains.svg", len(svg)//1024, "KB")
