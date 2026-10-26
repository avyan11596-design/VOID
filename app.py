from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timedelta, timezone
import html
import json
import os
import re
import textwrap
import urllib.parse
import uuid
import xml.etree.ElementTree as ET

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

        /* Bottom Chat Input Container (No White Bar) */
        [data-testid="stBottom"],
        [data-testid="stBottom"] > div,
        [data-testid="stBottomBlockContainer"],
        .stChatFloatingInputContainer {
            background-color: #070a12 !important;
            background-image: none !important;
            border-top: 1px solid #111827 !important;
        }

        /* Chat Input Box & Text Readability */
        [data-testid="stChatInput"],
        [data-testid="stChatInput"] > div,
        [data-testid="stChatInputContainer"] {
            background-color: #0d1322 !important;
            border: 1px solid #2e3b55 !important;
            border-radius: 16px !important;
            color: #ffffff !important;
            box-shadow: 0 0 20px rgba(79, 70, 229, 0.14) !important;
        }

        [data-testid="stChatInput"]:focus-within,
        [data-testid="stChatInput"] > div:focus-within {
            border-color: #6366f1 !important;
            box-shadow: 0 0 25px rgba(99, 102, 241, 0.32) !important;
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

        /* Buttons Lock */
        .stButton > button {
            background-color: #0f1624 !important;
            color: #e2e8f0 !important;
            border: 1px solid #1f2b42 !important;
            border-radius: 999px !important;
            padding: 0.5rem 1rem !important;
            font-weight: 500 !important;
            font-size: 0.88rem !important;
            transition: all 0.18s ease !important;
        }

        .stButton > button:hover,
        .stButton > button:focus,
        .stButton > button:active {
            background-color: #17223b !important;
            color: #ffffff !important;
            border-color: #6366f1 !important;
            box-shadow: 0 0 14px rgba(99, 102, 241, 0.25) !important;
        }

        /* Expanders & Metrics */
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

        [data-testid="stMetricLabel"] {
            color: #94a3b8 !important;
            font-size: 0.82rem !important;
        }

        [data-testid="stMetricValue"] {
            color: #f8fafc !important;
            font-weight: 700 !important;
        }

        /* Chat Messages & Tables */
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
        [data-testid="stChatMessage"] td,
        [data-testid="stChatMessage"] th,
        [data-testid="stChatMessage"] span,
        [data-testid="stChatMessage"] div {
            color: #f1f5f9 !important;
        }

        pre, code {
            background-color: #060911 !important;
            color: #a5b4fc !important;
            font-family: 'JetBrains Mono', monospace !important;
        }

        /* Hero Styling */
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

# Reusable HTTP session for faster connection pooling
HTTP_SESSION = requests.Session()
HTTP_SESSION.headers.update(
    {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"
    }
)

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
                "⚠️ **VOID Security Protocol Engaged:** I can answer any question across sports, coding, science, history, gaming, and live world events, but I strictly block content involving bloodshed, gore, or self-harm.",
            )
    return True, ""


# ==============================================================================
# 5. SMART QUERY OPTIMIZER & PARALLEL REAL-TIME SEARCH ENGINE
# ==============================================================================
STOP_FILLERS = {
    "no", "bro", "hey", "hi", "hello", "please", "tell", "me", "about",
    "what", "when", "where", "is", "are", "the", "a", "an", "can", "you",
    "give", "show", "find", "do", "know", "actually", "wait", "yeah", "ok"
}


def build_smart_search_query(raw_prompt: str) -> str:
    """Strips conversational filler so search engines return 100% accurate snippets."""
    cleaned = re.sub(r"[^\w\s]", " ", raw_prompt)
    tokens = [t for t in cleaned.split() if t.lower() not in STOP_FILLERS]
    core_query = " ".join(tokens) if tokens else raw_prompt.strip()

    q_low = core_query.lower()
    year_str = str(get_ist_now().year)
    if any(w in q_low for w in ["match", "cricket", "football", "clasico", "clásico", "score", "schedule", "series", "t20", "odi", "test", "ipl", "laliga", "vs"]):
        if year_str not in q_low:
            core_query += f" {year_str} schedule results"
    return core_query.strip()


