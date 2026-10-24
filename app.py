import streamlit as st
import streamlit.components.v1 as components
import requests
import json
import os
import uuid
import base64
import re
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# --- 1. AUTO-GENERATE CUSTOM VOID LOGO FILE ---
SVG_RAW = '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120"><defs><linearGradient id="g" x1="0%" y1="0%" x2="100%" y2="100%"><stop offset="0%" stop-color="#4facfe"/><stop offset="100%" stop-color="#9b51e0"/></linearGradient></defs><rect width="120" height="120" rx="28" fill="#0e1117" stroke="url(#g)" stroke-width="6"/><path d="M34 38 L60 86 L86 38" fill="none" stroke="url(#g)" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><circle cx="60" cy="34" r="7" fill="#ffffff"/></svg>'
LOGO_B64 = "data:image/svg+xml;base64," + base64.b64encode(SVG_RAW.encode("utf-8")).decode("utf-8")

if not os.path.exists("void_logo.svg"):
    try:
        with open("void_logo.svg", "w", encoding="utf-8") as f:
            f.write(SVG_RAW)
    except Exception:
        pass

LOGO_PATH = "logo.png" if os.path.exists("logo.png") else ("void_logo.svg" if os.path.exists("void_logo.svg") else "⚡")

st.set_page_config(
    page_title="VOID",
    page_icon=LOGO_PATH,
    layout="wide",
    initial_sidebar_state="expanded"
)

try:
    if LOGO_PATH != "⚡":
        st.logo(LOGO_PATH)
except Exception:
    pass

# --- 2. GEMINI-STYLE ULTRA-CLEAN CSS ---
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
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
    max-width: 1120px;
}
.stChatMessage {
    border-radius: 16px;
    padding: 14px 18px;
    margin-bottom: 10px;
    border: 1px solid rgba(128, 128, 128, 0.14);
}
.gemini-hero {
    text-align: center;
    padding: 28px 10px 20px 10px;
}
.gemini-gradient {
    font-size: 2.5rem;
    font-weight: 700;
    background: linear-gradient(90deg, #4facfe 0%, #a18cd1 50%, #fbc2eb 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 6px;
}
.gemini-sub {
    font-size: 1.1rem;
    opacity: 0.68;
    margin-bottom: 22px;
}
.topbar-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    margin-bottom: 12px;
}
.topbar-title {
    font-size: 1.35rem;
    font-weight: 700;
    letter-spacing: 1.5px;
}
.topbar-pill {
    font-size: 0.7rem;
    padding: 2px 8px;
    border-radius: 99px;
    background: rgba(79, 172, 254, 0.15);
    color: #4facfe;
    border: 1px solid rgba(79, 172, 254, 0.35);
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
    GMAIL_USER = st.secrets["GMAIL_USER"]
    GMAIL_PASS = st.secrets["GMAIL_APP_PASSWORD"]
except Exception:
    GMAIL_USER = ""
    GMAIL_PASS = ""

def send_otp_email(receiver_email, otp_code):
    if not GMAIL_USER or not GMAIL_PASS:
        return False, "Gmail credentials missing in Streamlit Secrets."
    try:
        msg = MIMEMultipart()
        msg['From'] = GMAIL_USER
        msg['To'] = receiver_email
        msg['Subject'] = "🔐 VOID Studio - Your Login Verification Code"
        
        body = f"""
        Hello,
        
        Your verification code to access VOID Studio is:
        
        {otp_code}
        
        Enter this code on the verification screen to proceed.
        
        - VOID Security Protocol
        """
        msg.attach(MIMEText(body, 'plain'))
        
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(GMAIL_USER, GMAIL_PASS)
        server.sendmail(GMAIL_USER, receiver_email, msg.as_string())
        server.quit()
        return True, None
    except Exception as e:
        return False, str(e)

# Map the 3 Cosmic Objects to underlying engine slugs safely
COSMIC_OBJECTS = {
    "🌙 Void Moon (Swift & Light)": "google/gemini-2.5-flash",
    "🪐 Nebula Core (Deep Logic)": "deepseek/deepseek-chat",
    "☀️ Supernova X (Master Architect)": "qwen/qwen-2.5-coder-32b-instruct"
}

def call_void_engine(cosmic_choice, system_prompt, messages_list, temp=0.2, tokens=1400):
    if not API_KEY:
        return None, "⚠️ Master API Key missing in Streamlit Secrets (`OPENROUTER_API_KEY`)."
    
    target_slug = COSMIC_OBJECTS.get(cosmic_choice, "google/gemini-2.5-flash")
    
    headers = {
        "Authorization": f"Bearer {API_KEY.strip()}",
        "Content-Type": "application/json",
        "HTTP-Referer": "https://void-ai-hub.streamlit.app",
        "X-Title": "VOID"
    }
    payload = [{"role": "system", "content": system_prompt}] + messages_list
    data = {
        "model": target_slug,
        "messages": payload,
        "temperature": temp,
        "max_tokens": tokens
    }
    try:
        r = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data, timeout=60)
        if r.status_code == 200:
            return r.json()["choices"][0]["message"]["content"], None
        return None, f"Resonance Error ({r.status_code}): {r.text}"
    except Exception as e:
        return None, f"Cosmic Connection Failed: {e}"

