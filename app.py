"""
VOID — Sovereign OS Intelligence · app.py
Version: 6.6.0-Obsidian Apex

High-Contrast Obsidian Desktop UI + Concrete Live Internet Grounding Engine
+ Multi-Provider Failover Chain. Retains all 7 Core Dimensions, VOID Prism,
PDF Forge, Interactive Slide Decks, and Identity Vault.
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

APP_VERSION = "6.6.0-Obsidian"

# ============================== 1. BRAND & PAGE ==============================
SVG_RAW = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120">'
    '<defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%">'
    '<stop offset="0%" stop-color="#3b82f6"/><stop offset="100%" stop-color="#8b5cf6"/>'
    '</linearGradient></defs>'
    '<rect width="120" height="120" rx="28" fill="#09090b" stroke="url(#g)" stroke-width="6"/>'
    '<path d="M34 38 L60 86 L86 38" fill="none" stroke="url(#g)" stroke-width="12" '
    'stroke-linecap="round" stroke-linejoin="round"/>'
    '<circle cx="60" cy="34" r="7" fill="#ffffff"/></svg>'
)
LOGO_B64 = "data:image/svg+xml;base64," + base64.b64encode(SVG_RAW.encode()).decode()

if not os.path.exists("void_logo.svg"):
    try:
        with open("void_logo.svg", "w", encoding="utf-8") as f:
            f.write(SVG_RAW)
    except OSError:
        pass
LOGO_PATH = next((p for p in ("logo.png", "void_logo.svg") if os.path.exists(p)), "⚡")

st.set_page_config(
    page_title="VOID — Sovereign OS Intelligence",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state="expanded",
)
try:
    if LOGO_PATH != "⚡":
        st.logo(LOGO_PATH)
except Exception:
    pass

# --- HIGH-END OBSIDIAN DESKTOP UI THEME ---
MINIMAL_CSS = """<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
  --bg: #09090b;
  --bg-elevated: #0e0e11;
  --surface: #121216;
  --surface-2: #18181e;
  --surface-hover: #1f1f27;
  --line: #232329;
  --line-2: #2e2e38;
  --line-focus: #3b82f6;
  --text: #f4f4f6;
  --text-2: #a1a1aa;
  --text-3: #71717a;
  --accent: #fafafa;
  --accent-blue: #3b82f6;
  --ok: #10b981;
  --warn: #f59e0b;
  --bad: #ef4444;
}

/* Global Reset & Viewport Lock */
html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
  background-color: var(--bg) !important;
  background-image: radial-gradient(circle at 50% 0%, rgba(59, 130, 246, 0.04), transparent 45%) !important;
  color: var(--text) !important;
  font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

[data-testid="stToolbarActions"], [data-testid="stAppDeployButton"], [data-testid="stDecoration"],
[data-testid="stStatusWidget"], #MainMenu, footer {
  display: none !important;
}

header[data-testid="stHeader"] {
  background: transparent !important;
  height: 2.5rem !important;
}

/* Main Container Spacing — generous bottom padding prevents chat input overlap */
.block-container {
  max-width: 1180px !important;
  padding-top: 1.6rem !important;
  padding-bottom: 9.5rem !important;
  padding-left: 2rem !important;
  padding-right: 2rem !important;
}

/* Sidebar Obsidian Styling */
section[data-testid="stSidebar"] {
  background-color: var(--bg-elevated) !important;
  border-right: 1px solid var(--line) !important;
}
section[data-testid="stSidebar"] > div {
  padding-top: 1.1rem !important;
}