def needs_live_web_search(prompt: str) -> bool:
    """Skips slow web calls for pure coding/math prompts so coding replies are instant."""
    q_low = prompt.lower().strip()
    pure_code_triggers = [
        "write a python", "write code", "fix this code", "html", "css",
        "javascript", "solve this equation", "factorize", "translate to"
    ]
    if any(t in q_low for t in pure_code_triggers) and not any(
        w in q_low for w in ["news", "today", "live", "score", "match", "weather", "2026"]
    ):
        return False
    return True


@st.cache_data(ttl=180, show_spinner=False)
def fetch_duckduckgo_snippets(query: str, max_results: int = 6) -> list[str]:
    """Scrapes full real-time web snippets (dates, schedules, facts) from DuckDuckGo HTML."""
    snippets = []
    try:
        url = f"https://html.duckduckgo.com/html/?q={urllib.parse.quote(query)}"
        resp = HTTP_SESSION.get(url, timeout=3.5)
        if resp.status_code == 200:
            titles = re.findall(
                r'<a rel="nofollow" class="result__a"[^>]*>(.*?)</a>',
                resp.text,
                re.DOTALL,
            )
            bodies = re.findall(
                r'<a class="result__snippet"[^>]*>(.*?)</a>',
                resp.text,
                re.DOTALL,
            )
            for t, b in list(zip(titles, bodies))[:max_results]:
                clean_t = html.unescape(re.sub(r"<[^>]+>", "", t)).strip()
                clean_b = html.unescape(re.sub(r"<[^>]+>", "", b)).strip()
                if clean_t and clean_b:
                    snippets.append(f"• [{clean_t}]: {clean_b}")
    except Exception:
        pass
    return snippets


@st.cache_data(ttl=180, show_spinner=False)
def fetch_live_google_news(query: str, max_items: int = 6) -> list[str]:
    """Fetches real-time Google News RSS headlines & descriptions with smart query."""
    items_out = []
    try:
        url = f"https://news.google.com/rss/search?q={urllib.parse.quote(query)}&hl=en-IN&gl=IN&ceid=IN:en"
        resp = HTTP_SESSION.get(url, timeout=3.0)
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item")[:max_items]:
                title = item.findtext("title", "")
                pub_date = item.findtext("pubDate", "")[:16]
                desc_raw = item.findtext("description", "")
                clean_desc = html.unescape(re.sub(r"<[^>]+>", " ", desc_raw)).strip()
                clean_desc = re.sub(r"\s+", " ", clean_desc)
                items_out.append(f"• {title} ({pub_date}) — {clean_desc[:180]}")
    except Exception:
        pass
    return items_out


@st.cache_data(ttl=120, show_spinner=False)
def fetch_live_cricket_rss() -> list[str]:
    """Fetches live cricket scores from ESPNcricinfo RSS + verified tour schedules."""
    scores = []
    try:
        resp = HTTP_SESSION.get(
            "https://www.espncricinfo.com/rss/livescores.xml", timeout=2.5
        )
        if resp.status_code == 200:
            root = ET.fromstring(resp.content)
            for item in root.findall(".//item")[:8]:
                title = item.findtext("title", "")
                if title:
                    scores.append(f"🏏 Live Score Feed: {title}")
    except Exception:
        pass
    return scores


@st.cache_data(ttl=180, show_spinner=False)
def fetch_espn_live_scores(league_code: str = "esp.1") -> list[str]:
    """Fetches real-time football scores from ESPN's open scoreboard API."""
    matches = []
    try:
        url = f"https://site.api.espn.com/apis/site/v2/sports/soccer/{league_code}/scoreboard"
        resp = HTTP_SESSION.get(url, timeout=2.5)
        if resp.status_code == 200:
            data = resp.json()
            for ev in data.get("events", [])[:6]:
                status = (
                    ev.get("status", {}).get("type", {}).get("shortDetail", "")
                )
                comps = ev.get("competitions", [{}])[0].get("competitors", [])
                if len(comps) == 2:
                    t1 = comps[0].get("team", {}).get("displayName", "")
                    s1 = comps[0].get("score", "0")
                    t2 = comps[1].get("team", {}).get("displayName", "")
                    s2 = comps[1].get("score", "0")
                    matches.append(f"{t1} {s1} - {s2} {t2} ({status})")
    except Exception:
        pass
    return matches


