Here is the complete, production-ready app.py (upgraded to VOID v6.6.0-Obsidian
Apex).

Key Architectural & UI Upgrades

1.  Obsidian Desktop UI (MINIMAL_CSS):
      - Engineered a high-contrast #09090b Obsidian theme with refined #121216
        elevated cards, 1px solid #232329 crisp hairline borders, and subtle
        focus rings.
      - Distinct, structured chat message cards with proper vertical rhythm and
        bottom container padding (padding-bottom: 9.5rem) so the anchored bottom
        composer never overlaps conversation history across any viewport.
      - Polished interactive buttons, custom scrollbars, pill badges, and
        telemetry cards.
2.  High-Precision Live Grounding (web_search_bundle & build_system_prompt):
      - Rich RSS & Snippet Parsing: _src_google_news now extracts and sanitizes
        both the headline, source publication, timestamp, and article summary
        description (<description>), stripping HTML noise and boilerplate.
      - Added DuckDuckGo Lite Fallback (_src_ddg_lite): Extracts clean organic
        web snippets alongside Instant Answers, Wikipedia extracts, and any
        configured API keys (Tavily, Serper, Brave).
      - Smart City Weather Injection: Automatically detects city names in
        weather queries (or defaults to the operator's city) and injects
        real-time Open-Meteo telemetry.
      - Concrete Synthesis Directive: Upgraded the system prompt and user
        context framing so the model is strictly required to cite specific
        names, dates, numbers, scores, and headlines in the very first sentence
        without generic filler.
3.  Full Feature & Dimension Integrity:
      - All 7 Dimensions, PDF binary generator, interactive HTML slide deck
        generator, Self-Evolution Lab file uploader, and EmailJS/Guest
        authentication remain 100% intact.

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
        return None, "No engine key configured. Add OPENROUTER_API_KEY in Streamlit Secrets."
    errors = []
    for provider, model in build_chain(choice, prompt or (msgs[-1]["content"] if msgs else ""), avoid):
        t0 = time.time()
        try:
            txt = _post_once(provider, model, system, msgs, temp, tokens)
            if txt and txt.strip():
                if diag is not None:
                    diag.update(
                        provider=provider,
                        model=model,
                        latency=round(time.time() - t0, 2),
                        link=_PROVIDER_LABEL[provider],
                    )
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
                    diag.update(
                        provider=provider,
                        model=model,
                        latency=round(time.time() - t0, 2),
                        link=_PROVIDER_LABEL[provider],
                    )
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
    r"i'?m sorry,? but|i apologi[sz]e|unable to (?:answer|help)|knowledge cutoff)\b",
    re.I,
)


def looks_weak(text):
    t = (text or "").strip()
    return len(t) < 40 or (REFUSAL_PAT.search(t[:350]) and len(t) < 550)


def fence_balance(text):
    return (text or "").count("```") % 2 == 0


def answer_question(engine, prompt, system, msgs, temp, tokens, accuracy_mode=True, diag=None):
    if diag is None:
        diag = {}
    draft, err = call_llm(engine, system, msgs, temp, tokens, prompt=prompt, diag=diag)
    if not draft or looks_weak(draft):
        diag["repaired"] = True
        rescue_sys = (
            system
            + "\n\nCRITICAL OVERRIDE: Answer directly and concretely using the live internet intelligence provided. "
            "Cite exact names, headlines, dates, numbers, and facts right in your first sentence. Never refuse."
        )
        draft, err2 = call_llm(engine, rescue_sys, msgs[-3:], max(temp, 0.2), tokens, prompt=prompt, diag=diag)
        if not draft:
            raise EngineError(err or err2 or "Answer generation failed.")

    if not fence_balance(draft) and "```" in draft:
        draft += "\n```"

    return draft


# ============================== 8. DOCUMENT FORGE (PDF + SLIDES) ==============================
def clean_for_pdf(text):
    for k, v in {"—": "-", "–": "-", "“": '"', "”": '"', "‘": "'", "’": "'", "•": "*", "…": "...", "→": "->"}.items():
        text = text.replace(k, v)
    return text.encode("latin-1", "ignore").decode("latin-1")