/* Anchored Bottom Chat Composer Bar */
[data-testid="stBottom"],
[data-testid="stBottom"] > div,
[data-testid="stBottomBlockContainer"],
.stChatFloatingInputContainer {
  background: linear-gradient(180deg, rgba(9, 9, 11, 0.75) 0%, rgba(9, 9, 11, 0.98) 35%, #09090b 100%) !important;
  backdrop-filter: blur(16px) !important;
  -webkit-backdrop-filter: blur(16px) !important;
  border-top: 1px solid var(--line) !important;
  padding-top: 0.65rem !important;
  padding-bottom: 0.85rem !important;
  z-index: 99 !important;
}

[data-testid="stChatInput"],
[data-testid="stChatInputContainer"] {
  background-color: var(--surface) !important;
  border: 1px solid var(--line-2) !important;
  border-radius: 14px !important;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.55) !important;
  transition: border-color 0.18s ease, box-shadow 0.18s ease !important;
}
[data-testid="stChatInput"]:focus-within {
  border-color: var(--line-focus) !important;
  box-shadow: 0 0 0 2px rgba(59, 130, 246, 0.18), 0 8px 30px rgba(0, 0, 0, 0.65) !important;
}
[data-testid="stChatInput"] textarea {
  color: var(--text) !important;
  -webkit-text-fill-color: var(--text) !important;
  background: transparent !important;
  font-size: 0.95rem !important;
  line-height: 1.5 !important;
}
[data-testid="stChatInput"] textarea::placeholder {
  color: var(--text-3) !important;
  -webkit-text-fill-color: var(--text-3) !important;
}

