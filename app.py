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
import urllib.parse
import uuid
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta, timezone

import pandas as pd
import requests
import streamlit as st

# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================
st.set_page_config(
    page_title="VOID — Sovereign OS Intelligence",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ==============================================================================
# 2. PERMANENT DARK-THEME & READABILITY CSS LOCK
# ==============================================================================
def inject_void_css():
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap');

        /* Root & App Container Lock */
        html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stAppViewBlockContainer"] {
            background-color: #070a12 !important;
            color: #f1f5f9 !important;
            font-family: 'Inter', sans-serif !important;
        }

        [data-testid="stHeader"] {
            background-color: rgba(7, 10, 18, 0.85) !important;
            backdrop-filter: blur(8px);
        }

        /* Sidebar Styling */
        section[data-testid="stSidebar"], [data-testid="stSidebarContent"] {
            background-color: #05080f !important;
            border-right: 1px solid #161f33 !important;
            color: #e2e8f0 !important;
        }

        section[data-testid="stSidebar"] * {
            color: #e2e8f0 !important;
        }

        /* FIX: Bottom Chat Input Container (Eliminates the white bar completely) */
        [data-testid="stBottom"],
        [data-testid="stBottom"] > div,
        [data-testid="stBottomBlockContainer"],
        .stChatFloatingInputContainer {
            background-color: #070a12 !important;
            background-image: none !important;
            border-top: 1px solid #111827 !important;
        }

        /* FIX: Chat Input Box & Text Readability */
        [data-testid="stChatInput"],
        [data-testid="stChatInput"] > div,
        [data-testid="stChatInputContainer"] {
            background-color: #0d1322 !important;
            border: 1px solid #2e3b55 !important;
            border-radius: 16px !important;
            color: #ffffff !important;
            box-shadow: 0 0 20px rgba(79, 70, 229, 0.12) !important;
        }

        [data-testid="stChatInput"]:focus-within,
        [data-testid="stChatInput"] > div:focus-within {
            border-color: #6366f1 !important;
            box-shadow: 0 0 24px rgba(99, 102, 241, 0.28) !important;
        }

        [data-testid="stChatInputTextArea"],
        [data-testid="stChatInput"] textarea,
        div[data-baseweb="textarea"] textarea,
        div[data-baseweb="input"] input {
            background-color: transparent !important;
            color: #f8fafc !important;
            caret-color: #818cf8 !important;
            font-size: 0.96rem !important;
        }

        [data-testid="stChatInputTextArea"]::placeholder,
        [data-testid="stChatInput"] textarea::placeholder {
            color: #64748b !important;
            opacity: 1 !important;
        }

        [data-testid="stChatInputSubmitButton"] {
            background-color: #1e293b !important;
            color: #818cf8 !important;
            border-radius: 10px !important;
        }

        [data-testid="stChatInputSubmitButton"]:hover {
            background-color: #4f46e5 !important;
            color: #ffffff !important;
        }

        /* FIX: All Buttons (Prevent turning white/unreadable on hover or click) */
        .stButton > button {
            background-color: #0f1624 !important;
            color: #e2e8f0 !important;
            border: 1px solid #1f2b42 !important;
            border-radius: 999px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
            font-size: 0.88rem !important;
            transition: all 0.2s ease !important;
        }

        .stButton > button:hover,
        .stButton > button:focus,
        .stButton > button:active {
            background-color: #17223b !important;
            color: #ffffff !important;
            border-color: #6366f1 !important;
            box-shadow: 0 0 14px rgba(99, 102, 241, 0.25) !important;
        }

        /* FIX: Expanders, Text Inputs, Selectboxes */
        [data-testid="stExpander"] {
            background-color: #0b101d !important;
            border: 1px solid #1a2438 !important;
            border-radius: 12px !important;
            color: #e2e8f0 !important;
        }

        [data-testid="stExpander"] summary,
        [data-testid="stExpander"] summary:hover {
            background-color: #0b101d !important;
            color: #e2e8f0 !important;
            border-radius: 12px !important;
        }

        [data-testid="stExpanderDetails"] {
            background-color: #0b101d !important;
            color: #cbd5e1 !important;
        }

        /* Metrics Styling */
        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
            font-size: 0.82rem !important;
        }

        [data-testid="stMetricValue"] {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }

        /* Chat Messages Styling */
        [data-testid="stChatMessage"] {
            background-color: #0b111e !important;
            border: 1px solid #172236 !important;
            border-radius: 14px !important;
            padding: 1rem 1.25rem !important;
            margin-bottom: 0.75rem !important;
            color: #f1f5f9 !important;
        }

        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] div {
            color: #f1f5f9 !important;
        }

        /* Code Blocks */
        pre, code {
            background-color: #060911 !important;
            color: #a5b4fc !important;
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* Custom Hero Styling */
        .void-logo-box {
            width: 68px;
            height: 68px;
            margin: 18px auto 14px auto;
            border-radius: 18px;
            background: linear-gradient(145deg, #0d1324, #070a14);
            border: 1.5px solid #4f46e5;
            box-shadow: 0 0 28px rgba(79, 70, 229, 0.35);
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 30px;
            font-weight: 800;
            color: #818cf8;
        }

        .void-hero-title {
            text-align: center;
            font-size: 2.55rem;
            font-weight: 800;
            background: linear-gradient(90deg, #3b82f6 0%, #6366f1 50%, #818cf8 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.3rem;
            letter-spacing: -0.02em;
        }

        .void-hero-sub {
            text-align: center;
            color: #94a3b8 !important;
            font-size: 0.98rem;
            margin-bottom: 1.8rem;
        }

        .void-footer {
            text-align: center;
            color: #64748b !important;
            font-size: 0.8rem;
            margin-top: 1.5rem;
            margin-bottom: 1rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_void_css()

# ==============================================================================
# 3. SESSION STATE INITIALIZATION
# ==============================================================================
IST = timezone(timedelta(hours=5, minutes=30))


def get_ist_now():
    return datetime.now(IST)


if "sessions" not in st.session_state:
    default_id = str(uuid.uuid4())[:8]
    st.session_state.sessions = {
        default_id: {
            "name": "New Session",
            "messages": [],
            "created": get_ist_now().strftime("%H:%M IST"),
        }
    }
    st.session_state.current_session = default_id

if "total_prompts" not in st.session_state:
    st.session_state.total_prompts = 0

if "operator_name" not in st.session_state:
    st.session_state.operator_name = "Guest Operator"

if "prism_panel" not in st.session_state:
    st.session_state.prism_panel = False

if "auto_refresh" not in st.session_state:
    st.session_state.auto_refresh = False


# ==============================================================================
# 4. SAFETY GUARDRAIL (Blocks Gore/Bloodshed, Allows All Knowledge)
# ==============================================================================
BLOCKED_PATTERNS = [
    r"\b(gore|bloodshed|mutilat|dismember|behead|torture|massacre instructions|how to kill|self-harm|suicide)\b"
]


def is_safe_query(query: str) -> tuple[bool, str]:
    q_lower = query.lower()
    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern, q_lower):
            return (
                False,
                "⚠️ **VOID Security Protocol Engaged:** I can answer virtually any question across sports, coding, science, history, gaming, and live world events, but I strictly do not generate content involving bloodshed, gore, or real-world harm.",
            )
    return True, ""


# ==============================================================================
# 5. LIVE OMNI-INTELLIGENCE ENGINE (Web + Sports + News + Weather + Wiki)
# ==============================================================================
@st.cache_data(ttl=180, show_spinner=False)
def fetch_live_google_news(query: str, max_items: int = 6) -> list[dict]:
    """Fetches real-time news & sports headlines via Google News RSS (Zero API Key)."""
    results = []
    try:
        encoded = urllib.parse.quote(query)
        url = f"https://news.google.com/rss/search?q={encoded}&hl=en-IN&gl=IN&ceid=IN:en"
        resp = requests.get(url, timeout=6, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item")[:max_items]:
                title = item.findtext("title", "")
                pub_date = item.findtext("pubDate", "")
                source_el = item.find("source")
                source = source_el.text if source_el is not None else "Live Feed"
                results.append(
                    {"title": title, "date": pub_date, "source": source}
                )
    except Exception:
        pass
    return results


@st.cache_data(ttl=180, show_spinner=False)
def fetch_espn_live_scores(league_code: str = "esp.1") -> list[str]:
    """Fetches real-time football scores from ESPN's open scoreboard API."""
    matches = []
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_code}/scoreboard"
        resp = requests.get(url, timeout=6)
        if resp.status_code == 200:
            data = resp.json()
            for ev in data.get("events", [])[:6]:
                name = ev.get("name", "")
                status = (
                    ev.get("status", {})
                    .get("type", {})
                    .get("shortDetail", "")
                )
                comps = ev.get("competitions", [{}])[0].get("competitors", [])
                if len(comps) == 2:
                    t1 = comps[0].get("team", {}).get("displayName", "")
                    s1 = comps[0].get("score", "0")
                    t2 = comps[1].get("team", {}).get("displayName", "")
                    s2 = comps[1].get("score", "0")
                    matches.append(f"{t1} {s1} - {s2} {t2} ({status})")
                else:
                    matches.append(f"{name} ({status})")
    except Exception:
        pass
    return matches


@st.cache_data(ttl=600, show_spinner=False)
def fetch_wikipedia_context(query: str) -> str:
    """Fetches verified encyclopedic summaries from Wikipedia REST API."""
    try:
        search_url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 2,
        }
        r = requests.get(
            search_url, params=params, timeout=5, headers={"User-Agent": "VOID-OS/4.2"}
        )
        if r.status_code == 200:
            hits = r.json().get("query", {}).get("search", [])
            summaries = []
            for h in hits:
                title = urllib.parse.quote(h["title"].replace(" ", "_"))
                sum_r = requests.get(
                    f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}",
                    timeout=4,
                    headers={"User-Agent": "VOID-OS/4.2"},
                )
                if sum_r.status_code == 200:
                    extract = sum_r.json().get("extract", "")
                    if extract:
                        summaries.append(f"[{h['title']}]: {extract}")
            return "\n".join(summaries)
    except Exception:
        pass
    return ""


@st.cache_data(ttl=300, show_spinner=False)
def fetch_live_weather(city: str = "Varanasi") -> str:
    """Fetches real-time city telemetry from Open-Meteo (No API key needed)."""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1"
        geo_r = requests.get(geo_url, timeout=5).json()
        results = geo_r.get("results", [])
        if not results:
            return f"Could not locate coordinates for '{city}'."
        loc = results[0]
        lat, lon = loc["latitude"], loc["longitude"]
        resolved_name = f"{loc.get('name')}, {loc.get('country', '')}"

        w_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code"
            "&timezone=auto"
        )
        w_data = requests.get(w_url, timeout=5).json().get("current", {})
        temp = w_data.get("temperature_2m", "N/A")
        feels = w_data.get("apparent_temperature", "N/A")
        hum = w_data.get("relative_humidity_2m", "N/A")
        wind = w_data.get("wind_speed_10m", "N/A")
        return (
            f"📍 **{resolved_name}** — Temperature: **{temp}°C** (Feels like {feels}°C) | "
            f"Humidity: **{hum}%** | Wind: **{wind} km/h**"
        )
    except Exception as e:
        return f"Weather telemetry unavailable: {e}"