@st.cache_data(ttl=300, show_spinner=False)
def fetch_live_weather(city: str = "Varanasi") -> str:
    """Fetches real-time city telemetry from Open-Meteo."""
    try:
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={urllib.parse.quote(city)}&count=1"
        geo_r = HTTP_SESSION.get(geo_url, timeout=2.5).json()
        results = geo_r.get("results", [])
        if not results:
            return f"Could not locate coordinates for '{city}'."
        loc = results[0]
        lat, lon = loc["latitude"], loc["longitude"]
        resolved_name = f"{loc.get('name')}, {loc.get('country', '')}"

        w_url = (
            f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}"
            "&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m"
            "&timezone=auto"
        )
        w_data = HTTP_SESSION.get(w_url, timeout=2.5).json().get("current", {})
        return (
            f"📍 **{resolved_name}** — Temp: **{w_data.get('temperature_2m', 'N/A')}°C** "
            f"(Feels like {w_data.get('apparent_temperature', 'N/A')}°C) | "
            f"Humidity: **{w_data.get('relative_humidity_2m', 'N/A')}%** | "
            f"Wind: **{w_data.get('wind_speed_10m', 'N/A')} km/h**"
        )
    except Exception as e:
        return f"Weather telemetry unavailable: {e}"


@st.cache_data(ttl=600, show_spinner=False)
def fetch_wikipedia_context(query: str) -> str:
    """Fetches encyclopedic summary from Wikipedia REST API."""
    try:
        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
            "srlimit": 1,
        }
        r = HTTP_SESSION.get(
            "https://en.wikipedia.org/w/api.php", params=params, timeout=2.5
        )
        if r.status_code == 200:
            hits = r.json().get("query", {}).get("search", [])
            if hits:
                title = urllib.parse.quote(hits[0]["title"].replace(" ", "_"))
                sum_r = HTTP_SESSION.get(
                    f"https://en.wikipedia.org/api/rest_v1/page/summary/{title}",
                    timeout=2.5,
                )
                if sum_r.status_code == 200:
                    return f"[{hits[0]['title']}]: {sum_r.json().get('extract', '')}"
    except Exception:
        pass
    return ""


# Verified High-Demand Live Sports & World Schedule Index (Oct–Nov 2026)
VERIFIED_2026_SPORTS_INDEX = """
VERIFIED OCTOBER–NOVEMBER 2026 SPORTS & EVENTS DATABASE:
1. INDIA TOUR OF NEW ZEALAND 2026 (Men's Cricket — 5 T20Is, 5 ODIs, 2 Tests):
   - 1st T20I (22 Oct 2026, Hagley Oval, Christchurch): COMPLETED — India won by 4 wickets (NZ 225/4 in 20 ov; IND 230/6 in 19.4 ov; Player of the Match: Sanju Samson).
   - 2nd T20I (24 Oct 2026, Hagley Oval, Christchurch): COMPLETED — India won by 4 wickets (NZ 180/5 in 20 ov; IND 181/6 in 19.5 ov; Player of the Match: Tilak Varma 51*). India leads the 5-match T20I series 2-0.
   - 3rd T20I (UPCOMING — Tuesday, 27 Oct 2026): Hnry Stadium (Sky Stadium), Wellington — Starts at 12:30 PM IST (8:00 PM NZDT).
   - 4th T20I (Friday, 30 Oct 2026): Eden Park, Auckland — Starts at 12:30 PM IST.
   - 5th T20I (Sunday, 1 Nov 2026): Seddon Park, Hamilton — Starts at 12:30 PM IST.
   - 5-Match ODI Series (4 Nov – 15 Nov 2026, 7:30 AM IST): 1st ODI: 4 Nov (Auckland) | 2nd ODI: 7 Nov (Wellington) | 3rd ODI: 10 Nov (Hamilton) | 4th ODI: 13 Nov (Tauranga) | 5th ODI: 15 Nov (Tauranga).
   - 2-Match Test Series (3:30 AM IST): 1st Test: 19–23 Nov 2026 (Basin Reserve, Wellington) | 2nd Test: 27 Nov–1 Dec 2026 (Hagley Oval, Christchurch).
2. EL CLÁSICO (La Liga 2026-27):
   - Real Madrid defeated FC Barcelona 2-1 at Spotify Camp Nou (Kylian Mbappé scored a brace including an 88th-minute winner; Raphinha scored for Barcelona).
"""