/* Typography & Hierarchy */
h1, h2, h3, h4, h5, h6 {
  color: var(--text) !important;
  font-weight: 600 !important;
  letter-spacing: -0.024em !important;
  line-height: 1.3 !important;
}
h1 { font-size: 1.75rem !important; }
h2 { font-size: 1.32rem !important; margin-top: 1.2rem !important; }
h3 { font-size: 1.1rem !important; }
p, li, .stMarkdown {
  color: var(--text) !important;
  font-size: 0.955rem !important;
  line-height: 1.72 !important;
}
span, label { color: var(--text) !important; }
small, .stCaption, [data-testid="stCaptionContainer"], .stCaption p {
  color: var(--text-3) !important;
  font-size: 0.79rem !important;
}
strong, b { font-weight: 600 !important; color: #ffffff !important; }
a {
  color: #60a5fa !important;
  text-decoration: underline;
  text-underline-offset: 3px;
}
a:hover { color: #93c5fd !important; }
hr {
  border: 0 !important;
  border-top: 1px solid var(--line) !important;
  margin: 1.4rem 0 !important;
}
blockquote {
  border-left: 2px solid var(--line-focus) !important;
  background: rgba(59, 130, 246, 0.04) !important;
  margin: 0.8rem 0 !important;
  padding: 0.5rem 1rem !important;
  border-radius: 0 8px 8px 0 !important;
  color: var(--text-2) !important;
}

/* Sleek Desktop Chat Message Bubbles */
.stChatMessage {
  background-color: var(--surface) !important;
  border: 1px solid var(--line) !important;
  border-radius: 14px !important;
  padding: 1.15rem 1.35rem !important;
  margin-bottom: 0.9rem !important;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.28) !important;
  transition: border-color 0.15s ease !important;
}
.stChatMessage:hover {
  border-color: var(--line-2) !important;
}
.stChatMessage p, .stChatMessage li {
  font-size: 0.955rem !important;
  line-height: 1.72 !important;
}
[data-testid="stChatMessageAvatarCustom"] img {
  border-radius: 8px !important;
  border: 1px solid var(--line-2) !important;
}

/* Text Inputs, Textareas, Selectboxes */
input[type="text"], input[type="password"], input[type="number"],
div[data-baseweb="input"] input, div[data-baseweb="base-input"] input,
div[data-baseweb="textarea"] textarea, [data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {
  background-color: var(--surface) !important;
  color: var(--text) !important;
  -webkit-text-fill-color: var(--text) !important;
  border-radius: 10px !important;
  font-size: 0.92rem !important;
}
div[data-baseweb="input"], div[data-baseweb="base-input"], div[data-baseweb="textarea"],
[data-testid="stTextInput"] > div, [data-testid="stTextArea"] > div {
  background-color: var(--surface) !important;
  border: 1px solid var(--line-2) !important;
  border-radius: 10px !important;
  box-shadow: none !important;
}
div[data-baseweb="input"]:focus-within, div[data-baseweb="textarea"]:focus-within {
  border-color: var(--line-focus) !important;
}
input::placeholder, textarea::placeholder {
  color: var(--text-3) !important;
  -webkit-text-fill-color: var(--text-3) !important;
}
div[data-baseweb="select"] > div {
  background-color: var(--surface) !important;
  border: 1px solid var(--line-2) !important;
  border-radius: 10px !important;
  color: var(--text) !important;
  font-size: 0.88rem !important;
  min-height: 2.45rem !important;
}
div[data-baseweb="popover"] ul, div[data-baseweb="menu"] {
  background-color: var(--surface-2) !important;
  border: 1px solid var(--line-2) !important;
  border-radius: 10px !important;
}
li[data-baseweb="menu-item"] {
  background-color: transparent !important;
  color: var(--text) !important;
  font-size: 0.88rem !important;
}
li[data-baseweb="menu-item"]:hover {
  background-color: var(--surface-hover) !important;
}

/* Buttons & Popovers */
.stButton > button, .stDownloadButton > button, [data-testid="stPopover"] > button {
  background-color: var(--surface) !important;
  color: var(--text) !important;
  border: 1px solid var(--line-2) !important;
  border-radius: 10px !important;
  font-weight: 500 !important;
  font-size: 0.85rem !important;
  padding: 0.44rem 0.9rem !important;
  min-height: 2.45rem !important;
  box-shadow: 0 1px 2px rgba(0, 0, 0, 0.3) !important;
  transition: all 0.15s ease !important;
}
.stButton > button:hover, .stDownloadButton > button:hover, [data-testid="stPopover"] > button:hover {
  background-color: var(--surface-hover) !important;
  border-color: #454552 !important;
  transform: translateY(-1px);
}
.stButton > button:active, .stDownloadButton > button:active {
  transform: translateY(0);
}
.stButton > button[kind="primary"], .stDownloadButton > button[kind="primary"] {
  background-color: var(--accent) !important;
  border: 1px solid var(--accent) !important;
  color: #09090b !important;
  font-weight: 600 !important;
}
.stButton > button[kind="primary"]:hover, .stDownloadButton > button[kind="primary"]:hover {
  background-color: #e4e4e7 !important;
  border-color: #e4e4e7 !important;
}
.stButton > button[kind="primary"] p, .stButton > button[kind="primary"] span,
.stDownloadButton > button[kind="primary"] p, .stDownloadButton > button[kind="primary"] span {
  color: #09090b !important;
}

/* Forms, Prism Cards, Expanders, Tabs */
[data-testid="stForm"], .prism-card {
  background-color: var(--surface) !important;
  border: 1px solid var(--line) !important;
  border-radius: 14px !important;
  padding: 1.35rem !important;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.35) !important;
}
[data-testid="stExpander"] {
  background-color: var(--surface) !important;
  border: 1px solid var(--line) !important;
  border-radius: 11px !important;
  margin-bottom: 0.55rem !important;
}
[data-testid="stExpander"] summary {
  color: var(--text-2) !important;
  font-size: 0.85rem !important;
  font-weight: 500 !important;
}
.stTabs [data-baseweb="tab-list"] {
  gap: 1.2rem !important;
  border-bottom: 1px solid var(--line) !important;
  background: transparent !important;
}
.stTabs [data-baseweb="tab"] {
  background: transparent !important;
  padding: 0.5rem 0.2rem !important;
  color: var(--text-3) !important;
  font-size: 0.86rem !important;
  font-weight: 500 !important;
}
.stTabs [aria-selected="true"] {
  color: var(--text) !important;
  border-bottom: 2px solid var(--text) !important;
}

/* Metrics */
[data-testid="stMetric"] {
  background-color: var(--surface) !important;
  border: 1px solid var(--line) !important;
  border-radius: 11px !important;
  padding: 0.65rem 0.85rem !important;
}
[data-testid="stMetricLabel"] p {
  color: var(--text-3) !important;
  font-size: 0.7rem !important;
  text-transform: uppercase;
  letter-spacing: 0.08em;
}
[data-testid="stMetricValue"] {
  color: var(--text) !important;
  font-size: 1.05rem !important;
  font-weight: 600 !important;
}

/* Code Blocks */
pre, code, .stCode, [data-testid="stCode"] {
  font-family: 'JetBrains Mono', ui-monospace, SFMono-Regular, Menlo, monospace !important;
  font-size: 0.86rem !important;
}
[data-testid="stCode"] {
  background-color: #0c0c0f !important;
  border: 1px solid var(--line) !important;
  border-radius: 11px !important;
}
code {
  background-color: #1a1a22 !important;
  color: #e4e4e7 !important;
  border-radius: 5px !important;
  padding: 0.12rem 0.35rem !important;
}
pre code {
  background: transparent !important;
  padding: 0 !important;
}

/* Custom Badges & Diagnostics */
.pill {
  display: inline-block;
  font-size: 0.65rem;
  letter-spacing: 0.07em;
  text-transform: uppercase;
  font-weight: 600;
  padding: 2px 9px;
  border-radius: 99px;
  border: 1px solid var(--line-2);
  color: var(--text-2) !important;
}
.pill-ok { border-color: rgba(16, 185, 129, 0.4); color: var(--ok) !important; background: rgba(16, 185, 129, 0.06); }
.pill-warn { border-color: rgba(245, 158, 11, 0.4); color: var(--warn) !important; background: rgba(245, 158, 11, 0.06); }
.pill-bad { border-color: rgba(239, 68, 68, 0.4); color: var(--bad) !important; background: rgba(239, 68, 68, 0.06); }

.meta-line {
  color: var(--text-3) !important;
  font-size: 0.72rem !important;
  letter-spacing: 0.04em;
  margin: 0.25rem 0 0.5rem;
  font-family: 'JetBrains Mono', monospace;
}
.diag-box {
  background-color: var(--bg-elevated) !important;
  border: 1px solid var(--line) !important;
  border-radius: 10px;
  padding: 0.7rem 0.95rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.73rem;
  color: var(--text-2) !important;
  line-height: 1.6;
  margin-top: 0.65rem;
  margin-bottom: 0.35rem;
}
.diag-box b { color: var(--text) !important; }
.kv {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  font-size: 0.78rem;
  color: var(--text-2) !important;
  padding: 0.32rem 0;
  border-bottom: 1px solid var(--line);
}
.kv:last-child { border-bottom: 0; }
.kv span { color: var(--text-2) !important; }

/* Hero & Branding */
.void-hero { text-align: center; padding: 2rem 1rem 1.4rem; }
.void-gradient {
  color: #fafafa !important;
  font-weight: 700 !important;
  font-size: 2.05rem !important;
  letter-spacing: -0.032em !important;
  margin-bottom: 0.35rem;
}
.void-sub {
  font-size: 0.92rem !important;
  color: var(--text-3) !important;
  margin-bottom: 1.5rem;
  max-width: 560px;
  margin-left: auto;
  margin-right: auto;
}
.hero-mark {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 50px;
  height: 50px;
  border: 1px solid var(--line-2);
  border-radius: 14px;
  margin-bottom: 0.85rem;
  background: var(--surface);
  box-shadow: 0 4px 16px rgba(0,0,0,0.4);
}
.topbar-brand { display: flex; align-items: center; gap: 10px; margin-bottom: 14px; }
.topbar-title {
  font-size: 1rem !important;
  font-weight: 700 !important;
  letter-spacing: 0.26em !important;
  color: #fafafa !important;
}
.topbar-pill {
  font-size: 0.58rem !important;
  letter-spacing: 0.12em;
  padding: 2px 8px !important;
  border-radius: 99px;
  border: 1px solid var(--line-2) !important;
  color: var(--text-3) !important;
  font-weight: 600 !important;
}
.void-footer {
  text-align: center;
  color: var(--text-3) !important;
  font-size: 0.73rem;
  padding: 2rem 0 0.5rem;
  letter-spacing: 0.03em;
}

/* Custom Scrollbar */
::-webkit-scrollbar { width: 8px; height: 8px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb { background: #27272f; border-radius: 99px; }
::-webkit-scrollbar-thumb:hover { background: #3a3a46; }
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

ENGINES = {
    "🧠 Auto-Route (Omni Intelligence)": "auto",
    "☀️ Supernova X (Coding & Architecture)": "qwen/qwen-2.5-coder-32b-instruct",
    "🪐 Nebula Core (Deep Logic Engine)": "deepseek/deepseek-chat",
    "🌙 Void Moon (Hyper-Fast Flash)": "google/gemini-2.0-flash-001",
    "🔥 Quasar Prime (Extreme Reasoning)": "deepseek/deepseek-r1",
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
FOUNDER_BIO = sget(
    "FOUNDER_BIO",
    "14-year-old Founder & Lead Architect of VOID, student at Sunbeam School Varuna in Varanasi, "
    "creator of VoidOS, author of World Zero, and gamer (NOTREFLEXGAMING05).",
)

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
        rec = {
            "name": nm,
            "city": "Varanasi",
            "joined": now,
            "last_active": now,
            "prompts": 0,
            "memory": FOUNDER_BIO if founder else f"Verified member of VOID Studio ({nm}).",
            "recent_topics": [],
        }
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
WMO = {
    0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
    45: "Foggy", 48: "Rime fog", 51: "Light drizzle", 53: "Drizzle",
    55: "Heavy drizzle", 61: "Light rain", 63: "Moderate rain", 65: "Heavy rain",
    71: "Light snow", 73: "Snow", 75: "Heavy snow", 80: "Rain showers",
    81: "Heavy showers", 95: "Thunderstorm", 96: "Thunderstorm with hail",
}

WEATHER_WORDS = (
    "weather", "temperature", "temp", "rain", "forecast",
    "climate", "outside", "cold", "hot", "humidity", "wind", "aqi",
)


@st.cache_data(ttl=3600, show_spinner=False)
def geocode(city):
    try:
        r = http_session().get(
            GEO_URL,
            params={"name": city, "count": 1, "language": "en", "format": "json"},
            timeout=5,
        ).json()
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
        d = http_session().get(
            WEATHER_URL,
            params={
                "latitude": lat,
                "longitude": lon,
                "timezone": "auto",
                "current": "temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m",
                "daily": "temperature_2m_max,temperature_2m_min",
            },
            timeout=5,
        ).json()
        cur, day = d.get("current", {}), d.get("daily", {})
        return (
            f"[LIVE WEATHER TELEMETRY — {label}]: Condition: {WMO.get(cur.get('weather_code'), 'Partly cloudy')} | "
            f"Current Temp: {cur.get('temperature_2m')}°C (Feels like {cur.get('apparent_temperature')}°C) | "
            f"Today's High/Low: {day.get('temperature_2m_max', ['N/A'])[0]}°C / {day.get('temperature_2m_min', ['N/A'])[0]}°C | "
            f"Humidity: {cur.get('relative_humidity_2m')}% | Wind: {cur.get('wind_speed_10m')} km/h"
        )
    except Exception:
        return "[Weather feed temporarily unavailable]"


def extract_weather_city(prompt, default_city):
    m = re.search(
        r"\b(?:in|at|for|of)\s+([a-zA-Z][a-zA-Z\s]{2,26}?)(?:\s+(?:right|today|now|tomorrow|currently)\b|[?.!,]|$)",
        prompt,
        re.I,
    )
    if m:
        candidate = m.group(1).strip()
        if candidate.lower() not in ("the", "this", "my", "our", "your", "current", "live"):
            return candidate.title()
    return default_city


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


# ============================== 6. HIGH-PRECISION LIVE INTERNET RETRIEVAL ==============================
_COMMON_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36"
    ),
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.9",
}


def _clean_text(t):
    if not t:
        return ""
    text = html.unescape(str(t))
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"&nbsp;|&#160;", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _refine_search_query(raw_q):
    """Strips conversational filler so search engines return high-signal factual articles."""
    q = re.sub(r"\s+", " ", raw_q).strip()
    q = re.sub(
        r"^(?:can you|could you|please|tell me|what is|what are|who is|who are|"
        r"give me|show me|find out|search for|let me know)\s+",
        "",
        q,
        flags=re.I,
    )
    return q[:180].strip() or raw_q[:180].strip()


def _src_google_news(q, n=6):
    """Fetches real-time live news with clean headline, source, date, and snippet from Google News RSS."""
    try:
        sq = _refine_search_query(q)
        url = f"https://news.google.com/rss/search?q={urllib.parse.quote(sq)}&hl=en-IN&gl=IN&ceid=IN:en"
        r = requests.get(url, headers=_COMMON_HEADERS, timeout=6)
        if r.status_code != 200:
            return []
        root = ET.fromstring(r.content)
        items = []
        for el in root.findall(".//item")[:n]:
            title = _clean_text(el.findtext("title", ""))
            pub = _clean_text(el.findtext("pubDate", ""))
            # Trim seconds/timezone noise from RSS pubDate for cleaner token usage
            pub_short = re.sub(r"\s+\d{2}:\d{2}:\d{2}\s+GMT$", "", pub)
            source = _clean_text(el.findtext("source", ""))
            desc_raw = _clean_text(el.findtext("description", ""))
            # Avoid repeating title if description is identical to title
            snippet = ""
            if desc_raw and desc_raw.lower()[:45] != title.lower()[:45]:
                snippet = f" — {desc_raw[:280]}"
            src_tag = f" [{source}]" if source and source.lower() not in title.lower() else ""
            if title:
                items.append(f"- [LIVE NEWS · {pub_short}]{src_tag} {title}{snippet}")
        return items
    except Exception:
        return []


def _src_ddg_lite(q, n=4):
    """Scrapes DuckDuckGo Lite endpoint for clean organic web snippets without JS blocks."""
    try:
        sq = _refine_search_query(q)
        r = requests.post(
            "https://lite.duckduckgo.com/lite/",
            data={"q": sq},
            headers=_COMMON_HEADERS,
            timeout=6,
        )
        if r.status_code != 200:
            return []
        links = re.findall(
            r'<a[^>]+class="result-link"[^>]+href="([^"]+)"[^>]*>(.*?)</a>',
            r.text,
            re.S | re.I,
        )
        snippets = re.findall(
            r'<td[^>]+class="result-snippet"[^>]*>(.*?)</td>',
            r.text,
            re.S | re.I,
        )
        out = []
        for idx, (href, title) in enumerate(links[:n]):
            snip = _clean_text(snippets[idx]) if idx < len(snippets) else ""
            clean_t = _clean_text(title)
            if clean_t and snip:
                out.append(f"- [WEB RESULT] {clean_t} ({href}): {snip[:340]}")
        return out
    except Exception:
        return []


def _src_ddg_instant(q):
    """DuckDuckGo Instant Answer API for direct factual definitions and entity summaries."""
    try:
        sq = _refine_search_query(q)
        url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(sq)}&format=json&no_html=1&skip_disambig=1"
        r = requests.get(url, headers=_COMMON_HEADERS, timeout=5)
        if r.status_code == 200:
            data = r.json()
            out = []
            if data.get("AbstractText"):
                out.append(f"- [ENCYCLOPEDIA SUMMARY] {_clean_text(data['AbstractText'])} ({data.get('AbstractURL', '')})")
            if data.get("Answer"):
                out.append(f"- [INSTANT FACT] {_clean_text(data['Answer'])}")
            for t in data.get("RelatedTopics", [])[:3]:
                if isinstance(t, dict) and t.get("Text"):
                    out.append(f"- [RELATED FACT] {_clean_text(t['Text'])[:280]}")
            return out
    except Exception:
        pass
    return []


def _src_wikipedia_deep(q, n=2):
    """Wikipedia Opensearch + Summary Extracts."""
    try:
        sq = _refine_search_query(q)
        r = http_session().get(
            WIKI_URL,
            params={
                "action": "query",
                "generator": "search",
                "gsrsearch": sq,
                "gsrlimit": n,
                "prop": "extracts",
                "exintro": 1,
                "explaintext": 1,
                "exchars": 750,
                "format": "json",
            },
            headers=_COMMON_HEADERS,
            timeout=6,
        ).json()
        pages = (r.get("query", {}) or {}).get("pages", {}).values()
        return [
            f"- [WIKIPEDIA: {p.get('title')}] {_clean_text(p.get('extract', ''))[:550]}"
            for p in pages
            if p.get("extract")
        ]
    except Exception:
        return []


def _src_tavily(q, n):
    k = SEARCH_KEYS["tavily"]
    if not k:
        return []
    try:
        r = http_session().post(
            "https://api.tavily.com/search",
            json={
                "api_key": k,
                "query": q,
                "max_results": n,
                "search_depth": "advanced",
                "include_answer": True,
            },
            timeout=8,
        ).json()
        out = []
        if r.get("answer"):
            out.append(f"- [VERIFIED SYNTHESIS] {_clean_text(r['answer'])}")
        for x in r.get("results", [])[:n]:
            out.append(
                f"- [WEB SOURCE] {_clean_text(x.get('title', ''))} ({x.get('url', '')}): "
                f"{_clean_text(x.get('content', ''))[:400]}"
            )
        return out
    except Exception:
        return []


def _src_serper(q, n):
    k = SEARCH_KEYS["serper"]
    if not k:
        return []
    try:
        r = http_session().post(
            "https://google.serper.dev/search",
            json={"q": q, "num": n},
            headers={"X-API-KEY": k, "Content-Type": "application/json"},
            timeout=8,
        ).json()
        out = []
        if r.get("answerBox", {}).get("answer"):
            out.append(f"- [DIRECT ANSWER BOX] {_clean_text(r['answerBox']['answer'])}")
        for x in r.get("organic", [])[:n]:
            out.append(
                f"- [GOOGLE RESULT] {_clean_text(x.get('title', ''))} ({x.get('link', '')}): "
                f"{_clean_text(x.get('snippet', ''))}"
            )
        return out
    except Exception:
        return []


def _src_brave(q, n):
    k = SEARCH_KEYS["brave"]
    if not k:
        return []
    try:
        r = http_session().get(
            "https://api.search.brave.com/res/v1/web/search",
            params={"q": q, "count": n},
            headers={"X-Subscription-Token": k, "Accept": "application/json"},
            timeout=8,
        ).json()
        return [
            f"- [BRAVE RESULT] {_clean_text(x.get('title', ''))} ({x.get('url', '')}): "
            f"{_clean_text(x.get('description', ''))}"
            for x in (r.get("web", {}) or {}).get("results", [])[:n]
        ]
    except Exception:
        return []


@st.cache_data(ttl=600, show_spinner=False, max_entries=256)
def web_search_bundle(query, n=5):
    """Executes all free + configured search feeds in parallel and consolidates clean, high-signal snippets."""
    q = re.sub(r"\s+", " ", query).strip()[:200]
    if len(q) < 3:
        return "", []

    funcs = [
        lambda: _src_tavily(q, n),
        lambda: _src_serper(q, n),
        lambda: _src_brave(q, n),
        lambda: _src_google_news(q, n + 1),
        lambda: _src_ddg_lite(q, n),
        lambda: _src_ddg_instant(q),
        lambda: _src_wikipedia_deep(q, 2),
    ]

    chunks, urls = [], []
    with ThreadPoolExecutor(max_workers=7) as ex:
        for res in ex.map(lambda f: f(), funcs):
            chunks.extend(res or [])

    for line in chunks:
        m = re.search(r"\((https?://[^\s\)]+)\)", line)
        if m and m.group(1) not in urls:
            urls.append(m.group(1))

    seen, dedup = set(), []
    for line in chunks:
        cleaned = line.strip()
        if not cleaned:
            continue
        sig = re.sub(r"\W+", "", cleaned.lower())[:75]
        if sig in seen:
            continue
        seen.add(sig)
        dedup.append(cleaned)

    return "\n".join(dedup[:16]), urls[:6]


@st.cache_data(ttl=1800, show_spinner=False, max_entries=96)
def read_page(url, limit=3500):
    try:
        r = http_session().get(
            "https://r.jina.ai/" + url,
            timeout=12,
            headers={"User-Agent": f"VOIDCore/{APP_VERSION}"},
        )
        if r.status_code == 200 and len(r.text) > 200:
            return re.sub(r"\n{3,}", "\n\n", r.text)[:limit]
    except Exception:
        pass
    return ""


# ---------- Exact Math Engine ----------
_MATH_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.Mod: operator.mod,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
    ast.FloorDiv: operator.floordiv,
}


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
            res.append(f"[EXACT VERIFIED CALCULATION] {e} = {round(v, 8) if isinstance(v, float) else v}")
        except Exception:
            continue
    pct = re.findall(r"(\d+(?:\.\d+)?)\s*(?:%|percent)\s*of\s*(\d+(?:\.\d+)?)", prompt, re.I)
    for a, b in pct[:3]:
        res.append(f"[EXACT VERIFIED CALCULATION] {a}% of {b} = {round(float(a) * float(b) / 100, 8)}")
    return "\n".join(res[:4])


def needs_search(prompt, depth="Standard"):
    """Triggers live search for any factual, news, entity, or real-world query."""
    if depth == "Off":
        return False
    p = prompt.lower().strip()
    if len(p) < 4:
        return False
    if p in ("hi", "hello", "hey", "yo", "thanks", "thank you", "ok", "okay"):
        return False
    if p.startswith(("write a poem", "tell me a joke", "make a game", "write a story")) and not any(
        k in p for k in ("news", "who", "when", "today", "current", "latest", "real")
    ):
        return False
    return depth in ("Standard", "Deep")


def grounding(prompt, depth="Standard", default_city="Varanasi", diag=None):
    """Builds the authoritative real-time context block (Weather + Math + Web + News + Deep Page Reads)."""
    parts = []
    calc = exact_math(prompt)
    if calc:
        parts.append(calc)

    p_low = prompt.lower()
    if any(w in p_low for w in WEATHER_WORDS):
        target_city = extract_weather_city(prompt, default_city)
        parts.append(fetch_live_weather(target_city))

    hits, urls, pages = 0, [], 0
    if needs_search(prompt, depth):
        text, urls = web_search_bundle(prompt, 6 if depth == "Deep" else 5)
        if text:
            hits = len(text.splitlines())
            parts.append("=== VERIFIED LIVE INTERNET & NEWS INTELLIGENCE (Retrieved Just Now) ===\n" + text)
        if depth == "Deep" and urls:
            for u in urls[:2]:
                body = read_page(u, 3000)
                if body:
                    pages += 1
                    parts.append(f"[LIVE PAGE EXCERPT — {u}]\n{body}")

    if diag is not None:
        diag.update(search_hits=hits, sources=urls[:4], pages_read=pages, math=bool(calc))
    return "\n\n".join(parts)


# ============================== 7. MULTI-PROVIDER RESILIENCY ==============================
class EngineError(Exception):
    pass


AUTO_ROUTES = {
    "code": ["qwen/qwen-2.5-coder-32b-instruct", "deepseek/deepseek-chat"],
    "math": ["deepseek/deepseek-r1", "deepseek/deepseek-chat"],
    "fresh": ["google/gemini-2.0-flash-001", "deepseek/deepseek-chat"],
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

_PROVIDER_LABEL = {
    "openrouter": "Cosmic Relay",
    "openai": "Nebula Relay",
    "groq": "Pulsar Relay",
    "google": "Quasar Relay",
}


def intent_of(prompt):
    p = prompt.lower()
    if any(w in p for w in ("code", "python", "js", "javascript", "html", "function", "bug", "sql", "react", "css")):
        return "code"
    if any(w in p for w in ("solve", "calculate", "equation", "math", "integral", "derivative", "probability")):
        return "math"
    if any(
        w in p
        for w in (
            "today", "news", "current", "latest", "who is", "who won",
            "weather", "match", "score", "price", "headline", "happening",
        )
    ):
        return "fresh"
    if any(w in p for w in ("pdf", "slides", "notes", "presentation", "document", "cheat sheet", "study guide")):
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


def _prepare_messages_with_grounding(msgs, live_intel):
    """Attaches live telemetry directly to the final user turn so models cannot ignore it."""
    trimmed = _trim(msgs)
    if not trimmed or not live_intel.strip():
        return trimmed
    augmented = [dict(m) for m in trimmed]
    last_msg = augmented[-1]
    if last_msg.get("role") == "user":
        last_msg["content"] = (
            f"{last_msg['content']}\n\n"
            f"--- [VERIFIED REAL-TIME CONTEXT — USE THESE SPECIFIC DETAILS, NAMES, DATES & NUMBERS] ---\n"
            f"{live_intel}"
        )
    return augmented


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
            "generationConfig": {"temperature": max(0.0, min(temp, 1.2)), "maxOutputTokens": tokens},
        }
        r = http_session().post(url, json=payload, timeout=90)
        if r.status_code != 200:
            raise EngineError(f"{_PROVIDER_LABEL[provider]} HTTP {r.status_code}: {r.text[:140]}")
        try:
            return r.json()["candidates"][0]["content"]["parts"][0]["text"]
        except Exception:
            raise EngineError("Empty response from Quasar Relay")

    url = {"openrouter": OPENROUTER_URL, "openai": OPENAI_URL, "groq": GROQ_URL}[provider]
    payload = {
        "model": model,
        "temperature": max(0.0, min(temp, 1.2)),
        "max_tokens": tokens,
        "messages": [{"role": "system", "content": system}] + _trim(msgs),
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
        "messages": [{"role": "system", "content": system}] + _trim(msgs),
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
        return None, "No engine key configured. Add OPE