def extract_code_blocks(markdown_text):
    pattern = r"```(\w+)?\n(.*?)```"
    return re.findall(pattern, markdown_text, re.DOTALL)

# --- 4. REAL-TIME OTP AUTHENTICATION GATE ---
if "user_email" not in st.session_state:
    st.markdown(f'<div class="gemini-hero"><img src="{LOGO_B64}" width="68" style="margin-bottom:12px;"/><div class="gemini-gradient">Welcome to VOID</div><div class="gemini-sub">Secure Email OTP Authentication Gateway</div></div>', unsafe_allow_html=True)
    
    c1, c2, c3 = st.columns([1, 1.3, 1])
    with c2:
        if "pending_email" not in st.session_state:
            with st.form("email_form"):
                email_input = st.text_input("Enter your Email Address", placeholder="name@example.com").strip().lower()
                send_btn = st.form_submit_button("Send Verification Code", type="primary", use_container_width=True)
                
                if send_btn:
                    if "@" in email_input and "." in email_input and len(email_input) > 5:
                        generated_otp = str(random.randint(100000, 999999))
                        success, err = send_otp_email(email_input, generated_otp)
                        if success:
                            st.session_state.pending_email = email_input
                            st.session_state.target_otp = generated_otp
                            st.success(f"Verification code sent to `{email_input}`!")
                            st.rerun()
                        else:
                            st.error(f"Failed to send email: {err}")
                    else:
                        st.error("Please enter a valid email address.")
        else:
            st.info(f"Code sent to: **{st.session_state.pending_email}**")
            with st.form("otp_form"):
                entered_otp = st.text_input("Enter 6-Digit OTP Code", placeholder="123456", max_chars=6)
                verify_btn = st.form_submit_button("Verify & Enter Studio", type="primary", use_container_width=True)
                back_btn = st.form_submit_button("Use a Different Email")
                
                if back_btn:
                    del st.session_state.pending_email
                    del st.session_state.target_otp
                    st.rerun()
                    
                if verify_btn:
                    if entered_otp.strip() == st.session_state.target_otp:
                        email_input = st.session_state.pending_email
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
                        
                        del st.session_state.pending_email
                        del st.session_state.target_otp
                        st.rerun()
                    else:
                        st.error("❌ Incorrect OTP code. Please check your inbox and try again.")
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

