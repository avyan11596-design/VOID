import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import os
import uuid
import base64
import re
import random
import textwrap
from datetime import datetime, timezone, timedelta

# --- 1. AUTO-GENERATE CUSTOM VOID LOGO FILE ---
SVG_RAW = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#4facfe"/><stop offset="100%" stop-color="#9b51e0"/></linearGradient></defs><rect width="120" height="120" rx="28" fill="#0b0e14" stroke="url(#g)" stroke-width="6"/><path d="M34 38 L60 86 L86 38" fill="none" stroke="url(#g)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><circle cx="60" cy="34" r="7" fill="#ffffff"/></svg>'
LOGO_B64 = "data:image/svg+xml;base64," + base64.b64encode(SVG_RAW.encode("utf-8")).decode("utf-8")

if not os.path.exists("void_logo.svg"):
    try:
        with open("void_logo.svg", "w", encoding="utf-8") as f:
            f.write(SVG_RAW)
    except Exception:
        pass

LOGO_PATH = "logo.png" if os.path.exists("logo.png") else ("void_logo.svg" if os.path.exists("void_logo.svg") else "⚡")

st.set_page_config(
    page_title="VOID — Cosmic Architecture & Creation Engine",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    if LOGO_PATH != "⚡":
        st.logo(LOGO_PATH)
except Exception:
    pass

# --- 2. PURE VOID ULTRA-DARK GLASS CSS & SEO ---
st.markdown("""
<head>
    <meta name="description" content="VOID is a next-generation digital workspace, scholastic codex, PDF/Slide forge, and live web studio architected by Avyan.">
    <meta name="keywords" content="VOID, Avyan, VoidOS, VOID Studio, VOID Codex, Web Studio">
    <meta name="author" content="Avyan">
</head>
<style>
div[data-testid="stToolbarActions"] { display: none !important; }
div[data-testid="stAppDeployButton"] { display: none !important; }
div[data-testid="stDecoration"] { display: none !important; }
div[data-testid="stStatusWidget"] { display: none !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
header[data-testid="stHeader"] { background: transparent !important; }

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2.5rem !important;
    max-width: 1380px;
}
section[data-testid="stSidebar"] {
    background-color: #07090e;
    border-right: 1px solid rgba(79, 172, 254, 0.14);
}
.stChatMessage {
    border-radius: 16px;
    padding: 16px 20px;
    margin-bottom: 12px;
    border: 1px solid rgba(79, 172, 254, 0.14);
    background: rgba(13, 16, 23, 0.82);
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.28);
}
.prism-card {
    background: #0b0f17;
    border: 1px solid rgba(79, 172, 254, 0.3);
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.45);
}
.void-hero {
    text-align: center;
    padding: 24px 10px 18px 10px;
}
.void-gradient {
    font-size: 2.6rem;
    font-weight: 800;
    letter-spacing: -0.5px;
    background: linear-gradient(135deg, #4facfe 0%, #00f2fe 45%, #a18cd1 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
}
.void-sub {
    font-size: 1.08rem;
    color: #8b949e;
    margin-bottom: 20px;
}
.topbar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 14px;
}
.topbar-title {
    font-size: 1.4rem;
    font-weight: 800;
    letter-spacing: 2px;
    color: #ffffff;
}
.topbar-pill {
    font-size: 0.65rem;
    padding: 3px 9px;
    border-radius: 99px;
    background: rgba(79, 172, 254, 0.15);
    color: #4facfe;
    border: 1px solid rgba(79, 172, 254, 0.35);
    font-weight: 700;
}
.stButton button {
    border-radius: 12px !important;
    border: 1px solid rgba(128, 128, 128, 0.22) !important;
    transition: all 0.2s ease !important;
}
.stButton button:hover {
    border-color: #4facfe !important;
    box-shadow: 0 0 12px rgba(79, 172, 254, 0.25) !important;
}
</style>
""", unsafe_allow_html=True)

# --- 3. PERSISTENT DATABASE & SECRETS ---
DB_FILE = "void_hub_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {"users": {}, "chats": {}}

def save_db(db_data):
    try:
        with open(DB_FILE, "w", encoding="utf-8") as f:
            json.dump(db_data, f, indent=2)
    except Exception:
        pass

db = load_db()

try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    API_KEY = ""

try:
    EMAILJS_SERVICE_ID = st.secrets["EMAILJS_SERVICE_ID"]
    EMAILJS_TEMPLATE_ID = st.secrets["EMAILJS_TEMPLATE_ID"]
    EMAILJS_PUBLIC_KEY = st.secrets["EMAILJS_PUBLIC_KEY"]
    EMAILJS_PRIVATE_KEY = st.secrets["EMAILJS_PRIVATE_KEY"]
except Exception:
    EMAILJS_SERVICE_ID = ""
    EMAILJS_TEMPLATE_ID = ""
    EMAILJS_PUBLIC_KEY = ""
    EMAILJS_PRIVATE_KEY = ""

# --- 4. SMART INTENT DETECTOR (NO PDF SPAM ON NORMAL CHAT) ---
def detect_prism_intent(user_prompt, reply_text=""):
    """Returns True ONLY when the user explicitly wants a PDF, study notes, slides/PPT, report, or web app."""
    p = user_prompt.lower()
    doc_triggers = [
        "pdf", "ppt", "powerpoint", "slide", "presentation", "study notes",
        "revision notes", "make notes", "write notes", "study guide", "cheat sheet",
        "exam questions", "question bank", "worksheet", "report", "document",
        "build a web app", "build an app", "create a web app", "html app", "make a game"
    ]
    if any(t in p for t in doc_triggers):
        return True
    if "```html" in reply_text.lower():
        return True
    return False

# --- 5. NATIVE PURE-PYTHON REAL PDF (.PDF) & SLIDE FORGE ---
def clean_for_pdf(text):
    replacements = {
        "—": "-", "–": "-", "“": '"', "”": '"', "‘": "'", "’": "'",
        "•": "*", "…": "...", "→": "->", "⚡": "[*]", "✦": "[*]",
        "🌙": "", "🪐": "", "☀️": "", "📖": "", "📄": "", "📊": ""
    }
    for k, v in replacements.items():
        text = text.replace(k, v)
    return text.encode("latin-1", "replace").decode("latin-1")

def escape_pdf_text(s):
    return s.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")

def generate_real_pdf_bytes(title, markdown_content, author="VOID Forge"):
    """Generates a genuine multi-page binary PDF-1.4 file with zero external dependencies."""
    clean_title = clean_for_pdf(title)
    raw_lines = clean_for_pdf(markdown_content).split("\n")

    styled_lines = [
        ("TITLE", clean_title),
        ("META", f"Architected by {author} | {datetime.now().strftime('%Y-%m-%d %H:%M')}"),
        ("SPACE", "")
    ]
    for line in raw_lines:
        stripped = line.strip()
        if not stripped:
            styled_lines.append(("SPACE", ""))
            continue
        if stripped.startswith("#"):
            hdr = stripped.lstrip("#").strip()
            for w in textwrap.wrap(hdr, width=68) or [hdr]:
                styled_lines.append(("H1", w))
        elif stripped.startswith(("* ", "- ", "+ ")):
            body = stripped[2:].replace("**", "")
            wrapped = textwrap.wrap(body, width=78) or [body]
            styled_lines.append(("BULLET", "* " + wrapped[0]))
            for w in wrapped[1:]:
                styled_lines.append(("BODY", "  " + w))
        else:
            clean_line = stripped.replace("**", "").replace("__", "").replace("`", "")
            for w in textwrap.wrap(clean_line, width=82) or [clean_line]:
                styled_lines.append(("BODY", w))

    pages_ops = []
    current_ops = ["BT"]
    y = 790
    for ltype, ltext in styled_lines:
        if y < 60:
            current_ops.append("ET")
            pages_ops.append("\n".join(current_ops))
            current_ops = ["BT"]
            y = 790
        esc = escape_pdf_text(ltext)
        if ltype == "TITLE":
            current_ops.append(f"/F2 16 Tf 1 0 0 1 50 {y} Tm ({esc}) Tj")
            y -= 24
        elif ltype == "META":
            current_ops.append(f"/F1 9 Tf 1 0 0 1 50 {y} Tm ({esc}) Tj")
            y -= 18
        elif ltype == "H1":
            y -= 6
            current_ops.append(f"/F2 13 Tf 1 0 0 1 50 {y} Tm ({esc}) Tj")
            y -= 18
        elif ltype == "BULLET":
            current_ops.append(f"/F1 10.5 Tf 1 0 0 1 56 {y} Tm ({esc}) Tj")
            y -= 15
        elif ltype == "BODY":
            current_ops.append(f"/F1 10.5 Tf 1 0 0 1 50 {y} Tm ({esc}) Tj")
            y -= 15
        elif ltype == "SPACE":
            y -= 9

    current_ops.append("ET")
    pages_ops.append("\n".join(current_ops))

    objects = []
    num_pages = len(pages_ops)
    page_obj_ids = [5 + i * 2 for i in range(num_pages)]
    kids_str = " ".join(f"{pid} 0 R" for pid in page_obj_ids)

    objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    objects.append(f"2 0 obj\n<< /Type /Pages /Kids [{kids_str}] /Count {num_pages} >>\nendobj\n".encode("latin-1"))
    objects.append(b"3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>\nendobj\n")
    objects.append(b"4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>\nendobj\n")

    for i, stream_str in enumerate(pages_ops):
        page_id = 5 + i * 2
        content_id = page_id + 1
        stream_bytes = stream_str.encode("latin-1")
        page_obj = (
            f"{page_id} 0 obj\n"
            f"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
            f"/Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> "
            f"/Contents {content_id} 0 R >>\nendobj\n"
        ).encode("latin-1")
        content_obj = (
            f"{content_id} 0 obj\n<< /Length {len(stream_bytes)} >>\nstream\n".encode("latin-1")
            + stream_bytes
            + b"\nendstream\nendobj\n"
        )
        objects.append(page_obj)
        objects.append(content_obj)

    pdf_bytes = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = []
    for obj in objects:
        offsets.append(len(pdf_bytes))
        pdf_bytes.extend(obj)

    xref_pos = len(pdf_bytes)
    total_objs = len(objects) + 1
    pdf_bytes.extend(f"xref\n0 {total_objs}\n0000000000 65535 f \n".encode("latin-1"))
    for off in offsets:
        pdf_bytes.extend(f"{off:010d} 00000 n \n".encode("latin-1"))

    pdf_bytes.extend(
        f"trailer\n<< /Size {total_objs} /Root 1 0 R >>\nstartxref\n{xref_pos}\n%%EOF".encode("latin-1")
    )
    return bytes(pdf_bytes)

def generate_interactive_slides_html(title, markdown_text):
    """Compiles structured content into an interactive VOID Slide Deck."""
    sections = re.split(r"\n(?=## |\n# )", markdown_text.strip())
    if len(sections) <= 1:
        paragraphs = [p.strip() for p in markdown_text.split("\n\n") if p.strip()]
        sections = ["\n\n".join(paragraphs[i:i+2]) for i in range(0, len(paragraphs), 2)] or [markdown_text]

    slides_html = ""
    for idx, sec in enumerate(sections):
        lines = sec.strip().split("\n")
        slide_heading = lines[0].lstrip("#").strip() if lines else f"Slide {idx+1}"
        body_lines = lines[1:] if len(lines) > 1 else lines
        body_html = "<br>".join([re.sub(r"\*\*(.*?)\*\*", r"<b>\1</b>", l) for l in body_lines])
        slides_html += f"""
        <div class="slide" style="display: {'block' if idx == 0 else 'none'};">
            <div class="slide-badge">VOID PRISM DECK • SLIDE {idx+1} OF {len(sections)}</div>
            <h2>{slide_heading}</h2>
            <div class="slide-body">{body_html}</div>
        </div>
        """

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
        body {{
            margin: 0; padding: 0; background: #080b12; color: #f0f6fc;
            font-family: 'Segoe UI', system-ui, sans-serif; display: flex;
            flex-direction: column; height: 96vh; justify-content: space-between;
        }}
        .slide-container {{
            flex: 1; display: flex; align-items: center; justify-content: center; padding: 24px;
        }}
        .slide {{
            width: 100%; max-width: 780px; background: linear-gradient(145deg, #101624, #0b0f17);
            border: 1px solid rgba(79,172,254,0.35); border-radius: 20px; padding: 36px 42px;
            box-shadow: 0 15px 40px rgba(0,0,0,0.6); min-height: 290px;
        }}
        .slide-badge {{
            font-size: 11px; letter-spacing: 1.5px; color: #4facfe; font-weight: 700; margin-bottom: 12px;
        }}
        h2 {{
            margin-top: 0; font-size: 26px;
            background: linear-gradient(90deg, #4facfe, #c471ed);
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        }}
        .slide-body {{ font-size: 16px; line-height: 1.65; color: #c9d1d9; }}
        .controls {{
            display: flex; justify-content: center; gap: 14px; padding: 12px;
        }}
        button {{
            background: rgba(79,172,254,0.15); color: #4facfe; border: 1px solid rgba(79,172,254,0.4);
            padding: 8px 20px; border-radius: 99px; cursor: pointer; font-weight: 600;
        }}
        button:hover {{ background: #4facfe; color: #080b12; }}
    </style>
    </head>
    <body>
        <div class="slide-container">{slides_html}</div>
        <div class="controls">
            <button onclick="move(-1)">◀ Previous</button>
            <button onclick="window.print()">🖨️ Export Slides to PDF</button>
            <button onclick="move(1)">Next ▶</button>
        </div>
        <script>
            let cur = 0;
            const slides = document.querySelectorAll('.slide');
            function move(dir) {{
                slides[cur].style.display = 'none';
                cur = (cur + dir + slides.length) % slides.length;
                slides[cur].style.display = 'block';
            }}
            document.addEventListener('keydown', (e) => {{
                if (e.key === 'ArrowRight') move(1);
                if (e.key === 'ArrowLeft') move(-1);
            }});
        </script>
    </body>
    </html>
    """

# --- 6. LIVE WORLD TELEMETRY (REAL-TIME WEATHER, CLOCK & ENCYCLOPEDIA) ---
def fetch_live_weather(city_name="Varanasi"):
    try:
        geo_url = f"[https://geocoding-api.open-meteo.com/v1/search?name=](https://geocoding-api.open-meteo.com/v1/search?name=){city_name}&count=1&language=en&format=json"
        geo_res = requests.get(geo_url, timeout=5).json()
        if "results" in geo_res and geo_res["results"]:
            loc = geo_res["results"][0]
            lat, lon = loc["latitude"], loc["longitude"]
            resolved_name = f"{loc.get('name', city_name)}, {loc.get('admin1', '')}, {loc.get('country', '')}"
        else:
            lat, lon, resolved_name = 25.3176, 82.9739, "Varanasi, Uttar Pradesh, India"

        w_url = (
            f"[https://api.open-meteo.com/v1/forecast?latitude=](https://api.open-meteo.com/v1/forecast?latitude=){lat}&longitude={lon}"
            f"&current=temperature_2m,relative_humidity_2m,apparent_temperature,weather_code,wind_speed_10m"
            f"&daily=temperature_2m_max,temperature_2m_min&timezone=auto"
        )
        w_data = requests.get(w_url, timeout=5).json()
        cur = w_data.get("current", {})
        daily = w_data.get("daily", {})
        w_codes = {
            0: "Clear sky", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
            45: "Foggy", 51: "Light drizzle", 61: "Light rain", 63: "Moderate rain",
            65: "Heavy rain", 80: "Rain showers", 95: "Thunderstorm"
        }
        desc = w_codes.get(cur.get("weather_code", 0), "Partly cloudy")
        max_t = daily.get("temperature_2m_max", ["N/A"])[0]
        min_t = daily.get("temperature_2m_min", ["N/A"])[0]
        return (
            f"[LIVE TELEMETRY — {resolved_name}]: "
            f"Sky: {desc} | Temp: {cur.get('temperature_2m')}°C "
            f"(Feels like {cur.get('apparent_temperature')}°C) | "
            f"High/Low: {max_t}°C / {min_t}°C | "
            f"Humidity: {cur.get('relative_humidity_2m')}% | Wind: {cur.get('wind_speed_10m')} km/h."
        )
    except Exception as e:
        return f"[Telemetry Offline]: ({e})"

def fetch_live_knowledge(query):
    try:
        clean_q = re.sub(r"[^a-zA-Z0-9\s]", "", query).strip()
        if len(clean_q) < 3:
            return ""
        search_url = f"[https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=](https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch=){clean_q}&utf8=&format=json&srlimit=2"
        headers = {"User-Agent": "VOIDCore/3.0"}
        s_res = requests.get(search_url, headers=headers, timeout=4).json()
        results = s_res.get("query", {}).get("search", [])
        if not results:
            return ""
        snippets = [re.sub(r"<.*?>", "", r.get("snippet", "")) for r in results]
        return f"[LIVE ARCHIVE DATA]: {' | '.join(snippets)}"
    except Exception:
        return ""

def build_live_sensor_context(user_prompt, default_city="Varanasi"):
    ist_now = datetime.now(timezone(timedelta(hours=5, minutes=30)))
    sensor_lines = [f"[VOID CHRONOMETER]: {ist_now.strftime('%A, %B %d, %Y | %I:%M %p IST')}"]

    lower_p = user_prompt.lower()
    weather_triggers = ["weather", "temperature", "temp", "rain", "forecast", "climate", "outside", "cold", "hot", "humidity"]
    if any(t in lower_p for t in weather_triggers):
        city_match = re.search(r"(?:in|at|for|of)\s+([a-zA-Z\s]{3,20})", lower_p)
        target_city = city_match.group(1).strip() if city_match else default_city
        sensor_lines.append(fetch_live_weather(target_city))
    else:
        sensor_lines.append(fetch_live_weather(default_city))

    if any(k in lower_p for k in ["who is", "what is", "tell me about", "history of", "explain", "news", "search"]):
        wiki_ctx = fetch_live_knowledge(user_prompt)
        if wiki_ctx:
            sensor_lines.append(wiki_ctx)

    return "\n".join(sensor_lines)

# --- 7. EMAILJS OTP GATEWAY & COSMIC ENGINES ---
def send_otp_email(receiver_email, otp_code):
    if not EMAILJS_SERVICE_ID or not EMAILJS_TEMPLATE_ID or not EMAILJS_PUBLIC_KEY:
        return False, "EmailJS credentials missing in Streamlit Secrets."
    try:
        url = "[https://api.emailjs.com/api/v1.0/email/send](https://api.emailjs.com/api/v1.0/email/send)"
        payload = {
            "service_id": EMAILJS_SERVICE_ID.strip(),
            "template_id": EMAILJS_TEMPLATE_ID.strip(),
            "user_id": EMAILJS_PUBLIC_KEY.strip(),
            "accessToken": EMAILJS_PRIVATE_KEY.strip(),
            "template_params": {
                "to_email": receiver_email,
                "otp_code": otp_code
            }
        }
        r = requests.post(url, json=payload, timeout=30)
        if r.status_code == 200:
            return True, None
        return False, r.text
    except Exception as e:
        return False, str(e)

COSMIC_OBJECTS = {
    "🌙 Void Moon (Swift Resonance)": "google/gemini-2.5-flash",
    "🪐 Nebula Core (Deep Logic)": "deepseek/deepseek-chat",
    "☀️ Supernova X (Master Architect)": "qwen/qwen-2.5-coder-32b-instruct"
}

def call_void_engine(cosmic_choice, system_prompt, messages_list, temp=0.25, tokens=2000):
    if not API_KEY:
        return None, "⚠️ Master Key missing in Streamlit Secrets (`OPENROUTER_API_KEY`)."
    target_slug = COSMIC_OBJECTS.get(cosmic_choice, "google/gemini-2.5-flash")
    headers = {
        "Authorization": f"Bearer {API_KEY.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "[https://void-ai-hub.streamlit.app](https://void-ai-hub.streamlit.app)",
        "X-Title": "VOID"
    }
    clean_msgs = [{"role": m["role"], "content": m["content"]} for m in messages_list]
    payload = [{"role": "system", "content": system_prompt}] + clean_msgs
    data = {"model": target_slug, "messages": payload, "temperature": temp, "max_tokens": tokens}
    try:
        r = requests.post("[https://openrouter.ai/api/v1/chat/completions](https://openrouter.ai/api/v1/chat/completions)", headers=headers, json=data, timeout=60)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"], None
        return None, f"Resonance Error ({r.status_code}): {r.text}"
    except Exception as e:
        return None, f"Cosmic Link Interrupted: {e}"

def extract_code_blocks(markdown_text):
    return re.findall(r"```(\w+)?\n(.*?)```", markdown_text, re.DOTALL)

# --- 8. PERSISTENT AUTHENTICATION GATE ---
if "user_email" not in st.session_state and "user" in st.query_params:
    st.session_state.user_email = st.query_params["user"]

if "user_email" not in st.session_state:
    st.markdown(f'<div class="void-hero"><img src="{LOGO_B64}" width="72" style="margin-bottom:14px;"/><div class="void-gradient">Welcome to VOID</div><div class="void-sub">Secure OTP Authentication Gateway</div></div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        if "pending_email" not in st.session_state:
            with st.form("email_form"):
                email_input = st.text_input("Enter your Email Address", placeholder="name@example.com").strip().lower()
                name_input = st.text_input("Your Display Name", placeholder="Avyan").strip()
                send_btn = st.form_submit_button("Send Verification Code", type="primary", use_container_width=True)
                
                if send_btn:
                    if "@" in email_input and "." in email_input and len(email_input) > 5:
                        generated_otp = str(random.randint(100000, 999999))
                        success, err = send_otp_email(email_input, generated_otp)
                        if success:
                            st.session_state.pending_email = email_input
                            st.session_state.pending_name = name_input or ("Avyan" if "avyan" in email_input else email_input.split("@")[0].capitalize())
                            st.session_state.target_otp = generated_otp
                            st.success(f"Verification code sent to `{email_input}`!")
                            st.rerun()
                        else:
                            st.error(f"Failed to send email: {err}")
                    else:
                        st.error("Please enter a valid email address.")
        else:
            st.info(f"Verification dispatched to: **{st.session_state.pending_email}**")
            with st.form("otp_form"):
                entered_otp = st.text_input("Enter 6-Digit OTP Code", placeholder="123456", max_chars=6)
                verify_btn = st.form_submit_button("Verify & Enter VOID", type="primary", use_container_width=True)
                back_btn = st.form_submit_button("Use a Different Email")
                
                if back_btn:
                    del st.session_state.pending_email
                    del st.session_state.target_otp
                    st.rerun()
                    
                if verify_btn:
                    if entered_otp.strip() == st.session_state.target_otp:
                        email_input = st.session_state.pending_email
                        chosen_name = st.session_state.get("pending_name", email_input.split("@")[0].capitalize())
                        now_str = datetime.now().strftime("%b %d, %H:%M")
                        
                        is_creator = ("avyan" in email_input.lower()) or (chosen_name.lower() == "avyan")
                        default_mem = (
                            "Founder & Lead Architect of VOID, 14-year-old Class 8 student at Sunbeam School Varuna in Varanasi, creator of VoidOS, author of World Zero."
                            if is_creator else f"Verified member of VOID Studio ({chosen_name})."
                        )
                        
                        if email_input not in db["users"]:
                            db["users"][email_input] = {
                                "name": "Avyan" if is_creator else chosen_name,
                                "city": "Varanasi",
                                "memory": default_mem,
                                "joined": now_str,
                                "last_active": now_str,
                                "prompts": 0
                            }
                        else:
                            db["users"][email_input]["last_active"] = now_str
                            if chosen_name:
                                db["users"][email_input]["name"] = "Avyan" if is_creator else chosen_name
                            
                        if email_input not in db["chats"] or not db["chats"][email_input]:
                            first_id = str(uuid.uuid4())[:8]
                            db["chats"][email_input] = {first_id: {"title": "New Session", "messages": []}}
                            
                        save_db(db)
                        st.session_state.user_email = email_input
                        st.query_params["user"] = email_input
                        st.session_state.current_chat_id = list(db["chats"][email_input].keys())[-1]
                        
                        del st.session_state.pending_email
                        del st.session_state.target_otp
                        st.rerun()
                    else:
                        st.error("❌ Incorrect code. Please check your inbox and try again.")
    st.stop()

# --- 9. ACTIVE USER IDENTITY vs FOUNDER IDENTITY ---
user_email = st.session_state.user_email
is_founder_account = "avyan" in user_email.lower()

user_record = db["users"].setdefault(user_email, {
    "name": "Avyan" if is_founder_account else user_email.split("@")[0].capitalize(),
    "city": "Varanasi",
    "memory": (
        "Founder & Lead Architect of VOID, 14-year-old Class 8 student at Sunbeam School Varuna in Varanasi, creator of VoidOS, author of World Zero."
        if is_founder_account else "Verified Guest on VOID."
    ),
    "joined": datetime.now().strftime("%b %d, %H:%M"),
    "last_active": datetime.now().strftime("%b %d, %H:%M"),
    "prompts": 0
})

user_name = user_record.get("name", "Avyan" if is_founder_account else user_email.split("@")[0].capitalize())
user_city = user_record.get("city", "Varanasi")
user_memory = user_record.get("memory", "")

user_chats = db["chats"].setdefault(user_email, {})
if not user_chats:
    new_id = str(uuid.uuid4())[:8]
    user_chats[new_id] = {"title": "New Session", "messages": []}
    save_db(db)

if "current_chat_id" not in st.session_state or st.session_state.current_chat_id not in user_chats:
    st.session_state.current_chat_id = list(user_chats.keys())[-1]

current_chat_id = st.session_state.current_chat_id
current_chat = user_chats[current_chat_id]

# --- 10. LEFT SIDEBAR (SESSIONS, PRISM TOGGLE, IDENTITY VAULT, FOUNDER PROFILE) ---
with st.sidebar:
    st.markdown(f'<div class="topbar-brand"><img src="{LOGO_B64}" width="32"/><span class="topbar-title">VOID</span><span class="topbar-pill">PRISM OS</span></div>', unsafe_allow_html=True)

    if st.button("✦ New Session", type="primary", use_container_width=True):
        new_id = str(uuid.uuid4())[:8]
        user_chats[new_id] = {"title": "New Session", "messages": []}
        st.session_state.current_chat_id = new_id
        st.session_state.active_prism_text = None
        save_db(db)
        st.rerun()

    prism_open = st.toggle("⚡ Open VOID Prism Panel", value=bool(st.session_state.get("active_prism_text")))

    st.markdown("##### Active Sessions")
    for c_id, c_data in reversed(list(user_chats.items())):
        col_t, col_d = st.columns([5, 1])
        with col_t:
            prefix = "● " if c_id == current_chat_id else "💬 "
            if st.button(f"{prefix}{c_data['title']}", key=f"c_{c_id}", use_container_width=True):
                st.session_state.current_chat_id = c_id
                st.rerun()
        with col_d:
            if len(user_chats) > 1:
                if st.button("✕", key=f"d_{c_id}"):
                    del user_chats[c_id]
                    if c_id == current_chat_id:
                        st.session_state.current_chat_id = list(user_chats.keys())[-1]
                    save_db(db)
                    st.rerun()

    st.markdown("---")
    with st.expander("🧬 Core Identity Vault", expanded=False):
        new_name = st.text_input("Your Display Name", value=user_name)
        new_city = st.text_input("Your Default City (Live Weather)", value=user_city)
        new_mem = st.text_area("Your Personal Notes", value=user_memory, height=100)
        if st.button("💾 Lock into VOID Core", use_container_width=True):
            user_record["name"] = new_name.strip() or user_name
            user_record["city"] = new_city.strip() or "Varanasi"
            user_record["memory"] = new_mem.strip()
            save_db(db)
            st.success("Identity synced!")
            st.rerun()

    with st.expander("👑 Founder Profile"):
        st.markdown("""
        **Avyan** (`×͜× ᴠᴏɪᴅ ᴀᴠʏᴀɴ ࿐`)  
        *Founder & Lead Architect of VOID*  
        
        * **Status:** 14 years old, Class 8 at Sunbeam School Varuna, Varanasi.
        * **Architecture:** Creator of VOID Studio, lightweight VoidOS, and author of *World Zero*.
        * **Discipline:** Calisthenics strength training, custom hardware, and competitive gaming (`NOTREFLEXGAMING05`).
        """)

    with st.expander(f"👥 Crew Activity ({len(db['users'])})"):
        for u_mail, u_info in db["users"].items():
            st.markdown(f"**{u_info.get('name', 'Member')}** (`{u_mail}`)  \n<small>Prompts: {u_info.get('prompts', 0)} • {u_info.get('last_active', '')}</small>", unsafe_allow_html=True)

    st.caption(f"Operator: **{user_name}** (`{user_email}`)")
    if st.button("Switch Account", use_container_width=True):
        if "user" in st.query_params:
            del st.query_params["user"]
        del st.session_state.user_email
        st.rerun()

# --- 11. TOP COMMAND BAR ---
top_c1, top_c2, top_c3, top_c4 = st.columns([1.9, 1.8, 1.7, 1.2])
with top_c1:
    ui_mode = st.selectbox(
        "Dimension",
        ["✦ VOID Core & Prism", "📖 VOID Codex (Study, PDF & Slides)", "⚡ Live Web App Studio", "🛠️ Side-by-Side Code Lab"],
        label_visibility="collapsed"
    )
with top_c2:
    cosmic_entity = st.selectbox(
        "Cosmic Engine",
        list(COSMIC_OBJECTS.keys()),
        label_visibility="collapsed"
    )
with top_c3:
    persona = st.selectbox(
        "Resonance Mode",
        ["✦ VOID Omni (Universal)", "🎓 Master Scholastic Tutor", "💻 Full-Stack Architect", "🎨 UI & Slide Designer", "🐞 Deep Bug Hunter"],
        label_visibility="collapsed"
    )
with top_c4:
    with st.popover("➕ Attach & Tune", use_container_width=True):
        uploaded_file = st.file_uploader("Attach Code / Text", type=["py", "js", "html", "css", "json", "txt", "md", "cpp"])
        file_context = ""
        if uploaded_file:
            try:
                file_context = uploaded_file.read().decode("utf-8")
                st.success(f"Loaded `{uploaded_file.name}`")
            except Exception:
                st.error("Unable to read file.")
        task_depth = st.select_slider("Depth", options=["Swift", "Balanced", "Maximum Power"], value="Maximum Power")
        temperature = st.slider("Creativity", 0.0, 1.0, 0.25, 0.05)
        max_tokens = st.slider("Max Output Capacity", 500, 4000, 2200, 100)

# Master System Prompt with strict Founder vs. Guest separation & zero external brand names
def build_master_system_prompt(user_query, is_prism_task=False, extra_instructions=""):
    live_sensors = build_live_sensor_context(user_query, default_city=user_city)
    formatting_rule = (
        "The user is requesting a formal document, study guide, PDF, slide presentation, or web app. Structure your output with clean Markdown headings (# and ##) and bullet points so VOID Prism can compile it into a downloadable PDF and interactive slide deck."
        if is_prism_task else
        "Respond naturally, directly, and conversationally. Do NOT format casual chat messages as formal reports or PDFs unless the user explicitly asks for a PDF, notes, or slides."
    )
    return f"""You are VOID, a sovereign, ultra-powerful cosmic intelligence and digital workspace created solely by Avyan.
Never refer to yourself using any external company or model names—you are strictly VOID, powered by the Cosmic Engines (Void Moon, Nebula Core, and Supernova X).

=== 1. WHO IS USING VOID RIGHT NOW (CURRENT OPERATOR) ===
- Logged-In Operator Name: {user_name}
- Logged-In Operator Email: {user_email}
- Operator City: {user_city}
- Operator Memory Profile: {user_memory}
RULE: If the user asks "Who am I?" or "What is my name?", tell them they are **{user_name}** (signed in via `{user_email}`) and share their specific Operator Memory Profile above.

=== 2. WHO CREATED VOID (THE FOUNDER & ARCHITECT: AVYAN) ===
- Founder Name: Avyan (Handle: `×͜× ᴠᴏɪᴅ ᴀᴠʏᴀɴ ࿐`)
- Founder Bio: 14-year-old Founder & Lead Architect of VOID, studying in Class 8 at Sunbeam School Varuna in Varanasi. Creator of the lightweight VoidOS concept, author of the adventure book 'World Zero' set in the Sea of Ciphers, dedicated calisthenics athlete (5:30 AM Winter Arc discipline), and gamer (`NOTREFLEXGAMING05`).
RULE: If anyone (whether Avyan himself or one of his friends) asks "Who is Avyan?", "Who created VOID?", "Who made you?", or "Who is the founder?", proudly present Avyan's full Founder Bio above!

=== 3. LIVE WORLD TELEMETRY ===
{live_sensors}
Use this exact real-time telemetry whenever asked about the current weather, temperature, time, or date.

=== 4. RESPONSE STYLE ===
- Active Resonance Mode: {persona} | Depth: {task_depth}
- {formatting_rule}
{extra_instructions}"""

# =========================================================
# DIMENSION 1: ✦ VOID CORE & PRISM
# =========================================================
if ui_mode == "✦ VOID Core & Prism":
    if prism_open:
        chat_col, prism_col = st.columns([1.18, 1], gap="large")
    else:
        chat_col = st.container()
        prism_col = None

    quick_prompt = None

    with chat_col:
        if not current_chat["messages"]:
            st.markdown(f'<div class="void-hero"><img src="{LOGO_B64}" width="58" style="margin-bottom:10px;"/><div class="void-gradient">Welcome, {user_name}</div><div class="void-sub">VOID Core • Live Telemetry • On-Demand Prism Forge</div></div>', unsafe_allow_html=True)

            s1, s2, s3, s4 = st.columns(4)
            with s1:
                if st.button("🌦️ Live Weather\n\nReal-time city scan", use_container_width=True):
                    quick_prompt = f"What is the exact live weather and temperature right now in {user_city}?"
            with s2:
                if st.button("📄 Forge Study PDF\n\nNotes + Real PDF export", use_container_width=True):
                    quick_prompt = "Make a complete Class 8 Science study guide PDF on Force and Pressure with definitions, formulas, and exam questions."
            with s3:
                if st.button("⚡ Build Web App\n\nLaunch in VOID Prism", use_container_width=True):
                    quick_prompt = "Build a sleek darksynth Hand Cricket mini-game in a single HTML file."
            with s4:
                if st.button("👑 Who is Avyan?\n\nFounder & Identity", use_container_width=True):
                    quick_prompt = "Who am I, and who is Avyan, the Founder of VOID?"

        for idx, msg in enumerate(current_chat["messages"]):
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])
                # ONLY show PDF & Prism buttons if this specific message was a document/notes/slides/app request!
                if msg["role"] == "assistant" and msg.get("is_prism", False):
                    btn_c1, btn_c2 = st.columns([1, 1])
                    with btn_c1:
                        pdf_data = generate_real_pdf_bytes(current_chat["title"], msg["content"], author=f"VOID Forge ({user_name})")
                        st.download_button(
                            "📄 Download Real PDF (.pdf)",
                            data=pdf_data,
                            file_name=f"VOID_{current_chat['title'][:15].replace(' ', '_')}_{idx}.pdf",
                            mime="application/pdf",
                            key=f"pdf_chat_{idx}",
                            use_container_width=True
                        )
                    with btn_c2:
                        if st.button("⚡ Open in VOID Prism", key=f"open_prism_{idx}", use_container_width=True):
                            st.session_state.active_prism_text = msg["content"]
                            st.session_state.active_prism_title = current_chat["title"]
                            st.rerun()

    typed_prompt = st.chat_input(f"Command VOID Core, {user_name} (chat naturally, or ask for a PDF, slides, weather, or web app)...")
    active_prompt = quick_prompt or typed_prompt

    if active_prompt:
        full_user_prompt = f"Attached File (`{uploaded_file.name}`):\n```\n{file_context}\n```\n\n{active_prompt}" if file_context else active_prompt

        if not current_chat["messages"]:
            clean_title = active_prompt.strip().replace("\n", " ")
            current_chat["title"] = (clean_title[:26] + "...") if len(clean_title) > 26 else clean_title

        wants_prism = detect_prism_intent(active_prompt)

        current_chat["messages"].append({"role": "user", "content": full_user_prompt})
        user_record["prompts"] = user_record.get("prompts", 0) + 1
        user_record["last_active"] = datetime.now().strftime("%b %d, %H:%M")
        save_db(db)

        with chat_col:
            with st.chat_message("user"):
                st.markdown(full_user_prompt)

            master_sys = build_master_system_prompt(active_prompt, is_prism_task=wants_prism)

            with st.chat_message("assistant"):
                with st.spinner("VOID Core resonating..."):
                    reply, err = call_void_engine(cosmic_entity, master_sys, current_chat["messages"], temperature, max_tokens)
                    if reply:
                        st.markdown(reply)
                        is_prism_output = detect_prism_intent(active_prompt, reply)
                        current_chat["messages"].append({
                            "role": "assistant",
                            "content": reply,
                            "is_prism": is_prism_output
                        })
                        if is_prism_output:
                            st.session_state.active_prism_text = reply
                            st.session_state.active_prism_title = current_chat["title"]
                        save_db(db)
                        st.rerun()
                    else:
                        st.error(err)

    # --- SIDE-BY-SIDE ⚡ VOID PRISM PANEL ---
    if prism_open and prism_col is not None:
        with prism_col:
            st.markdown('<div class="prism-card">', unsafe_allow_html=True)
            st.markdown("#### ⚡ VOID Prism")
            
            prism_text = st.session_state.get("active_prism_text")
            prism_title = st.session_state.get("active_prism_title", current_chat["title"])
            if not prism_text:
                for m in reversed(current_chat["messages"]):
                    if m["role"] == "assistant":
                        prism_text = m["content"]
                        break

            if prism_text:
                blocks = extract_code_blocks(prism_text)
                has_html = any((b[0].lower() in ["html", "xml", "svg"] or "<html" in b[1].lower() or "<style" in b[1].lower()) for b in blocks)

                t_doc, t_slides, t_app, t_edit = st.tabs(["📄 PDF & Document", "📊 Slide Deck", "🖥️ Live App / Code", "✏️ Edit"])

                with t_doc:
                    dl_c1, dl_c2 = st.columns(2)
                    with dl_c1:
                        real_pdf = generate_real_pdf_bytes(prism_title, prism_text, author=f"VOID Forge ({user_name})")
                        st.download_button(
                            "📥 Download Real PDF (.pdf)",
                            data=real_pdf,
                            file_name=f"VOID_{prism_title[:15].replace(' ', '_')}.pdf",
                            mime="application/pdf",
                            type="primary",
                            use_container_width=True
                        )
                    with dl_c2:
                        slide_html_bytes = generate_interactive_slides_html(prism_title, prism_text).encode("utf-8")
                        st.download_button(
                            "📊 Download Slide Deck (.html)",
                            data=slide_html_bytes,
                            file_name=f"VOID_Slides_{prism_title[:15].replace(' ', '_')}.html",
                            mime="text/html",
                            use_container_width=True
                        )
                    st.markdown("---")
                    st.markdown(prism_text)

                with t_slides:
                    st.caption("Navigate slides with Next/Previous or Left/Right arrow keys.")
                    components.html(generate_interactive_slides_html(prism_title, prism_text), height=440, scrolling=False)

                with t_app:
                    if blocks:
                        lang = blocks[0][0].lower() if blocks[0][0] else "txt"
                        code_body = blocks[0][1].strip()
                        if has_html:
                            components.html(code_body, height=460, scrolling=True)
                        else:
                            st.code(code_body, language=lang)
                    else:
                        st.info("Ask VOID Core to build an HTML/JS web app or write code to run it live here.")

                with t_edit:
                    edited_prism = st.text_area("Modify Prism Content", value=prism_text, height=340)
                    if st.button("🔄 Update Prism & Rebuild PDF", use_container_width=True):
                        st.session_state.active_prism_text = edited_prism
                        st.rerun()
            else:
                st.info("Ask VOID for a PDF, study guide, presentation, or web app—and it will materialize inside VOID Prism.")
            st.markdown('</div>', unsafe_allow_html=True)

# =========================================================
# DIMENSION 2: 📖 VOID CODEX (STUDY NOTEBOOK, REAL PDF & SLIDES)
# =========================================================
elif ui_mode == "📖 VOID Codex (Study, PDF & Slides)":
    st.markdown("### 📖 VOID Scholastic Codex — Explanations, Questions & Instant PDF/Slide Forge")
    st.caption("Dedicated academic engine: generate crystal-clear explanations, revision notes, and exam question banks with 1-click Real PDF and Slide Deck downloads.")

    col_s1, col_s2, col_s3 = st.columns([2.2, 1.3, 1])
    with col_s1:
        study_topic = st.text_input("📚 Chapter or Topic", placeholder="E.g., Force & Pressure, Cell Structure, Linear Equations, The Indian Constitution...")
    with col_s2:
        study_format = st.selectbox(
            "Codex Mode",
            [
                "📘 Complete Revision Notes + Formulas",
                "💡 Easy Explanation with Real-Life Examples",
                "❓ Exam Question Bank (MCQs + Long Answers + Key)",
                "📊 Full Slide Presentation Deck (8 Slides)"
            ]
        )
    with col_s3:
        class_level = st.selectbox("Level", ["Class 8 (CBSE / ICSE)", "High School (Class 9-10)", "Olympiad / Advanced", "Quick 5-Minute Summary"])

    if st.button("✨ Forge Codex Material", type="primary", use_container_width=True):
        if study_topic:
            study_sys = build_master_system_prompt(
                study_topic,
                is_prism_task=True,
                extra_instructions=(
                    f"Create a master-level academic guide for {user_name} ({class_level}) on '{study_topic}'. "
                    f"Selected Format: {study_format}. "
                    "Use clean # and ## section headers so each section forms a clear page/slide. "
                    "Include: 1. Core Concept Explanation, 2. Key Definitions & Formulas, 3. Worked Examples, and 4. High-Probability Exam Questions with Answers."
                )
            )
            with st.spinner(f"Forging '{study_topic}' into Codex Notes, Real PDF, and Slide Deck..."):
                res, err = call_void_engine(cosmic_entity, study_sys, [{"role": "user", "content": f"Forge {study_format} for: {study_topic}"}], 0.2, 2600)
                if res:
                    st.session_state.codex_output = res
                    st.session_state.codex_topic = study_topic
                else:
                    st.error(err)
        else:
            st.warning("Enter a topic or chapter name first.")

    if "codex_output" in st.session_state:
        nb_text = st.session_state.codex_output
        nb_topic = st.session_state.get("codex_topic", "Study_Codex")
        safe_fname = re.sub(r"[^a-zA-Z0-9_]", "_", nb_topic)[:25]

        st.markdown("---")
        dl1, dl2, dl3 = st.columns(3)
        with dl1:
            pdf_bytes = generate_real_pdf_bytes(f"VOID Codex: {nb_topic}", nb_text, author=f"VOID Codex ({user_name})")
            st.download_button(
                "📄 Download Real PDF (.pdf)",
                data=pdf_bytes,
                file_name=f"VOID_Codex_{safe_fname}.pdf",
                mime="application/pdf",
                type="primary",
                use_container_width=True
            )
        with dl2:
            slides_bytes = generate_interactive_slides_html(nb_topic, nb_text).encode("utf-8")
            st.download_button(
                "📊 Download Interactive Slide Deck (.html)",
                data=slides_bytes,
                file_name=f"VOID_Slides_{safe_fname}.html",
                mime="text/html",
                use_container_width=True
            )
        with dl3:
            st.download_button(
                "📝 Download Markdown (.md)",
                data=nb_text,
                file_name=f"VOID_Codex_{safe_fname}.md",
                mime="text/markdown",
                use_container_width=True
            )

        nb_tab1, nb_tab2 = st.tabs(["📖 Formatted Codex Notes", "📊 Interactive Slide Deck"])
        with nb_tab1:
            st.markdown(nb_text)
        with nb_tab2:
            components.html(generate_interactive_slides_html(nb_topic, nb_text), height=500, scrolling=False)

# =========================================================
# DIMENSION 3: ⚡ LIVE WEB APP STUDIO
# =========================================================
elif ui_mode == "⚡ Live Web App Studio":
    st.markdown("### ⚡ VOID Live Web App & Game Studio")
    st.caption("Describe any web app, calculator, dashboard, or mini-game—VOID builds and executes it live on screen.")
    ui_prompt = st.text_area("What should VOID build?", placeholder="E.g., Build a sleek dark-mode Hand Cricket game or Pomodoro study dashboard...", height=85)
    if st.button("🚀 Forge & Launch App", type="primary"):
        if ui_prompt:
            builder_sys = "Output ONLY a single, complete, self-contained HTML file (with embedded <style> CSS and <script> JS) inside ```html ... ```."
            with st.spinner("Forging interactive web app..."):
                res, err = call_void_engine(cosmic_entity, builder_sys, [{"role": "user", "content": ui_prompt}], 0.3, max_tokens)
                if res:
                    clean_html = res.split("```html")[1].split("```")[0].strip() if "```html" in res else (res.split("```")[1].split("```")[0].strip() if "```" in res else res)
                    st.session_state.studio_html = clean_html
                else:
                    st.error(err)

    if "studio_html" in st.session_state:
        col_prev, col_src = st.columns([1.4, 1])
        with col_prev:
            st.markdown("##### 🖥️ Live Interactive App")
            components.html(st.session_state.studio_html, height=500, scrolling=True)
        with col_src:
            st.markdown("##### 📄 Source Code")
            st.download_button("📥 Download index.html", st.session_state.studio_html, file_name="index.html", mime="text/html", use_container_width=True)
            st.code(st.session_state.studio_html, language="html")

# =========================================================
# DIMENSION 4: 🛠️ SIDE-BY-SIDE CODE LAB
# =========================================================
elif ui_mode == "🛠️ Side-by-Side Code Lab":
    st.markdown("### 🛠️ VOID Code Refactor & Bug Lab")
    lab_action = st.selectbox("Operation", ["🐞 Find & Fix All Bugs", "🚀 Optimize for Maximum Speed", "🛡️ Security Audit & Error Handling", "🔄 Convert to Python / JS / C++"])
    l_col, r_col = st.columns(2)
    with l_col:
        raw_code = st.text_area("📥 Input Code:", height=340, placeholder="Paste your broken or unoptimized code here...")
        run_lab = st.button("⚡ Transform Code", type="primary", use_container_width=True)
    with r_col:
        st.markdown("**📤 Transformed Output:**")
        if run_lab and raw_code:
            lab_sys = f"Perform this exact operation on the user's code: {lab_action}. Briefly highlight key fixes, then provide the complete upgraded code."
            with st.spinner("Refactoring code..."):
                lab_res, lab_err = call_void_engine(cosmic_entity, lab_sys, [{"role": "user", "content": raw_code}], 0.1, max_tokens)
                if lab_res:
                    st.markdown(lab_res)
                else:
                    st.error(lab_err)
        else:
            st.info("Paste code on the left and click Transform to view the upgraded code side-by-side.")
