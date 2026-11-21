#!/usr/bin/env python3
"""Builds assets/banner.svg and assets/ai-stack.svg.
Usage: python3 build.py [photo.jpg|png]  -> photo mode puts your photo in a neon hex frame."""
import sys, base64, mimetypes, math
photo = sys.argv[1] if len(sys.argv) > 1 else None
W, H = 1200, 520
cx, cy = 985, 262

DEFS = '''<linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#07071a"/><stop offset=".6" stop-color="#120a2b"/><stop offset="1" stop-color="#0a1428"/></linearGradient>
<linearGradient id="neon" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#00f0ff"/><stop offset="1" stop-color="#ff2bd6"/></linearGradient>
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse"><path d="M40 0H0V40" fill="none" stroke="#00f0ff" stroke-opacity=".07"/></pattern>
<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.5" fill="#000" opacity=".3"/></pattern>
<filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="3" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'''

def chips(items, x0, y, h=34, size=14):
    out, x = "", x0
    for t in items:
        w = round(len(t) * 9.4 + 30)
        out += (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="17" fill="#0b0b22" stroke="url(#neon)" stroke-width="1.6"/>'
                f'<text x="{x+w/2}" y="{y+h/2+5}" text-anchor="middle" class="chip">{t}</text>')
        x += w + 12
    return out


pages = [
 [ ("role","Full Stack Engineer | AI &amp; Cloud-Native Systems"),
   ("backend","Java, Spring Boot, Python, FastAPI, Node.js"),
   ("frontend","React, TypeScript, Angular, Redux"),
   ("ai","LLMs, RAG, LangGraph, LangChain, MCP"),
   ("ml/dl","Machine Learning, Deep Learning, model serving"),
   ("cloud","AWS, Azure, GCP, Docker, Kubernetes, Terraform"),
   ("data","PostgreSQL, pgvector, Oracle, MongoDB, Kafka"),
   ("security","OAuth2, JWT, SSO, Okta, encryption"),
   ("testing","JUnit, Jest, Cypress, Playwright, LLM tests"),
   ("quality","Secure, tested, observable, production-ready") ],
 [ ("llm","Claude API, OpenAI, Azure OpenAI, prompt engineering"),
   ("rag","Chunking, embeddings, pgvector, Azure AI Search"),
   ("agents","LangGraph, LangChain, OpenAI Agents SDK, tool calling"),
   ("mcp","MCP servers, function calling, governed enterprise APIs"),
   ("ml","Machine Learning, Deep Learning, FastAPI model serving") ],
 [ ("sql","PostgreSQL, Oracle, MySQL, SQL Server, PL/SQL"),
   ("nosql","MongoDB, DynamoDB, Redis"),
   ("streaming","Kafka, Apache Flink, RabbitMQ, SQS/SNS"),
   ("big data","PySpark, Spark, batch and stream pipelines"),
   ("vector","pgvector, Azure AI Search, embeddings, similarity search") ],
]
DUR = 30
CW = 10.9
tl = ""
windows = [(0.01, 0.40), (0.42, 0.68), (0.70, 0.96)]   # per-page start, end (fractions of DUR)
n = 0
for (p0, p1), lines in zip(windows, pages):
    typing = (p1 - p0) * 0.55
    step = typing / len(lines)
    for i, (k, v) in enumerate(lines):
        y = 196 + i * 29
        w = round(len(f"> {k}: {v}".replace("&amp;", "&")) * CW)
        st = p0 + i * step
        en = st + step * 0.9
        ke = p1
        kt = f"0;{st:.4f};{en:.4f};{ke:.4f};{ke+0.005:.4f};1"
        tl += (f'<clipPath id="c{n}"><rect x="56" y="{y-20}" width="0" height="26"><animate attributeName="width" dur="{DUR}s" repeatCount="indefinite" keyTimes="{kt}" values="0;0;{w};{w};0;0"/></rect></clipPath>'
               f'<text x="60" y="{y}" class="tl" clip-path="url(#c{n})"><tspan class="k">&gt; {k}:</tspan> {v}</text>')
        n += 1


