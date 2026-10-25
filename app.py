import base64
import hashlib
import hmac
import html
import json
import os
import re
import secrets as pysecrets
import textwrap
import time
import uuid
from datetime import datetime, timedelta, timezone

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components

APP_VERSION = "4.0.3-Supernova"

# ============================== 1. BRAND & PAGE ==============================
SVG_RAW = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#3b82f6"/><stop offset="100%" stop-color="#8b5cf6"/></linearGradient></defs><rect width="120" height="120" rx="28" fill="#11151c" stroke="url(#g)" stroke-width="6"/><path d="M34 38 L60 86 L86 38" fill="none" stroke="url(#g)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><circle cx="60" cy="34" r="7" fill="#ffffff"/></svg>'
LOGO_B64 = "data:image/svg+xml;base64," + base64.b64encode(SVG_RAW.encode()).decode()

if not os.path.exists("void_logo.svg"):
    try:
        with open("void_logo.svg", "w", encoding="utf-8") as f:
            f.write(SVG_RAW)
    except OSError:
        pass
LOGO_PATH = next((p for p in ("logo.png", "void_logo.svg") if os.path.exists(p)), "⚡")

st.set_page_config(page_title="VOID — Sovereign OS Intelligence",
                    page_icon=LOGO_PATH, layout="wide", initial_sidebar_state="expanded")
try:
    if LOGO_PATH != "⚡":
        st.logo(LOGO_PATH)
except Exception:
    pass

# --- MATERIAL SLATE OS THEME & ABSOLUTE TEXT READABILITY FIXES ---
st.markdown("""<style>
.stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
    background-color: #11151c !important;
    color: #f8fafc !important;
}
[data-testid="stForm"] {
    background: linear-gradient(145deg, #181f2c, #11151c) !important;
    border: 1px solid rgba(59,130,246,.3) !important;
    border-radius: 18px !important;
    padding: 24px !important;
    box-shadow: 0 12px 35px rgba(0,0,0,.5) !important;
}
[data-testid="stToolbarActions"], [data-testid="stAppDeployButton"], [data-testid="stDecoration"], [data-testid="stStatusWidget"] {
    display: none !important;
}
#MainMenu, footer { visibility: hidden !important; }
header[data-testid="stHeader"] { background: transparent !important; }
.block-container { padding-top: 1rem !important; padding-bottom: 5rem !important; max-width: 1420px; }
section[data-testid="stSidebar"] { background: #0d1117 !important; border-right: 1px solid rgba(59,130,246,.15); }

/* HIGH CONTRAST TEXT GLOBALS */
p, span, label, h1, h2, h3, h4, h5, h6, .stMarkdown, .stText {
    color: #f8fafc !important;
}
.stChatMessage {
    border-radius: 16px;
    padding: 18px 22px;
    margin-bottom: 14px;
    border: 1px solid rgba(59,130,246,0.3);
    background: rgba(24,31,44,0.98) !important;
    box-shadow: 0 6px 24px rgba(0,0,0,0.4);
}
.stChatMessage p, .stChatMessage div, .stChatMessage span, .stChatMessage li {
    color: #ffffff !important;
    font-size: 1.03rem !important;
}

/* FIX CHAT INPUT BOX (NO MORE WHITE BOX / INVISIBLE TEXT) */
[data-testid="stChatInput"] {
    background-color: #161d2a !important;
    border: 1px solid #3b82f6 !important;
    border-radius: 16px !important;
}
[data-testid="stChatInput"] textarea {
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
    background-color: transparent !important;
}
[data-testid="stChatInput"] textarea::placeholder {
    color: #94a3b8 !important;
    -webkit-text-fill-color: #94a3b8 !important;
}

.prism-card { background: #161d2a; border: 1px solid rgba(59,130,246,.35); border-radius: 16px; padding: 20px; box-shadow: 0 10px 30px rgba(0,0,0,.45); }
.void-hero { text-align: center; padding: 28px 10px 20px; }
.void-gradient { font-size: 2.8rem; font-weight: 800; letter-spacing: -.5px; background: linear-gradient(135deg,#3b82f6,#60a5fa 40%,#a78bfa); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 6px; }
.void-sub { font-size: 1.12rem; color: #cbd5e1 !important; margin-bottom: 22px; }
.topbar-brand { display: flex; align-items: center; gap: 12px; margin-bottom: 16px; }
.topbar-title { font-size: 1.45rem; font-weight: 800; letter-spacing: 2px; color: #fff; }
.topbar-pill { font-size: .65rem; padding: 3px 10px; border-radius: 99px; background: rgba(59,130,246,0.25); color: #60a5fa; border: 1px solid rgba(59,130,246,.5); font-weight: 700; }
.void-footer { text-align: center; color: #64748b !important; font-size: .78rem; padding: 26px 0 8px; letter-spacing: .4px; }
.void-footer span { color: #64748b !important; }
.stButton button { border-radius: 12px !important; border: 1px solid rgba(148,163,184,.3) !important; background: #1e293b !important; color: #f8fafc !important; transition: all .2s ease !important; font-weight: 600 !important; }
.stButton button:hover { border-color: #3b82f6 !important; background: #2563eb !important; box-shadow: 0 0 14px rgba(59,130,246,.5) !important; }
</style>""", unsafe_allow_html=True)

# ============================== 2. CONFIG & SECRETS ==============================
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
EMAILJS_URL = "https://api.emailjs.com/api/v1.0/email/send"
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
WIKI_URL = "https://en.wikipedia.org/w/api.php"
DB_FILE, KEY_FILE = "void_hub_db.json", ".void_signing_key"
MAX_HISTORY, MAX_FILE_CHARS = 24, 40000
OTP_TTL, OTP_MAX_TRIES, OTP_COOLDOWN, LOGIN_DAYS = 600, 5, 30, 365
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")

ENGINES = {
    "☀️ Supernova X (Master Coding Architect)": "qwen/qwen-2.5-coder-32b-instruct",
    "🪐 Nebula Core (Deep Logic Engine)": "deepseek/deepseek-chat",
    "🌙 Void Moon (Swift Resonance)": "google/gemini-2.5-flash",
}

def sget(key, default=""):
    try:
        return str(st.secrets[key]).strip()
    except Exception:
        return default

API_KEY = sget("OPENROUTER_API_KEY")
EJS_SERVICE, EJS_TEMPLATE = sget("EMAILJS_SERVICE_ID"), sget("EMAILJS_TEMPLATE_ID")
EJS_PUBLIC, EJS_PRIVATE = sget("EMAILJS_PUBLIC_KEY"), sget("EMAILJS_PRIVATE_KEY")
FOUNDERS = {e.strip().lower() for e in sget("FOUNDER_EMAILS").split(",") if e.strip()}
FOUNDER_NAME = sget("FOUNDER_NAME", "Avyan")
FOUNDER_BIO = sget("FOUNDER_BIO", "14-year-old Founder & Lead Architect of VOID, student at Sunbeam School Varuna in Varanasi, creator of VoidOS, author of World Zero, and gamer (NOTREFLEXGAMING05).")

def esc(s):
    return html.escape(str(s))

def safe_name(s, n=25):
    return re.sub(r"\W+", "_", s).strip("_")[:n] or "VOID"

