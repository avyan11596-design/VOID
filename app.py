import streamlit as st
import requests
import json
import os
import uuid
from datetime import datetime

# --- 1. PAGE SETUP & MINIMALIST STYLING ---
st.set_page_config(page_title="VOID // AI Hub", page_icon="⚡", layout="centered")

st.markdown("""
    <style>
    .stChatMessage { border-radius: 8px; padding: 12px; }
    div[data-testid="stSidebarNav"] { display: none; }
    .block-container { padding-top: 2rem; padding-bottom: 2rem; }
    </style>
""", unsafe_allow_html=True)

# --- 2. PERSISTENT SERVER STORAGE (Cross-Device User & Chat Saving) ---
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

# Load Master API Key from Streamlit Secrets
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    API_KEY = ""

# --- 3. EMAIL AUTHENTICATION PORTAL ---
if "user_email" not in st.session_state:
    st.title("VOID // AI Hub")
    st.caption("Private Coding, Architecture & Design Workspace")
    st.markdown("---")
    
    with st.form("login_gate"):
        st.subheader("🔒 Authenticate to Continue")
        email_input = st.text_input("Enter your email address:", placeholder="you@example.com").strip().lower()
        submit = st.form_submit_button("Enter Workspace", type="primary", use_container_width=True)
        
        if submit:
            if "@" in email_input and "." in email_input and len(email_input) > 5:
                now_str = datetime.now().strftime("%b %d, %H:%M")
                if email_input not in db["users"]:
                    db["users"][email_input] = {"joined": now_str, "last_active": now_str, "prompts": 0}
                else:
                    db["users"][email_input]["last_active"] = now_str
                
                if email_input not in db["chats"] or not db["chats"][email_input]:
                    first_id = str(uuid.uuid4())[:8]
                    db["chats"][email_input] = {
                        first_id: {"title": "New Conversation", "messages": []}
                    }
                
                save_db(db)
                st.session_state.user_email = email_input
                st.session_state.current_chat_id = list(db["chats"][email_input].keys())[-1]
                st.rerun()
            else:
                st.error("Please enter a valid email address.")
    st.stop()

# Active User Context
user_email = st.session_state.user_email
user_chats = db["chats"].setdefault(user_email, {})

if not user_chats:
    new_id = str(uuid.uuid4())[:8]
    user_chats[new_id] = {"title": "New Conversation", "messages": []}
    save_db(db)

if "current_chat_id" not in st.session_state or st.session_state.current_chat_id not in user_chats:
    st.session_state.current_chat_id = list(user_chats.keys())[-1]

current_chat_id = st.session_state.current_chat_id
current_chat = user_chats[current_chat_id]