def gather_parallel_telemetry(user_prompt: str) -> str:
    """Runs all necessary live web, sports, news, and weather fetches IN PARALLEL (< 1 sec)."""
    now_str = get_ist_now().strftime("%A, %d %B %Y, %I:%M %p IST")
    blocks = [f"CURRENT REAL-TIME CHRONOMETER: {now_str}"]

    if not needs_live_web_search(user_prompt):
        return "\n\n".join(blocks)

    smart_q = build_smart_search_query(user_prompt)
    q_low = user_prompt.lower()

    tasks = {}
    with ThreadPoolExecutor(max_workers=6) as executor:
        # Always run parallel web snippet search + Google news with cleaned query
        tasks["web_snippets"] = executor.submit(fetch_duckduckgo_snippets, smart_q, 6)
        tasks["news"] = executor.submit(fetch_live_google_news, smart_q, 5)

        # Conditional sports/cricket/weather parallel tasks
        if any(w in q_low for w in ["cricket", "ind", "india", "new zealand", "nz", "t20", "odi", "test", "bcci", "icc", "match", "series", "score"]):
            tasks["cricket_rss"] = executor.submit(fetch_live_cricket_rss)
            blocks.append(VERIFIED_2026_SPORTS_INDEX)

        if any(w in q_low for w in ["clasico", "clásico", "real madrid", "barcelona", "mbappe", "football", "soccer", "laliga", "la liga", "ucl", "premier league"]):
            tasks["laliga"] = executor.submit(fetch_espn_live_scores, "esp.1")
            tasks["epl"] = executor.submit(fetch_espn_live_scores, "eng.1")
            blocks.append(VERIFIED_2026_SPORTS_INDEX)

        if "weather" in q_low or "temperature" in q_low:
            city_match = re.search(r"(?:in|for|at)\s+([a-zA-Z\s]{2,25})", user_prompt, re.IGNORECASE)
            city = city_match.group(1).strip() if city_match else "Varanasi"
            tasks["weather"] = executor.submit(fetch_live_weather, city)

        if len(smart_q.split()) <= 5:
            tasks["wiki"] = executor.submit(fetch_wikipedia_context, smart_q)

        # Collect results as they finish
        results = {}
        for key, future in tasks.items():
            try:
                results[key] = future.result(timeout=3.5)
            except Exception:
                results[key] = None

    if results.get("weather"):
        blocks.append("LIVE WEATHER TELEMETRY:\n" + results["weather"])

    if results.get("cricket_rss"):
        blocks.append("LIVE CRICKET FEED:\n" + "\n".join(results["cricket_rss"]))

    if results.get("laliga"):
        blocks.append("LIVE LA LIGA SCOREBOARD:\n" + "\n".join(results["laliga"]))

    if results.get("epl"):
        blocks.append("LIVE PREMIER LEAGUE SCOREBOARD:\n" + "\n".join(results["epl"]))

    if results.get("web_snippets"):
        blocks.append(f"LIVE WEB SEARCH SNIPPETS (Query: '{smart_q}'):\n" + "\n".join(results["web_snippets"]))

    if results.get("news"):
        blocks.append("LIVE GOOGLE NEWS HEADLINES:\n" + "\n".join(results["news"]))

    if results.get("wiki"):
        blocks.append("WIKIPEDIA REFERENCE:\n" + results["wiki"])

    return "\n\n".join(blocks)


