import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import os
import uuid
from datetime import datetime

# --- 1. LOGO & BRANDING SETUP ---
# Automatically uses "logo.png" if you upload one to GitHub; otherwise uses a custom SVG icon
CUSTOM_SVG_LOGO = """
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" width="42" height="42">
  <rect width="100" height="100" rx="22" fill="#111318" stroke="#2d333b" stroke-width="4"/>
  <path d="M28 30 L50 72 L72 30" fill="none" stroke="#ffffff" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>
  <circle cx="50" cy="28" r="5" fill="#58a6ff"/>
</svg>
"""

HAS_LOGO_FILE = os.path.exists("logo.png")
PAGE_ICON = "logo.png" if HAS_LOGO_FILE else "⚡"

st.set_page_config(
    page_title="VOID",
    page_icon=PAGE_ICON,
    layout="wide",
    initial_sidebar_state="collapsed"
)

if HAS_LOGO_FILE:
    st.logo("logo.png")

# --- 2. STEALTH MINIMALIST CSS (Hides Streamlit Clutter) ---
st.markdown("""
    <style>
    /* Hide Streamlit branding, top-right buttons, top bar, and footer */
    div[data-testid="stToolbarActions"] { display: none !important; }
    div[data-testid="stAppDeployButton"] { display: none !important; }
    div[data-testid="stDecoration"] { display: none !important; }
    div[data-testid="stStatusWidget"] { display: none !important; }
    #MainMenu { visibility: hidden !important; }
    footer { visibility: hidden !important; }
    header[data-testid="stHeader"] { background: transparent !important; }

    /* Clean Modern Studio Layout */
    .block-container {
        padding-top: 1.5rem !important;
        padding-bottom: 2rem !important;
        max-width: 1100px;
    }
    .stChatMessage {
        border: 1px solid rgba(128, 128, 128, 0.15);
        border-radius: 12px;
        padding: 14px;
        margin-bottom: 8px;
    }
    .void-header {
        display: flex;
        align-items: center;
        gap: 14px;
        padding-bottom: 10px;
        border-bottom: 1px solid rgba(128, 128, 128, 0.2);
        margin-bottom: 18px;
    }
    .void-title {
        font-size: 1.55rem;
        font-weight: 700;
        letter-spacing: 1.5px;
        margin: 0;
    }
    .void-badge {
        font-size: 0.72rem;
        padding: 3px 8px;
        border-radius: 6px;
        background: rgba(88, 166, 255, 0.12);
        color: #58a6ff;
        border: 1px solid rgba(88, 166, 255, 0.3);
        font-family: monospace;
    }
    </style>
""", unsafe_allow_html=True)

# --- 3. DATABASE & API SETUP ---
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

def call_void_ai(model_slug, system_prompt, messages_list, temp=0.2, tokens=1200):
    if not API_KEY:
        return None, "⚠️ Master API Key missing in Streamlit Secrets (`OPENROUTER_API_KEY`)."
    headers = {
        "Authorization": f"Bearer {API_KEY.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://void-ai-hub.streamlit.app",
        "X-Title": "VOID"
    }
    payload = [{"role": "system", "content": system_prompt}] + messages_list
    data = {
        "model": model_slug,
        "messages": payload,
        "temperature": temp,
        "max_tokens": tokens
    }
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=60)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"], None
        return None, f"API Error ({r.status_code}): {r.text}"
    except Exception as e:
        return None, f"Connection Failed: {e}"

# Custom Header Helper
def render_header(subtitle="AI WORKSPACE"):
    st.markdown(f"""
        <div class="void-header">
            {CUSTOM_SVG_LOGO}
            <div>
                <div style="display:flex; align-items:center; gap:10px;">
                    <span class="void-title">VOID</span>
                    <span class="void-badge">{subtitle}</span>
                </div>
                <div style="font-size:0.8rem; opacity:0.65;">×͜× Elite Coding, Architecture & Design System</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

# --- 4. EMAIL AUTHENTICATION GATE ---
if "user_email" not in st.session_state:
    render_header("ACCESS PORTAL")
    col_a, col_b, col_c = st.columns([1, 1.4, 1])
    with col_b:
        with st.form("login_gate"):
            st.markdown("#### 🔒 Authenticate Session")
            st.caption("Enter your email to access VOID Studio.")
            email_input = st.text_input("Email Address", placeholder="you@example.com").strip().lower()
            submit = st.form_submit_button("Launch VOID", type="primary", use_container_width=True)
            
            if submit:
                if "@" in email_input and "." in email_input and len(email_input) > 5:
                    now_str = datetime.now().strftime("%b %d, %H:%M")
                    if email_input not in db["users"]:
                        db["users"][email_input] = {"joined": now_str, "last_active": now_str, "prompts": 0}
                    else:
                        db["users"][email_input]["last_active"] = now_str
                    
                    if email_input not in db["chats"] or not db["chats"][email_input]:
                        first_id = str(uuid.uuid4())[:8]
                        db["chats"][email_input] = {first_id: {"title": "New Session", "messages": []}}
                    
                    save_db(db)
                    st.session_state.user_email = email_input
                    st.session_state.current_chat_id = list(db["chats"][email_input].keys())[-1]
                    st.rerun()
                else:
                    st.error("Please enter a valid email address.")
    st.stop()

# Active User Setup
user_email = st.session_state.user_email
user_chats = db["chats"].setdefault(user_email, {})
if not user_chats:
    new_id = str(uuid.uuid4())[:8]
    user_chats[new_id] = {"title": "New Session", "messages": []}
    save_db(db)

if "current_chat_id" not in st.session_state or st.session_state.current_chat_id not in user_chats:
    st.session_state.current_chat_id = list(user_chats.keys())[-1]

current_chat_id = st.session_state.current_chat_id
current_chat = user_chats[current_chat_id]

# --- 5. SIDEBAR: SAVED CHATS & ENGINE TUNING ---
with st.sidebar:
    st.markdown(f"### ×͜× VOID Control")
    st.caption(f"Signed in: `{user_email}`")
    
    if st.button("➕ New Chat Thread", type="primary", use_container_width=True):
        new_id = str(uuid.uuid4())[:8]
        user_chats[new_id] = {"title": "New Session", "messages": []}
        st.session_state.current_chat_id = new_id
        save_db(db)
        st.rerun()

    st.markdown("##### 💬 Saved Threads")
    for c_id, c_data in reversed(list(user_chats.items())):
        c1, c2 = st.columns([5, 1])
        with c1:
            active_mark = "▸ " if c_id == current_chat_id else ""
            if st.button(f"{active_mark}{c_data['title']}", key=f"chat_{c_id}", use_container_width=True):
                st.session_state.current_chat_id = c_id
                st.rerun()
        with c2:
            if len(user_chats) > 1:
                if st.button("✕", key=f"del_{c_id}"):
                    del user_chats[c_id]
                    if c_id == current_chat_id:
                        st.session_state.current_chat_id = list(user_chats.keys())[-1]
                    save_db(db)
                    st.rerun()

    if current_chat["messages"]:
        export_md = f"# {current_chat['title']}\n\n"
        for m in current_chat["messages"]:
            export_md += f"### {m['role'].upper()}:\n{m['content']}\n\n---\n\n"
        st.download_button("📥 Export Chat (.md)", export_md, file_name=f"void_{current_chat_id}.md", use_container_width=True)

    st.markdown