# --- 5. LEFT DRAWER (SIDEBAR) ---
with st.sidebar:
    st.markdown(f'<div class="topbar-brand"><img src="{LOGO_B64}" width="32"/><span class="topbar-title">VOID</span><span class="topbar-pill">ULTRA</span></div>', unsafe_allow_html=True)

    if st.button("✦ New Thread", type="primary", use_container_width=True):
        new_id = str(uuid.uuid4())[:8]
        user_chats[new_id] = {"title": "New Thread", "messages": []}
        st.session_state.current_chat_id = new_id
        save_db(db)
        st.rerun()

    st.markdown("##### Recent Threads")
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
    canvas_open = st.toggle("⚡ Split-Screen VOID Canvas", value=False)

    if current_chat["messages"]:
        export_md = f"# {current_chat['title']}\n\n"
        for m in current_chat["messages"]:
            export_md += f"### {m['role'].upper()}:\n{m['content']}\n\n---\n\n"
        st.download_button("📥 Export Thread (.md)", export_md, file_name=f"void_{current_chat_id}.md", use_container_width=True)

    with st.expander(f"👥 Crew Activity ({len(db['users'])})"):
        for u_mail, u_info in db["users"].items():
            st.markdown(f"**`{u_mail}`**  \n<small>Prompts: {u_info.get('prompts', 0)} • {u_info.get('last_active', '')}</small>", unsafe_allow_html=True)

    st.caption(f"Signed in as `{user_email}`")
    if st.button("Switch Account", use_container_width=True):
        del st.session_state.user_email
        st.rerun()

# --- 6. TOP CONTROL BAR & COSMIC SWITCHER ---
top_c1, top_c2, top_c3, top_c4 = st.columns([1.8, 1.8, 1.8, 1.2])
with top_c1:
    ui_mode = st.selectbox(
        "Interface",
        ["✦ Assistant & Canvas", "⚡ Live Web App Studio", "🛠️ Side-by-Side Code Lab"],
        label_visibility="collapsed"
    )
with top_c2:
    cosmic_entity = st.selectbox(
        "Cosmic Entity",
        list(COSMIC_OBJECTS.keys()),
        label_visibility="collapsed"
    )
with top_c3:
    persona = st.selectbox(
        "Persona",
        ["✦ VOID Pro (All-Rounder)", "💻 Full-Stack Coder", "🎨 UI/UX Designer", "🏗️ System Architect", "🐞 Deep Bug Hunter"],
        label_visibility="collapsed"
    )
with top_c4:
    with st.popover("➕ Attach & Tune", use_container_width=True):
        st.markdown("**📎 Attach Code / File**")
        uploaded_file = st.file_uploader("Upload file", type=["py", "js", "html", "css", "json", "txt", "md", "cpp"], label_visibility="collapsed")
        file_context = ""
        if uploaded_file:
            try:
                file_context = uploaded_file.read().decode("utf-8")
                st.success(f"Attached `{uploaded_file.name}`")
            except Exception:
                st.error("Unable to read file.")
        st.markdown("---")
        task_depth = st.select_slider("Thinking Depth", options=["Fast", "Balanced", "Deep Reasoning"], value="Balanced")
        temperature = st.slider("Creativity", 0.0, 1.0, 0.2, 0.1)
        max_tokens = st.slider("Max Output Tokens", 400, 3500, 1500, 100)