cx, cy = 990, 262
ringC = ["Java","Python","TypeScript","React","Angular","Node.js","Spring Boot","AWS","Azure","GCP","Docker","K8s"]
ringB = ["FastAPI","LangGraph","LangChain","RAG","MCP","Kafka","PostgreSQL","MongoDB"]
ringA = ["LLMs","ML","DL","pgvector"]
RING = [(64, ringA, "#8a2be2"), (118, ringB, "#ff2bd6"), (166, ringC, "#00f0ff")]
def boxes(offs):
    bx = []
    for (r, labels, _), off in zip(RING, offs):
        n = len(labels)
        for i, t in enumerate(labels):
            ang = math.radians(off) + 2*math.pi*i/n
            x, y = r*math.cos(ang), r*math.sin(ang)
            w = len(t)*6.6 + 18
            bx.append((x, y, w, 22, t))
    return bx
def overlaps(bx, pad=5):
    c = 0
    for i in range(len(bx)):
        for j in range(i+1, len(bx)):
            a, b = bx[i], bx[j]
            if abs(a[0]-b[0]) < (a[2]+b[2])/2+pad and abs(a[1]-b[1]) < (a[3]+b[3])/2+pad: c += 1
    return c
def inside(bx): return all(abs(x)+w/2 <= 196 and abs(y)+11 <= 215 for x, y, w, h, t in bx)
best = None
for oa in range(0, 90, 5):
    for ob in range(0, 45, 3):
        for oc in range(0, 30, 2):
            bx = boxes((oa, ob, oc))
            sc = overlaps(bx) * 100 + (0 if inside(bx) else 50)
            if best is None or sc < best[0]: best = (sc, (oa, ob, oc), bx)
print("orbit layout score", best[0], best[1])
bx = best[2]
labels_svg = ""
k = 0
for (r, labels, col) in RING:
    for t in labels:
        x, y, w, h, _ = bx[k]
        labels_svg += (f'<g transform="translate({x:.1f},{y:.1f})"><rect x="{-w/2:.1f}" y="-11" width="{w:.1f}" height="22" rx="11" fill="#0b0b22" stroke="{col}" stroke-width="1.5">'
                       f'<animate attributeName="stroke-opacity" values="1;.45;1" dur="{3+k%5*.6:.1f}s" begin="{(k%7)*.4:.1f}s" repeatCount="indefinite"/></rect>'
                       f'<text x="0" y="4" text-anchor="middle" class="ot">{t}</text></g>')
        k += 1
rings_svg = ""
for (r, labels, col), d, dirn in zip(RING, (14, 22, 30), (1, -1, 1)):
    rings_svg += (f'<circle r="{r}" fill="none" stroke="{col}" stroke-opacity=".4" stroke-width="1.5" stroke-dasharray="3 7"/>'
                  f'<g><animateTransform attributeName="transform" type="rotate" from="0" to="{360*dirn}" dur="{d}s" repeatCount="indefinite"/>'
                  f'<circle cx="{r}" cy="0" r="4" fill="{col}" filter="url(#glow)"/></g>')
figure = (f'<g transform="translate({cx},{cy})">'
  '<circle r="205" fill="#8a2be2" opacity=".14" filter="url(#glow)"/>'
  + rings_svg + labels_svg +
  '<polygon points="0,-34 29.4,-17 29.4,17 0,34 -29.4,17 -29.4,-17" fill="#0b0b22" stroke="url(#neon)" stroke-width="3" filter="url(#glow)"><animate attributeName="stroke-width" values="2;4;2" dur="2.4s" repeatCount="indefinite"/></polygon>'
  '<rect x="-12" y="-12" width="24" height="24" rx="4" fill="none" stroke="#00f0ff" stroke-width="2"/>'
  '<path d="M-18 -6H-12M-18 6H-12M12 -6H18M12 6H18M-6 -18V-12M6 -18V-12M-6 12V18M6 12V18" stroke="#ff2bd6" stroke-width="2" stroke-linecap="round"/>'
  '<text x="0" y="4.5" text-anchor="middle" class="core">AI</text></g>')