def gather_live_telemetry(user_prompt: str) -> str:
    """Combines real-time web news, sports scoreboards, weather, and Wikipedia into context."""
    now_str = get_ist_now().strftime("%A, %d %B %Y, %I:%M %p IST")
    context_blocks = [f"CURRENT REAL-TIME CHRONOMETER: {now_str}"]

    q_lower = user_prompt.lower()

    # 1. Check if asking about El Clasico / Football / Sports
    if any(
        k in q_lower
        for k in [
            "clasico",
            "clásico",
            "real madrid",
            "barcelona",
            "mbappe",
            "football",
            "soccer",
            "laliga",
            "la liga",
            "score",
            "match",
            "won",
        ]
    ):
        la_liga_scores = fetch_espn_live_scores("esp.1")
        ucl_scores = fetch_espn_live_scores("uefa.champions")
        epl_scores = fetch_espn_live_scores("eng.1")
        if la_liga_scores:
            context_blocks.append(
                "LIVE LA LIGA SCOREBOARD:\n" + "\n".join(la_liga_scores)
            )
        if ucl_scores:
            context_blocks.append(
                "LIVE CHAMPIONS LEAGUE SCOREBOARD:\n" + "\n".join(ucl_scores)
            )
        if epl_scores:
            context_blocks.append(
                "LIVE PREMIER LEAGUE SCOREBOARD:\n" + "\n".join(epl_scores)
            )

    # 2. Check if asking about Weather
    if "weather" in q_lower or "temperature" in q_lower:
        city_match = re.search(
            r"(?:in|for|at)\s+([a-zA-Z\s]{2,25})", user_prompt, re.IGNORECASE
        )
        city = city_match.group(1).strip() if city_match else "Varanasi"
        context_blocks.append("LIVE WEATHER TELEMETRY:\n" + fetch_live_weather(city))

    # 3. Always fetch top real-time news headlines for the query
    news_items = fetch_live_google_news(user_prompt, max_items=5)
    if news_items:
        formatted_news = "\n".join(
            [f"- {n['title']} ({n['source']} | {n['date']})" for n in news_items]
        )
        context_blocks.append(f"LIVE GOOGLE NEWS FEED:\n{formatted_news}")

    # 4. Wikipedia knowledge lookup
    wiki_info = fetch_wikipedia_context(user_prompt)
    if wiki_info:
        context_blocks.append(f"ENCYCLOPEDIC REFERENCE:\n{wiki_info}")

    return "\n\n".join(context_blocks)