# --- 4. SIDEBAR: SAVED CHATS, ENGINE & CUSTOMIZATION ---
with st.sidebar:
    st.title("VOID // Control")
    st.caption(f"👤 `{user_email}`")
    
    # New Chat Button
    if st.button("➕ New Chat", type="primary", use_container_width=True):
        new_id = str(uuid.uuid4())[:8]
        user_chats[new_id] = {"title": "New Conversation", "messages": []}
        st.session_state.current_chat_id = new_id
        save_db(db)
        st.rerun()

    # Saved Chats List
    st.markdown("##### 💬 Saved Chats")
    for c_id, c_data in reversed(list(user_chats.items())):
        col1, col2 = st.columns([5, 1])
        with col1:
            is_active = (c_id == current_chat_id)
            btn_label = f"{'▶ ' if is_active else ''}{c_data['title']}"
            if st.button(btn_label, key=f"chat_{c_id}", use_container_width=True):
                st.session_state.current_chat_id = c_id
                st.rerun()
        with col2:
            if len(user_chats) > 1:
                if st.button("✕", key=f"del_{c_id}", help="Delete chat"):
                    del user_chats[c_id]
                    if c_id == current_chat_id:
                        st.session_state.current_chat_id = list(user_chats.keys())[-1]
                    save_db(db)
                    st.rerun()

    # Export / Download Current Chat
    if current_chat["messages"]:
        chat_export_text = f"# {current_chat['title']}\nExported from VOID // AI Hub ({user_email})\n\n"
        for m in current_chat["messages"]:
            role_label = "USER" if m["role"] == "user" else "VOID AI"
            chat_export_text += f"### {role_label}:\n{m['content']}\n\n---\n\n"
            
        st.download_button(
            label="📥 Download Chat (.md)",
            data=chat_export_text,
            file_name=f"void_chat_{current_chat_id}.md",
            mime="text/markdown",
            use_container_width=True
        )

    st.markdown("---")
    
    # Core Intelligence Settings
    st.markdown("##### 🧠 Intelligence Engine")
    model_list = [
        "google/gemini-2.5-flash",
        "deepseek/deepseek-chat",
        "qwen/qwen-2.5-coder-32b-instruct",
        "Custom Model Slug..."
    ]
    selected_model = st.selectbox("Model", model_list)
    if selected_model == "Custom Model Slug...":
        model = st.text_input("Enter OpenRouter Model Slug:", value="google/gemini-2.5-flash")
    else:
        model = selected_model

    mode = st.selectbox(
        "Specialist Mode",
        [
            "💻 Full-Stack Coder",
            "🏗️ System Architect",
            "🐞 Deep Debugger",
            "🎨 UI / Frontend Designer",
            "🚀 Code Optimizer & Reviewer",
            "🎓 Concept Tutor (Explain Simply)"
        ]
    )

    task_depth = st.select_slider(
        "Task Complexity Depth",
        options=["⚡ Fast & Direct", "⚖️ Balanced", "🧠 Deep Reasoning (Hardest)"]
    )

    # File Context Attachment
    with st.expander("📎 Attach Code / File Context"):
        uploaded_file = st.file_uploader(
            "Upload script or document", 
            type=["py", "js", "html", "css", "json", "txt", "md", "cpp", "java"]
        )
        file_context = ""
        if uploaded_file is not None:
            try:
                file_context = uploaded_file.read().decode("utf-8")
                st.success(f"Loaded `{uploaded_file.name}` ({len(file_context)} chars)")
            except Exception:
                st.error("Could not read file as text.")

    # Advanced Tuning
    with st.expander("🎛️ Advanced Customization"):
        temperature = st.slider("Creativity (Temperature)", 0.0, 1.0, 0.2, 0.1)
        max_tokens = st.slider("Max Output Tokens", 250, 4000, 1500, 250)
        
        base_personas = {
            "💻 Full-Stack Coder": "You are an elite software engineer. Write clean, modular, production-ready code with clear structure.",
            "🏗️ System Architect": "You are a principal systems architect. Design scalable file structures, database schemas, and robust technical architectures.",
            "🐞 Deep Debugger": "You are an expert bug hunter. Identify root causes, edge cases, and security flaws, and provide exact fixed code.",
            "🎨 UI / Frontend Designer": "You are a minimalist UI/UX engineer. Build modern, responsive, clean interfaces with refined CSS and layouts.",
            "🚀 Code Optimizer & Reviewer": "You refactor code for maximum performance, readability, and lower time/space complexity.",
            "🎓 Concept Tutor (Explain Simply)": "You explain complex programming and math concepts clearly from first principles with easy examples."
        }
        
        depth_directives = {
            "⚡ Fast & Direct": "Be concise. Provide the direct code or answer immediately with minimal explanation.",
            "⚖️ Balanced": "Provide a clear explanation followed by well-commented, complete code.",
            "🧠 Deep Reasoning (Hardest)": "Think step-by-step. Break down the architecture, edge cases, and logic systematically before writing the complete, highest-quality solution."
        }
        
        default_directive = f"{base_personas[mode]}\n\nExecution Style: {depth_directives[task_depth]}"
        custom_system_prompt = st.text_area("Custom System Directive", value=default_directive, height=130)

    # Live User Registry (See who has joined your app)
    with st.expander(f"👥 Registered Users ({len(db['users'])})"):
        for u_mail, u_info in db["users"].items():
            st.markdown(f"**`{u_mail}`**  \n<small>Joined: {u_info['joined']} | Prompts: {u_info.get('prompts', 0)}</small>", unsafe_allow_html=True)

    st.markdown("---")
    if st.button("🚪 Switch Account / Logout", use_container_width=True):
        del st.session_state.user_email
        st.rerun()

