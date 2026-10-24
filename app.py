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

    st.markdown("---")
    st.markdown("##### 🧠 Neural Engine")
    model = st.selectbox(
        "AI Model",
        [
            "google/gemini-2.5-flash",
            "deepseek/deepseek-chat",
            "qwen/qwen-2.5-coder-32b-instruct"
        ]
    )
    
    task_depth = st.select_slider(
        "Reasoning Power",
        options=["⚡ Fast", "⚖️ Balanced", "🧠 Deep (Hardest)"],
        value="⚖️ Balanced"
    )

    with st.expander("🎛️ Fine-Tune Parameters"):
        temperature = st.slider("Creativity", 0.0, 1.0, 0.2, 0.1)
        max_tokens = st.slider("Max Output Tokens", 300, 3500, 1400, 100)

    with st.expander(f"👥 Crew Registry ({len(db['users'])})"):
        for u_mail, u_info in db["users"].items():
            st.markdown(f"**`{u_mail}`**  \n<small>Prompts: {u_info.get('prompts', 0)} | Last: {u_info.get('last_active', '')}</small>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🚪 Logout", use_container_width=True):
        del st.session_state.user_email
        st.rerun()

# --- 6. MULTI-INTERFACE WORKSPACE ---
render_header("STUDIO v5.0")

# 3 Distinct Interfaces via Clean Tabs
tab_chat, tab_studio, tab_lab = st.tabs([
    "💬 Neural Chat",
    "⚡ Live Web & UI Builder",
    "🛠️ Code Refactor Lab"
])

# ==========================================
# INTERFACE 1: NEURAL CHAT (Conversational)
# ==========================================
with tab_chat:
    col_mode, col_file = st.columns([2, 1])
    with col_mode:
        persona_mode = st.segmented_control(
            "Specialist Persona",
            ["💻 Coder", "🏗️ Architect", "🐞 Debugger", "🎨 UI Designer", "🎓 Tutor"],
            default="💻 Coder"
        )
    with col_file:
        uploaded_file = st.file_uploader("📎 Attach Code File (Optional)", type=["py", "js", "html", "css", "json", "txt", "md"], label_visibility="collapsed")
        file_context = ""
        if uploaded_file:
            try:
                file_context = uploaded_file.read().decode("utf-8")
                st.caption(f"✅ Attached `{uploaded_file.name}`")
            except Exception:
                pass

    for message in current_chat["messages"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("Ask anything from quick syntax to complex architecture..."):
        full_prompt = f"Attached File (`{uploaded_file.name}`):\n```\n{file_context}\n```\n\nTask: {prompt}" if file_context else prompt

        if not current_chat["messages"]:
            clean_t = prompt.strip().replace("\n", " ")
            current_chat["title"] = (clean_t[:24] + "...") if len(clean_t) > 24 else clean_t

        current_chat["messages"].append({"role": "user", "content": full_prompt})
        db["users"][user_email]["prompts"] = db["users"][user_email].get("prompts", 0) + 1
        save_db(db)

        with st.chat_message("user"):
            st.markdown(full_prompt)

        sys_directive = (
            f"You are VOID AI operating as {persona_mode}. "
            f"Depth mode: {task_depth}. Provide clean, well-structured, high-precision output."
        )

        with st.chat_message("assistant"):
            with st.spinner("Synthesizing..."):
                reply, err = call_void_ai(model, sys_directive, current_chat["messages"], temperature, max_tokens)
                if reply:
                    st.markdown(reply)
                    current_chat["messages"].append({"role": "assistant", "content": reply})
                    save_db(db)
                else:
                    st.error(err)

# ==========================================
# INTERFACE 2: LIVE WEB & UI BUILDER
# ==========================================
with tab_studio:
    st.markdown("#### ⚡ Instant Web App & Component Generator")
    st.caption("Describe any web tool, mini-game, calculator, or UI layout—VOID will code it and render a live interactive preview right here.")
    
    ui_prompt = st.text_area(
        "Describe what to build:",
        placeholder="E.g., Build a sleek dark-mode Pomodoro timer with neon accents, start/reset buttons, and sound visualizers...",
        height=90
    )
    
    if st.button("🚀 Build & Launch Live Preview", type="primary"):
        if not ui_prompt:
            st.warning("Please describe what you want to build first.")
        else:
            builder_sys = (
                "You are an elite frontend developer. Output ONLY a single, complete, self-contained HTML file "
                "(including embedded <style> CSS and <script> JS). Do NOT wrap it in markdown explanations—just output raw HTML code inside ```html ... ```."
            )
            with st.spinner("Compiling HTML/CSS/JS & rendering preview..."):
                res, err = call_void_ai(model, builder_sys, [{"role": "user", "content": ui_prompt}], 0.3, max_tokens)
                if res:
                    # Extract raw HTML if wrapped in code blocks
                    clean_html = res
                    if "```html" in res:
                        clean_html = res.split("```html")[1].split("```")[0].strip()
                    elif "```" in res:
                        clean_html = res.split("```")[1].split("```")[0].strip()
                    st.session_state.last_built_html = clean_html
                else:
                    st.error(err)

    if "last_built_html" in st.session_state:
        p_col1, p_col2 = st.columns([3, 2])
        with p_col1:
            st.markdown("##### 🖥️ Live Interactive Preview")
            components.html(st.session_state.last_built_html, height=460, scrolling=True)
        with p_col2:
            st.markdown("##### 📄 Generated Source Code")
            st.download_button(
                "📥 Download index.html",
                st.session_state.last_built_html,
                file_name="index.html",
                mime="text/html",
                use_container_width=True
            )
            st.code(st.session_state.last_built_html, language="html")

# ==========================================
# INTERFACE 3: SIDE-BY-SIDE CODE LAB
# ==========================================
with tab_lab:
    st.markdown("#### 🛠️ Side-by-Side Code Refactor & Bug Lab")
    st.caption("Paste your code on the left, select an operation, and get the upgraded version on the right.")
    
    lab_action = st.selectbox(
        "Select Operation",
        [
            "🐞 Find & Fix All Bugs",
            "🚀 Optimize for Maximum Speed & Cleanliness",
            "🛡️ Audit Security & Add Error Handling",
            "📝 Add Professional Documentation & Comments",
            "🔄 Convert to Python / JavaScript / C++"
        ]
    )
    
    left_col, right_col = st.columns(2)
    with left_col:
        raw_code = st.text_area("📥 Input Code:", height=320, placeholder="Paste your code or error traceback here...")
        run_lab = st.button("⚡ Execute Lab Operation", type="primary", use_container_width=True)
        
    with right_col:
        st.markdown("**📤 Output Result:**")
        if run_lab and raw_code:
            lab_sys = f"You are an expert code refactoring engine. Perform this exact operation on the user's code: {lab_action}. Explain key changes briefly, then provide the complete updated code."
            with st.spinner("Analyzing & refactoring code..."):
                lab_res, lab_err = call_void_ai(model, lab_sys, [{"role": "user", "content": raw_code}], 0.1, max_tokens)
                if lab_res:
                    st.markdown(lab_res)
                else:
                    st.error(lab_err)
        elif not raw_code:
            st.info("Paste your code on the left and click Execute to see the transformed result here.")