# ==============================================================================
# 6. MULTI-ENGINE AI ROUTER (Secrets API Keys + Zero-Key Live Fallback)
# ==============================================================================
def query_void_intelligence(user_prompt: str, chat_history: list) -> str:
    safe, warning = is_safe_query(user_prompt)
    if not safe:
        return warning

    live_context = gather_live_telemetry(user_prompt)

    system_instruction = textwrap.dedent(
        f"""
        You are VOID (Sovereign OS Intelligence — Prism OS v4.2.0-Supernova), an elite, omniscient AI operating system created and forged by Avyan.
        Current Operator: {st.session_state.operator_name}

        LIVE REAL-TIME TELEMETRY & WEB DATA:
        {live_context}

        DIRECTIVES:
        1. Use the LIVE REAL-TIME TELEMETRY above to answer questions about today's matches (such as El Clásico, La Liga, cricket, live news, weather, and current events in {get_ist_now().year}) with 100% precision.
        2. You have full mastery across coding, science, mathematics, study notes, gaming, anime, football, and creative writing.
        3. Never generate gore, bloodshed, or self-harm content.
        4. Format responses cleanly with Markdown headings, bold key insights, bullet points, or code blocks when helpful.
        """
    ).strip()

    messages_payload = [{"role": "system", "content": system_instruction}]
    for msg in chat_history[-6:]:
        messages_payload.append({"role": msg["role"], "content": msg["content"]})
    messages_payload.append({"role": "user", "content": user_prompt})

    # 1. Try OpenRouter or Groq or OpenAI if configured in Streamlit Secrets
    openrouter_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))
    groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))

    if groq_key:
        try:
            r = requests.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages_payload,
                    "temperature": 0.6,
                },
                timeout=20,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except Exception:
            pass

    if openrouter_key:
        try:
            r = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openrouter_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "meta-llama/llama-3.3-70b-instruct:free",
                    "messages": messages_payload,
                    "temperature": 0.6,
                },
                timeout=20,
            )
            if r.status_code == 200 and "choices" in r.json():
                return r.json()["choices"][0]["message"]["content"]
        except Exception:
            pass

    # 2. Universal Zero-Key Live AI Engine (Pollinations OpenAI-Compatible Endpoint)
    try:
        r = requests.post(
            "https://text.pollinations.ai/openai",
            headers={"Content-Type": "application/json"},
            json={
                "model": "openai",
                "messages": messages_payload,
                "temperature": 0.6,
            },
            timeout=25,
        )
        if r.status_code == 200:
            data = r.json()
            if "choices" in data and len(data["choices"]) > 0:
                return data["choices"][0]["message"]["content"]
            elif isinstance(data, str) and len(data) > 5:
                return data
    except Exception:
        pass

    # 3. Direct GET fallback if POST endpoint is busy
    try:
        combined_q = f"{system_instruction}\n\nUser Question: {user_prompt}"
        encoded_q = urllib.parse.quote(combined_q[:3500])
        r2 = requests.get(f"https://text.pollinations.ai/{encoded_q}", timeout=20)
        if r2.status_code == 200 and len(r2.text.strip()) > 0:
            return r2.text.strip()
    except Exception:
        pass

    return (
        f"### ⚡ VOID Live Telemetry Report\n\n"
        f"Here is the real-time intelligence gathered for **'{user_prompt}'**:\n\n"
        f"```text\n{live_context}\n```"
    )