@st.cache_resource(show_spinner=False)
def http_session():
    s = requests.Session()
    s.headers.update({"User-Agent": f"VOIDCore/{APP_VERSION}", "X-Title": "VOID"})
    return s

# ============================== 3. DATABASE ==============================
def load_db():
    try:
        with open(DB_FILE, encoding="utf-8") as f:
            d = json.load(f)
        d.setdefault("users", {})
        d.setdefault("chats", {})
        d.setdefault("usage", {})
        return d
    except Exception:
        return {"users": {}, "chats": {}, "usage": {}}

def save_db(d):
    try:
        tmp = DB_FILE + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(d, f, indent=2)
        os.replace(tmp, DB_FILE)
    except OSError:
        pass

db = load_db()

def new_chat(email):
    cid = uuid.uuid4().hex[:8]
    db["chats"].setdefault(email, {})[cid] = {"title": "New Session", "messages": []}
    return cid

def ensure_user(email, name=None):
    now = datetime.now().strftime("%b %d, %H:%M")
    founder = email in FOUNDERS or "avyan" in email.lower()
    rec = db["users"].get(email)
    if rec is None:
        nm = FOUNDER_NAME if founder else (name or email.split("@")[0].capitalize())
        rec = {"name": nm, "city": "Varanasi", "joined": now, "last_active": now, "prompts": 0,
               "memory": FOUNDER_BIO if founder else f"Verified member of VOID Studio ({nm}).",
               "recent_topics": []}
        db["users"][email] = rec
    else:
        rec.setdefault("recent_topics", [])
        rec["last_active"] = now
        if name and not founder:
            rec["name"] = name
    if not db["chats"].get(email):
        new_chat(email)
    save_db(db)
    return rec

def bump_daily_usage():
    today = datetime.now().strftime("%Y-%m-%d")
    db.setdefault("usage", {})
    db["usage"][today] = db["usage"].get(today, 0) + 1
    if len(db["usage"]) > 60:
        for k in sorted(db["usage"])[:-60]:
            db["usage"].pop(k, None)

# ============================== 4. BULLETPROOF SIGNED LOGIN ==============================
def signing_key():
    k = sget("APP_SECRET")
    if k:
        return k.encode()
    try:
        if not os.path.exists(KEY_FILE):
            with open(KEY_FILE, "w") as f:
                f.write(pysecrets.token_hex(32))
        with open(KEY_FILE) as f:
            return f.read().strip().encode()
    except OSError:
        return (API_KEY or "void").encode()

def sign(email, ts):
    return hmac.new(signing_key(), f"{email}|{ts}".encode(), hashlib.sha256).hexdigest()[:32]

def remember_login(email):
    ts = str(int(time.time()))
    qp = st.query_params
    if qp.get("user") != email or not qp.get("ts") or not qp.get("sig"):
        qp.update({"user": email, "ts": ts, "sig": sign(email, ts)})

def restore_login():
    qp = st.query_params
    email, ts, sig = qp.get("user"), qp.get("ts"), qp.get("sig")
    if email and ts and sig and str(ts).isdigit() and time.time() - int(ts) < LOGIN_DAYS * 86400:
        if hmac.compare_digest(str(sig), sign(str(email), str(ts))):
            return str(email)
    return None

# ============================== 5. LIVE CONTEXT ==============================
WMO = {0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast", 45: "Foggy", 48: "Rime fog",
       51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle", 61: "Light rain", 63: "Moderate rain",
       65: "Heavy rain", 71: "Light snow", 73: "Snow", 75: "Heavy snow", 80: "Rain showers",
       81: "Heavy showers", 95: "Thunderstorm", 96: "Thunderstorm with hail"}

@st.cache_data(ttl=3600, show_spinner=False)
def geocode(city):
    r = http_session().get(GEO_URL, params={"name": city, "count": 1, "language": "en", "format": "json"}, timeout=5).json()
    res = (r.get("results") or [None])[0]
    if not res:
        return None
    label = ", ".join(filter(None, [res.get("name"), res.get("admin1"), res.get("country")]))
    return res["latitude"], res["longitude"], label

@st.cache_data(ttl=600, show_spinner=False)
def fetch_live_weather(city):
    try:
        lat, lon, label = geocode(city) or (25.3176, 82.9739, "Varanasi, Uttar Pradesh, India")
        d = http_session().get(WEATHER_URL, params={
            "latitude": lat, "longitude": lon, "timezone": "auto",
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
            "daily": "temperature_2m_max,temperature_2m_min"}, timeout=5).json()
        cur, day = d.get("current", {}), d.get("daily", {})
        return (f"[LIVE WEATHER — {label}]: {WMO.get(cur.get('weather_code'), 'Partly cloudy')} | "
                f"Temp {cur.get('temperature_2m')}°C (feels {cur.get('apparent_temperature')}°C) | "
                f"High/Low {day.get('temperature_2m_max', ['N/A'])[0]}°C / {day.get('temperature_2m_min', ['N/A'])[0]}°C | "
                f"Humidity {cur.get('relative_humidity_2m')}% | Wind {cur.get('wind_speed_10m')} km/h")
    except Exception:
        return "[Weather feed temporarily unavailable]"

@st.cache_data(ttl=1800, show_spinner=False)
def fetch_live_knowledge(query):
    try:
        q = re.sub(r"[^a-zA-Z0-9\s]", "", query).strip()[:120]
        if len(q) < 3:
            return ""
        r = http_session().get(WIKI_URL, params={"action": "query", "list": "search", "srsearch": q, "format": "json", "srlimit": 2},
                       headers={"User-Agent": f"VOIDCore/{APP_VERSION}"}, timeout=4).json()
        snips = [re.sub(r"<.*?>", "", x.get("snippet", "")) for x in r.get("query", {}).get("search", [])]
        return f"[LIVE ARCHIVE DATA]: {' | '.join(snips)}" if snips else ""
    except Exception:
        return ""

@st.cache_data(ttl=900, show_spinner=False)
def engine_status():
    if not API_KEY:
        return "offline", "add OPENROUTER_API_KEY to secrets"
    try:
        r = http_session().get(OPENROUTER_MODELS_URL, timeout=6)
        if r.status_code == 200:
            n = len(r.json().get("data", []))
            return "online", f"link stable • {n} models reachable"
        return "error", f"gateway HTTP {r.status_code}"
    except Exception as e:
        return "error", str(e)[:70]

WEATHER_WORDS = ("weather", "temperature", "temp", "rain", "forecast", "climate", "outside", "cold", "hot", "humidity")
KNOW_WORDS = ("who is", "what is", "tell me about", "history of", "explain", "news", "search")

def build_live_context(prompt, default_city):
    now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    lines = [f"[CHRONOMETER]: {now.strftime('%A, %B %d, %Y | %I:%M %p IST')}"]
    p = prompt.lower()
    if any(w in p for w in WEATHER_WORDS):
        m = re.search(r"\b(?:in|at|for|of)\s+([a-z][a-z ]{2,24}?)(?:\s+(?:right|today|now|tomorrow)\b|[?.!,]|$)", p)
        lines.append(fetch_live_weather(m.group(1).strip().title() if m else default_city))
    if any(k in p for k in KNOW_WORDS):
        ctx = fetch_live_knowledge(prompt)
        if ctx:
            lines.append(ctx)
    return "\n".join(lines)

