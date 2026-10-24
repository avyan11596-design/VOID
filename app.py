import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import os
import uuid
import base64
import re
from datetime import datetime

# --- 1. NATIVE BASE64 LOGO (Impossible to render as raw code) ---
SVG_RAW = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#4facfe"/><stop offset="100%" stop-color="#9b51e0"/></linearGradient></defs><rect width="120" height="120" rx="28" fill="#0e1117" stroke="url(#g)" stroke-width="6"/><path d="M34 38 L60 86 L86 38" fill="none" stroke="url(#g)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><circle cx="60" cy="34" r="7" fill="#ffffff"/></svg>'
LOGO_B64 = "data:image/svg+xml;base64," + base64.b64encode(SVG_RAW.encode("utf-8")).decode("utf-8")

 LOGO_FILE = "logo.png" if os.path.exists("logo.png") else LOGO_B64

st.set_page_config(
    page_title="VOID",
    page_icon=LOGO_FILE,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Native Streamlit Top-Left & Sidebar Logo
try:
    st.logo(LOGO_FILE)
except Exception:
    pass

# --- 2. GEMINI-INSPIRED ULTRA-CLEAN CSS ---
st.markdown("""
<style>
div[data-testid="stToolbarActions"] { display: none !important; }
div[data-testid="stAppDeployButton"] { display: none !important; }
div[data-testid="stDecoration"] { display: none !important; }
div[data-testid="stStatusWidget"] { display: none !important; }
#MainMenu { visibility: hidden !important; }
footer { visibility: hidden !important; }
header[data-testid="stHeader"] { background: transparent !important; }

.block-container {
    padding-top: 1.2rem !important;
    padding-bottom: 2rem !important;
    max-width: 1050px;
}
.stChatMessage {
    border-radius: 16px;
    padding: 14px 18px;
    margin-bottom: 10px;
}
.gemini-hero {
    text-align: center;
    padding: 35px 10px 25px 10px;
}
.gemini-gradient {
    font-size: 2.4rem;
    font-weight: 700;
    background: linear-gradient(90deg, #4facfe 0%, #a18cd1 50%, #fbc2eb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
}
.gemini-sub {
    font-size: 1.15rem;
    opacity: 0.65;
    margin-bottom: 24px;
}
.topbar-brand {
    display: flex;
    align-items: center;
    gap: 12px;
    margin-bottom: 10px;
}
.topbar-title {
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: 1px;
}
.topbar-pill {
    font-size: 0.72rem;
    padding: 2px 9px;
    border-radius: 99px;
    background: rgba(79, 172, 254, 0.15);
    color: #4facfe;
    border: 1px solid rgba(79, 172, 254, 0.35);
}
</style>
""", unsafe_allow_html=True)

# --- 3. PERSISTENT DATABASE & API ENGINE ---
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

def call_void_ai(model_slug, system_prompt, messages_list, temp=0.2, tokens=1400):
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

def extract_code_blocks(markdown_text):
    pattern = r"```(\w+)?\n(.*?)```"
    return re.findall(pattern, markdown_text, re.DOTALL)

# --- 4. EMAIL AUTHENTICATION GATE ---
if "user_email" not in st.session_state:
    st.markdown(f'<div class="gemini-hero"><img src="{LOGO_B64}" width="64" style="margin-bottom:14px;"/><div class="gemini-gradient">Welcome to VOID</div><div class="gemini-sub">Next-Gen AI Studio & Interactive Code Canvas</div></div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        with st.form("auth_gate"):
            email_input = st.text_input("Sign in with your Email", placeholder="name@example.com").strip().lower()
            submit = st.form_submit_button("Continue to Studio", type="primary", use_container_width=True)
            if submit:
                if "@" in email_input and "." in email_input and len(email_input) > 5:
                    now_str = datetime.now().strftime("%b %d, %H:%M")
                    if email_input not in db["users"]:
                        db["users"][email_input] = {"joined": now_str, "last_active": now_str, "prompts": 0}
                    else:
                        db["users"][email_input]["last_active"] = now_str
                    if email_input not in db["chats"] or not db["chats"][email_input]:
                        first_id = str(uuid.uuid4())[:8]
                        db["chats"][email_input] = {first_id: {"title": "New Chat", "messages": []}}
                    save_db(db)
                    st.session_state.user_email = email_input
                    st.session_state.current_chat_id = list(db["chats"][email_input].keys())[-1]
                    st.rerun()
                else:
                    st.error("Please enter a valid email address.")
    st.stop()

# Active User & Session State
user_email = st.session_state.user_email
user_name = user_email.split("@")[0].capitalize()
user_chats = db["chats"].setdefault(user_email, {})
if not user_chats:
    new_id = str(uuid.uuid4())[:8]
    user_chats[new_id] = {"title": "New Chat", "messages": []}
    save_db(db)

if "current_chat_id" not in st.session_state or st.session_state.current_chat_id not in user_chats:
    st.session_state.current_chat_id = list(user_chats.keys())[-1]

current_chat_id = st.session_state.current_chat_id
current_chat = user_chats[current_chat_id]

# --- 5. LEFT DRAWER (GEMINI-STYLE SIDEBAR) ---
with st.sidebar:
    st.markdown(f'<div class="topbar-brand"><img src="{LOGO_B64}" width="32"/><span class="topbar-title">VOID</span><span class="topbar-pill">ULTRA</span></div>', unsafe_allow_html=True)
    
    if st.button("✦ New Chat", type="primary", use_container_width=True):
        new_id = str(uuid.uuid4())[:8]
        user_chats[new_id] = {"title": "New Chat", "messages": []}
        st.session_state.current_chat_id = new_id
        save_db(db)
        st.rerun()

    st.markdown("##### Recent")
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
    
    # Canvas Side-by-Side Toggle
    canvas_open = st.toggle("⚡ Open VOID Canvas (Split View)", value=False)

    if current_chat["messages"]:
        export_md = f"# {current_chat['title']}\n\n"
        for m in current_chat["messages"]:
            export_md += f"### {m['role'].upper()}:\n{m['content']}\n\n---\n\n"
        st.download_button("📥 Export Chat (.md)", export_md, file_name=f"void_{current_chat_id}.md", use_container_width=True)

    with st.expander(f"👥 Crew Activity ({len(db['users'])})"):
        for u_mail, u_info in db["users"].items():
            st.markdown(f"**`{u_mail}`**  \n<small>Prompts: {u_info.get('prompts', 0)} • {u_info.get('last_active', '')}</small>", unsafe_allow_html=True)

    st.caption(f"Signed in as `{user_email}`")
    if st.button("Switch Account", use_container_width=True):
        del st.session_state.user_email
        st.rerun()

# --- 6. TOP ACTION BAR (Model, Mode & Popover Tools) ---
bar_c1, bar_c2, bar_c3 = st.columns([2, 2, 1.2])
with bar_c1:
    model = st.selectbox(
        "Model",
        ["google/gemini-2.5-flash", "deepseek/deepseek-chat", "qwen/qwen-2.5-coder-32b-instruct"],
        label_visibility="collapsed"
    )
with bar_c2:
    persona = st.selectbox(
        "Mode",
        [
            "✦ VOID Pro (All-Rounder)",
            "💻 Elite Full-Stack Coder",
            "🎨 Live Web & UI Builder",
            "🏗️ System Architect",
            "🐞 Deep Bug Hunter"
        ],
        label_visibility="collapsed"
    )
with bar_c3:
    with st.popover("➕ Attach & Tune", use_container_width=True):
        st.markdown("**📎 Attach File Context**")
        uploaded_file = st.file_uploader("Upload code/text", type=["py", "js", "html", "css", "json", "txt", "md", "cpp"], label_visibility="collapsed")
        file_context = ""
        if uploaded_file:
            try:
                file_context = uploaded_file.read().decode("utf-8")
                st.success(f"Attached `{uploaded_file.name}`")
            except Exception:
                st.error("Unable to read file.")
        st.markdown("---")
        st.markdown("**🧠 Thinking Depth**")
        task_depth = st.select_slider("Depth", options=["Fast", "Balanced", "Deep Reasoning"], value="Balanced")
        temperature = st.slider("Creativity", 0.0, 1.0, 0.2, 0.1)
        max_tokens = st.slider("Max Output Tokens", 400, 3500, 1500, 100)

# --- 7. MAIN WORKSPACE: CHAT + INTERACTIVE CANVAS ---
if canvas_open:
    chat_col, canvas_col = st.columns([1.15, 1], gap="large")
else:
    chat_col = st.container()
    canvas_col = None

quick_prompt = None

with chat_col:
    # GEMINI-STYLE HERO SCREEN WHEN CHAT IS EMPTY
    if not current_chat["messages"]:
        st.markdown(f'<div class="gemini-hero"><img src="{LOGO_B64}" width="54" style="margin-bottom:10px;"/><div class="gemini-gradient">Hello, {user_name}</div><div class="gemini-sub">How can VOID help you build, debug, or design today?</div></div>', unsafe_allow_html=True)
        
        s1, s2, s3, s4 = st.columns(4)
        with s1:
            if st.button("⚡ Web App\n\nBuild an interactive UI", use_container_width=True):
                quick_prompt = "Build a sleek, modern single-file HTML/CSS/JS web app for a synthwave music visualizer and beat pad."
        with s2:
            if st.button("💻 Write Code\n\nClean production scripts", use_container_width=True):
                quick_prompt = "Write a clean, modular Python script with a modern CLI interface and error handling."
        with s3:
            if st.button("🐞 Fix Bugs\n\nIsolate & patch errors", use_container_width=True):
                quick_prompt = "I have a bug in my code. Ask me to paste it and explain how you will analyze it."
        with s4:
            if st.button("🏗️ System Design\n\nFull project architecture", use_container_width=True):
                quick_prompt = "Design a complete, scalable system architecture and folder structure for a full-stack application."

    # Render Chat Messages
    for msg in current_chat["messages"]:
        avatar_icon = LOGO_FILE if msg["role"] == "assistant" else None
        with st.chat_message(msg["role"], avatar=avatar_icon):
            st.markdown(msg["content"])

# Chat Input Bar (Pinned at Bottom)
typed_prompt = st.chat_input("Ask VOID anything, or describe an app to build...")
active_prompt = quick_prompt or typed_prompt

if active_prompt:
    full_user_prompt = f"Attached File (`{uploaded_file.name}`):\n```\n{file_context}\n```\n\n{active_prompt}" if file_context else active_prompt

    if not current_chat["messages"]:
        clean_title = active_prompt.strip().replace("\n", " ")
        current_chat["title"] = (clean_title[:24] + "...") if len(clean_title) > 24 else clean_title

    current_chat["messages"].append({"role": "user", "content": full_user_prompt})
    db["users"][user_email]["prompts"] = db["users"][user_email].get("prompts", 0) + 1
    db["users"][user_email]["last_active"] = datetime.now().strftime("%b %d, %H:%M")
    save_db(db)

    with chat_col:
        with st.chat_message("user"):
            st.markdown(full_user_prompt)

        sys_prompt = (
            f"You are VOID, an ultra-intelligent AI assistant operating in '{persona}' mode. "
            f"Reasoning depth: {task_depth}. If asked to build a web UI, game, or component, include a complete self-contained ```html code block so the user can preview it live in VOID Canvas."
        )

        with st.chat_message("assistant", avatar=LOGO_FILE):
            with st.spinner("Thinking..."):
                reply, err = call_void_ai(model, sys_prompt, current_chat["messages"], temperature, max_tokens)
                if reply:
                    st.markdown(reply)
                    current_chat["messages"].append({"role": "assistant", "content": reply})
                    save_db(db)
                    if quick_prompt:
                        st.rerun()
                else:
                    st.error(err)

# --- 8. VOID CANVAS (SIDE-BY-SIDE ARTIFACT & LIVE PREVIEW PANEL) ---
if canvas_open and canvas_col is not None:
    with canvas_col:
        st.markdown("#### ⚡ VOID Canvas")
        st.caption("Automatically captures code & renders live interactive web previews from your chat.")
        
        # Find latest code block from assistant replies
        latest_code = None
        latest_lang = "html"
        for m in reversed(current_chat["messages"]):
            if m["role"] == "assistant":
                blocks = extract_code_blocks(m["content"])
                if blocks:
                    latest_lang = blocks[0][0].lower() if blocks[0][0] else "txt"
                    latest_code = blocks[0][1].strip()
                    break

        if latest_code:
            c_tab1, c_tab2 = st.tabs(["🖥️ Live Preview / Run", "📄 Editable Code"])
            with c_tab1:
                if latest_lang in ["html", "xml", "svg"] or "<html" in latest_code.lower() or "<style" in latest_code.lower():
                    components.html(latest_code, height=480, scrolling=True)
                else:
                    st.info(f"Detected `{latest_lang}` code block. Switch to the **Editable Code** tab or ask VOID to build an HTML/JS web app for an interactive visual preview!")
                    st.code(latest_code, language=latest_lang)
            with c_tab2:
                edited_code = st.text_area("Canvas Editor", value=latest_code, height=380, label_visibility="collapsed")
                ext = latest_lang if latest_lang in ["py", "js", "html", "css", "json", "cpp"] else "txt"
                st.download_button(
                    f"📥 Download File (.{ext})",
                    edited_code,
                    file_name=f"void_canvas.{ext}",
                    use_container_width=True
                )
        else:
            st.info("No code generated in this chat yet. Ask VOID to write a script or build an interactive web app, and it will appear right here in Canvas!")