banner = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" aria-label="Mallikarjun - Full Stack and AI Engineer">
<defs>{DEFS}
<style>
.tag{{font:700 13px 'Courier New',monospace;fill:#ff2bd6;letter-spacing:4px}}
.name{{font:800 58px 'Segoe UI',Arial,sans-serif;fill:url(#neon);letter-spacing:1px}}
.sub{{font:600 23px 'Segoe UI',Arial,sans-serif;fill:#e8f7ff;letter-spacing:1px}}
.tl{{font:600 18px 'Courier New',Consolas,monospace;fill:#e8f7ff}}
.k{{fill:#ff2bd6}}
.chip{{font:700 13.5px 'Segoe UI',Arial,sans-serif;fill:#c9f6ff;letter-spacing:.5px}}
.ot{{font:700 10.5px 'Segoe UI',Arial,sans-serif;fill:#d9f8ff}}
.core{{font:800 14px 'Segoe UI',Arial,sans-serif;fill:#fff}}
</style></defs>
<rect width="{W}" height="{H}" rx="18" fill="url(#bg)"/><rect width="{W}" height="{H}" rx="18" fill="url(#grid)"/>
<rect x="2" y="2" width="{W-4}" height="{H-4}" rx="17" fill="none" stroke="url(#neon)" stroke-width="3" filter="url(#glow)"/>
<text x="60" y="62" class="tag">// INTRO</text>
<text x="60" y="132" class="name" filter="url(#glow)">Mallikarjun Kotupalli</text>
<rect x="60" y="150" width="220" height="3" fill="url(#neon)"/>
{tl}
{figure}
<rect x="3" y="3" width="{W-6}" height="{H-6}" rx="16" fill="url(#scan)" opacity=".2"/>
</svg>'''
open("assets/banner.svg", "w").write(banner)

# ---------- AI architecture diagram ----------
def box(x, y, w, h, title, sub, hot=False):
    st = 'url(#neon)' if hot else '#00f0ff'
    return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="#0b0b22" stroke="{st}" stroke-width="{2.4 if hot else 1.6}" {"filter=\"url(#glow)\"" if hot else ""}/>'
            f'<text x="{x+w/2}" y="{y+h/2-3}" text-anchor="middle" class="bt">{title}</text>'
            f'<text x="{x+w/2}" y="{y+h/2+19}" text-anchor="middle" class="bs">{sub}</text>')
paths = [
 ("p1","M250 100 L290 100"), ("p2","M520 100 L560 100"), ("p3","M790 100 L830 100"),
 ("p4","M250 270 L290 270"), ("p5","M520 270 L560 270"),
 ("p6","M675 232 L675 140"), ("p7","M910 232 L910 140"),
]
lines = "".join(f'<path id="{i}" d="{d}" stroke="#00f0ff" stroke-opacity=".5" stroke-width="2" fill="none" stroke-dasharray="4 5"/>' for i, d in paths)
dots = "".join(f'<circle r="4.5" fill="#ff2bd6" filter="url(#glow)"><animateMotion dur="{2+i*.15:.2f}s" repeatCount="indefinite"><mpath href="#{p}"/></animateMotion></circle>' for i, (p, _) in enumerate(paths))
ai = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="1200" height="380" role="img" aria-label="AI platform architecture: RAG, agents, MCP and LLMs">
<defs>{DEFS}<style>.bt{{font:700 17px 'Segoe UI',Arial,sans-serif;fill:#fff}}.bs{{font:500 12.5px 'Segoe UI',Arial,sans-serif;fill:#8fe9ff}}.h{{font:700 13px 'Courier New',monospace;fill:#ff2bd6;letter-spacing:4px}}</style></defs>
<rect width="1200" height="380" rx="18" fill="url(#bg)"/><rect width="1200" height="380" rx="18" fill="url(#grid)"/>
<rect x="2" y="2" width="1196" height="376" rx="17" fill="none" stroke="url(#neon)" stroke-width="2.5" filter="url(#glow)"/>
<text x="40" y="44" class="h">// AI ENGINEERING - HOW I BUILD IT</text>
{lines}
{box(40,70,210,60,"React UI","TypeScript | Streaming")}
{box(290,70,230,60,"Spring Boot API","Java | Security | Validation")}
{box(560,70,230,60,"Agent Orchestrator","Python | FastAPI | LangGraph",True)}
{box(830,70,330,60,"LLM Providers","Claude | OpenAI | Azure OpenAI")}
{box(40,240,210,60,"Enterprise Data","Docs | APIs | Databases")}
{box(290,240,230,60,"Embeddings","Chunking | Vectorization")}
{box(560,240,230,60,"Vector Store","pgvector | Azure AI Search")}
{box(830,240,330,60,"MCP Tools","MCP Servers | Function Calling")}
{dots}
<text x="40" y="350" class="bs">Guardrails | Structured JSON outputs | Output validation | LLM integration tests | Observability | CI/CD on AWS, Azure and GCP</text>
</svg>'''
open("assets/ai-stack.svg", "w").write(ai)
print("ok", "photo" if photo else "character")

# ---------- Full stack architecture diagram ----------
fs_boxes = (
 box(40,70,210,60,"React | Angular","TypeScript | Redux | Next.js")
 + box(290,70,230,60,"API Gateway","OAuth2 | JWT | SSO | REST")
 + box(560,70,230,60,"Spring Boot Services","Java | Microservices | Python",True)
 + box(830,70,330,60,"Event Streaming","Kafka | RabbitMQ | SQS/SNS | Flink")
 + box(40,240,210,60,"CI/CD","GitHub Actions | Jenkins | GitLab")
 + box(290,240,230,60,"Containers","Docker | Kubernetes | Helm")
 + box(560,240,230,60,"Cloud","AWS | Azure | GCP | Terraform")
 + box(830,240,330,60,"Data Stores","PostgreSQL | Oracle | MongoDB | Redis"))
fs_paths = [("q1","M250 100 L290 100"),("q2","M520 100 L560 100"),("q3","M790 100 L830 100"),
            ("q4","M250 270 L290 270"),("q5","M520 270 L560 270"),("q6","M675 140 L675 232"),("q7","M910 140 L910 232")]
fl = "".join(f'<path id="{i}" d="{d}" stroke="#00f0ff" stroke-opacity=".5" stroke-width="2" fill="none" stroke-dasharray="4 5"/>' for i, d in fs_paths)
fd = "".join(f'<circle r="4.5" fill="#ff2bd6" filter="url(#glow)"><animateMotion dur="{2+i*.15:.2f}s" repeatCount="indefinite"><mpath href="#{p}"/></animateMotion></circle>' for i, (p, _) in enumerate(fs_paths))
fs = f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 380" width="1200" height="380" role="img" aria-label="Full stack engineering architecture">
<defs>{DEFS}<style>.bt{{font:700 17px 'Segoe UI',Arial,sans-serif;fill:#fff}}.bs{{font:500 12.5px 'Segoe UI',Arial,sans-serif;fill:#8fe9ff}}.h{{font:700 13px 'Courier New',monospace;fill:#ff2bd6;letter-spacing:4px}}</style></defs>
<rect width="1200" height="380" rx="18" fill="url(#bg)"/><rect width="1200" height="380" rx="18" fill="url(#grid)"/>
<rect x="2" y="2" width="1196" height="376" rx="17" fill="none" stroke="url(#neon)" stroke-width="2.5" filter="url(#glow)"/>
<text x="40" y="44" class="h">// FULL STACK ENGINEERING - HOW I BUILD IT</text>
{fl}{fs_boxes}{fd}
<text x="40" y="350" class="bs">Clean architecture | REST and GraphQL | Secure by design | Automated testing | Observability | Infrastructure as Code</text>
</svg>'''
open("assets/fullstack-stack.svg", "w").write(fs)
print("fullstack ok")
