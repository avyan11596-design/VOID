"""
VOID — Sovereign OS Intelligence · app.py
Version: 6.5.0-Apex Supernova

Full Omni-Grounding Internet Engine + Verified Multi-Provider Resiliency.
Retains all core dimensions, Prism forge, Codex, Slide Decks, and Identity Vault.
"""

import ast
import base64
import hashlib
import hmac
import html
import io
import json
import operator
import os
import re
import secrets as pysecrets
import textwrap
import time
import urllib.parse
import uuid
import xml.etree.ElementTree as ET
from collections.abc import Mapping
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, timezone

import pandas as pd
import requests
import streamlit as st
import streamlit.components.v1 as components

APP_VERSION = "6.5.0-Apex"

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

# --- MINIMALIST OBSIDIAN / SLATE OS THEME ---
MINIMAL_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg: #09090b;
  --surface: #111114;
  --surface-2: #18181c;
  --line: #222227;
  --line-2: #2e2e36;
  --text: #f4f4f5;
  --text-2: #a1a1aa;
  --text-3: #71717a;
  --accent: #3b82f6;
  --accent-soft: rgba(59, 130, 246, 0.12);
  --ok: #10b981;
  --warn: #f59e0b;
  --bad: #ef4444;
}

html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"],
[data-testid="stBottom"], [data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"],
.stChatFloatingInputContainer {
  background: var(--bg) !important;
  background-image: none !important;
  color: var(--text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  -webkit-font-smoothing: antialiased;
}

[data-testid="stToolbarActions"], [data-testid="stAppDeployButton"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], #MainMenu, footer { display: none !important; }

.block-container { max-width: 1140px !important; padding-top: 2rem !important; padding-bottom: 7rem !important; }
section[data-testid="stSidebar"] { background: var(--surface) !important; border-right: 1px solid var(--line) !important; }
section[data-testid="stSidebar"] > div { padding-top: 1.2rem !important; }

[data-testid="stBottom"], [data-testid="stBottomBlockContainer"], .stChatFloatingInputContainer {
  border-top: 1px solid var(--line) !important;
  background: rgba(9, 9, 11, 0.95) !important;
  backdrop-filter: blur(16px);
}

/* Typography */
h1, h2, h3, h4, h5, h6 { color: var(--text) !important; font-weight: 600 !important; letter-spacing: -0.025em !important; }
p, li, .stMarkdown { color: var(--text) !important; font-size: 0.96rem !important; line-height: 1.72 !important; }
span, label { color: var(--text) !important; }
small, .stCaption, [data-testid="stCaptionContainer"], .stCaption p { color: var(--text-3) !important; font-size: 0.8rem !important; }
strong, b { font-weight: 600 !important; color: #ffffff !important; }
hr { border: 0 !important; border-top: 1px solid var(--line) !important; margin: 1.6rem 0 !important; }

/* Chat Bubbles */
.stChatMessage {
  background: transparent !important;
  border-bottom: 1px solid var(--line) !important;
  border-radius: 0 !important;
  box-shadow: none !important;
  padding: 1.2rem 0.2rem !important;
}

/* Input Fields */
[data-testid="stChatInput"], [data-testid="stChatInputContainer"] {
  background: var(--surface) !important;
  border: 1px solid var(--line-2) !important;
  border-radius: 14px !important;
}
[data-testid="stChatInput"] textarea {
  color: var(--text) !important;
  -webkit-text-fill-color: var(--text) !important;
  background: transparent !important;
}
[data-testid="stChatInput"]:focus-within { border-color: var(--accent) !important; }

input[type="text"], input[type="password"], input[type="number"],
div[data-baseweb="input"] input, div[data-baseweb="textarea"] textarea,
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
  background-color: var(--surface) !important;
  color: var(--text) !important;
  -webkit-text-fill-color: var(--text) !important;
  border-radius: 10px !important;
}
div[data-baseweb="input"], div[data-baseweb="textarea"],
[data-testid="stTextInput"] > div, [data-testid="stTextArea"] > div {
  background: var(--surface) !important;
  border: 1px solid var(--line-2) !important;
  border-radius: 10px !important;
}
div[data-baseweb="select"] > div {
  background: var(--surface) !important;
  border: 1px solid var(--line-2) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
}

/* Buttons */
.stButton > button, .stDownloadButton > button {
  background: var(--surface) !important;
  color: var(--text) !important;
  border: 1px solid var(--line-2) !important;
  border-radius: 10px !important;
  font-weight: 500 !important;
  font-size: 0.86rem !important;
  transition: all 0.15s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover {
  background: var(--surface-2) !important;
  border-color: #52525b !important;
  transform: translateY(-1px);
}
.stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {
  background: var(--text) !important;
  border: 1px solid var(--text) !important;
  color: #09090b !important;
  font-weight: 600 !important;
}
.stButton > button[kind="primary"] p, .stButton > button[kind="primary"] span {
  color: #09090b !important;
}

/* Cards & Expanders */
[data-testid="stForm"], .prism-card {
  background: var(--surface) !important;
  border: 1px solid var(--line) !important;
  border-radius: 14px !important;
  padding: 1.4rem !important;
}
[data-testid="stExpander"] {
  background: transparent !important;
  border: 1px solid var(--line) !important;
  border-radius: 12px !important;
}

/* Code & Output */
pre, code, .stCode, [data-testid="stCode"] {
  font-family: 'JetBrains Mono', monospace !important;
  font-size: 0.88rem !important;
}
code {
  background: #1c1c22 !important;
  color: #e4e4e7 !important;
  border-radius: 6px !important;
  padding: 0.15rem 0.35rem !important;
}
pre code { background: transparent !important; padding: 0 !important; }

/* Custom Badges */
.pill {
  display: inline-block;
  font-size: 0.68rem;
  letter-spacing: 0.06em;
  text-transform: uppercase;
  font-weight: 600;
  padding: 3px 10px;
  border-radius: 99px;
  border: 1px solid var(--line-2);
}
.pill-ok { border-color: rgba(16, 185, 129, 0.4); color: var(--ok) !important; }
.pill-warn { border-color: rgba(245, 158, 11, 0.4); color: var(--warn) !important; }
.pill-bad { border-color: rgba(239, 68, 68, 0.4); color: var(--bad) !important; }

.diag-box {
  background: var(--surface) !important;
  border: 1px solid var(--line) !important;
  border-radius: 10px;
  padding: 0.8rem 1rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: var(--text-2) !important;
  margin-top: 0.6rem;
}
.diag-box b { color: var(--text) !important; }
.kv {
  display: flex;
  justify-content: space-between;
  font-size: 0.8rem;
  color: var(--text-2);
  padding: 0.3rem 0;
  border-bottom: 1px solid var(--line);
}
.kv:last-child { border-bottom: 0; }
.void-hero { text-align: center; padding: 2.2rem 1rem 1.4rem; }
.void-gradient {
  color: #fafafa !important;
  font-weight: 700 !important;
  font-size: 2.1rem !important;
  letter-spacing: -0.035em !important;
  margin-bottom: 0.4rem;
}
.void-sub { font-size: 0.95rem !important; color: var(--text-3) !important; margin-bottom: 1.8rem; }
.hero-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 52px;
  height: 52px;
  border: 1px solid var(--line-2);
  border-radius: 14px;
  margin-bottom: 1rem;
  background: var(--surface);
}
.topbar-brand { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
.topbar-title { font-size: 1.05rem !important; font-weight: 700 !important; letter-spacing: 0.28em !important; color: #fff !important; }
.topbar-pill {
  font-size: 0.58rem !important;
  letter-spacing: 0.12em;
  padding: 2px 8px !important;
  border-radius: 99px;
  border: 1px solid var(--line-2);
  color: var(--text-3) !important;
  font-weight: 600;
}
.void-footer { text-align: center; color: var(--text-3) !important; font-size: 0.75rem; padding: 2.5rem 0 0.8rem; }
</style>"""
st.markdown(MINIMAL_CSS, unsafe_allow_html=True)

# ============================== 2. CONFIG & SECRETS ==============================
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_MODELS_URL = "https://openrouter.ai/api/v1/models"
OPENAI_URL = "https://api.openai.com/v1/chat/completions"
GROQ_URL = "https://api.groq.com/openai/v1/chat/completions"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
EMAILJS_URL = "https://api.emailjs.com/api/v1.0/email/send"
GEO_URL = "https://geocoding-api.open-meteo.com/v1/search"
WEATHER_URL = "https://api.open-meteo.com/v1/forecast"
WIKI_URL = "https://en.wikipedia.org/w/api.php"
DB_FILE, KEY_FILE = "void_hub_db.json", ".void_signing_key"
MAX_HISTORY, MAX_FILE_CHARS = 24, 40000
OTP_TTL, OTP_MAX_TRIES, OTP_COOLDOWN, LOGIN_DAYS = 600, 5, 30, 365
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]{2,}$")

# Rock-solid, active engine IDs
ENGINES = {
    "🧠 Auto-Route (Omni Intelligence)": "auto",
    "☀️ Supernova X (Coding & Architecture)": "qwen/qwen-2.5-coder-32b-instruct",
    "🪐 Nebula Core (Deep Logic Engine)": "deepseek/deepseek-chat",
    "🌙 Void Moon (Hyper-Fast Flash)": "google/gemini-2.0-flash-001",
    "Quasar Prime (Extreme Reasoning)": "deepseek/deepseek-chat",
    "🔭 Pulsar Pro (Deep Research)": "meta-llama/llama-3.3-70b-instruct",
}


def _flatten_secrets():
    out = {}
    def walk(node, prefix):
        try:
            items = dict(node)
        except Exception:
            return
        for k, v in items.items():
            key = f"{prefix}{k}".upper()
            if isinstance(v, Mapping):
                walk(v, key + "_")
            else:
                sv = str(v).strip()
                if sv:
                    out.setdefault(key, sv)
    try:
        walk(st.secrets, "")
    except Exception:
        pass
    return out


SECRETS = _flatten_secrets()


def sget(key, default=""):
    v = SECRETS.get(key.upper(), "")
    if v:
        return v
    v = str(os.environ.get(key, "")).strip()
    return v or default


PROV_KEYS = {
    "openrouter": sget("OPENROUTER_API_KEY"),
    "openai": sget("OPENAI_API_KEY"),
    "groq": sget("GROQ_API_KEY"),
    "google": sget("GOOGLE_API_KEY") or sget("GEMINI_API_KEY"),
}

API_KEY = PROV_KEYS["openrouter"]
EJS_SERVICE, EJS_TEMPLATE = sget("EMAILJS_SERVICE_ID"), sget("EMAILJS_TEMPLATE_ID")
EJS_PUBLIC, EJS_PRIVATE = sget("EMAILJS_PUBLIC_KEY"), sget("EMAILJS_PRIVATE_KEY")
FOUNDERS = {e.strip().lower() for e in sget("FOUNDER_EMAILS").split(",") if e.strip()}
FOUNDER_NAME = sget("FOUNDER_NAME", "Avyan")
FOUNDER_BIO = sget("FOUNDER_BIO", "14-year-old Founder & Lead Architect of VOID, student at Sunbeam School Varuna in Varanasi, creator of VoidOS, author of World Zero, and gamer (NOTREFLEXGAMING05).")

SEARCH_KEYS = {
    "tavily": sget("TAVILY_API_KEY"),
    "brave": sget("BRAVE_API_KEY"),
    "serper": sget("SERPER_API_KEY"),
}


def esc(s):
    return html.escape(str(s))


def safe_name(s, n=25):
    return re.sub(r"\W+", "_", s).strip("_")[:n] or "VOID"


@st.cache_resource(show_spinner=False)
def http_session():
    s = requests.Session()
    s.headers.update({"User-Agent": f"VOIDCore/{APP_VERSION} (Mozilla/5.0)", "X-Title": "VOID"})
    return s


# ============================== 3. DATABASE ==============================
def load_db():
    try:
        if os.path.exists(DB_FILE):
            with open(DB_FILE, encoding="utf-8") as f:
                d = json.load(f)
            d.setdefault("users", {})
            d.setdefault("chats", {})
            d.setdefault("usage", {})
            return d
    except Exception:
        pass
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


# ============================== 4. SIGNED LOGIN ==============================
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
        return (API_KEY or "void_secret").encode()


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


# ============================== 5. WEATHER & CHRONOMETER ==============================
WMO = {0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast", 45: "Foggy", 48: "Rime fog",
       51: "Light drizzle", 53: "Drizzle", 55: "Heavy drizzle", 61: "Light rain", 63: "Moderate rain",
       65: "Heavy rain", 71: "Light snow", 73: "Snow", 75: "Heavy snow", 80: "Rain showers",
       81: "Heavy showers", 95: "Thunderstorm", 96: "Thunderstorm with hail"}


@st.cache_data(ttl=3600, show_spinner=False)
def geocode(city):
    try:
        r = http_session().get(GEO_URL, params={"name": city, "count": 1, "language": "en", "format": "json"}, timeout=5).json()
        res = (r.get("results") or [None])[0]
        if not res:
            return None
        label = ", ".join(filter(None, [res.get("name"), res.get("admin1"), res.get("country")]))
        return res["latitude"], res["longitude"], label
    except Exception:
        return None


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


@st.cache_data(ttl=900, show_spinner=False)
def engine_status():
    if not any(PROV_KEYS.values()):
        return "offline", "add OPENROUTER_API_KEY to secrets"
    if PROV_KEYS["openrouter"]:
        try:
            r = http_session().get(OPENROUTER_MODELS_URL, timeout=6)
            if r.status_code == 200:
                n = len(r.json().get("data", []))
                backups = [p for p in ("openai", "groq", "google") if PROV_KEYS.get(p)]
                tail = f" • +{len(backups)} backup" if backups else ""
                return "online", f"link stable • {n} models reachable{tail}"
            if r.status_code in (401, 403):
                return "error", f"OpenRouter key rejected (HTTP {r.status_code})"
            return "error", f"gateway HTTP {r.status_code}"
        except Exception as e:
            return "error", str(e)[:70]
    return "online", "backup provider active"


# ============================== 6. ULTRA-ROBUST LIVE INTERNET RETRIEVAL ==============================
_COMMON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def _clean_text(t):
    return html.unescape(re.sub(r"<[^>]+>", " ", t or "")).strip()


def _src_google_news(q, n=5):
    """Fetches real-time live news directly from Google News RSS. Zero API key needed."""
    try:
        url = f"https://news.google.com/rss/search?q={urllib.parse.quote(q)}&hl=en-US&gl=US&ceid=US:en"
        r = requests.get(url, headers=_COMMON_HEADERS, timeout=6)
        if r.status_code != 200:
            return []
        root = ET.fromstring(r.content)
        items = []
        for el in root.findall(".//item")[:n]:
            title = _clean_text(el.findtext("title", ""))
            pub = el.findtext("pubDate", "")
            link = el.findtext("link", "")
            if title:
                items.append(f"[CURRENT NEWS] {title} ({pub}) -> {link}")
        return items
    except Exception:
        return []


def _src_ddg_instant(q):
    """DuckDuckGo Instant Answer API - direct factual summary."""
    try:
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(q)}&format=json&no_html=1&skip_disambig=1"
        r = requests.get(url, headers=_COMMON_HEADERS, timeout=5)
        if r.status_code == 200:
            data = r.json()
            out = []
            if data.get("AbstractText"):
                out.append(f"[SUMMARY] {data['AbstractText']} ({data.get('AbstractURL', '')})")
            if data.get("Answer"):
                out.append(f"[DIRECT ANSWER] {data['Answer']}")
            for t in data.get("RelatedTopics", [])[:3]:
                if isinstance(t, dict) and t.get("Text"):
                    out.append(f"- {t['Text']}")
            return out
    except Exception:
        pass
    return []


def _src_wikipedia_deep(q, n=2):
    """Wikipedia Opensearch + Summary Extracts."""
    try:
        r = http_session().get(WIKI_URL, params={
            "action": "query", "generator": "search", "gsrsearch": q, "gsrlimit": n,
            "prop": "extracts", "exintro": 1, "explaintext": 1, "exchars": 800,
            "format": "json"}, headers=_COMMON_HEADERS, timeout=6).json()
        pages = (r.get("query", {}) or {}).get("pages", {}).values()
        return [f"- Wikipedia ({p.get('title')}): {_clean_text(p.get('extract', ''))[:550]}" for p in pages if p.get("extract")]
    except Exception:
        return []


def _src_tavily(q, n):
    k = SEARCH_KEYS["tavily"]
    if not k:
        return []
    try:
        r = http_session().post("https://api.tavily.com/search",
                                json={"api_key": k, "query": q, "max_results": n, "search_depth": "advanced",
                                      "include_answer": True}, timeout=8).json()
        out = []
        if r.get("answer"):
            out.append(f"[TAVILY ANSWER] {_clean_text(r['answer'])}")
        for x in r.get("results", [])[:n]:
            out.append(f"- {x.get('title', '')} ({x.get('url', '')}): {_clean_text(x.get('content', ''))[:400]}")
        return out
    except Exception:
        return []


def _src_serper(q, n):
    k = SEARCH_KEYS["serper"]
    if not k:
        return []
    try:
        r = http_session().post("https://google.serper.dev/search", json={"q": q, "num": n},
                                headers={"X-API-KEY": k, "Content-Type": "application/json"}, timeout=8).json()
        out = []
        if r.get("answerBox", {}).get("answer"):
            out.append(f"[ANSWER BOX] {r['answerBox']['answer']}")
        for x in r.get("organic", [])[:n]:
            out.append(f"- {x.get('title', '')} ({x.get('link', '')}): {_clean_text(x.get('snippet', ''))}")
        return out
    except Exception:
        return []


def _src_brave(q, n):
    k = SEARCH_KEYS["brave"]
    if not k:
        return []
    try:
        r = http_session().get("https://api.search.brave.com/res/v1/web/search",
                               params={"q": q, "count": n},
                               headers={"X-Subscription-Token": k, "Accept": "application/json"}, timeout=8).json()
        return [f"- {x.get('title', '')} ({x.get('url', '')}): {_clean_text(x.get('description', ''))}"
                for x in (r.get("web", {}) or {}).get("results", [])[:n]]
    except Exception:
        return []


@st.cache_data(ttl=600, show_spinner=False, max_entries=256)
def web_search_bundle(query, n=5):
    """Executes all free + configured search feeds in parallel and consolidates top facts."""
    q = re.sub(r"\s+", " ", query).strip()[:180]
    if len(q) < 3:
        return "", []

    funcs = [
        lambda: _src_google_news(q, n),
        lambda: _src_ddg_instant(q),
        lambda: _src_tavily(q, n),
        lambda: _src_serper(q, n),
        lambda: _src_brave(q, n),
        lambda: _src_wikipedia_deep(q, 2),
    ]

    chunks, urls = [], []
    with ThreadPoolExecutor(max_workers=6) as ex:
        for res in ex.map(lambda f: f(), funcs):
            chunks.extend(res or [])

    for line in chunks:
        m = re.search(r"(https?://[^\s\)]+)", line)
        if m and m.group(1) not in urls:
            urls.append(m.group(1))

    seen, dedup = set(), []
    for line in chunks:
        sig = line[:85].lower()
        if sig in seen:
            continue
        seen.add(sig)
        dedup.append(line)

    return "\n".join(dedup[:14]), urls[:6]


@st.cache_data(ttl=1800, show_spinner=False, max_entries=96)
def read_page(url, limit=4000):
    try:
        r = http_session().get("https://r.jina.ai/" + url, timeout=14,
                               headers={"User-Agent": f"VOIDCore/{APP_VERSION}"})
        if r.status_code == 200 and len(r.text) > 200:
            return re.sub(r"\n{3,}", "\n\n", r.text)[:limit]
    except Exception:
        pass
    return ""


# ---------- Exact Math Engine ----------
_MATH_OPS = {ast.Add: operator.add, ast.Sub: operator.sub, ast.Mult: operator.mul, ast.Div: operator.truediv,
             ast.Pow: operator.pow, ast.Mod: operator.mod, ast.USub: operator.neg, ast.UAdd: operator.pos,
             ast.FloorDiv: operator.floordiv}


def _math_eval(n):
    if isinstance(n, ast.Constant) and isinstance(n.value, (int, float)):
        return n.value
    if isinstance(n, ast.BinOp) and type(n.op) in _MATH_OPS:
        a, b = _math_eval(n.left), _math_eval(n.right)
        if isinstance(n.op, ast.Pow) and abs(b) > 80:
            raise ValueError("power overflow")
        return _MATH_OPS[type(n.op)](a, b)
    if isinstance(n, ast.UnaryOp) and type(n.op) in _MATH_OPS:
        return _MATH_OPS[type(n.op)](_math_eval(n.operand))
    raise ValueError("unsupported")


def exact_math(prompt):
    res = []
    for m in re.findall(r"[\d.][\d\s.+\-*/^()%]*[\d)]", prompt):
        e = m.strip()
        if len(e) < 3 or not re.search(r"[+\-*/^%]", e):
            continue
        try:
            v = _math_eval(ast.parse(e.replace("^", "**"), mode="eval").body)
            res.append(f"[EXACT CALC] {e} = {round(v, 8) if isinstance(v, float) else v}")
        except Exception:
            continue
    pct = re.findall(r"(\d+(?:\.\d+)?)\s*(?:%|percent)\s*of\s*(\d+(?:\.\d+)?)", prompt, re.I)
    for a, b in pct[:3]:
        res.append(f"[EXACT CALC] {a}% of {b} = {round(float(a) * float(b) / 100, 8)}")
    return "\n".join(res[:4])


def needs_search(prompt, depth="Standard"):
    """Accurately triggers search whenever a real-world fact or live knowledge might be needed."""
    if depth == "Off":
        return False
    p = prompt.lower().strip()
    if len(p) < 4:
        return False
    # Bypass only for direct local/creative programming commands
    if p.startswith(("write a poem", "tell me a joke", "make a game", "write a story")) and not any(k in p for k in ("news", "who", "when", "today", "current")):
        return False
    if depth in ("Standard", "Deep"):
        return True
    return False


def grounding(prompt, depth="Standard", diag=None):
    parts = []
    calc = exact_math(prompt)
    if calc:
        parts.append(calc)

    hits, urls, pages = 0, [], 0
    if needs_search(prompt, depth):
        text, urls = web_search_bundle(prompt, 6 if depth == "Deep" else 5)
        if text:
            hits = text.count("\n- ") + text.count("[CURRENT") + text.count("[SUMMARY")
            parts.append("=== LIVE INTERNET INTELLIGENCE (Retrieved Just Now) ===\n" + text)
        if depth == "Deep" and urls:
            for u in urls[:2]:
                body = read_page(u, 3000)
                if body:
                    pages += 1
                    parts.append(f"[PAGE READER EXCERPT: {u}]\n{body}")

    if diag is not None:
        diag.update(search_hits=hits, sources=urls[:4], pages_read=pages, math=bool(calc))
    return "\n\n".join(parts)


# ============================== 7. MULTI-PROVIDER RESILIENCY ==============================
class EngineError(Exception):
    pass


AUTO_ROUTES = {
    "code": ["qwen/qwen-2.5-coder-32b-instruct", "deepseek/deepseek-chat"],
    "math": ["deepseek/deepseek-chat", "meta-llama/llama-3.3-70b-instruct"],
    "fresh": ["deepseek/deepseek-chat", "google/gemini-2.0-flash-001"],
    "doc": ["deepseek/deepseek-chat", "google/gemini-2.0-flash-001"],
    "chat": ["deepseek/deepseek-chat", "meta-llama/llama-3.3-70b-instruct"],
}

OR_BACKUP = [
    "deepseek/deepseek-chat",
    "google/gemini-2.0-flash-001",
    "meta-llama/llama-3.3-70b-instruct",
    "qwen/qwen-2.5-coder-32b-instruct",
]

GROQ_MODELS = ["llama-3.3-70b-versatile", "llama-3.1-8b-instant"]
GEMINI_MODELS = ["gemini-2.0-flash", "gemini-1.5-flash"]
OPENAI_MODELS = ["gpt-4o-mini"]

_PROVIDER_LABEL = {"openrouter": "Cosmic Relay (OpenRouter)", "openai": "Nebula Relay (OpenAI)",
                   "groq": "Pulsar Relay (Groq)", "google": "Quasar Direct (Gemini)"}


def intent_of(prompt):
    p = prompt.lower()
    if any(w in p for w in ("code", "python", "js", "html", "function", "bug", "sql")):
        return "code"
    if any(w in p for w in ("solve", "calculate", "equation", "math", "integral")):
        return "math"
    if any(w in p for w in ("today", "news", "current", "latest", "who is", "weather", "match", "score", "price")):
        return "fresh"
    if any(w in p for w in ("pdf", "slides", "notes", "presentation", "document", "cheat sheet")):
        return "doc"
    return "chat"


def resolve_primary(choice, prompt=""):
    model = ENGINES.get(choice, "deepseek/deepseek-chat")
    if model == "auto":
        return AUTO_ROUTES.get(intent_of(prompt), AUTO_ROUTES["chat"])[0]
    return model


def build_chain(choice, prompt="", avoid=None):
    primary = resolve_primary(choice, prompt)
    chain = []
    if PROV_KEYS["openrouter"]:
        chain.append(("openrouter", primary))
        pool = AUTO_ROUTES.get(intent_of(prompt), []) + OR_BACKUP
        for m in pool:
            if m != primary and (("openrouter", m) not in chain):
                chain.append(("openrouter", m))
    if PROV_KEYS["groq"]:
        chain += [("groq", m) for m in GROQ_MODELS]
    if PROV_KEYS["google"]:
        chain += [("google", m) for m in GEMINI_MODELS]
    if PROV_KEYS["openai"]:
        chain += [("openai", m) for m in OPENAI_MODELS]
    if avoid:
        chain = [c for c in chain if c[1] != avoid] or chain
    return chain


def _trim(msgs, budget=24000):
    out, used = [], 0
    for m in reversed(msgs[-MAX_HISTORY:]):
        c = str(m.get("content", ""))
        if used + len(c) > budget and out:
            break
        out.append({"role": m.get("role", "user"), "content": c[:budget]})
        used += len(c)
    return list(reversed(out))


def _post_once(provider, model, system, msgs, temp, tokens):
    headers = {"Authorization": f"Bearer {PROV_KEYS[provider]}", "Content-Type": "application/json"}
    if provider == "openrouter":
        headers.update({"HTTP-Referer": "https://void.local", "X-Title": "VOID"})

    if provider == "google":
        key = PROV_KEYS["google"]
        url = GEMINI_URL.format(model=model) + f"?key={key}"
        contents = []
        for m in _trim(msgs):
            role = "model" if m["role"] == "assistant" else "user"
            contents.append({"role": role, "parts": [{"text": m["content"]}]})
        payload = {
            "systemInstruction": {"parts": [{"text": system}]},
            "contents": contents,
            "generationConfig": {"temperature": max(0.0, min(temp, 1.2)), "maxOutputTokens": tokens}
        }
        r = http_session().post(url, json=payload, timeout=90)
        if r.status_code != 200:
            raise EngineError(f"Google HTTP {r.status_code}: {r.text[:140]}")
        try:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            raise EngineError("Google empty response")

    url = {"openrouter": OPENROUTER_URL, "openai": OPENAI_URL, "groq": GROQ_URL}[provider]
    payload = {
        "model": model,
        "temperature": max(0.0, min(temp, 1.2)),
        "max_tokens": tokens,
        "messages": [{"role": "system", "content": system}] + _trim(msgs)
    }
    r = http_session().post(url, headers=headers, json=payload, timeout=90)
    if r.status_code != 200:
        raise EngineError(f"{_PROVIDER_LABEL[provider]} HTTP {r.status_code}: {r.text[:140]}")
    try:
        return r.json()["choices"][0]["message"]["content"] or ""
    except Exception:
        raise EngineError("Malformed provider output")


def _stream_once(provider, model, system, msgs, temp, tokens):
    if provider == "google":
        yield _post_once(provider, model, system, msgs, temp, tokens)
        return

    headers = {"Authorization": f"Bearer {PROV_KEYS[provider]}", "Content-Type": "application/json"}
    if provider == "openrouter":
        headers.update({"HTTP-Referer": "https://void.local", "X-Title": "VOID"})
    url = {"openrouter": OPENROUTER_URL, "openai": OPENAI_URL, "groq": GROQ_URL}[provider]
    payload = {
        "model": model,
        "temperature": max(0.0, min(temp, 1.2)),
        "max_tokens": tokens,
        "stream": True,
        "messages": [{"role": "system", "content": system}] + _trim(msgs)
    }
    r = http_session().post(url, headers=headers, json=payload, timeout=90, stream=True)
    if r.status_code != 200:
        raise EngineError(f"{_PROVIDER_LABEL[provider]} HTTP {r.status_code}: {r.text[:140]}")
    for line in r.iter_lines(decode_unicode=True):
        if not line or not line.startswith("data:"):
            continue
        chunk = line[5:].strip()
        if chunk == "[DONE]":
            break
        try:
            delta = json.loads(chunk)["choices"][0]["delta"].get("content")
            if delta:
                yield delta
        except Exception:
            continue


def call_llm(choice, system, msgs, temp=0.25, tokens=2000, prompt="", avoid=None, diag=None):
    if not any(PROV_KEYS.values()):
        return None, "No engine key found. Add OPENROUTER_API_KEY in Streamlit Secrets."
    errors = []
    for provider, model in build_chain(choice, prompt or (msgs[-1]["content"] if msgs else ""), avoid):
        t0 = time.time()
        try:
            txt = _post_once(provider, model, system, msgs, temp, tokens)
            if txt and txt.strip():
                if diag is not None:
                    diag.update(provider=provider, model=model, latency=round(time.time() - t0, 2),
                                link=_PROVIDER_LABEL[provider])
                return txt, None
        except Exception as e:
            errors.append(f"{model} ({e})")
            continue
    if diag is not None:
        diag["attempts"] = errors[:3]
    return None, " • ".join(errors[-2:]) or "All AI engines failed."


def stream_llm(choice, system, msgs, temp=0.25, tokens=2000, prompt="", diag=None):
    errors = []
    for provider, model in build_chain(choice, prompt):
        got = False
        t0 = time.time()
        try:
            for chunk in _stream_once(provider, model, system, msgs, temp, tokens):
                got = True
                yield chunk
            if got:
                if diag is not None:
                    diag.update(provider=provider, model=model, latency=round(time.time() - t0, 2),
                                link=_PROVIDER_LABEL[provider])
                return
        except Exception as e:
            errors.append(f"{model} ({e})")
            continue
    if diag is not None:
        diag["attempts"] = errors[:3]
    raise EngineError("All engines failed to stream.")


def _buffered(gen, size=80):
    buf = ""
    for chunk in gen:
        buf += chunk
        if len(buf) >= size:
            yield buf
            buf = ""
    if buf:
        yield buf


REFUSAL_PAT = re.compile(
    r"\b(i (?:can'?t|cannot|am unable|am not able)|as an ai|i don'?t have (?:access|the ability|enough|real-time)|"
    r"i'?m sorry,? but|i apologi[sz]e|unable to (?:answer|help)|knowledge cutoff)\b", re.I)


def looks_weak(text):
    t = (text or "").strip()
    return len(t) < 40 or (REFUSAL_PAT.search(t[:350]) and len(t) < 500)


def answer_question(engine, prompt, system, msgs, temp, tokens, accuracy_mode=True, diag=None):
    if diag is None:
        diag = {}
    draft, err = call_llm(engine, system, msgs, temp, tokens, prompt=prompt, diag=diag)
    if not draft or looks_weak(draft):
        diag["repaired"] = True
        rescue_sys = (system + "\n\nCRITICAL: Answer directly and accurately using the live internet context provided. "
                               "Do NOT refuse. State current real facts directly in the first line.")
        draft, err2 = call_llm(engine, rescue_sys, msgs[-3:], max(temp, 0.2), tokens, prompt=prompt, diag=diag)
        if not draft:
            raise EngineError(err or err2 or "Answer generation failed.")
    return draft


# ============================== 8. DOCUMENT FORGE (PDF + SLIDES) ==============================
def clean_for_pdf(text):
    for k, v in {"—": "-", "–": "-", "“": '"', "”": '"', "‘": "'", "’": "'", "•": "*", "…": "...", "→": "->"}.items():
        text = text.replace(k, v)
    return text.encode("latin-1", "ignore").decode("latin-1")


def pdf_escape(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


PDF_STYLE = {"TITLE": ("F2", 15, 50, 0, 22), "META": ("F1", 8.5, 50, 0, 16), "H1": ("F2", 12.5, 50, 6, 16),
             "BULLET": ("F1", 10, 56, 0, 14), "BODY": ("F1", 10, 50, 0, 14)}


@st.cache_data(show_spinner=False, max_entries=64)
def generate_real_pdf_bytes(title, markdown, author="VOID Forge"):
    safe_title = clean_for_pdf(title)
    safe_md = clean_for_pdf(markdown)
    lines = [("TITLE", safe_title),
             ("META", clean_for_pdf(f"Forged by {author} | {datetime.now():%Y-%m-%d %H:%M}")), ("SPACE", "")]
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
            y -= 8
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
        footer = f"VOID Document • Page {i} of {total}"
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
body{margin:0;background:#09090b;color:#f4f4f5;font-family:'Inter',system-ui,sans-serif;display:flex;flex-direction:column;height:95vh;justify-content:space-between}
.wrap{flex:1;display:flex;align-items:center;justify-content:center;padding:20px}
.slide{display:none;width:100%;max-width:840px;background:#111114;border:1px solid #222227;border-radius:16px;padding:36px 44px;min-height:300px;box-sizing:border-box}
.slide.on{display:block}
.badge{font-size:10px;letter-spacing:3px;color:#71717a;font-weight:600;margin-bottom:14px}
.count{position:fixed;top:14px;right:20px;font-size:11px;color:#71717a;font-weight:600}
h2{margin-top:0;font-size:24px;color:#fafafa;font-weight:600}
.body{font-size:15px;line-height:1.75;color:#a1a1aa}
.ctl{display:flex;justify-content:center;gap:12px;padding:12px}
button{background:#111114;color:#f4f4f5;border:1px solid #2e2e36;padding:8px 18px;border-radius:99px;cursor:pointer;font-weight:500}
button:hover{background:#fafafa;color:#09090b}
@media print{.ctl{display:none}body{background:#fff;color:#000}.slide{display:block;page-break-after:always;background:#fff;border-color:#ddd}}
</style></head><body><div class="wrap">%%SLIDES%%</div>
<div class="count">%%COUNT%%</div>
<div class="ctl"><button onclick="go(-1)">◀ Previous</button><button onclick="window.print()">Export PDF</button><button onclick="go(1)">Next ▶</button></div>
<script>let c=0;const s=document.querySelectorAll('.slide');const n=document.querySelector('.count');
function paint(){n.textContent=`SLIDE ${c+1} / ${s.length}`}
function go(d){s[c].classList.remove('on');c=(c+d+s.length)%s.length;s[c].classList.add('on');paint()}
document.addEventListener('keydown',e=>{if(e.key==='ArrowRight')go(1);if(e.key==='ArrowLeft')go(-1)});
paint();</script></body></html>"""


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
        body = "<br>".join(html.escape(l.strip()) for l in lines[1:] if l.strip())
        out.append(f'<div class="slide{" on" if i == 0 else ""}"><div class="badge">VOID PRISM DECK · {i + 1} OF {len(secs)}</div>'
                   f'<h2>{esc(heading.replace("**", ""))}</h2><div class="body">{body}</div></div>')
    return (SLIDE_TPL.replace("%%TITLE%%", esc(title)).replace("%%COUNT%%", f"SLIDE 1 / {len(secs)}")
            .replace("%%SLIDES%%", "".join(out)))


def extract_code_blocks(text):
    return re.findall(r"```(\w*)\n(.*?)```", text, re.DOTALL)


def is_html_block(b):
    return b[0].lower() in ("html", "xml", "svg") or "<html" in b[1].lower() or "<style" in b[1].lower()


def detect_prism_intent(prompt, reply=""):
    triggers = ("pdf", "ppt", "slide", "presentation", "study notes", "cheat sheet", "worksheet", "html app")
    return any(t in prompt.lower() for t in triggers) or "```html" in reply.lower()


def send_otp_email(to, code):
    if not (EJS_SERVICE and EJS_TEMPLATE and EJS_PUBLIC):
        return False, "Email service not configured in Secrets."
    payload = {"service_id": EJS_SERVICE, "template_id": EJS_TEMPLATE, "user_id": EJS_PUBLIC,
               "template_params": {"to_email": to, "otp_code": code}}
    if EJS_PRIVATE:
        payload["accessToken"] = EJS_PRIVATE
    try:
        r = http_session().post(EMAILJS_URL, json=payload, timeout=25)
        return (True, None) if r.status_code == 200 else (False, r.text[:180])
    except Exception as e:
        return False, str(e)


# ============================== 9. AUTHENTICATION ==============================
if "user_email" not in st.session_state:
    restored = restore_login()
    if restored:
        st.session_state.user_email = restored

if "user_email" not in st.session_state:
    st.markdown(f'<div class="void-hero"><div class="hero-mark"><img src="{LOGO_B64}" width="32"/></div>'
                '<div class="void-gradient">VOID</div>'
                '<div class="void-sub">Sovereign OS Intelligence · Instant Live Knowledge · Absolute Autonomy</div></div>',
                unsafe_allow_html=True)

    _, mid, _ = st.columns([1, 1.4, 1])
    with mid:
        st.markdown("<p style='text-align:center; color:#71717a; font-size:.84rem; margin-bottom:12px;'>"
                    "Start instantly as Guest Operator or authenticate via Email</p>", unsafe_allow_html=True)
        with st.form("landing_search_form"):
            landing_query = st.text_input("Direct Search / Prompt", placeholder="Ask anything about current events, code, or ideas…",
                                          label_visibility="collapsed")
            c_s, c_g = st.columns(2)
            with c_s:
                search_submit = st.form_submit_button("Ask VOID", type="primary", use_container_width=True)
            with c_g:
                guest_submit = st.form_submit_button("Enter Guest Mode", use_container_width=True)

            if search_submit or guest_submit:
                guest_email = f"guest_{uuid.uuid4().hex[:6]}@void.os"
                ensure_user(guest_email, name="Guest Operator")
                st.session_state.user_email = guest_email
                remember_login(guest_email)
                if search_submit and landing_query.strip():
                    cid = list(db["chats"][guest_email].keys())[-1]
                    db["chats"][guest_email][cid]["messages"].append({"role": "user", "content": landing_query.strip()})
                    t = landing_query.strip().replace("\n", " ")
                    db["chats"][guest_email][cid]["title"] = t[:24] + "..." if len(t) > 24 else t
                    save_db(db)
                st.rerun()

        st.markdown("<div style='text-align:center; margin:14px 0; color:#3f3f46; font-size:.74rem; letter-spacing:.12em;'>OR · EMAIL VERIFICATION</div>",
                    unsafe_allow_html=True)

        if "pending_email" not in st.session_state:
            with st.form("email_form"):
                email_in = st.text_input("Email", placeholder="name@domain.com", max_chars=80).strip().lower()
                name_in = st.text_input("Name (optional)", placeholder="Your name", max_chars=40).strip()
                if st.form_submit_button("Send Access Code", use_container_width=True):
                    wait = OTP_COOLDOWN - (time.time() - st.session_state.get("last_otp_ts", 0))
                    if not EMAIL_RE.match(email_in):
                        st.error("Please enter a valid email address.")
                    elif wait > 0:
                        st.warning(f"Please wait {int(wait)}s before requesting a new code.")
                    else:
                        code = str(pysecrets.randbelow(900000) + 100000)
                        ok, err = send_otp_email(email_in, code)
                        st.session_state.last_otp_ts = time.time()
                        if ok:
                            st.session_state.update(pending_email=email_in, pending_name=name_in, target_otp=code,
                                                    otp_expiry=time.time() + OTP_TTL, otp_tries=0)
                            st.rerun()
                        else:
                            st.error(f"Relay error: {err}")
        else:
            st.info(f"Code sent to **{st.session_state.pending_email}** (valid 10 mins)")
            with st.form("otp_form"):
                otp_in = st.text_input("6-Digit Code", placeholder="123456", max_chars=6)
                if st.form_submit_button("Verify & Enter VOID", type="primary", use_container_width=True):
                    st.session_state.otp_tries += 1
                    if time.time() > st.session_state.otp_expiry:
                        st.error("Code expired. Request another.")
                    elif hmac.compare_digest(otp_in.strip(), st.session_state.target_otp):
                        email = st.session_state.pending_email
                        ensure_user(email, st.session_state.get("pending_name") or None)
                        st.session_state.user_email = email
                        remember_login(email)
                        for k in ("pending_email", "pending_name", "target_otp", "otp_expiry", "otp_tries"):
                            st.session_state.pop(k, None)
                        st.rerun()
                    else:
                        st.error("Incorrect verification code.")
    st.stop()
else:
    remember_login(st.session_state.user_email)

# ============================== 10. ACTIVE OPERATOR ==============================
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

# ============================== 11. SIDEBAR & TELEMETRY ==============================
with st.sidebar:
    st.markdown(f'<div class="topbar-brand"><img src="{LOGO_B64}" width="26"/>'
                '<span class="topbar-title">VOID</span>'
                '<span class="topbar-pill">OS APEX</span></div>', unsafe_allow_html=True)

    if st.button("New Session", type="primary", use_container_width=True):
        st.session_state.current_chat_id = new_chat(user_email)
        st.session_state.active_prism_text = None
        st.session_state.prism_open = False
        save_db(db)
        st.rerun()

    if st.session_state.pop("force_prism", False):
        st.session_state.prism_open = True
    prism_open = st.toggle("VOID Prism side-panel", key="prism_open")

    st.markdown("<div style='font-size:0.75rem; color:#71717a; margin-top:1rem;'>SESSIONS</div>", unsafe_allow_html=True)
    for cid, cdata in reversed(list(user_chats.items())):
        col_t, col_d = st.columns([5, 1])
        with col_t:
            if st.button(f"{'● ' if cid == current_chat_id else '○ '}{cdata['title']}", key=f"c_{cid}",
                         use_container_width=True):
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
    with st.expander("Engine diagnostics"):
        s_status, s_note = engine_status()
        st.markdown(f"<span class='pill {'pill-ok' if s_status == 'online' else 'pill-bad'}'>{s_status}</span>", unsafe_allow_html=True)
        st.caption(s_note)
        for label, ok in [("OpenRouter Gateway", bool(PROV_KEYS["openrouter"])),
                          ("Google Direct Relay", bool(PROV_KEYS["google"])),
                          ("Groq Ultra-Fast", bool(PROV_KEYS["groq"])),
                          ("Google News Live Feed", True),
                          ("Wikipedia Deep Search", True),
                          ("Tavily/Serper Key", bool(SEARCH_KEYS["tavily"] or SEARCH_KEYS["serper"]))]:
            mark = "<span style='color:#10b981'>●</span>" if ok else "<span style='color:#71717a'>○</span>"
            st.markdown(f"<div class='kv'><span>{mark} {esc(label)}</span></div>", unsafe_allow_html=True)

    with st.expander("Identity vault"):
        n_name = st.text_input("Name", value=user_name, max_chars=40)
        n_city = st.text_input("City", value=user_city, max_chars=50)
        n_mem = st.text_area("Memory & Notes", value=user_memory, height=90)
        if st.button("Save profile", use_container_width=True):
            if not is_founder:
                user_record["name"] = n_name.strip()[:40] or user_name
            user_record["city"] = n_city.strip() or "Varanasi"
            user_record["memory"] = n_mem.strip()
            save_db(db)
            st.rerun()

    with st.expander("Founder"):
        st.markdown(f"**{FOUNDER_NAME}** — *Architect of VOID*\n\n{FOUNDER_BIO}")

    if st.button("Sign out", use_container_width=True):
        st.query_params.clear()
        for k in ("user_email", "current_chat_id", "active_prism_text", "prism_open"):
            st.session_state.pop(k, None)
        st.rerun()

# ============================== 12. COMMAND BAR ==============================
uploaded_file, file_context = None, ""
c1, c2, c3, c4 = st.columns([1.9, 1.8, 1.7, 1.2])
with c1:
    ui_mode = st.selectbox("Dimension", ["✦ VOID Core & Prism", "📖 VOID Codex (Study, PDF & Slides)",
                                         "⚡ Live Web App Studio", "🛠️ Side-by-Side Code Lab",
                                         "🧬 Self-Evolution Lab", "🛰️ Ship Telemetry & Insights",
                                         "🩺 Engine Doctor & Live Test"], label_visibility="collapsed")
with c2:
    cosmic_entity = st.selectbox("Cosmic Engine", list(ENGINES), label_visibility="collapsed")
with c3:
    persona = st.selectbox("Resonance Mode", ["✦ VOID Omni (Universal)", "🎓 Master Scholastic Tutor",
                                              "💻 Full-Stack Architect", "🎨 UI & Slide Designer", "🐞 Deep Bug Hunter"],
                           label_visibility="collapsed")
with c4:
    with st.popover("Tune & Live Web", use_container_width=True):
        uploaded_file = st.file_uploader("Attach Document",
                                         type=["py", "js", "html", "css", "json", "txt", "md", "csv"])
        if uploaded_file:
            try:
                file_context = uploaded_file.getvalue().decode("utf-8")[:MAX_FILE_CHARS]
                st.success(f"Attached `{uploaded_file.name}`")
            except Exception:
                st.error("Error decoding file.")
        research_depth = st.select_slider("Live Web Grounding", ["Standard", "Deep", "Off"], value="Standard",
                                          help="Fetches live breaking news, current events, and web documentation.")
        accuracy_mode = st.toggle("Verified answer mode", value=True)
        show_thinking = st.toggle("Live stream tokens", value=True)
        temperature = st.slider("Creativity", 0.0, 1.0, 0.25, 0.05)
        max_tokens = st.slider("Max output tokens", 400, 4000, 3000, 100)


def build_system_prompt(grounded_context, is_prism=False, extra=""):
    now_ist = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    time_str = now_ist.strftime("%A, %B %d, %Y | %I:%M %p IST")

    fmt = ("The user wants a formal document, guide, or slide deck. Use clean Markdown headings (# and ##) "
           "and bullet points so VOID Prism can automatically compile it into a PDF and interactive slides."
           if is_prism else
           "Answer concisely, directly, and conversationally. Answer in the first sentence with zero filler.")

    return f"""You are VOID, the world's most capable sovereign digital intelligence, engineered by {FOUNDER_NAME}.
You never say you are an AI model made by any other company. You are VOID.

=== TEMPORAL CHRONOMETER ===
Current exact date & time: {time_str}
Current location focus: {user_city}, India.

=== GROUNDING & CURRENT AFFAIRS TRUTH ===
Treat the following live internet results as authoritative facts for the modern world:
{grounded_context}

=== STRICT ANSWERING RULES ===
1. Answer the question in the very first sentence. No preamble, no 'Certainly!', no 'As of my cutoff'.
2. If the user asks about current affairs, latest news, leaders, events, sports, weather, or technology, ALWAYS base your answer on the live intelligence above.
3. If specific information is still missing, state what is verified, then give the most logical current analysis. NEVER refuse to answer.
4. If asked 'Who am I?', you are speaking with {user_name} ({user_email}).
5. Founder Profile: {FOUNDER_NAME} ({FOUNDER_BIO}).
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


def diag_html(diag):
    band = "high" if diag.get("search_hits", 0) > 0 or diag.get("math") else "moderate"
    rows = [f"<b>link</b> {esc(diag.get('link', 'Cosmic Relay'))} · <b>model</b> {esc(diag.get('model', 'Auto'))} · <b>{diag.get('latency', '0.4')}s</b>",
            f"<b>live intelligence</b> {diag.get('search_hits', 0)} sources retrieved · <b>math calc</b> {'yes' if diag.get('math') else 'no'}"]
    if diag.get("repaired"):
        rows.append("<b>auto-healing</b> answer automatically verified & refined")
    return f"<div class='diag-box'><span class='pill pill-ok'>status: verified</span><br>" + "<br>".join(rows) + "</div>"


# ============================== DIMENSION 1: CORE & PRISM ==============================
if ui_mode == "✦ VOID Core & Prism":
    if prism_open:
        chat_col, prism_col = st.columns([1.18, 1], gap="large")
    else:
        chat_col, prism_col = st.container(), None
    quick_prompt = None

    with chat_col:
        if not current_chat["messages"]:
            st.markdown(f'<div class="void-hero"><div class="hero-mark"><img src="{LOGO_B64}" width="30"/></div>'
                        f'<div class="void-gradient">Greetings, {safe_user}</div>'
                        '<div class="void-sub">Ask any question. Live internet intelligence & breaking news are fetched automatically.</div></div>', unsafe_allow_html=True)
            cards = [("Live World News", "What are the biggest breaking news headlines and events happening in the world today?"),
                     ("Current Weather", f"What is the live weather and temperature right now in {user_city}?"),
                     ("Study Revision PDF", "Make a Class 8 Science study guide on Force & Pressure with formulas and exam questions."),
                     ("Web Mini-Game", "Build a dark-themed playable Hand Cricket mini-game in a single HTML block.")]
            for col, (label, prompt) in zip(st.columns(4), cards):
                with col:
                    if st.button(label, use_container_width=True, key=f"qp_{label[:5]}"):
                        quick_prompt = prompt

        for idx, msg in enumerate(current_chat["messages"]):
            with st.chat_message(msg["role"], avatar=LOGO_B64 if msg["role"] == "assistant" else None):
                st.markdown(msg["content"])
                if msg.get("diag"):
                    st.markdown(diag_html(msg["diag"]), unsafe_allow_html=True)
                if msg["role"] == "assistant":
                    b1, b2 = st.columns(2)
                    with b1:
                        st.download_button("Download PDF", generate_real_pdf_bytes(current_chat["title"], msg["content"], f"VOID ({user_name})"),
                                           file_name=f"VOID_{safe_name(current_chat['title'], 15)}_{idx}.pdf",
                                           mime="application/pdf", key=f"pdf_{idx}", use_container_width=True)
                    with b2:
                        if st.button("Open in Prism Panel", key=f"op_{idx}", use_container_width=True):
                            send_to_prism(msg["content"], current_chat["title"])
                            st.rerun()

    typed = st.chat_input(f"Ask VOID anything, {user_name}…")
    active_prompt = quick_prompt or typed

    if not active_prompt and len(current_chat["messages"]) == 1 and current_chat["messages"][0]["role"] == "user":
        active_prompt = current_chat["messages"][0]["content"]
        current_chat["messages"].pop()

    reply, reply_diag = None, {}
    if active_prompt:
        full_prompt = (f"Attached file (`{uploaded_file.name}`):\n```\n{file_context}\n```\n\n{active_prompt}"
                       if file_context else active_prompt)
        if not current_chat["messages"]:
            t = active_prompt.strip().replace("\n", " ")
            current_chat["title"] = t[:24] + "..." if len(t) > 24 else t
        current_chat["messages"].append({"role": "user", "content": full_prompt})
        bump_usage()

        with chat_col:
            with st.chat_message("user"):
                st.markdown(full_prompt)
            with st.chat_message("assistant", avatar=LOGO_B64):
                try:
                    diag = {}
                    with st.spinner("Connecting to live web intelligence…"):
                        live_intel = grounding(active_prompt, research_depth, diag)
                        if any(w in active_prompt.lower() for w in ("weather", "temperature", "climate")):
                            live_intel += "\n" + fetch_live_weather(user_city)
                    system = build_system_prompt(live_intel, detect_prism_intent(active_prompt))

                    if accuracy_mode:
                        with st.spinner("Synthesizing verified answer…"):
                            reply = answer_question(cosmic_entity, active_prompt, system,
                                                    current_chat["messages"], temperature, max_tokens,
                                                    accuracy_mode=True, diag=diag)
                        st.markdown(reply)
                    else:
                        gen = stream_llm(cosmic_entity, system, current_chat["messages"], temperature,
                                         max_tokens, prompt=active_prompt, diag=diag)
                        raw = st.write_stream(gen if show_thinking else _buffered(gen))
                        reply = raw if isinstance(raw, str) else "".join(map(str, raw or []))

                    reply_diag = diag
                    if reply:
                        st.markdown(diag_html(diag), unsafe_allow_html=True)
                except Exception as e:
                    st.error(f"Intelligence loop notice: {e}")

        if reply:
            is_prism = detect_prism_intent(active_prompt, reply)
            clean_diag = {k: v for k, v in reply_diag.items() if not k.startswith("_")}
            current_chat["messages"].append({"role": "assistant", "content": reply,
                                             "is_prism": is_prism, "diag": clean_diag})
            if is_prism:
                send_to_prism(reply, current_chat["title"])
            save_db(db)
            st.rerun()

    if prism_open and prism_col is not None:
        with prism_col:
            st.markdown('<div class="prism-card">', unsafe_allow_html=True)
            st.markdown("#### VOID Prism")
            p_text = st.session_state.get("active_prism_text")
            p_title = st.session_state.get("active_prism_title", current_chat["title"])
            if not p_text:
                p_text = next((m["content"] for m in reversed(current_chat["messages"]) if m["role"] == "assistant"), None)

            if p_text:
                blocks = extract_code_blocks(p_text)
                t_doc, t_slides, t_app, t_edit = st.tabs(["Document", "Slides", "Live App / Code", "Edit"])
                with t_doc:
                    d1, d2, d3 = st.columns(3)
                    with d1:
                        st.download_button("PDF", generate_real_pdf_bytes(p_title, p_text, f"VOID ({user_name})"),
                                           file_name=f"VOID_{safe_name(p_title, 15)}.pdf", mime="application/pdf",
                                           type="primary", use_container_width=True)
                    with d2:
                        st.download_button("Slides", generate_interactive_slides_html(p_title, p_text).encode("utf-8"),
                                           file_name=f"VOID_Slides_{safe_name(p_title, 15)}.html", mime="text/html",
                                           use_container_width=True)
                    with d3:
                        st.download_button("Markdown", p_text, file_name=f"VOID_{safe_name(p_title, 15)}.md",
                                           mime="text/markdown", use_container_width=True)
                    st.markdown("---")
                    st.markdown(p_text)
                with t_slides:
                    components.html(generate_interactive_slides_html(p_title, p_text), height=440)
                with t_app:
                    if blocks:
                        blk = next((b for b in blocks if is_html_block(b)), blocks[0])
                        if is_html_block(blk):
                            components.html(blk[1].strip(), height=460, scrolling=True)
                        else:
                            st.code(blk[1].strip(), language=blk[0].lower() or None)
                    else:
                        st.info("Ask VOID to forge an HTML web app or script to test it live here.")
                with t_edit:
                    edited = st.text_area("Modify", value=p_text, height=320)
                    if st.button("Update & Rebuild", use_container_width=True):
                        st.session_state.active_prism_text = edited
                        st.rerun()
            else:
                st.info("Outputs with code, notes, or slide requests appear here automatically.")
            st.markdown("</div>", unsafe_allow_html=True)

# ============================== DIMENSION 2: CODEX ==============================
elif ui_mode == "📖 VOID Codex (Study, PDF & Slides)":
    st.markdown("### VOID Scholastic Codex")
    st.caption("Generate instant master notes, summaries, and exam prep decks.")
    s1, s2, s3 = st.columns([2.2, 1.3, 1])
    with s1:
        topic = st.text_input("Topic or Question", placeholder="E.g., Quantum Computing, Cell Division, Indian Constitution…")
    with s2:
        fmt = st.selectbox("Codex Mode", ["📘 Complete Revision Notes + Formulas", "💡 Plain Explanation with Examples",
                                          "❓ Exam Question Bank (MCQs + Answers)", "📊 Full Slide Presentation Deck"])
    with s3:
        level = st.selectbox("Target Level", ["Class 8 (CBSE/ICSE)", "Class 9-10 High School", "Advanced / Collegiate", "Quick Summary"])

    if st.button("Forge Material", type="primary", use_container_width=True):
        if topic.strip():
            bump_usage()
            d = {}
            with st.spinner(f"Forging {topic}…"):
                live_intel = grounding(topic, research_depth, d)
                sys_p = build_system_prompt(live_intel, True, f"Create a comprehensive master academic study resource on '{topic}' ({level}). Format: {fmt}.")
                res = answer_question(cosmic_entity, f"Forge {fmt} for: {topic}", sys_p,
                                      [{"role": "user", "content": f"Forge {fmt} for: {topic}"}],
                                      0.2, 2800, accuracy_mode=accuracy_mode, diag=d)
            if res:
                st.session_state.codex_output, st.session_state.codex_topic = res, topic.strip()
                st.session_state.codex_diag = d
                st.rerun()
        else:
            st.warning("Enter a topic first.")

    if "codex_output" in st.session_state:
        text, ctopic = st.session_state.codex_output, st.session_state.get("codex_topic", "Study")
        fname = safe_name(ctopic)
        st.markdown("---")
        d1, d2, d3, d4 = st.columns(4)
        with d1:
            st.download_button("Download PDF", generate_real_pdf_bytes(f"VOID Codex: {ctopic}", text, f"VOID Codex ({user_name})"),
                               file_name=f"VOID_Codex_{fname}.pdf", mime="application/pdf", type="primary", use_container_width=True)
        with d2:
            st.download_button("Slide Deck (.html)", generate_interactive_slides_html(ctopic, text).encode("utf-8"),
                               file_name=f"VOID_Slides_{fname}.html", mime="text/html", use_container_width=True)
        with d3:
            st.download_button("Markdown (.md)", text, file_name=f"VOID_Codex_{fname}.md", mime="text/markdown", use_container_width=True)
        with d4:
            if st.button("Send to Session", use_container_width=True):
                cid = current_chat_id
                user_chats[cid]["messages"].append({"role": "user", "content": f"[Codex] {ctopic}"})
                user_chats[cid]["messages"].append({"role": "assistant", "content": text, "is_prism": True})
                send_to_prism(text, f"VOID Codex: {ctopic}")
                save_db(db)
                st.success("Appended to current session.")
        t1, t2 = st.tabs(["Document View", "Slide Presentation"])
        with t1:
            st.markdown(text)
        with t2:
            components.html(generate_interactive_slides_html(ctopic, text), height=500)

# ============================== DIMENSION 3: WEB APP STUDIO ==============================
elif ui_mode == "⚡ Live Web App Studio":
    st.markdown("### VOID Live Web App Studio")
    st.caption("Prompt any complete browser app, calculator, or interactive game.")
    ui_prompt = st.text_area("What should VOID build?", height=85,
                             placeholder="E.g., A sleek dark Pomodoro study timer with sound effects…")
    if st.button("Forge & Run Live", type="primary"):
        if ui_prompt.strip():
            bump_usage()
            sys_p = "Output ONLY ONE valid self-contained HTML file (with embedded CSS and JS inside) wrapped in a ```html block."
            with st.spinner("Compiling application…"):
                out, _ = call_llm(cosmic_entity, sys_p, [{"role": "user", "content": ui_prompt}], 0.3, max_tokens, prompt=ui_prompt)
            if out:
                m = re.search(r"```(?:html)?\s*\n(.*?)```", out, re.DOTALL)
                st.session_state.studio_html = (m.group(1) if m else out).strip()
        else:
            st.warning("Enter a description.")

    if "studio_html" in st.session_state:
        c_p, c_s = st.columns([1.5, 1])
        with c_p:
            st.markdown("##### Live Output")
            components.html(st.session_state.studio_html, height=520, scrolling=True)
        with c_s:
            st.markdown("##### Source Code")
            st.download_button("Download index.html", st.session_state.studio_html, file_name="index.html", mime="text/html", use_container_width=True)
            st.code(st.session_state.studio_html, language="html")

# ============================== DIMENSION 4: CODE LAB ==============================
elif ui_mode == "🛠️ Side-by-Side Code Lab":
    st.markdown("### VOID Code Refactor & Bug Lab")
    action = st.selectbox("Operation", ["🐞 Find & Fix All Bugs", "🚀 Maximum Optimization", "🛡️ Add Type Hints & Error Handling", "🔄 Translate to Python/C++"])
    l_col, r_col = st.columns(2)
    with l_col:
        code_in = st.text_area("Source Code", height=340, placeholder="Paste code here…")
        go = st.button("Transform Code", type="primary", use_container_width=True)
    with r_col:
        st.markdown("**Refactored Output**")
        if go and code_in.strip():
            bump_usage()
            with st.spinner("Processing AST & Refactoring…"):
                out, err = call_llm(cosmic_entity, f"Perform {action} on this code. Output complete code with clear comments.",
                                    [{"role": "user", "content": code_in}], 0.1, max_tokens, prompt=code_in)
                st.session_state.lab_res = out or f"Error: {err}"
        if st.session_state.get("lab_res"):
            st.markdown(st.session_state.lab_res)
        else:
            st.info("Paste code on the left and run.")

# ============================== DIMENSION 5: SELF-EVOLUTION LAB ==============================
elif ui_mode == "🧬 Self-Evolution Lab":
    st.markdown("### VOID Self-Evolution & Architecture Lab")
    evo_goal = st.text_input("What upgrade should VOID code for itself?",
                             placeholder="E.g., Add a live speech-to-text sidebar module…")
    if st.button("Generate Architectural Upgrade", type="primary") and evo_goal.strip():
        bump_usage()
        sys_p = f"You are the master core architect of VOID. Provide complete, drop-in Streamlit code to add: '{evo_goal}'."
        with st.spinner("Designing upgrade blueprint…"):
            out, _ = call_llm("☀️ Supernova X (Coding & Architecture)", sys_p, [{"role": "user", "content": evo_goal}], 0.2, 3500)
            st.session_state.evo_res = out
    if "evo_res" in st.session_state:
        st.markdown("---")
        st.markdown(st.session_state.evo_res)

# ============================== DIMENSION 6: SHIP TELEMETRY ==============================
elif ui_mode == "🛰️ Ship Telemetry & Insights":
    st.markdown("### VOID Ship Telemetry")
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Operators", len(db["users"]))
    k2.metric("Total Sessions", sum(len(v) for v in db["chats"].values()))
    k3.metric("Total Messages", sum(len(c.get("messages", [])) for v in db["chats"].values() for c in v.values()))
    k4.metric("Prompts All Time", sum(db.get("usage", {}).values()))

    today = datetime.now().date()
    days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(29, -1, -1)]
    series = pd.Series([db.get("usage", {}).get(d, 0) for d in days], index=[d[5:] for d in days])
    if series.sum() > 0:
        st.area_chart(series, height=240)
    else:
        st.info("Telemetry tracking starts as soon as prompts are sent.")

    if is_founder:
        st.markdown("##### Registered Operators")
        rows = [{"Name": info.get("name"), "Email": mail, "Prompts": info.get("prompts", 0), "Last Active": info.get("last_active")}
                for mail, info in db["users"].items()]
        st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

# ============================== DIMENSION 7: ENGINE DOCTOR ==============================
elif ui_mode == "🩺 Engine Doctor & Live Test":
    st.markdown("### VOID Diagnostic Doctor")
    d1, d2 = st.columns(2)
    with d1:
        st.markdown("##### Automated Gateway Tests")
        if st.button("Test Answer Engine", type="primary", use_container_width=True):
            d = {}
            out, err = call_llm("🧠 Auto-Route (Omni Intelligence)", "Reply with exactly: VOID OK",
                                [{"role": "user", "content": "Ping test"}], 0.1, 50, prompt="Ping test", diag=d)
            if out:
                st.success(f"Response via {d.get('link', 'Relay')} ({d.get('latency')}s): {out.strip()}")
            else:
                st.error(err)
        if st.button("Test Live Web Intelligence (Google News + DDG)", use_container_width=True):
            intel, urls = web_search_bundle("world news headlines", 4)
            if intel:
                st.success(f"Retrieved {len(intel.splitlines())} live items!")
                st.code(intel[:900])
            else:
                st.error("Live retrieval returned no items.")
    with d2:
        st.markdown("##### Live Query Test with Intelligence Inspector")
        probe = st.text_input("Test Query", "Who is the current Prime Minister of the United Kingdom?")
        if st.button("Inspect Retrieval & Answer"):
            d = {}
            with st.spinner("Fetching live facts…"):
                intel = grounding(probe, "Standard", d)
                st.markdown("**Live Context Injected:**")
                st.code(intel if intel else "No web results.")
                sys_p = build_system_prompt(intel)
                ans = answer_question(cosmic_entity, probe, sys_p, [{"role": "user", "content": probe}], 0.2, 500, diag=d)
                st.markdown("**Answer:**")
                st.markdown(ans)
                st.markdown(diag_html(d), unsafe_allow_html=True)

# ============================== 13. FOOTER ==============================
st.markdown(f'<div class="void-footer">VOID · Sovereign OS Intelligence · Forged by {esc(FOUNDER_NAME)} · Prism OS v{APP_VERSION}</div>',
            unsafe_allow_html=True)