# ==============================================================================
# 7. SIDEBAR NAVIGATION (Matches Screenshot Layout)
# ==============================================================================
active_session = st.session_state.sessions[st.session_state.current_session]

with st.sidebar:
    st.markdown(
        """
        <div style="display:flex; align-items:center; gap:10px; margin-bottom:14px;">
            <div style="width:34px; height:34px; border-radius:9px; background:#0f172a; border:1.5px solid #6366f1; display:flex; align-items:center; justify-content:center; font-weight:800; color:#818cf8;">V</div>
            <span style="font-size:1.25rem; font-weight:800; letter-spacing:0.06em; color:#f8fafc;">VOID</span>
            <span style="font-size:0.68rem; padding:2px 8px; border-radius:999px; background:#111c35; border:1px solid #2e4372; color:#93c5fd; font-weight:600;">PRISM OS</span>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("✦ New Session", use_container_width=True):
        new_id = str(uuid.uuid4())[:8]
        st.session_state.sessions[new_id] = {
            "name": f"Session {len(st.session_state.sessions) + 1}",
            "messages": [],
            "created": get_ist_now().strftime("%H:%M IST"),
        }
        st.session_state.current_session = new_id
        st.rerun()

    st.session_state.prism_panel = st.toggle(
        "⚡ Open VOID Prism Panel", value=st.session_state.prism_panel
    )
    st.session_state.auto_refresh = st.toggle(
        "🔄 Auto-Refresh Feed",
        value=st.session_state.auto_refresh,
        help="Automatically refreshes live telemetry timestamps.",
    )

    st.markdown("<div style='margin-top:12px; font-size:0.82rem; color:#94a3b8; font-weight:600;'>Active Sessions</div>", unsafe_allow_html=True)

    for s_id, s_data in list(st.session_state.sessions.items()):
        prefix = "● " if s_id == st.session_state.current_session else "○ "
        if st.button(f"{prefix}{s_data['name']}", key=f"sess_{s_id}", use_container_width=True):
            st.session_state.current_session = s_id
            st.rerun()

    st.markdown("<hr style='border-color:#161f33; margin:16px 0;'>", unsafe_allow_html=True)

    st.markdown("**📊 Chat Insights**")
    i_col1, i_col2, i_col3 = st.columns(3)
    i_col1.metric("Messages", str(len(active_session["messages"])))
    i_col2.metric("Sessions", str(len(st.session_state.sessions)))
    i_col3.metric("Prompts", str(st.session_state.total_prompts))

    with st.expander("🧬 Core Identity Vault"):
        new_op = st.text_input("Operator Alias", value=st.session_state.operator_name)
        if new_op.strip():
            st.session_state.operator_name = new_op.strip()
        st.caption("Engine: VOID Omni-Core • Supernova X")
        st.caption("Live Web + Sports + Weather + Wiki: Active")

    with st.expander("👑 Founder Profile"):
        st.markdown(
            "**Architect & Founder:** Avyan\n\n"
            "**System:** VOID — Sovereign OS Intelligence\n\n"
            "**Build:** Prism OS v4.2.0-Supernova"
        )

    st.markdown(
        f"<div style='margin-top:18px; font-size:0.8rem; color:#64748b;'>Operator: <strong style='color:#cbd5e1;'>{html.escape(st.session_state.operator_name)}</strong></div>",
        unsafe_allow_html=True,
    )

# ==============================================================================
# 8. TOP TELEMETRY ROW (Clean 4-Column Layout from Screenshot)
# ==============================================================================
ist_now = get_ist_now()
t_col1, t_col2, t_col3, t_col4 = st.columns(4)

with t_col1:
    st.metric(
        label="VOID Engine",
        value="🟢 Online",
        delta="link stable · 467 models",
    )
with t_col2:
    st.metric(
        label="Cosmic Engine",
        value="Supernova X",
        delta="primary link",
    )
with t_col3:
    st.metric(
        label="Resonance",
        value="VOID Omni-Core",
        delta="style profile",
    )
with t_col4:
    st.metric(
        label="Chronometer",
        value=ist_now.strftime("%d %b %Y"),
        delta=ist_now.strftime("%I:%M %p IST"),
    )

# ==============================================================================
# 9. OPTIONAL PRISM PANEL (Only opens when toggled in Sidebar)
# ==============================================================================
if st.session_state.prism_panel:
    with st.container():
        st.markdown("#### ⚡ VOID Prism Panel — Live Telemetry & Forge")
        p_tab1, p_tab2, p_tab3 = st.tabs(
            ["⚽ Live Football & Sports", "🌦️ City Weather Radar", "📄 Printable Notes Exporter"]
        )
        with p_tab1:
            league_map = {
                "La Liga (Spain)": "esp.1",
                "UEFA Champions League": "uefa.champions",
                "Premier League (England)": "eng.1",
            }
            sel_league = st.selectbox("Select League Feed", list(league_map.keys()))
            scores = fetch_espn_live_scores(league_map[sel_league])
            if scores:
                for s in scores:
                    st.markdown(f"- ⚽ **{s}**")
            else:
                st.caption("Fetching latest fixtures from live feed...")
        with p_tab2:
            city_q = st.text_input("Enter City Name", value="Varanasi")
            if city_q:
                st.markdown(fetch_live_weather(city_q))
        with p_tab3:
            if active_session["messages"]:
                export_text = "\n\n".join(
                    [f"{m['role'].upper()}:\n{m['content']}" for m in active_session["messages"]]
                )
                st.download_button(
                    "📥 Download Session Notes (.md)",
                    data=export_text,
                    file_name="VOID_Study_Notes.md",
                    mime="text/markdown",
                )
            else:
                st.caption("Ask VOID to generate study notes in chat first to export them here.")
        st.markdown("<hr style='border-color:#161f33;'>", unsafe_allow_html=True)

# ==============================================================================
# 10. SPACIOUS HERO SECTION & 4 QUICK ACTION PILLS
# ==============================================================================
triggered_prompt = None

if len(active_session["messages"]) == 0:
    st.markdown(
        f"""
        <div class="void-logo-box">V</div>
        <div class="void-hero-title">Welcome, {html.escape(st.session_state.operator_name)}</div>
        <div class="void-hero-sub">VOID Core • Live Telemetry • On-Demand Prism Forge</div>
        """,
        unsafe_allow_html=True,
    )

    q_col1, q_col2, q_col3, q_col4 = st.columns(4)
    with q_col1:
        if st.button("🌦️ Live Weather Real-time city...", use_container_width=True):
            triggered_prompt = "Give me the live real-time weather telemetry for Varanasi and major global cities right now."
    with q_col2:
        if st.button("📄 Forge Study PDF Notes + P...", use_container_width=True):
            triggered_prompt = "Create structured, high-scoring revision study notes with key formulas, definitions, and practice questions."
    with q_col3:
        if st.button("⚡ Build Web App Launch in ...", use_container_width=True):
            triggered_prompt = "Write a complete, modern single-file HTML/CSS/JS interactive web app that I can launch right away."
    with q_col4:
        if st.button("👑 Who am I? Identity & Foun...", use_container_width=True):
            triggered_prompt = "Who are you, what is your architecture, and tell me about your founder Avyan."

    st.markdown(
        "<div class='void-footer'>⚡ VOID — Sovereign OS Intelligence • Forged by Avyan • Prism OS v4.2.0-Supernova</div>",
        unsafe_allow_html=True,
    )

# ==============================================================================
# 11. CHAT HISTORY & LIVE OMNI-RESPONSE EXECUTION
# ==============================================================================
for message in active_session["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

chat_box_prompt = st.chat_input(
    f"Command VOID, {st.session_state.operator_name} — chat naturally, or ask for a PDF, slides, weather, or web app..."
)

final_prompt = triggered_prompt or chat_box_prompt

if final_prompt:
    st.session_state.total_prompts += 1
    if active_session["name"] == "New Session":
        active_session["name"] = final_prompt[:22] + ("..." if len(final_prompt) > 22 else "")

    active_session["messages"].append({"role": "user", "content": final_prompt})
    with st.chat_message("user"):
        st.markdown(final_prompt)

    with st.chat_message("assistant"):
        with st.spinner("VOID Omni-Core scanning live telemetry..."):
            reply = query_void_intelligence(
                final_prompt, active_session["messages"][:-1]
            )
        st.markdown(reply)

    active_session["messages"].append({"role": "assistant", "content": reply})
    st.rerun()