# =========================================================
# INTERFACE 1: ASSISTANT + SPLIT-SCREEN CANVAS
# =========================================================
if ui_mode == "✦ Assistant & Canvas":
    if canvas_open:
        chat_col, canvas_col = st.columns([1.15, 1], gap="large")
    else:
        chat_col = st.container()
        canvas_col = None

    quick_prompt = None

    with chat_col:
        if not current_chat["messages"]:
            st.markdown(f'<div class="gemini-hero"><img src="{LOGO_B64}" width="56" style="margin-bottom:10px;"/><div class="gemini-gradient">Hello, {user_name}</div><div class="gemini-sub">What are we building, designing, or solving today?</div></div>', unsafe_allow_html=True)

            s1, s2, s3, s4 = st.columns(4)
            with s1:
                if st.button("⚡ Web App\n\nInteractive HTML/JS UI", use_container_width=True):
                    quick_prompt = "Build a sleek, modern single-file HTML/CSS/JS web app for a darksynth beat pad and audio visualizer."
            with s2:
                if st.button("💻 Write Code\n\nClean production scripts", use_container_width=True):
                    quick_prompt = "Write a clean, modular Python script with a modern CLI interface and full error handling."
            with s3:
                if st.button("🐞 Fix Bugs\n\nIsolate & patch errors", use_container_width=True):
                    quick_prompt = "I have a bug in my code. Ask me to paste it and explain how you will isolate and patch it."
            with s4:
                if st.button("🏗️ Architecture\n\nFull system blueprint", use_container_width=True):
                    quick_prompt = "Design a complete, scalable system architecture and folder structure for a modern full-stack app."

        for msg in current_chat["messages"]:
            with st.chat_message(msg["role"]):
                st.markdown(msg["content"])

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
                f"You are VOID, an elite cosmic architecture entity operating in '{persona}' mode. "
                f"Reasoning depth: {task_depth}. If asked to build a web UI, game, or component, include a complete self-contained ```html code block so the user can preview it live in VOID Canvas."
            )

            with st.chat_message("assistant"):
                with st.spinner("Synthesizing resonance..."):
                    reply, err = call_void_engine(cosmic_entity, sys_prompt, current_chat["messages"], temperature, max_tokens)
                    if reply:
                        st.markdown(reply)
                        current_chat["messages"].append({"role": "assistant", "content": reply})
                        save_db(db)
                        if quick_prompt:
                            st.rerun()
                    else:
                        st.error(err)

    if canvas_open and canvas_col is not None:
        with canvas_col:
            st.markdown("#### ⚡ VOID Canvas")
            st.caption("Live interactive preview & code editor for your current chat.")
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
                c_tab1, c_tab2 = st.tabs(["🖥️ Live Preview", "📄 Editable Code"])
                with c_tab1:
                    if latest_lang in ["html", "xml", "svg"] or "<html" in latest_code.lower() or "<style" in latest_code.lower():
                        components.html(latest_code, height=480, scrolling=True)
                    else:
                        st.info(f"Detected `{latest_lang}` code. Ask VOID for an HTML/JS web app to run a visual preview here!")
                        st.code(latest_code, language=latest_lang)
                with c_tab2:
                    edited_code = st.text_area("Canvas Editor", value=latest_code, height=380, label_visibility="collapsed")
                    ext = latest_lang if latest_lang in ["py", "js", "html", "css", "json", "cpp"] else "txt"
                    st.download_button(f"📥 Download (.{ext})", edited_code, file_name=f"void_canvas.{ext}", use_container_width=True)
            else:
                st.info("Ask VOID to write code or build a web app in the chat, and it will automatically load here!")

# =========================================================
# INTERFACE 2: DEDICATED LIVE WEB APP STUDIO
# =========================================================
elif ui_mode == "⚡ Live Web App Studio":
    st.markdown("### ⚡ Instant Web App & Game Generator")
    st.caption("Describe any web app, calculator, dashboard, or mini-game—VOID builds it and runs it live on screen.")
    ui_prompt = st.text_area("What should VOID build?", placeholder="E.g., Build a sleek dark-mode calculator and unit converter with glowing buttons...", height=85)
    if st.button("🚀 Generate & Launch App", type="primary"):
        if ui_prompt:
            builder_sys = "Output ONLY a single, complete, self-contained HTML file (with embedded <style> CSS and <script> JS) inside ```html ... ```."
            with st.spinner("Building interactive web app..."):
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
            components.html(st.session_state.studio_html, height=480, scrolling=True)
        with col_src:
            st.markdown("##### 📄 Source Code")
            st.download_button("📥 Download index.html", st.session_state.studio_html, file_name="index.html", mime="text/html", use_container_width=True)
            st.code(st.session_state.studio_html, language="html")

# =========================================================
# INTERFACE 3: SIDE-BY-SIDE CODE REFACTOR LAB
# =========================================================
elif ui_mode == "🛠️ Side-by-Side Code Lab":
    st.markdown("### 🛠️ Side-by-Side Code Refactor & Bug Lab")
    lab_action = st.selectbox("Operation", ["🐞 Find & Fix All Bugs", "🚀 Optimize for Maximum Speed", "🛡️ Security Audit & Error Handling", "🔄 Convert to Python / JS / C++"])
    l_col, r_col = st.columns(2)
    with l_col:
        raw_code = st.text_area("📥 Paste Input Code:", height=340, placeholder="Paste your broken or unoptimized code here...")
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