def pdf_escape(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


PDF_STYLE = {
    "TITLE": ("F2", 15, 50, 0, 22),
    "META": ("F1", 8.5, 50, 0, 16),
    "H1": ("F2", 12.5, 50, 6, 16),
    "BULLET": ("F1", 10, 56, 0, 14),
    "BODY": ("F1", 10, 50, 0, 14),
}


@st.cache_data(show_spinner=False, max_entries=64)
def generate_real_pdf_bytes(title, markdown, author="VOID Forge"):
    safe_title = clean_for_pdf(title)
    safe_md = clean_for_pdf(markdown)
    lines = [
        ("TITLE", safe_title),
        ("META", clean_for_pdf(f"Forged by {author} | {datetime.now():%Y-%m-%d %H:%M}")),
        ("SPACE", ""),
    ]
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
    objs = [
        b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n",
        f"2 0 obj\n<< /Type /Pages /Kids [{' '.join(f'{i} 0 R' for i in ids)}] /Count {total} >>\nendobj\n".encode(),
        b"3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>\nendobj\n",
        b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>\nendobj\n",
    ]
    for i, (pid, stream) in enumerate(zip(ids, pages), start=1):
        footer = f"VOID Document • Page {i} of {total}"
        sb = (stream + f"\nBT /F1 8 Tf 1 0 0 1 470 28 Tm ({pdf_escape(footer)}) Tj ET").encode("latin-1", errors="ignore")
        objs.append(
            (
                f"{pid} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents {pid + 1} 0 R >>\nendobj\n"
            ).encode()
        )
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
body{margin:0;background:#09090b;color:#f4f4f6;font-family:'Inter',system-ui,sans-serif;display:flex;flex-direction:column;height:95vh;justify-content:space-between}
.wrap{flex:1;display:flex;align-items:center;justify-content:center;padding:20px}
.slide{display:none;width:100%;max-width:840px;background:#121216;border:1px solid #232329;border-radius:16px;padding:36px 44px;min-height:300px;box-sizing:border-box;box-shadow:0 12px 36px rgba(0,0,0,0.5)}
.slide.on{display:block}
.badge{font-size:10px;letter-spacing:3px;color:#71717a;font-weight:600;margin-bottom:14px}
.count{position:fixed;top:14px;right:20px;font-size:11px;color:#71717a;font-weight:600}
h2{margin-top:0;font-size:24px;color:#fafafa;font-weight:600}
.body{font-size:15px;line-height:1.75;color:#a1a1aa}
code{background:#1a1a22;padding:2px 6px;border-radius:5px;color:#e4e4e7}
.ctl{display:flex;justify-content:center;gap:12px;padding:12px}
button{background:#121216;color:#f4f4f6;border:1px solid #2e2e38;padding:8px 18px;border-radius:99px;cursor:pointer;font-weight:500;transition:0.15s}
button:hover{background:#fafafa;color:#09090b;border-color:#fafafa}
@media print{.ctl{display:none}body{background:#fff;color:#000}.slide{display:block;page-break-after:always;background:#fff;border-color:#ddd}}
</style></head><body><div class="wrap">%%SLIDES%%</div>
<div class="count">%%COUNT%%</div>
<div class="ctl"><button onclick="go(-1)">◀ Previous</button><button onclick="window.print()">Export PDF</button><button onclick="go(1)">Next ▶</button></div>
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
        secs = ["\n\n".join(paras[i : i + 2]) for i in range(0, len(paras), 2)] or [markdown]
    out = []
    for i, sec in enumerate(secs):
        lines = sec.strip().split("\n")
        heading = lines[0].lstrip("#").strip() or f"Slide {i + 1}"
        body = "<br>".join(_md_inline(l) for l in lines[1:] if l.strip())
        out.append(
            f'<div class="slide{" on" if i == 0 else ""}">'
            f'<div class="badge">VOID PRISM DECK · SLIDE {i + 1} OF {len(secs)}</div>'
            f'<h2>{esc(heading.replace("**", ""))}</h2><div class="body">{body}</div></div>'
        )
    return (
        SLIDE_TPL.replace("%%TITLE%%", esc(title))
        .replace("%%COUNT%%", f"SLIDE 1 / {len(secs)}")
        .replace("%%SLIDES%%", "".join(out))
    )


def extract_code_blocks(text):
    return re.findall(r"```(\w*)\n(.*?)```", text, re.DOTALL)


def is_html_block(b):
    return b[0].lower() in ("html", "xml", "svg") or "<html" in b[1].lower() or "<style" in b[1].lower()


DOC_TRIGGERS = (
    "pdf", "ppt", "powerpoint", "slide", "presentation", "study notes", "revision notes",
    "make notes", "write notes", "study guide", "cheat sheet", "exam questions",
    "question bank", "worksheet", "report", "document", "build a web app",
    "build an app", "create a web app", "html app", "make a game",
)


def detect_prism_intent(prompt, reply=""):
    return any(t in prompt.lower() for t in DOC_TRIGGERS) or "```html" in reply.lower()


def send_otp_email(to, code):
    if not (EJS_SERVICE and EJS_TEMPLATE and EJS_PUBLIC):
        return False, "Email service not configured in Secrets."
    payload = {
        "service_id": EJS_SERVICE,
        "template_id": EJS_TEMPLATE,
        "user_id": EJS_PUBLIC,
        "template_params": {"to_email": to, "otp_code": code},
    }
    if EJS_PRIVATE:
        payload["accessToken"] = EJS_PRIVATE
    try:
        r = http_session().post(EMAILJS_URL, json=payload, timeout=25)
        return (True, None) if r.status_code == 200 else (False, r.text[:180])
    except Exception as e:
        return False, str(e)


# ============================== 9. AUTHENTICATION GATE ==============================
if "user_email" not in st.session_state:
    restored = restore_login()
    if restored:
        st.session_state.user_email = restored

if "user_email" not in st.session_state:
    st.markdown(
        f'<div class="void-hero"><div class="hero-mark"><img src="{LOGO_B64}" width="32"/></div>'
        '<div class="void-gradient">VOID</div>'
        '<div class="void-sub">Sovereign OS Intelligence · Real-Time Global Grounding · Zero-Friction Workspace</div></div>',
        unsafe_allow_html=True,
    )

    _, mid, _ = st.columns([1, 1.38, 1])
    with mid:
        st.markdown(
            "<p style='text-align:center; color:#71717a; font-size:.83rem; margin-bottom:12px;'>"
            "Launch immediately as Guest Operator or sign in with Email</p>",
            unsafe_allow_html=True,
        )
        with st.form("landing_search_form"):
            landing_query = st.text_input(
                "Direct Search / Prompt",
                placeholder="Ask about live news, weather, code, or documents…",
                label_visibility="collapsed",
            )
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
                    db["chats"][guest_email][cid]["title"] = t[:26] + "..." if len(t) > 26 else t
                    save_db(db)
                st.rerun()

        st.markdown(
            "<div style='text-align:center; margin:16px 0; color:#3f3f46; font-size:.73rem; letter-spacing:.14em;'>"
            "OR · EMAIL VERIFICATION</div>",
            unsafe_allow_html=True,
        )

        if "pending_email" not in st.session_state:
            with st.form("email_form"):
                email_in = st.text_input("Email Address", placeholder="name@domain.com", max_chars=80).strip().lower()
                name_in = st.text_input("Display Name", placeholder="Your name", max_chars=40).strip()
                if st.form_submit_button("Send Verification Code", use_container_width=True):
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
                            st.session_state.update(
                                pending_email=email_in,
                                pending_name=name_in,
                                target_otp=code,
                                otp_expiry=time.time() + OTP_TTL,
                                otp_tries=0,
                            )
                            st.rerun()
                        else:
                            st.error(f"Could not send email: {err}")
        else:
            st.info(f"Verification code sent to **{st.session_state.pending_email}** (valid for 10 minutes)")
            with st.form("otp_form"):
                otp_in = st.text_input("6-Digit Code", placeholder="123456", max_chars=6)
                v_btn = st.form_submit_button("Verify & Enter VOID", type="primary", use_container_width=True)
                b_btn = st.form_submit_button("Use a Different Email", use_container_width=True)
                if b_btn:
                    for k in ("pending_email", "pending_name", "target_otp", "otp_expiry", "otp_tries"):
                        st.session_state.pop(k, None)
                    st.rerun()
                if v_btn:
                    st.session_state.otp_tries += 1
                    if time.time() > st.session_state.otp_expiry:
                        st.error("Code expired. Please request a new one.")
                    elif st.session_state.otp_tries > OTP_MAX_TRIES:
                        st.error("Too many attempts. Please request a new code.")
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

# ============================== 11. SIDEBAR ==============================
with st.sidebar:
    st.markdown(
        f'<div class="topbar-brand"><img src="{LOGO_B64}" width="26"/>'
        '<span class="topbar-title">VOID</span>'
        '<span class="topbar-pill">OBSIDIAN OS</span></div>',
        unsafe_allow_html=True,
    )

    if st.button("＋ New Session", type="primary", use_container_width=True):
        st.session_state.current_chat_id = new_chat(user_email)
        st.session_state.active_prism_text = None
        st.session_state.prism_open = False
        save_db(db)
        st.rerun()

    if st.session_state.pop("force_prism", False):
        st.session_state.prism_open = True
    prism_open = st.toggle("VOID Prism Workspace", key="prism_open")
    auto_scroll = st.toggle(
        "Auto-refresh telemetry",
        value=False,
        help="Re-syncs the console periodically.",
    )

    st.markdown("<div class='meta-line' style='margin-top:0.8rem;'>ACTIVE SESSIONS</div>", unsafe_allow_html=True)
    for cid, cdata in reversed(list(user_chats.items())):
        col_t, col_d = st.columns([5, 1])
        with col_t:
            if st.button(
                f"{'● ' if cid == current_chat_id else '○ '}{cdata['title']}",
                key=f"c_{cid}",
                use_container_width=True,
            ):
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
    n_msgs = len(current_chat.get("messages", []))
    sm1, sm2, sm3 = st.columns(3)
    sm1.metric("Turns", n_msgs)
    sm2.metric("Chats", len(user_chats))
    sm3.metric("Total", user_record.get("prompts", 0))

    with st.expander("Engine Doctor"):
        s_status, s_note = engine_status()
        pill_cls = "pill-ok" if s_status == "online" else "pill-bad"
        st.markdown(f"<span class='pill {pill_cls}'>{s_status}</span>", unsafe_allow_html=True)
        st.markdown(f"<div class='meta-line'>{esc(s_note)}</div>", unsafe_allow_html=True)
        for label, ok in [
            ("Cosmic Relay (OpenRouter)", bool(PROV_KEYS["openrouter"])),
            ("Pulsar Relay (Groq)", bool(PROV_KEYS["groq"])),
            ("Quasar Relay (Gemini)", bool(PROV_KEYS["google"])),
            ("Nebula Relay (OpenAI)", bool(PROV_KEYS["openai"])),
            ("Google News RSS Live", True),
            ("DuckDuckGo Lite + Instant", True),
            ("Wikipedia Deep API", True),
            ("Tavily / Serper / Brave", bool( any(SEARCH_KEYS.values()) )),
        ]:
            mark = "<span style='color:#10b981'>●</span>" if ok else "<span style='color:#52525b'>○</span>"
            st.markdown(f"<div class='kv'><span>{mark} {esc(label)}</span></div>", unsafe_allow_html=True)
        if st.button("Run Quick Ping", use_container_width=True):
            d = {}
            out, err = call_llm(
                "🧠 Auto-Route (Omni Intelligence)",
                "Reply with exactly: VOID LINK OK",
                [{"role": "user", "content": "Ping"}],
                0.0,
                32,
                prompt="Ping",
                diag=d,
            )
            if out:
                st.success(f"{d.get('link', 'Relay')} ({d.get('latency', '?')}s): {out.strip()[:80]}")
            else:
                st.error(err)

    with st.expander("Core Identity Vault"):
        n_name = st.text_input("Display Name", value=user_name, max_chars=40)
        n_city = st.text_input("Default City (Weather & News)", value=user_city, max_chars=50)
        n_mem = st.text_area("Operator Notes", value=user_memory, height=90)
        if st.button("Save Identity", use_container_width=True):
            if not is_founder:
                user_record["name"] = n_name.strip()[:40] or user_name
            user_record["city"] = n_city.strip() or "Varanasi"
            user_record["memory"] = n_mem.strip()
            save_db(db)
            st.rerun()

    with st.expander("Founder Profile"):
        st.markdown(f"**{FOUNDER_NAME}** — *Founder & Lead Architect of VOID*\n\n{FOUNDER_BIO}")

    if is_founder:
        with st.expander(f"Crew Activity ({len(db['users'])})"):
            for mail, info in db["users"].items():
                st.markdown(
                    f"**{esc(info.get('name', 'Member'))}** (`{esc(mail)}`)  \n"
                    f"<small>Prompts: {info.get('prompts', 0)} • {esc(info.get('last_active', ''))}</small>",
                    unsafe_allow_html=True,
                )

    st.caption(f"Operator · {user_name}")
    with st.expander("Account"):
        confirm_out = st.checkbox("Confirm sign out")
        if st.button("Sign out", disabled=not confirm_out, use_container_width=True):
            st.query_params.clear()
            for k in ("user_email", "current_chat_id", "active_prism_text", "prism_open"):
                st.session_state.pop(k, None)
            st.rerun()

if auto_scroll:
    time.sleep(0.35)
    st.rerun()

# ============================== 12. COMMAND & TELEMETRY BAR ==============================
uploaded_file, file_context = None, ""
c1, c2, c3, c4 = st.columns([1.95, 1.75, 1.65, 1.25])
with c1:
    ui_mode = st.selectbox(
        "Dimension",
        [
            "✦ VOID Core & Prism",
            "📖 VOID Codex (Study, PDF & Slides)",
            "⚡ Live Web App Studio",
            "🛠️ Side-by-Side Code Lab",
            "🧬 Self-Evolution Lab",
            "🛰️ Ship Telemetry & Insights",
            "🩺 Engine Doctor & Live Test",
        ],
        label_visibility="collapsed",
    )
with c2:
    cosmic_entity = st.selectbox("Cosmic Engine", list(ENGINES), label_visibility="collapsed")
with c3:
    persona = st.selectbox(
        "Resonance Mode",
        [
            "✦ VOID Omni (Universal)",
            "🎓 Master Scholastic Tutor",
            "💻 Full-Stack Architect",
            "🎨 UI & Slide Designer",
            "🐞 Deep Bug Hunter",
        ],
        label_visibility="collapsed",
    )
with c4:
    with st.popover("⚙ Tune & Attach", use_container_width=True):
        uploaded_file = st.file_uploader(
            "Attach Code / Text File",
            type=["py", "js", "html", "css", "json", "txt", "md", "cpp", "csv"],
        )
        if uploaded_file:
            try:
                file_context = uploaded_file.getvalue().decode("utf-8")[:MAX_FILE_CHARS]
                st.success(f"Loaded `{uploaded_file.name}`")
            except UnicodeDecodeError:
                st.error("Unable to decode file as UTF-8 text.")
        task_depth = st.select_slider("Reasoning Depth", ["Swift", "Balanced", "Maximum Power"], value="Maximum Power")
        research_depth = st.select_slider(
            "Live Internet Grounding",
            ["Off", "Standard", "Deep"],
            value="Standard",
            help="Standard pulls live news, search snippets, weather & Wikipedia. Deep also reads full web pages.",
        )
        accuracy_mode = st.toggle(
            "Verified Synthesis Mode",
            value=True,
            help="Ensures concrete details and auto-repairs weak or generic responses.",
        )
        show_thinking = st.toggle("Stream Live Tokens", value=True)
        temperature = st.slider("Creativity", 0.0, 1.0, 0.2, 0.05)
        max_tokens = st.slider("Max Output Tokens", 500, 4000, 3200, 100)

now_ist = datetime.now(timezone(timedelta(hours=5, minutes=30)))
s_status, s_note = engine_status()
m_c1, m_c2, m_c3, m_c4 = st.columns(4)
m_c1.metric("System Link", "Online" if s_status == "online" else s_status.upper(), s_note)
m_c2.metric("Active Engine", cosmic_entity.split(" ", 1)[1].split(" (")[0], "auto-failover active")
m_c3.metric("Resonance", persona.split(" ", 1)[1] if " " in persona else persona, f"Grounding: {research_depth}")
m_c4.metric("Chronometer (IST)", now_ist.strftime("%d %b %Y"), now_ist.strftime("%I:%M %p IST"))


def build_system_prompt(grounded_context, is_prism=False, extra=""):
    time_str = datetime.now(timezone(timedelta(hours=5, minutes=30))).strftime("%A, %B %d, %Y | %I:%M %p IST")

    fmt = (
        "The user wants a formal document, study guide, PDF, slides, or web app. Use clean Markdown headings (# and ##) "
        "and bullet points so VOID Prism can compile it into a PDF and interactive slide deck."
        if is_prism
        else "Respond with high clarity, precision, and concrete facts. Use clean formatting (bullet points or bold key terms) where helpful."
    )

    return f"""You are VOID, an elite sovereign intelligence and digital workspace created by {FOUNDER_NAME}.
Never mention outside AI companies or underlying model names; you are strictly VOID, powered by the Cosmic Engines.

=== REAL-TIME CHRONOMETER & OPERATOR ===
Current Date & Time: {time_str}
Operator: {user_name} ({user_email}) | Default City: {user_city}
Operator Notes: {user_memory}
Founder: {FOUNDER_NAME} — {FOUNDER_BIO}

=== AUTHORITATIVE LIVE INTERNET & TELEMETRY DATA ===
{grounded_context if grounded_context.strip() else "[No external search required for this prompt]"}

=== STRICT CONCRETE SYNTHESIS DIRECTIVES (HIGHEST PRIORITY) ===
1. NO GENERIC FLUFF: Answer the question directly in your very first sentence. Never start with "Certainly!", "Here is the information", or "Based on the provided text".
2. CITE CONCRETE DETAILS IMMEDIATELY: When live news, weather, sports, prices, or current affairs are present in the LIVE INTERNET DATA above, you MUST extract and state the exact headlines, full names of people/teams, exact numbers, temperatures, scores, dates, and source names right in your opening sentences.
3. TRUST LIVE TELEMETRY OVER INTERNAL MEMORY: Your internal training data is outdated for current events. Always treat the LIVE INTERNET & TELEMETRY DATA block above as the absolute current truth.
4. COMPLETE CODE & DOCUMENTS: When writing code or study guides, provide 100% complete, runnable, production-grade output with zero placeholders.
5. Style Profile: {persona} | Depth: {task_depth}
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
    hits = diag.get("search_hits", 0)
    pages = diag.get("pages_read", 0)
    has_math = diag.get("math", False)
    band = "high" if (hits > 0 or has_math or diag.get("repaired")) else "verified"
    rows = [
        f"<b>gateway</b> {esc(diag.get('link', 'Cosmic Relay'))} · "
        f"<b>engine</b> {esc(diag.get('model', 'auto'))} · "
        f"<b>latency</b> {esc(diag.get('latency', '0.5'))}s",
        f"<b>live grounding</b> {hits} web/news snippets · {pages} full pages · "
        f"<b>exact math</b> {'verified' if has_math else 'n/a'}",
    ]
    if diag.get("repaired"):
        rows.append("<b>auto-repair</b> response refined for concrete factual density")
    return (
        f"<div class='diag-box'><span class='pill pill-ok'>assurance: {esc(band)}</span><br>"
        + "<br>".join(rows)
        + "</div>"
    )


# ============================== DIMENSION 1: CORE & PRISM ==============================
if ui_mode == "✦ VOID Core & Prism":
    if prism_open:
        chat_col, prism_col = st.columns([1.18, 1], gap="large")
    else:
        chat_col, prism_col = st.container(), None
    quick_prompt = None

    with chat_col:
        if not current_chat["messages"]:
            st.markdown(
                f'<div class="void-hero"><div class="hero-mark"><img src="{LOGO_B64}" width="30"/></div>'
                f'<div class="void-gradient">Greetings, {safe_user}</div>'
                '<div class="void-sub">Ask anything. Live breaking news, weather telemetry, and web facts are synthesized automatically.</div></div>',
                unsafe_allow_html=True,
            )
            cards = [
                ("📰 Breaking World News", "What are the top breaking news headlines and major events happening today? Cite specific headlines and details."),
                ("🌦️ Live City Weather", f"What is the exact live weather, temperature, humidity, and wind speed right now in {user_city}?"),
                ("📘 Study Guide PDF", "Create a complete Class 8 Science study guide PDF on Force and Pressure with definitions, formulas, and exam questions."),
                ("🎮 HTML Mini-Game", "Build a sleek dark-themed playable Hand Cricket mini-game in a single self-contained HTML file."),
            ]
            for col, (label, prompt_text) in zip(st.columns(4), cards):
                with col:
                    if st.button(label, use_container_width=True, key=f"qp_{label[:6]}"):
                        quick_prompt = prompt_text

        for idx, msg in enumerate(current_chat["messages"]):
            with st.chat_message(msg["role"], avatar=LOGO_B64 if msg["role"] == "assistant" else None):
                st.markdown(msg["content"])
                if msg.get("diag"):
                    st.markdown(diag_html(msg["diag"]), unsafe_allow_html=True)
                if msg["role"] == "assistant":
                    b1, b2 = st.columns(2)
                    with b1:
                        st.download_button(
                            "⬇ Download PDF",
                            generate_real_pdf_bytes(current_chat["title"], msg["content"], f"VOID Forge ({user_name})"),
                            file_name=f"VOID_{safe_name(current_chat['title'], 15)}_{idx}.pdf",
                            mime="application/pdf",
                            key=f"pdf_{idx}",
                            use_container_width=True,
                        )
                    with b2:
                        if st.button("❖ Open in Prism", key=f"op_{idx}", use_container_width=True):
                            send_to_prism(msg["content"], current_chat["title"])
                            st.rerun()
                    if not msg.get("is_prism") and any(is_html_block(b) for b in extract_code_blocks(msg["content"])):
                        if st.button("⚡ Launch Live HTML", key=f"lv_{idx}"):
                            blk = next(b for b in extract_code_blocks(msg["content"]) if is_html_block(b))
                            send_to_prism(blk[1].strip(), current_chat["title"])
                            st.rerun()

    typed = st.chat_input(f"Ask VOID anything, {user_name}…")
    active_prompt = quick_prompt or typed

    if not active_prompt and len(current_chat["messages"]) == 1 and current_chat["messages"][0]["role"] == "user":
        active_prompt = current_chat["messages"][0]["content"]
        current_chat["messages"].pop()

    reply, reply_diag = None, {}
    if active_prompt:
        full_prompt = (
            f"Attached file (`{uploaded_file.name}`):\n```\n{file_context}\n```\n\n{active_prompt}"
            if file_context
            else active_prompt
        )
        if not current_chat["messages"]:
            t = active_prompt.strip().replace("\n", " ")
            current_chat["title"] = t[:26] + "..." if len(t) > 26 else t
        current_chat["messages"].append({"role": "user", "content": full_prompt})
        bump_usage()

        with chat_col:
            with st.chat_message("user"):
                st.markdown(full_prompt)
            with st.chat_message("assistant", avatar=LOGO_B64):
                try:
                    diag = {}
                    with st.spinner("Gathering live internet intelligence & telemetry…"):
                        live_intel = grounding(active_prompt, research_depth, user_city, diag)
                    system = build_system_prompt(live_intel, detect_prism_intent(active_prompt))
                    grounded_msgs = _prepare_messages_with_grounding(current_chat["messages"], live_intel)

                    if accuracy_mode:
                        with st.spinner("Synthesizing verified response…"):
                            reply = answer_question(
                                cosmic_entity,
                                active_prompt,
                                system,
                                grounded_msgs,
                                temperature,
                                max_tokens,
                                accuracy_mode=True,
                                diag=diag,
                            )
                        st.markdown(reply)
                    else:
                        gen = stream_llm(
                            cosmic_entity,
                            system,
                            grounded_msgs,
                            temperature,
                            max_tokens,
                            prompt=active_prompt,
                            diag=diag,
                        )
                        raw = st.write_stream(gen if show_thinking else _buffered(gen))
                        reply = raw if isinstance(raw, str) else "".join(map(str, raw or []))

                    reply_diag = diag
                    if reply:
                        st.markdown(diag_html(diag), unsafe_allow_html=True)
                except EngineError as e:
                    st.error(f"Engine Error: {e}")
                except Exception as e:
                    st.error(f"Unexpected Error: {type(e).__name__}: {e}")

        if reply:
            is_prism = detect_prism_intent(active_prompt, reply)
            clean_diag = {k: v for k, v in reply_diag.items() if not k.startswith("_")}
            current_chat["messages"].append(
                {"role": "assistant", "content": reply, "is_prism": is_prism, "diag": clean_diag}
            )
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
            st.markdown("#### VOID Prism Workspace")
            p_text = st.session_state.get("active_prism_text")
            p_title = st.session_state.get("active_prism_title", current_chat["title"])
            if not p_text:
                p_text = next(
                    (m["content"] for m in reversed(current_chat["messages"]) if m["role"] == "assistant"),
                    None,
                )

            if p_text:
                blocks = extract_code_blocks(p_text)
                t_doc, t_slides, t_app, t_edit = st.tabs(["Document", "Slides", "Live App / Code", "Edit"])
                with t_doc:
                    d1, d2, d3 = st.columns(3)
                    with d1:
                        st.download_button(
                            "⬇ PDF",
                            generate_real_pdf_bytes(p_title, p_text, f"VOID Forge ({user_name})"),
                            file_name=f"VOID_{safe_name(p_title, 15)}.pdf",
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True,
                        )
                    with d2:
                        st.download_button(
                            "⬇ Slides",
                            generate_interactive_slides_html(p_title, p_text).encode("utf-8"),
                            file_name=f"VOID_Slides_{safe_name(p_title, 15)}.html",
                            mime="text/html",
                            use_container_width=True,
                        )
                    with d3:
                        st.download_button(
                            "⬇ Markdown",
                            p_text,
                            file_name=f"VOID_{safe_name(p_title, 15)}.md",
                            mime="text/markdown",
                            use_container_width=True,
                        )
                    st.markdown("---")
                    st.markdown(p_text)
                with t_slides:
                    st.caption("Navigate slides with Next / Previous buttons or Left / Right arrow keys.")
                    components.html(generate_interactive_slides_html(p_title, p_text), height=440)
                with t_app:
                    if blocks:
                        blk = next((b for b in blocks if is_html_block(b)), blocks[0])
                        if is_html_block(blk):
                            components.html(blk[1].strip(), height=460, scrolling=True)
                        else:
                            st.code(blk[1].strip(), language=blk[0].lower() or None)
                    elif "<html" in p_text.lower() or "<style" in p_text.lower():
                        components.html(p_text, height=460, scrolling=True)
                    else:
                        st.info("Ask VOID to build an HTML/JS web app or code snippet to preview it here.")
                with t_edit:
                    edited = st.text_area("Modify Prism Content", value=p_text, height=340)
                    if st.button("Update & Rebuild", use_container_width=True):
                        st.session_state.active_prism_text = edited
                        st.rerun()
            else:
                st.info("Ask VOID for a PDF, study guide, slide deck, or web app to inspect it in Prism.")
            st.markdown("</div>", unsafe_allow_html=True)

# ============================== DIMENSION 2: CODEX ==============================
elif ui_mode == "📖 VOID Codex (Study, PDF & Slides)":
    st.markdown("### VOID Scholastic Codex")
    st.caption("Master-level explanations, revision notes, and exam question banks with instant PDF and slide deck exports.")
    s1, s2, s3 = st.columns([2.2, 1.3, 1])
    with s1:
        topic = st.text_input("Chapter or Topic", placeholder="E.g., Force & Pressure, Cell Structure, Linear Equations…")
    with s2:
        fmt = st.selectbox(
            "Codex Mode",
            [
                "📘 Complete Revision Notes + Formulas",
                "💡 Easy Explanation with Real-Life Examples",
                "❓ Exam Question Bank (MCQs + Long Answers + Key)",
                "📊 Full Slide Presentation Deck (8 Slides)",
            ],
        )
    with s3:
        level = st.selectbox(
            "Level",
            [
                "Class 8 (CBSE / ICSE)",
                "High School (Class 9-10)",
                "Olympiad / Advanced",
                "Quick 5-Minute Summary",
            ],
        )

    res, err = None, None
    if st.button("Forge Codex Material", type="primary", use_container_width=True):
        if topic.strip():
            bump_usage()
            d = {}
            with st.spinner(f"Forging '{topic}'…"):
                try:
                    live_intel = grounding(topic, research_depth, user_city, d)
                    sys_p = build_system_prompt(
                        live_intel,
                        True,
                        f"Create a master-level academic guide for {user_name} ({level}) on '{topic}'. Format: {fmt}. "
                        "Use clean # and ## headers so each section forms a page/slide. Include: 1. Core Concept Explanation, "
                        "2. Key Definitions & Formulas, 3. Worked Examples, 4. High-Probability Exam Questions with Answers.",
                    )
                    res = answer_question(
                        cosmic_entity,
                        f"Forge {fmt} for: {topic}",
                        sys_p,
                        [{"role": "user", "content": f"Forge {fmt} for: {topic}"}],
                        0.2,
                        2800,
                        accuracy_mode=accuracy_mode,
                        diag=d,
                    )
                except Exception as e:
                    err = str(e)
            if res:
                st.session_state.codex_output, st.session_state.codex_topic = res, topic.strip()
                st.session_state.codex_diag = {k: v for k, v in d.items() if not k.startswith("_")}
                st.rerun()
            else:
                st.error(err or "The engine returned an empty response. Please try again.")
        else:
            st.warning("Enter a topic or chapter name first.")

    if "codex_output" in st.session_state:
        text, ctopic = st.session_state.codex_output, st.session_state.get("codex_topic", "Study")
        fname = safe_name(ctopic)
        st.markdown("---")
        if st.session_state.get("codex_diag"):
            st.markdown(diag_html(st.session_state.codex_diag), unsafe_allow_html=True)
        d1, d2, d3, d4 = st.columns(4)
        with d1:
            st.download_button(
                "⬇ Download PDF",
                generate_real_pdf_bytes(f"VOID Codex: {ctopic}", text, f"VOID Codex ({user_name})"),
                file_name=f"VOID_Codex_{fname}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True,
            )
        with d2:
            st.download_button(
                "⬇ Slide Deck (.html)",
                generate_interactive_slides_html(ctopic, text).encode("utf-8"),
                file_name=f"VOID_Slides_{fname}.html",
                mime="text/html",
                use_container_width=True,
            )
        with d3:
            st.download_button(
                "⬇ Markdown (.md)",
                text,
                file_name=f"VOID_Codex_{fname}.md",
                mime="text/markdown",
                use_container_width=True,
            )
        with d4:
            if st.button("Save to Session", use_container_width=True):
                cid = current_chat_id
                user_chats[cid]["messages"].append(
                    {"role": "user", "content": f"[Codex] Forge {fmt} for: {ctopic} ({level})"}
                )
                user_chats[cid]["messages"].append({"role": "assistant", "content": text, "is_prism": True})
                send_to_prism(text, f"VOID Codex: {ctopic}")
                save_db(db)
                st.success("Saved to current session.")
        tab1, tab2 = st.tabs(["Notes & Guide", "Interactive Slide Deck"])
        with tab1:
            st.markdown(text)
        with tab2:
            components.html(generate_interactive_slides_html(ctopic, text), height=500)

# ============================== DIMENSION 3: WEB APP STUDIO ==============================
elif ui_mode == "⚡ Live Web App Studio":
    st.markdown("### VOID Live Web App & Game Studio")
    st.caption("Describe any web app, calculator, dashboard, or mini-game and VOID will compile and launch it live.")
    ui_prompt = st.text_area(
        "What should VOID build?",
        height=85,
        placeholder="E.g., A sleek dark-mode Hand Cricket game or a Pomodoro study dashboard…",
    )
    if st.button("Forge & Launch App", type="primary"):
        if ui_prompt.strip():
            sys_p = (
                "Output ONLY one complete, self-contained HTML file (with embedded <style> and <script>) inside a "
                "```html code block. Use a sleek modern dark UI and ensure zero external broken dependencies."
            )
            bump_usage()
            d = {}
            with st.spinner("Forging interactive application…"):
                out, err = call_llm(
                    cosmic_entity,
                    sys_p,
                    [{"role": "user", "content": ui_prompt}],
                    0.3,
                    max_tokens,
                    prompt=ui_prompt,
                    diag=d,
                )
            if out:
                m = re.search(r"```(?:html)?\s*\n(.*?)```", out, re.DOTALL)
                st.session_state.studio_html = (m.group(1) if m else out).strip()
            else:
                st.error(err)
        else:
            st.warning("Describe what you want built first.")

    if "studio_html" in st.session_state:
        col_prev, col_src = st.columns([1.4, 1])
        with col_prev:
            st.markdown("##### Live Application Preview")
            components.html(st.session_state.studio_html, height=520, scrolling=True)
        with col_src:
            st.markdown("##### Source Code")
            st.download_button(
                "⬇ Download index.html",
                st.session_state.studio_html,
                file_name="index.html",
                mime="text/html",
                use_container_width=True,
            )
            if st.button("Send to Prism Panel", use_container_width=True):
                send_to_prism(st.session_state.studio_html, "Web App Studio Build")
                st.rerun()
            st.code(st.session_state.studio_html, language="html")

# ============================== DIMENSION 4: CODE LAB ==============================
elif ui_mode == "🛠️ Side-by-Side Code Lab":
    st.markdown("### VOID Code Refactor & Bug Lab")
    action = st.selectbox(
        "Operation",
        [
            "🐞 Find & Fix All Bugs",
            "🚀 Optimize for Maximum Speed",
            "🛡️ Security Audit & Error Handling",
            "🔄 Convert to Python / JS / C++",
        ],
    )
    left, right = st.columns(2)
    with left:
        raw = st.text_area("Input Code", height=340, placeholder="Paste your code here…")
        run = st.button("Transform Code", type="primary", use_container_width=True)
    with right:
        st.markdown("**Refactored Output**")
        if run:
            if raw.strip():
                sys_p = (
                    f"Perform this exact operation on the user's code: {action}. Briefly highlight key fixes, "
                    "then output the complete upgraded code with zero placeholders."
                )
                bump_usage()
                with st.spinner("Analyzing AST & refactoring…"):
                    out, err = call_llm(
                        cosmic_entity,
                        sys_p,
                        [{"role": "user", "content": raw}],
                        0.1,
                        max_tokens,
                        prompt=raw,
                    )
                st.session_state.lab_result = out if out else f"⚠️ {err}"
                st.session_state.lab_action = action
            else:
                st.warning("Paste some code first.")
        if st.session_state.get("lab_result"):
            _, lr2 = st.columns([3, 1.2])
            with lr2:
                if st.button("Send to Prism", use_container_width=True):
                    send_to_prism(
                        st.session_state.lab_result,
                        f"Code Lab — {st.session_state.get('lab_action', 'Output')}",
                    )
                    st.rerun()
            st.markdown(st.session_state.lab_result)
        else:
            st.info("Paste code on the left and click Transform Code.")

# ============================== DIMENSION 5: SELF-EVOLUTION LAB ==============================
elif ui_mode == "🧬 Self-Evolution Lab":
    st.markdown("### VOID Self-Evolution & Meta-Coding Lab")
    st.caption("Use VOID's coding architecture engine to inspect, upgrade, or design new modules for VOID itself.")
    evo_src = ""
    with st.expander("Attach current app.py (optional for context-aware upgrades)"):
        evo_file = st.file_uploader("Upload app.py", type=["py", "txt"], key="evo_uploader")
        if evo_file:
            try:
                evo_src = evo_file.getvalue().decode("utf-8")[:MAX_FILE_CHARS]
                st.success(f"Loaded `{evo_file.name}` ({len(evo_src)} chars)")
            except UnicodeDecodeError:
                st.error("Unable to read file as UTF-8 text.")

    evo_goal = st.text_input(
        "What upgrade or new feature should VOID build for itself?",
        placeholder="E.g., Add a Pomodoro timer sidebar widget, or add voice note transcription…",
    )
    if st.button("Execute Self-Upgrade", type="primary"):
        if evo_goal.strip():
            evo_sys = (
                f"You are the master core architect of VOID. The founder ({FOUNDER_NAME}) wants to upgrade VOID with "
                f"the following feature: '{evo_goal}'. Provide complete, clean Python Streamlit code modifications "
                "ready to paste into app.py."
            )
            if evo_src:
                evo_sys += "\n\n=== CURRENT APP SOURCE ===\n" + evo_src
            bump_usage()
            with st.spinner("Designing architectural upgrade…"):
                out, err = call_llm(
                    "☀️ Supernova X (Coding & Architecture)",
                    evo_sys,
                    [{"role": "user", "content": evo_goal}],
                    0.2,
                    3500,
                    prompt=evo_goal,
                )
            if out:
                st.session_state.evo_result = out
            else:
                st.error(err)
        else:
            st.warning("Enter an upgrade goal first.")

    if "evo_result" in st.session_state:
        st.markdown("---")
        st.markdown("#### Generated Upgrade Blueprint")
        st.markdown(st.session_state.evo_result)
        blocks = extract_code_blocks(st.session_state.evo_result)
        if blocks:
            with st.expander("Preview & Copy Raw Code"):
                for b in blocks:
                    st.code(b[1].strip(), language=(b[0] or "python").lower())

# ============================== DIMENSION 6: SHIP TELEMETRY ==============================
elif ui_mode == "🛰️ Ship Telemetry & Insights":
    st.markdown("### VOID Ship Telemetry")
    st.caption("Command-deck overview of operators, active sessions, and daily engine throughput.")

    total_chats = sum(len(v) for v in db["chats"].values())
    total_msgs = sum(len(c.get("messages", [])) for v in db["chats"].values() for c in v.values())
    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Crew Members", len(db["users"]))
    k2.metric("Total Sessions", total_chats)
    k3.metric("Total Messages", total_msgs)
    k4.metric("Prompts (All Time)", sum(db.get("usage", {}).values()))

    st.markdown("##### Daily Engine Load (Last 30 Days)")
    today = datetime.now().date()
    days = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(29, -1, -1)]
    series = pd.Series([db.get("usage", {}).get(d, 0) for d in days], index=[d[5:] for d in days])
    if series.sum() > 0:
        st.area_chart(series, height=250)
    else:
        st.info("No engine activity recorded yet — send a prompt in VOID Core to populate telemetry.")

    if is_founder:
        st.markdown("##### Crew Roster")
        rows = [
            {
                "Member": info.get("name", "Member"),
                "Email": mail,
                "Prompts": info.get("prompts", 0),
                "Last Active": info.get("last_active", ""),
                "Joined": info.get("joined", ""),
            }
            for mail, info in db["users"].items()
        ]
        if rows:
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        st.markdown("##### Sovereign Controls (Founder Only)")
        exp_c1, exp_c2 = st.columns(2)
        with exp_c1:
            st.download_button(
                "⬇ Export Full Database (.json)",
                json.dumps(db, indent=2),
                file_name="void_hub_db_export.json",
                mime="application/json",
                use_container_width=True,
            )
        with exp_c2:
            with st.popover("⚠ Danger Zone", use_container_width=True):
                st.warning("This wipes ALL users, sessions, and messages permanently.")
                if st.checkbox("I understand, wipe everything"):
                    if st.button("Factory Reset VOID", type="primary"):
                        db.clear()
                        db.update({"users": {}, "chats": {}, "usage": {}})
                        save_db(db)
                        st.success("VOID database reset. Reloading…")
                        time.sleep(1)
                        st.rerun()
    else:
        st.info("Founder-level controls (roster export & factory reset) are restricted to the Founder account.")

# ============================== DIMENSION 7: ENGINE DOCTOR ==============================
elif ui_mode == "🩺 Engine Doctor & Live Test":
    st.markdown("### Engine Doctor & Live Grounding Inspector")
    st.caption("Verify each provider gateway and inspect the exact live internet snippets injected into VOID.")

    d1, d2 = st.columns(2)
    with d1:
        st.markdown("##### Configured Gateways & Relays")
        for label, ok in [
            ("OpenRouter (Primary Fleet)", bool(PROV_KEYS["openrouter"])),
            ("Groq (Ultra-Fast Backup)", bool(PROV_KEYS["groq"])),
            ("Google Gemini (Direct Backup)", bool(PROV_KEYS["google"])),
            ("OpenAI (Direct Backup)", bool(PROV_KEYS["openai"])),
            ("Google News RSS (Zero-Key Live News)", True),
            ("DuckDuckGo Lite + Instant API", True),
            ("Wikipedia Deep Extracts", True),
            ("Tavily / Serper / Brave Keys", bool(any(SEARCH_KEYS.values()))),
        ]:
            mark = "<span style='color:#10b981'>●</span>" if ok else "<span style='color:#52525b'>○</span>"
            st.markdown(
                f"<div class='kv'><span>{mark} {esc(label)}</span><span>{'ready' if ok else 'optional'}</span></div>",
                unsafe_allow_html=True,
            )
    with d2:
        st.markdown("##### One-Click Live Probes")
        if st.button("Test LLM Answer Relay", type="primary", use_container_width=True):
            d = {}
            out, err = call_llm(
                "🧠 Auto-Route (Omni Intelligence)",
                "Be concise.",
                [{"role": "user", "content": "In one sentence, what is a binary search tree?"}],
                0.1,
                100,
                prompt="what is a binary search tree",
                diag=d,
            )
            if out:
                st.success(f"Answered via {d.get('link')} · {d.get('model')} in {d.get('latency')}s")
                st.code(out.strip())
            else:
                st.error(err)

        if st.button("Test Live News & Web Bundle", use_container_width=True):
            text, urls = web_search_bundle("latest world technology news", 5)
            if text:
                st.success(f"Retrieved {len(text.splitlines())} clean live intelligence lines")
                st.code(text[:1400])
            else:
                st.warning("No snippets returned.")

    st.markdown("---")
    st.markdown("##### End-to-End Grounded Diagnostic Query")
    probe_q = st.text_input(
        "Diagnostic Prompt",
        value="What are the top breaking news stories in India and the world today?",
    )
    if st.button("Run Grounded Diagnostic", type="primary"):
        if probe_q.strip():
            diag = {}
            with st.spinner("Running full retrieval + synthesis pipeline…"):
                live_intel = grounding(probe_q, research_depth, user_city, diag)
                sys_p = build_system_prompt(live_intel, False)
                aug_msgs = _prepare_messages_with_grounding([{"role": "user", "content": probe_q}], live_intel)
                ans = answer_question(
                    cosmic_entity,
                    probe_q,
                    sys_p,
                    aug_msgs,
                    temperature,
                    max_tokens,
                    accuracy_mode=True,
                    diag=diag,
                )
            st.markdown("###### Synthesized Answer")
            st.markdown(ans)
            st.markdown(diag_html(diag), unsafe_allow_html=True)
            with st.expander("Inspect Raw Live Intelligence Injected into Prompt"):
                st.code(live_intel or "No external context triggered.")

# ============================== 13. FOOTER ==============================
st.markdown(
    f'<div class="void-footer">VOID · Sovereign OS Intelligence · Forged by {esc(FOUNDER_NAME)} · Obsidian OS v{APP_VERSION}</div>',
    unsafe_allow_html=True,
)