# ============================== 6. BULLETPROOF PDF FORGE (UNICODE SAFE) ==============================
DOC_TRIGGERS = ("pdf", "ppt", "powerpoint", "slide", "presentation", "study notes", "revision notes", "make notes",
                "write notes", "study guide", "cheat sheet", "exam questions", "question bank", "worksheet",
                "report", "document", "build a web app", "build an app", "create a web app", "html app", "make a game")

def detect_prism_intent(prompt, reply=""):
    return any(t in prompt.lower() for t in DOC_TRIGGERS) or "```html" in reply.lower()

def clean_for_pdf(text):
    for k, v in {"—": "-", "–": "-", "“": '"', "”": '"', "‘": "'", "’": "'", "•": "*", "…": "...", "→": "->"}.items():
        text = text.replace(k, v)
    return text.encode("latin-1", "ignore").decode("latin-1")

def pdf_escape(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

PDF_STYLE = {"TITLE": ("F2", 16, 50, 0, 24), "META": ("F1", 9, 50, 0, 18), "H1": ("F2", 13, 50, 6, 18),
             "BULLET": ("F1", 10.5, 56, 0, 15), "BODY": ("F1", 10.5, 50, 0, 15)}

@st.cache_data(show_spinner=False, max_entries=64)
def generate_real_pdf_bytes(title, markdown, author="VOID Forge"):
    safe_title = clean_for_pdf(title)
    safe_md = clean_for_pdf(markdown)
    lines = [("TITLE", safe_title),
             ("META", clean_for_pdf(f"Architected by {author} | {datetime.now():%Y-%m-%d %H:%M}")), ("SPACE", "")]
    for raw in safe_md.split("\n"):
        s = raw.strip()
        if not s:
            lines.append(("SPACE", ""))
        elif s.startswith("#"):
            h = s.lstrip("#").strip().replace("**", "")
            lines += [("H1", w) for w in textwrap.wrap(h, 68) or [h]]
        elif s.startswith(("* ", "- ", "+ ")):
            w = textwrap.wrap(s[2:].replace("**", "").replace("`", ""), 78) or [""]
            lines.append(("BULLET", "* " + w[0]))
            lines += [("BODY", "  " + x) for x in w[1:]]
        else:
            c = s.replace("**", "").replace("__", "").replace("`", "")
            lines += [("BODY", w) for w in textwrap.wrap(c, 82) or [c]]

    pages, cur, y = [], [], 790
    for kind, text in lines:
        if y < 60:
            pages.append("\n".join(cur))
            cur, y = [], 790
        if kind == "SPACE":
            y -= 9
            continue
        font, size, x, pre, post = PDF_STYLE[kind]
        y -= pre
        cur.append(f"BT /{font} {size} Tf 1 0 0 1 {x} {y} Tm ({pdf_escape(text)}) Tj ET")
        y -= post
    pages.append("\n".join(cur))

    total = len(pages)
    ids = [5 + i * 2 for i in range(total)]
    objs = [b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
            f"2 0 obj\n<< /Type /Pages /Kids [{' '.join(f'{i} 0 R' for i in ids)}] /Count {total} >>\nendobj\n".encode(),
            b"3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>\nendobj\n",
            b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>\nendobj\n"]
    for i, (pid, stream) in enumerate(zip(ids, pages), start=1):
        footer = f"VOID Prism • Page {i} of {total}"
        sb = (stream + f"\nBT /F1 8 Tf 1 0 0 1 470 28 Tm ({pdf_escape(footer)}) Tj ET").encode("latin-1", errors="ignore")
        objs.append((f"{pid} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                     f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {pid + 1} 0 R >>\nendobj\n").encode())
        objs.append(f"{pid + 1} 0 obj\n<< /Length {len(sb)} >>\nstream\n".encode() + sb + b"\nendstream\nendobj\n")

    out, offsets = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n"), []
    for o in objs:
        offsets.append(len(out))
        out += o
    xref = len(out)
    out += f"xref\n0 {len(objs) + 1}\n0000000000 65535 f \n".encode()
    for off in offsets:
        out += f"{off:010d} 00000 n \n".encode()
    out += f"trailer\n<< /Size {len(objs) + 1} /Root 1 0 R >>\nstartxref\n{xref}\n%%EOF".encode()
    return bytes(out)

SLIDE_TPL = """<!DOCTYPE html><html><head><meta charset="utf-8"><title>%%TITLE%%</title><style>
body{margin:0;background:#11151c;color:#f0f6fc;font-family:'Segoe UI',system-ui,sans-serif;display:flex;flex-direction:column;height:96vh;justify-content:space-between}
.wrap{flex:1;display:flex;align-items:center;justify-content:center;padding:24px}
.slide{display:none;width:100%;max-width:820px;background:linear-gradient(145deg,#181f2c,#11151c);border:1px solid rgba(59,130,246,.4);border-radius:24px;padding:40px 48px;box-shadow:0 20px 50px rgba(0,0,0,.7);min-height:310px;box-sizing:border-box}
.slide.on{display:block}
.badge{font-size:11px;letter-spacing:2px;color:#3b82f6;font-weight:700;margin-bottom:14px}
.count{position:fixed;top:14px;right:20px;font-size:12px;color:#64748b;font-weight:700;letter-spacing:1px}
h2{margin-top:0;font-size:28px;background:linear-gradient(90deg,#3b82f6,#60a5fa,#a78bfa);-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.body{font-size:16px;line-height:1.7;color:#cbd5e1}
code{background:#1e293b;padding:1px 6px;border-radius:5px}
.ctl{display:flex;justify-content:center;gap:16px;padding:14px}
button{background:rgba(59,130,246,.2);color:#60a5fa;border:1px solid rgba(59,130,246,.5);padding:10px 22px;border-radius:99px;cursor:pointer;font-weight:700;transition:.2s}
button:hover{background:#3b82f6;color:#fff;box-shadow:0 0 15px rgba(59,130,246,.5)}
@media print{.ctl{display:none}body{height:auto;background:#fff}.slide{display:block;page-break-after:always;margin-bottom:16px}}
</style></head><body><div class="wrap">%%SLIDES%%</div>
<div class="count">%%COUNT%%</div>
<div class="ctl"><button onclick="go(-1)">◀ Previous</button><button onclick="window.print()">🖨️ Export to PDF</button><button onclick="go(1)">Next ▶</button></div>
<script>let c=0;const s=document.querySelectorAll('.slide');const n=document.querySelector('.count');
function paint(){n.textContent=`SLIDE ${c+1} / ${s.length}`}
function go(d){s[c].classList.remove('on');c=(c+d+s.length)%s.length;s[c].classList.add('on');paint()}
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(1);if(e.key==='ArrowLeft')go(-1)});
paint();</script></body></html>"""

def _md_inline(line):
    line = line.strip()
    head = line.startswith("#")
    line = html.escape(line.lstrip("#").strip() if head else line)
    line = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", line)
    line = re.sub(r"`(.+?)`", r"<code>\1</code>", line)
    line = re.sub(r"^[-*+] ", "• ", line)
    return f"<b>{line}</b>" if head else line

@st.cache_data(show_spinner=False, max_entries=64)
def generate_interactive_slides_html(title, markdown):
    secs = [s for s in re.split(r"(?m)^(?=#{1,2} )", markdown.strip()) if s.strip()]
    if len(secs) <= 1:
        paras = [p.strip() for p in markdown.split("\n\n") if p.strip()]
        secs = ["\n\n".join(paras[i:i + 2]) for i in range(0, len(paras), 2)] or [markdown]
    out = []
    for i, sec in enumerate(secs):
        lines = sec.strip().split("\n")
        heading = lines[0].lstrip("#").strip() or f"Slide {i + 1}"
        body = "<br>".join(_md_inline(l) for l in lines[1:] if l.strip())
        out.append(f'<div class="slide{" on" if i == 0 else ""}"><div class="badge">VOID PRISM DECK • SLIDE {i + 1} OF {len(secs)}</div>'
                    f'<h2>{esc(heading.replace("**", ""))}</h2><div class="body">{body}</div></div>')
    return (SLIDE_TPL.replace("%%TITLE%%", esc(title)).replace("%%COUNT%%", f"SLIDE 1 / {len(secs)}")
            .replace("%%SLIDES%%", "".join(out)))

def extract_code_blocks(text):
    return re.findall(r"```(\w*)\n(.*?)```", text, re.DOTALL)

def is_html_block(b):
    return b[0].lower() in ("html", "xml", "svg") or "<html" in b[1].lower() or "<style" in b[1].lower()

# ============================== 7. SERVICES (EMAIL + AI ENGINE) ==============================
def send_otp_email(to, code):
    if not (EJS_SERVICE and EJS_TEMPLATE and EJS_PUBLIC):
        return False, "Email service is not configured."
    payload = {"service_id": EJS_SERVICE, "template_id": EJS_TEMPLATE, "user_id": EJS_PUBLIC,
               "template_params": {"to_email": to, "otp_code": code}}
    if EJS_PRIVATE:
        payload["accessToken"] = EJS_PRIVATE
    try:
        r = http_session().post(EMAILJS_URL, json=payload, timeout=30)
        return (True, None) if r.status_code == 200 else (False, r.text[:200])
    except requests.RequestException as e:
        return False, str(e)

class EngineError(Exception):
    pass

def _post(choice, system, msgs, temp, tokens, stream=False):
    if not API_KEY:
        raise EngineError("Master key missing: add OPENROUTER_API_KEY to your app secrets.")
    msgs = [{"role": m["role"], "content": m["content"]} for m in msgs[-MAX_HISTORY:]]
    body = {"model": ENGINES.get(choice, "qwen/qwen-2.5-coder-32b-instruct"), "temperature": temp,
            "max_tokens": tokens, "stream": stream, "messages": [{"role": "system", "content": system}] + msgs}
    headers = {"Authorization": f"Bearer {API_KEY}", "Content-Type": "application/json"}
    last_err = None
    for attempt in range(2):  # one automatic retry on transient connection failures
        try:
            r = http_session().post(OPENROUTER_URL, headers=headers, json=body, timeout=90, stream=stream)
            if r.status_code == 429 or r.status_code >= 500:
                last_err = EngineError(f"Engine busy ({r.status_code}): {r.text[:200]}")
                if attempt == 0:
                    time.sleep(1.5)
                    continue
                raise last_err
            if r.status_code != 200:
                raise EngineError(f"Engine error ({r.status_code}): {r.text[:300]}")
            r.encoding = "utf-8"
            return r
        except requests.RequestException as e:
            last_err = EngineError(f"Connection interrupted: {e}")
            if attempt == 0:
                time.sleep(1.5)
                continue
            raise last_err
    raise last_err or EngineError("Unknown engine failure.")

def call_void_engine(choice, system, msgs, temp=0.25, tokens=2000):
    try:
        return _post(choice, system, msgs, temp, tokens).json()["choices"][0]["message"]["content"], None
    except EngineError as e:
        return None, str(e)
    except (KeyError, IndexError, ValueError):
        return None, "The engine returned an unexpected response."

def stream_void_engine(choice, system, msgs, temp=0.25, tokens=2000):
    r = _post(choice, system, msgs, temp, tokens, stream=True)
    for line in r.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data:"):
            continue
        chunk = line[5:].strip()
        if chunk == "[DONE]":
            break
        try:
            delta = json.loads(chunk)["choices"][0]["delta"].get("content")
        except (ValueError, KeyError, IndexError):
            continue
        if delta:
            yield delta


def clean_stream(gen):
    """Buffer the raw token stream into larger, smoother chunks (calm typing mode)."""
    buf = ""
    for chunk in gen:
        buf += chunk
        if len(buf) >= 120:
            yield buf
            buf = ""
    if buf:
        yield buf
# ============================== 8. AUTHENTICATION GATE & PERSISTENCE FIX ==============================
if "user_email" not in st.session_state:
    restored = restore_login()
    if restored:
        st.session_state.user_email = restored

if "user_email" not in st.session_state:
    st.markdown(f'<div class="void-hero"><img src="{LOGO_B64}" width="72" style="margin-bottom:14px;"/>'
                '<div class="void-gradient">Welcome to VOID</div><div class="void-sub">Secure OTP Authentication Gateway</div></div>',
                unsafe_allow_html=True)
    _, mid, _ = st.columns([1, 1.3, 1])
    with mid:
        if "pending_email" not in st.session_state:
            with st.form("email_form"):
                email_in = st.text_input("Email Address", placeholder="name@example.com", max_chars=80).strip().lower()
                name_in = st.text_input("Display Name", placeholder="Your name", max_chars=40).strip()
                if st.form_submit_button("Send Verification Code", type="primary", use_container_width=True):
                    wait = OTP_COOLDOWN - (time.time() - st.session_state.get("last_otp_ts", 0))
                    if not EMAIL_RE.match(email_in):
                        st.error("Please enter a valid email address.")
                    elif wait > 0:
                        st.warning(f"Please wait {int(wait)}s before requesting another code.")
                    else:
                        code = str(pysecrets.randbelow(900000) + 100000)
                        ok, err = send_otp_email(email_in, code)
                        st.session_state.last_otp_ts = time.time()
                        if ok:
                            st.session_state.update(pending_email=email_in, pending_name=name_in, target_otp=code,
                                                    otp_expiry=time.time() + OTP_TTL, otp_tries=0)
                            st.rerun()
                        else:
                            st.error(f"Could not send the email: {err}")
        else:
            st.info(f"Code sent to **{st.session_state.pending_email}** (valid for 10 minutes)")
            with st.form("otp_form"):
                otp_in = st.text_input("6-Digit Code", placeholder="123456", max_chars=6)
                verify = st.form_submit_button("Verify & Enter VOID", type="primary", use_container_width=True)
                back = st.form_submit_button("Use a Different Email", use_container_width=True)
                if back:
                    for k in ("pending_email", "target_otp", "otp_expiry", "otp_tries"):
                        st.session_state.pop(k, None)
                    st.rerun()
                if verify:
                    st.session_state.otp_tries += 1
                    if time.time() > st.session_state.otp_expiry:
                        st.error("This code has expired. Request a new one.")
                    elif st.session_state.otp_tries > OTP_MAX_TRIES:
                        st.error("Too many attempts. Request a new code.")
                    elif hmac.compare_digest(otp_in.strip(), st.session_state.target_otp):
                        email = st.session_state.pending_email
                        ensure_user(email, st.session_state.get("pending_name") or None)
                        st.session_state.user_email = email
                        remember_login(email)
                        for k in ("pending_email", "pending_name", "target_otp", "otp_expiry", "otp_tries"):
                            st.session_state.pop(k, None)
                        st.rerun()
                    else:
                        st.error("❌ Incorrect code. Please try again.")
    st.stop()
else:
    # Always refresh login state query params so session remains active across re-runs
    remember_login(st.session_state.user_email)

# ============================== 9. ACTIVE USER ==============================
user_email = st.session_state.user_email
is_founder = user_email in FOUNDERS
user_record = db["users"].get(user_email) or ensure_user(user_email)
user_name = user_record.get("name", "Member")
user_city = user_record.get("city", "Varanasi")
user_memory = user_record.get("memory", "")
safe_user = esc(user_name)

user_chats = db["chats"].setdefault(user_email, {})
if not user_chats:
    new_chat(user_email)
    save_db(db)
if st.session_state.get("current_chat_id") not in user_chats:
    st.session_state.current_chat_id = list(user_chats)[-1]
current_chat_id = st.session_state.current_chat_id
current_chat = user_chats[current_chat_id]

# ============================== 10. SIDEBAR ==============================
with st.sidebar:
    st.markdown(f'<div class="topbar-brand"><img src="{LOGO_B64}" width="32"/><span class="topbar-title">VOID</span>'
                '<span class="topbar-pill">PRISM OS</span></div>', unsafe_allow_html=True)
    if st.button("✦ New Session", type="primary", use_container_width=True):
        st.session_state.current_chat_id = new_chat(user_email)
        st.session_state.active_prism_text = None
        st.session_state.prism_open = False
        save_db(db)
        st.rerun()

    if st.session_state.pop("force_prism", False):
        st.session_state.prism_open = True
    prism_open = st.toggle("⚡ Open VOID Prism Panel", key="prism_open")
    auto_scroll = st.toggle("🔄 Auto-Refresh Feed", value=False, help="Live-telemetry style: the app re-syncs every 10 seconds while you watch the console.")

    st.markdown("##### Active Sessions")
    for cid, cdata in reversed(list(user_chats.items())):
        col_t, col_d = st.columns([5, 1])
        with col_t:
            if st.button(f"{'● ' if cid == current_chat_id else '💬 '}{cdata['title']}", key=f"c_{cid}", use_container_width=True):
                st.session_state.current_chat_id = cid
                st.rerun()
        with col_d:
            if len(user_chats) > 1 and st.button("✕", key=f"d_{cid}"):
                del user_chats[cid]
                if cid == current_chat_id:
                    st.session_state.current_chat_id = list(user_chats)[-1]
                save_db(db)
                st.rerun()

    st.markdown("---")
    st.markdown("##### 📊 Chat Insights")
    n_msgs = len(current_chat.get("messages", []))
    m1, m2, m3 = st.columns(3)
    m1.metric("Messages", n_msgs)
    m2.metric("Sessions", len(user_chats))
    m3.metric("Prompts", user_record.get("prompts", 0))

    with st.expander("🧬 Core Identity Vault"):
        n_name = st.text_input("Display Name", value=user_name, max_chars=40)
        n_city = st.text_input("Default City (Live Weather)", value=user_city, max_chars=60)
        n_mem = st.text_area("Personal Notes", value=user_memory, height=100)
        if st.button("💾 Save Identity", use_container_width=True):
            if not is_founder:
                user_record["name"] = n_name.strip()[:40] or user_name
            user_record["city"] = n_city.strip()[:60]
            user_record["memory"] = n_mem.strip()
            save_db(db)
            st.rerun()

    with st.expander("👑 Founder Profile"):
        st.markdown(f"**{FOUNDER_NAME}** — *Founder & Lead Architect of VOID*\n\n{FOUNDER_BIO}")

    if is_founder:
        with st.expander(f"👥 Crew Activity ({len(db['users'])})"):
            for mail, info in db["users"].items():
                st.markdown(f"**{esc(info.get('name', 'Member'))}** (`{esc(mail)}`)  \n"
                            f"<small>Prompts: {info.get('prompts', 0)} • {esc(info.get('last_active', ''))}</small>",
                            unsafe_allow_html=True)

    st.caption(f"Operator: **{user_name}** (`{user_email}`)")
    with st.expander("⏻ Account"):
        confirm_out = st.checkbox("Confirm sign out")
        if st.button("Sign Out", disabled=not confirm_out, use_container_width=True):
            st.query_params.clear()
            for k in ("user_email", "current_chat_id", "active_prism_text", "prism_open"):
                st.session_state.pop(k, None)
            st.rerun()

if auto_scroll:
    time.sleep(0.35)
    st.rerun()

# ============================== 11. COMMAND BAR ==============================
c1, c2, c3, c4 = st.columns([1.9, 1.8, 1.7, 1.2])
with c1:
    ui_mode = st.selectbox("Dimension", ["✦ VOID Core & Prism", "📖 VOID Codex (Study, PDF & Slides)",
                                        "⚡ Live Web App Studio", "🛠️ Side-by-Side Code Lab",
                                        "🧬 Self-Evolution Lab", "🛰️ Ship Telemetry & Insights"], label_visibility="collapsed")
with c2:
    cosmic_entity = st.selectbox("Cosmic Engine", list(ENGINES), label_visibility="collapsed")
with c3:
    persona = st.selectbox("Resonance Mode", ["✦ VOID Omni (Universal)", "🎓 Master Scholastic Tutor",
                                            "💻 Full-Stack Architect", "🎨 UI & Slide Designer", "🐞 Deep Bug Hunter"],
                           label_visibility="collapsed")
with c4:
    with st.popover("➕ Attach & Tune", use_container_width=True):
        uploaded_file = st.file_uploader("Attach Code / Text", type=["py", "js", "html", "css", "json", "txt", "md", "cpp"])
        file_context = ""
        if uploaded_file:
            try:
                file_context = uploaded_file.getvalue().decode("utf-8")[:MAX_FILE_CHARS]
                st.success(f"Loaded `{uploaded_file.name}`")
            except UnicodeDecodeError:
                st.error("Unable to read this file as text.")
        task_depth = st.select_slider("Depth", ["Swift", "Balanced", "Maximum Power"], value="Maximum Power")
        show_thinking = st.toggle("⌨️ Show Live Typing Telemetry", value=True,
                                  help="Echo the model's raw tokens as they stream in. Turn off for a clean console.")
        temperature = st.slider("Creativity", 0.0, 1.0, 0.25, 0.05)
        max_tokens = st.slider("Max Output Length", 500, 4000, 3200, 100)

with st.container():
    hc_col, spacer, engine_col, persona_col, date_col = st.columns([1.1, 0.4, 1.4, 1.4, 1.6])
    s_status, s_note = engine_status()
    hc_col.metric("VOID Engine", "🟢 Online" if s_status == "online" else ("🔴 " + s_status.upper()), s_note)
    engine_col.metric("Cosmic Engine", cosmic_entity.split(" ", 1)[1].split(" (")[0], "primary link")
    persona_col.metric("Resonance", persona.split(" ", 1)[1] if " " in persona else persona, "style profile")
    date_col.metric("Chronometer", datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%d %b %Y"),
                    datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%I:%M %p IST"))

def build_system_prompt(query, is_prism=False, extra=""):
    fmt = ("The user wants a formal document, study guide, PDF, slides, or web app. Use clean Markdown headings (# and ##) "
           "and bullet points so VOID Prism can compile it into a PDF and slide deck."
           if is_prism else
           "Respond naturally and conversationally. Do NOT format casual chat as formal reports unless the user asks for a PDF, notes, or slides.")
    return f"""You are VOID, an elite sovereign coding intelligence and digital workspace created by {FOUNDER_NAME}.
Never mention any outside company or model names; you are strictly VOID, powered by the Cosmic Engines (Supernova X, Nebula Core, Void Moon).

=== CURRENT OPERATOR (CRITICAL IDENTITY) ===
- Operator Name: {user_name}
- Operator Email: {user_email}
- Operator City: {user_city}
- Operator Bio / Memory: {user_memory}
RULE: If the operator or anyone asks "Who am I?", "What is my name?", or queries their identity, immediately state that they are **{user_name}** (`{user_email}`) and detail their background from the Operator Bio above!

=== FOUNDER & CREATOR ===
- Founder Name: {FOUNDER_NAME}
- Founder Bio: {FOUNDER_BIO}
RULE: If anyone asks "Who is Avyan?", "Who created you?", "Who is the founder of VOID?", or "Who made this app?", proudly explain that **Avyan** is the 14-year-old Founder & Lead Architect of VOID, studying in Class 8 at Sunbeam School Varuna in Varanasi, creator of VoidOS, author of 'World Zero', and gamer (NOTREFLEXGAMING05).

=== LIVE TELEMETRY ===
{build_live_context(query, user_city)}
Use this for current time, date, weather, and facts.

=== STYLE ===
Mode: {persona} | Depth: {task_depth}
{fmt}
{extra}"""

def send_to_prism(text, title):
    st.session_state.active_prism_text = text
    st.session_state.active_prism_title = title
    st.session_state.force_prism = True

def bump_usage():
    user_record["prompts"] = user_record.get("prompts", 0) + 1
    user_record["last_active"] = datetime.now().strftime("%b %d, %H:%M")
    bump_daily_usage()
    save_db(db)

# ============================== DIMENSION 1: CORE & PRISM ==============================
if ui_mode == "✦ VOID Core & Prism":
    if prism_open:
        chat_col, prism_col = st.columns([1.18, 1], gap="large")
    else:
        chat_col, prism_col = st.container(), None
    quick_prompt = None

    with chat_col:
        if not current_chat["messages"]:
            st.markdown(f'<div class="void-hero"><img src="{LOGO_B64}" width="58" style="margin-bottom:10px;"/>'
                        f'<div class="void-gradient">Welcome, {safe_user}</div>'
                        '<div class="void-sub">VOID Core • Live Telemetry • On-Demand Prism Forge</div></div>', unsafe_allow_html=True)
            cards = [("🌦️ Live Weather\n\nReal-time city scan", f"What is the exact live weather and temperature right now in {user_city}?"),
                     ("📄 Forge Study PDF\n\nNotes + PDF export", "Make a complete Class 8 Science study guide PDF on Force and Pressure with definitions, formulas, and exam questions."),
                     ("⚡ Build Web App\n\nLaunch in VOID Prism", "Build a sleek dark-themed Hand Cricket mini-game in a single HTML file."),
                     ("👑 Who am I?\n\nIdentity & Founder", "Who am I, and who is the Founder of VOID?")]
            for col, (label, prompt) in zip(st.columns(4), cards):
                with col:
                    if st.button(label, use_container_width=True, key=f"qp_{label[:6]}"):
                        quick_prompt = prompt

        for idx, msg in enumerate(current_chat["messages"]):
            with st.chat_message(msg["role"], avatar=LOGO_B64 if msg["role"] == "assistant" else None):
                st.markdown(msg["content"])
                if msg["role"] == "assistant":
                    b1, b2 = st.columns(2)
                    with b1:
                        st.download_button("📄 Download PDF", generate_real_pdf_bytes(current_chat["title"], msg["content"], f"VOID Forge ({user_name})"),
                                           file_name=f"VOID_{safe_name(current_chat['title'], 15)}_{idx}.pdf",
                                           mime="application/pdf", key=f"pdf_{idx}", use_container_width=True)
                    with b2:
                        if st.button("⚡ Open in Prism", key=f"op_{idx}", use_container_width=True):
                            send_to_prism(msg["content"], current_chat["title"])
                            st.rerun()
                    if not msg.get("is_prism") and any(is_html_block(b) for b in extract_code_blocks(msg["content"])):
                        if st.button("🖥️ Launch Live HTML", key=f"lv_{idx}"):
                            blk = next(b for b in extract_code_blocks(msg["content"]) if is_html_block(b))
                            send_to_prism(blk[1].strip(), current_chat["title"])
                            st.rerun()

    typed = st.chat_input(f"Command VOID, {user_name} — chat naturally, or ask for a PDF, slides, weather, or web app...")
    active_prompt = quick_prompt or typed

    if active_prompt:
        full_prompt = f"Attached file (`{uploaded_file.name}`):\n```\n{file_context}\n```\n\n{active_prompt}" if file_context else active_prompt
        if not current_chat["messages"]:
            t = active_prompt.strip().replace("\n", " ")
            current_chat["title"] = t[:26] + "..." if len(t) > 26 else t
        current_chat["messages"].append({"role": "user", "content": full_prompt})
        bump_usage()

        with chat_col:
            with st.chat_message("user"):
                st.markdown(full_prompt)
            with st.chat_message("assistant", avatar=LOGO_B64):
                reply = None
                try:
                    system = build_system_prompt(active_prompt, detect_prism_intent(active_prompt))
                    gen = stream_void_engine(cosmic_entity, system, current_chat["messages"], temperature, max_tokens)
                    if show_thinking:
                        reply = st.write_stream(gen)
                    else:
                        reply = st.write_stream(clean_stream(gen))
                    if not reply:
                        st.error("The engine returned an empty response. Please try again.")
                except EngineError as e:
                    st.error(str(e))

        if reply:
            is_prism = detect_prism_intent(active_prompt, reply)
            current_chat["messages"].append({"role": "assistant", "content": reply, "is_prism": is_prism})
            if is_prism:
                send_to_prism(reply, current_chat["title"])
            save_db(db)
            st.rerun()
        else:
            current_chat["messages"].pop()
            save_db(db)

    if prism_open and prism_col is not None:
        with prism_col:
            st.markdown('<div class="prism-card">', unsafe_allow_html=True)
            st.markdown("#### ⚡ VOID Prism")
            p_text = st.session_state.get("active_prism_text")
            p_title = st.session_state.get("active_prism_title", current_chat["title"])
            if not p_text:
                p_text = next((m["content"] for m in reversed(current_chat["messages"]) if m["role"] == "assistant"), None)

            if p_text:
                blocks = extract_code_blocks(p_text)
                t_doc, t_slides, t_app, t_edit = st.tabs(["📄 Document", "📊 Slides", "🖥️ Live App / Code", "✏️ Edit"])
                with t_doc:
                    d1, d2, d3 = st.columns(3)
                    with d1:
                        st.download_button("📥 PDF", generate_real_pdf_bytes(p_title, p_text, f"VOID Forge ({user_name})"),
                                           file_name=f"VOID_{safe_name(p_title, 15)}.pdf", mime="application/pdf",
                                           type="primary", use_container_width=True)
                    with d2:
                        st.download_button("📊 Slides", generate_interactive_slides_html(p_title, p_text).encode("utf-8"),
                                           file_name=f"VOID_Slides_{safe_name(p_title, 15)}.html", mime="text/html", use_container_width=True)
                    with d3:
                        st.download_button("📝 Markdown", p_text, file_name=f"VOID_{safe_name(p_title, 15)}.md",
                                           mime="text/markdown", use_container_width=True)
                    st.markdown("---")
                    st.markdown(p_text)
                with t_slides:
                    st.caption("Use Next/Previous or the arrow keys.")
                    components.html(generate_interactive_slides_html(p_title, p_text), height=440)
                with t_app:
                    if blocks:
                        blk = next((b for b in blocks if is_html_block(b)), blocks[0])
                        if is_html_block(blk):
                            components.html(blk[1].strip(), height=460, scrolling=True)
                        else:
                            st.code(blk[1].strip(), language=blk[0].lower() or None)
                    else:
                        st.info("Ask VOID to build an HTML/JS app or write code to run it live here.")
                with t_edit:
                    edited = st.text_area("Modify content", value=p_text, height=340)
                    if st.button("🔄 Update & Rebuild", use_container_width=True):
                        st.session_state.active_prism_text = edited
                        st.rerun()
            else:
                st.info("Ask VOID for a PDF, study guide, presentation, or web app and it will appear here.")
            st.markdown("</div>", unsafe_allow_html=True)

# ============================== DIMENSION 2: CODEX ==============================
elif ui_mode == "📖 VOID Codex (Study, PDF & Slides)":
    st.markdown("### 📖 VOID Scholastic Codex")
    st.caption("Explanations, revision notes, and exam question banks with one-click PDF and slide downloads.")
    s1, s2, s3 = st.columns([2.2, 1.3, 1])
    with s1:
        topic = st.text_input("📚 Chapter or Topic", placeholder="E.g., Force & Pressure, Cell Structure, Linear Equations...")
    with s2:
        fmt = st.selectbox("Codex Mode", ["📘 Complete Revision Notes + Formulas", "💡 Easy Explanation with Real-Life Examples",
                                          "❓ Exam Question Bank (MCQs + Long Answers + Key)", "📊 Full Slide Presentation Deck (8 Slides)"])
    with s3:
        level = st.selectbox("Level", ["Class 8 (CBSE / ICSE)", "High School (Class 9-10)", "Olympiad / Advanced", "Quick 5-Minute Summary"])

    if st.button("✨ Forge Codex Material", type="primary", use_container_width=True):
        if topic.strip():
            sys_p = build_system_prompt(topic, True, (
                f"Create a master-level academic guide for {user_name} ({level}) on '{topic}'. Format: {fmt}. "
                "Use clean # and ## headers so each section forms a page/slide. Include: 1. Core Concept Explanation, "
                "2. Key Definitions & Formulas, 3. Worked Examples, 4. High-Probability Exam Questions with Answers."))
            bump_usage()
            with st.spinner(f"Forge '{topic}' in progress..."):
                res, err = call_void_engine(cosmic_entity, sys_p, [{"role": "user", "content": f"Forge {fmt} for: {topic}"}], 0.2, 2600)
            if res:
                st.session_state.codex_output, st.session_state.codex_topic = res, topic.strip()
                st.rerun()
            else:
                st.error(err)
        else:
            st.warning("Enter a topic or chapter name first.")

    if "codex_output" in st.session_state:
        text, ctopic = st.session_state.codex_output, st.session_state.get("codex_topic", "Study")
        fname = safe_name(ctopic)
        st.markdown("---")
        d1, d2, d3, d4 = st.columns(4)
        with d1:
            st.download_button("📄 PDF", generate_real_pdf_bytes(f"VOID Codex: {ctopic}", text, f"VOID Codex ({user_name})"),
                               file_name=f"VOID_Codex_{fname}.pdf", mime="application/pdf", type="primary", use_container_width=True)
        with d2:
            st.download_button("📊 Slide Deck (.html)", generate_interactive_slides_html(ctopic, text).encode("utf-8"),
                               file_name=f"VOID_Slides_{fname}.html", mime="text/html", use_container_width=True)
        with d3:
            st.download_button("📝 Markdown (.md)", text, file_name=f"VOID_Codex_{fname}.md", mime="text/markdown", use_container_width=True)
        with d4:
            if st.button("🧵 Save to Session", use_container_width=True):
                cid = current_chat_id
                user_chats[cid]["messages"].append({"role": "user", "content": f"[Codex] Forge {fmt} for: {ctopic} ({level})"})
                user_chats[cid]["messages"].append({"role": "assistant", "content": text, "is_prism": True})
                send_to_prism(text, f"VOID Codex: {ctopic}")
                save_db(db)
                st.success("Saved to current session.")
        tab1, tab2 = st.tabs(["📖 Notes", "📊 Slide Deck"])
        with tab1:
            st.markdown(text)
        with tab2:
            components.html(generate_interactive_slides_html(ctopic, text), height=500)

# ============================== DIMENSION 3: WEB APP STUDIO ==============================
elif ui_mode == "⚡ Live Web App Studio":
    st.markdown("### ⚡ VOID Live Web App & Game Studio")
    st.caption("Describe a web app, calculator, dashboard, or mini-game and VOID builds it live.")
    ui_prompt = st.text_area("What should VOID build?", height=85,
                            placeholder="E.g., A dark-mode Hand Cricket game or a Pomodoro study dashboard...")
    if st.button("🚀 Forge & Launch App", type="primary"):
        if ui_prompt.strip():
            sys_p = "Output ONLY one complete, self-contained HTML file (embedded <style> and <script>) inside a ```html code block."
            bump_usage()
            with st.spinner("Forging interactive app..."):
                res, err = call_void_engine(cosmic_entity, sys_p, [{"role": "user", "content": ui_prompt}], 0.3, max_tokens)
            if res:
                m = re.search(r"```(?:html)?\s*\n(.*?)```", res, re.DOTALL)
                st.session_state.studio_html = (m.group(1) if m else res).strip()
            else:
                st.error(err)
        else:
            st.warning("Describe what you want built first.")

    if "studio_html" in st.session_state:
        col_prev, col_src = st.columns([1.4, 1])
        with col_prev:
            st.markdown("##### 🖥️ Live App")
            components.html(st.session_state.studio_html, height=500, scrolling=True)
        with col_src:
            st.markdown("##### 📄 Source")
            st.download_button("📥 Download index.html", st.session_state.studio_html, file_name="index.html",
                               mime="text/html", use_container_width=True)
            if st.button("⚡ Send to Prism Panel", use_container_width=True):
                send_to_prism(st.session_state.studio_html, "Web App Studio Build")
                st.rerun()
            st.code(st.session_state.studio_html, language="html")

# ============================== DIMENSION 4: CODE LAB ==============================
elif ui_mode == "🛠️ Side-by-Side Code Lab":
    st.markdown("### 🛠️ VOID Code Refactor & Bug Lab")
    action = st.selectbox("Operation", ["🐞 Find & Fix All Bugs", "🚀 Optimize for Maximum Speed",
                                        "🛡️ Security Audit & Error Handling", "🔄 Convert to Python / JS / C++"])
    left, right = st.columns(2)
    with left:
        raw = st.text_area("📥 Input Code", height=340, placeholder="Paste your code here...")
        run = st.button("⚡ Transform Code", type="primary", use_container_width=True)
    with right:
        st.markdown("**📤 Output**")
        if run:
            if raw.strip():
                sys_p = f"Perform this exact operation on the user's code: {action}. Briefly highlight the key changes, then give the complete upgraded code."
                bump_usage()
                with st.spinner("Refactoring..."):
                    res, err = call_void_engine(cosmic_entity, sys_p, [{"role": "user", "content": raw}], 0.1, max_tokens)
                st.session_state.lab_result = res if res else f"⚠️ {err}"
                st.session_state.lab_action = action
            else:
                st.warning("Paste some code first.")
        if st.session_state.get("lab_result"):
            lr1, lr2 = st.columns([3, 1.1])
            with lr2:
                if st.button("⚡ Send to Prism", use_container_width=True):
                    send_to_prism(st.session_state.lab_result, f"Code Lab — {st.session_state.get('lab_action', 'Output')}")
                    st.rerun()
            st.markdown(st.session_state.lab_result)
        else:
            st.info("Paste code on the left and click Transform.")

# ============================== DIMENSION 5: SELF-EVOLUTION LAB ==============================
elif ui_mode == "🧬 Self-Evolution Lab":
    st.markdown("### 🧬 VOID Self-Evolution & Meta-Coding Lab")
    st.caption("Use VOID's maximum coding power to inspect, upgrade, or add new features directly to VOID itself.")
    with st.expander("📎 Attach current app.py (recommended for precision upgrades)"):
        evo_file = st.file_uploader("Upload app.py", type=["py", "txt"], key="evo_uploader")
        evo_src = ""
        if evo_file:
            try:
                evo_src = evo_file.getvalue().decode("utf-8")[:MAX_FILE_CHARS]
                st.success(f"Loaded `{evo_file.name}` ({len(evo_src)} chars) — upgrades will be generated against YOUR code.")
            except UnicodeDecodeError:
                st.error("Unable to read this file as text.")

    evo_goal = st.text_input("What upgrade or new feature should VOID build for itself?", placeholder="E.g., Add a Pomodoro timer sidebar widget, or add speech-to-text input...")
    if st.button("⚡ Execute Self-Upgrade", type="primary"):
        if evo_goal.strip():
            evo_sys = (
                f"You are the master core architect of VOID. The founder ({FOUNDER_NAME}) wants to upgrade VOID with the following feature: '{evo_goal}'. "
                "Provide complete, clean Python code modifications or additions (using Streamlit) so Avyan can easily copy and paste them into app.py."
            )
            if evo_src:
                evo_sys += "\n\n=== CURRENT APP SOURCE (upgrade THIS code, output full modified sections) ===\n" + evo_src
            bump_usage()
            with st.spinner("Analyzing app architecture and generating upgrade..."):
                res, err = call_void_engine("☀️ Supernova X (Master Coding Architect)", evo_sys, [{"role": "user", "content": evo_goal}], 0.2, 3500)
            if res:
                st.session_state.evo_result = res
            else:
                st.error(err)
        else:
            st.warning("Enter an upgrade goal first.")

    if "evo_result" in st.session_state:
        st.markdown("---")
        st.markdown("#### 🛠️ Generated Upgrade Blueprint")
        st.markdown(st.session_state.evo_result)
        blocks = extract_code_blocks(st.session_state.evo_result)
        if blocks:
            with st.expander("🐍 Preview & copy code"):
                for bi, b in enumerate(blocks):
                    st.code(b[1].strip(), language=(b[0] or "python").lower())

# ============================== DIMENSION 6: SHIP TELEMETRY & INSIGHTS ==============================
elif ui_mode == "🛰️ Ship Telemetry & Insights":
    st.markdown("### 🛰️ VOID Ship Telemetry")
    st.caption("Command-deck overview of the whole VOID installation: crew, sessions, and daily engine load.")

    total_chats = sum(len(v) for v in db["chats"].values())
    total_msgs = sum(len(c.get("messages", [])) for v in db["chats"].values() for c in v.values())
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("👥 Crew Members", len(db["users"]))
    k2.metric("💬 Total Sessions", total_chats)
    k3.metric("✉️ Total Messages", total_msgs)
    k4.metric("🔥 Prompts (all time)", sum(db.get("usage", {}).values()))

    st.markdown("##### 🔥 Daily Engine Load (last 30 days)")
    today = datetime.now().date()
    days = [(today - timedelta(days=i)).strftime("%Y-%m-%d"] for i in range(29, -1, -1)]
    series = pd.Series([db.get("usage", {}).get(d, 0) for d in days], index=[d[5:] for d in days])
    if series.sum() > 0:
        st.area_chart(series, height=260)
    else:
        st.info("No engine activity recorded in the last 30 days yet — send a command in VOID Core and return here.")

    if is_founder:
        st.markdown("##### 👥 Crew Roster")
        rows = [{"Member": info.get("name", "Member"), "Email": mail, "Prompts": info.get("prompts", 0),
                 "Last Active": info.get("last_active", ""), "Joined": info.get("joined", "")}
                for mail, info in db["users"].items()]
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)
        else:
            st.info("No crew members registered yet.")

        st.markdown("##### 🧭 Sovereign Controls (Founder only)")
        exp_c1, exp_c2 = st.columns(2)
        with exp_c1:
            if st.button("📤 Export Full Database (.json)", use_container_width=True):
                st.download_button("📥 Download void_hub_db.json", json.dumps(db, indent=2),
                                   file_name="void_hub_db_export.json", mime="application/json", use_container_width=True)
        with exp_c2:
            with st.popover("☢️ Danger Zone"):
                st.warning("This wipes ALL users, sessions and messages. Cannot be undone.")
                if st.checkbox("I understand, wipe everything"):
                    if st.button("💥 Factory Reset VOID", type="primary"):
                        db.clear()
                        db.update({"users": {}, "chats": {}, "usage": {}})
                        save_db(db)
                        st.success("VOID has been reset. Reloading...")
                        time.sleep(1)
                        st.rerun()
    else:
        st.info("Founder-level telemetry (crew roster, database export, factory reset) is restricted to the Founder account.")

    st.markdown("##### 🧩 System Status")
    stc1, stc2, stc3, stc4 = st.columns(4)
    stc1.metric("Engine Link", "🟢 Stable" if s_status == "online" else "🔴 Check secrets")
    stc2.metric("Mail Relay", "🟢 Configured" if (EJS_SERVICE and EJS_TEMPLATE and EJS_PUBLIC) else "🟠 Not configured")
    stc3.metric("App Version", "v" + APP_VERSION.replace("-Supernova", " Supernova"))
    stc4.metric("Data Store", "🟢 " + DB_FILE)

# ============================== 12. FOOTER ==============================
st.markdown('<div class="void-footer">⚡ VOID — Sovereign OS Intelligence • Forged by ' + esc(FOUNDER_NAME) +
            ' • Prism OS v' + APP_VERSION + '</div>', unsafe_allow_html=True)