# --- 5. MAIN CHAT WORKSPACE ---
st.title("VOID // AI Hub")
st.caption(f"Mode: **{mode}** &nbsp;•&nbsp; Depth: **{task_depth}** &nbsp;•&nbsp; Model: `{model}`")
st.markdown("---")

# Empty State Quick Starters
if not current_chat["messages"]:
    st.markdown("#### What are we building today?")
    c1, c2 = st.columns(2)
    quick_prompt = None
    with c1:
        if st.button("💻 Build a Web App Layout", use_container_width=True):
            quick_prompt = "Build a clean, modern responsive dashboard layout in HTML, CSS, and JS."
        if st.button("🐞 Debug & Fix Broken Code", use_container_width=True):
            quick_prompt = "I have a bug in my script. Tell me what details you need to isolate and fix it."
    with c2:
        if st.button("🏗️ Architect a Full Project", use_container_width=True):
            quick_prompt = "Design a complete folder structure and architecture for a scalable Python application."
        if st.button("🚀 Optimize an Algorithm", use_container_width=True):
            quick_prompt = "How can I optimize a slow data-processing loop in Python for maximum speed?"
else:
    quick_prompt = None

# Render Conversation History
for message in current_chat["messages"]:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input Bar
chat_box_prompt = st.chat_input("Ask anything from a quick syntax check to complex system architecture...")
active_prompt = quick_prompt or chat_box_prompt

if active_prompt:
    if not API_KEY:
        st.error("⚠️ Master API Key missing! Add `OPENROUTER_API_KEY` in your Streamlit App Secrets.")
    else:
        # Attach uploaded file content if present
        full_user_content = active_prompt
        if file_context:
            full_user_content = f"**Attached File (`{uploaded_file.name}`):**\n```\n{file_context}\n```\n\n**Task:**\n{active_prompt}"

        # Auto-title chat on first message
        if not current_chat["messages"]:
            clean_title = active_prompt.strip().replace("\n", " ")
            current_chat["title"] = (clean_title[:26] + "...") if len(clean_title) > 26 else clean_title

        # Save & Display User Message
        current_chat["messages"].append({"role": "user", "content": full_user_content})
        db["users"][user_email]["prompts"] = db["users"][user_email].get("prompts", 0) + 1
        db["users"][user_email]["last_active"] = datetime.now().strftime("%b %d, %H:%M")
        save_db(db)

        with st.chat_message("user"):
            st.markdown(full_user_content)

        # Build OpenRouter Payload
        headers = {
            "Authorization": f"Bearer {API_KEY.strip()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://void-ai-hub.streamlit.app",
            "X-Title": "VOID AI Hub"
        }

        messages_payload = [{"role": "system", "content": custom_system_prompt}]
        for m in current_chat["messages"]:
            messages_payload.append({"role": m["role"], "content": m["content"]})

        data = {
            "model": model,
            "messages": messages_payload,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Request & Render Assistant Response
        with st.chat_message("assistant"):
            with st.spinner("Processing..."):
                try:
                    response = requests.post(
                        "https://openrouter.ai/api/v1/chat/completions",
                        headers=headers,
                        json=data,
                        timeout=60
                    )
                    
                    if response.status_code == 200:
                        result = response.json()["choices"][0]["message"]["content"]
                        st.markdown(result)
                        current_chat["messages"].append({"role": "assistant", "content": result})
                        save_db(db)
                        if quick_prompt:
                            st.rerun()
                    else:
                        st.error(f"API Error ({response.status_code}): {response.text}")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")