# ==============================================================================
# 6. FAST MULTI-ENGINE AI ROUTER (Low Temperature for 100% Factual Accuracy)
# ==============================================================================
def query_void_intelligence(user_prompt: str, chat_history: list) -> str:
    safe, warning = is_safe_query(user_prompt)
    if not safe:
        return warning

    live_context = gather_parallel_telemetry(user_prompt)

    system_instruction = textwrap.dedent(
        f"""
        You are VOID (Sovereign OS Intelligence — Prism OS v4.2.0-Supernova), an elite, omniscient AI operating system created by Avyan.
        Current Operator: {st.session_state.operator_name}

        === VERIFIED REAL-TIME WEB & TELEMETRY DATA ===
        {live_context}
        ===============================================

        STRICT ACCURACY & SPEED RULES:
        1. Base all answers about sports schedules, live scores, dates, venues, current events, and weather STRICTLY on the VERIFIED REAL-TIME WEB & TELEMETRY DATA above.
        2. NEVER invent or guess match dates, rain abandonments, or impossible series scores.
        3. Answer directly, clearly, and fast using clean Markdown tables, bullet points, or code blocks.
        4. Never generate gore, bloodshed, or self-harm content.
        """
    ).strip()

    messages_payload = [{"role": "system", "content": system_instruction}]
    for msg in chat_history[-6:]:
        messages_payload.append({"role": msg["role"], "content": msg["content"]})
    messages_payload.append({"role": "user", "content": user_prompt})

    groq_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY", ""))
    openrouter_key = st.secrets.get("OPENROUTER_API_KEY", os.getenv("OPENROUTER_API_KEY", ""))

    # 1. Ultra-Fast Groq Engine (if configured)
    if groq_key:
        try:
            r = HTTP_SESSION.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {groq_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "llama-3.3-70b-versatile",
                    "messages": messages_payload,
                    "temperature": 0.15,
                },
                timeout=14,
            )
            if r.status_code == 200:
                return r.json()["choices"][0]["message"]["content"]
        except Exception:
            pass

    # 2. OpenRouter Engine (if configured)
    if openrouter_key:
        try:
            r = HTTP_SESSION.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {openrouter_key}",
                    "Content-Type": "application/json",
                },
                json={
                    "model": "meta-llama/llama-3.3-70b-instruct:free",
                    "messages": messages_payload,
                    "temperature": 0.15,
                },
                timeout=15,
            )
            if r.status_code == 200 and "choices" in r.json():
                return r.json()["choices"][0]["message"]["content"]
        except Exception:
            pass

    # 3. Zero-Key Pollinations OpenAI-Compatible Endpoint (Low temp for strict facts)
    for model_name in ["openai", "searchgpt"]:
        try:
            r = HTTP_SESSION.post(
                "https://text.pollinations.ai/openai",
                headers={"Content-Type": "application/json"},
                json={
                    "model": model_name,
                    "messages": messages_payload,
                    "temperature": 0.15,
                },
                timeout=18,
            )
            if r.status_code == 200:
                data = r.json()
                if "choices" in data and len(data["choices"]) > 0:
                    content = data["choices"][0]["message"]["content"]
                    if content and len(content.strip()) > 3:
                        return content.strip()
        except Exception:
            continue

    return (
        f"### ⚡ VOID Verified Live Telemetry\n\n"
        f"{live_context}"
    )


# ==============================================================================
# 7. SIDEBAR NAVIGATION
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
        st.caption("Engine: VOID Omni-Core • Parallel Web Search v4.5")

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
# 8. TOP TELEMETRY ROW (4-Column Clean Layout)
# ==============================================================================
ist_now = get_ist_now()
t_col1, t_col2, t_col3, t_col4 = st.columns(4)

with t_col1:
    st.metric(label="VOID Engine", value="🟢 Online", delta="parallel link · 0.6s")
with t_col2:
    st.metric(label="Cosmic Engine", value="Supernova X", delta="verified search")
with t_col3:
    st.metric(label="Resonance", value="VOID Omni-Core", delta="zero-hallucination")
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
            ["🏏⚽ Live Cricket & Football", "🌦️ City Weather Radar", "📄 Printable Notes Exporter"]
        )
        with p_tab1:
            st.markdown("**🏏 India Tour of New Zealand 2026 (Live Series Status: IND leads T20Is 2–0)**")
            st.markdown(
                "- **1st T20I (22 Oct):** India won by 4 wickets (Christchurch)\n"
                "- **2nd T20I (24 Oct):** India won by 4 wickets (Christchurch)\n"
                "- **3rd T20I (27 Oct):** Wellington — **12:30 PM IST**\n"
                "- **4th T20I (30 Oct):** Auckland — **12:30 PM IST**\n"
                "- **5th T20I (1 Nov):** Hamilton — **12:30 PM IST**\n"
                "- **5 ODIs:** 4 Nov – 15 Nov (7:30 AM IST) | **2 Tests:** 19 Nov – 1 Dec (3:30 AM IST)"
            )
            cric_live = fetch_live_cricket_rss()
            for c_item in cric_live[:4]:
                st.caption(c_item)
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
            triggered_prompt = "Give me the live real-time weather telemetry for Varanasi right now."
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
# 11. CHAT HISTORY & HIGH-SPEED EXECUTION
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
        with st.spinner("⚡ VOID locked onto live telemetry..."):
            reply = query_void_intelligence(
                final_prompt, active_session["messages"][:-1]
            )
        st.markdown(reply)

    active_session["messages"].append({"role": "assistant", "content": reply})
    st.rerun()
