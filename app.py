import streamlit as st
import requests

# Page Configuration & Aesthetic Layout
st.set_page_config(
    page_title="VOID // AI Control Panel", 
    page_icon="⚡", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Cyberpunk / Darksynth CSS Styling for Aesthetic UI
st.markdown("""
    <style>
    .stApp {
        background-color: #0d1117;
        color: #c9d1d9;
    }
    .stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] {
        background-color: #161b22 !important;
        color: #ffffff !important;
        border: 1px solid #30363d !important;
        border-radius: 6px;
    }
    h1, h2, h3 {
        color: #58a6ff !important;
        font-family: monospace;
    }
    .stButton button {
        background: linear-gradient(135deg, #238636 0%, #2ea043 100%);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton button:hover {
        background: linear-gradient(135deg, #2ea043 0%, #3fb950 100%);
        box-shadow: 0 0 15px rgba(46, 160, 67, 0.4);
    }
    </style>
""", unsafe_allow_html=True)

# App Header
st.title("×͜× VOID // AI CONTROL PANEL")
st.markdown("`SYSTEM STATUS: ONLINE` &nbsp;|&nbsp; *Elite Coding, Architecture & Design Hub for the Crew*")
st.markdown("---")

# Sidebar Configuration & Customization
with st.sidebar:
    st.header("⚙️ SYSTEM CONFIG")
    
    # API Key Input (Hardcoded default placeholder or user entry)
    api_key_input = st.text_input(
        "OpenRouter API Key", 
        value="PASTE_YOUR_KEY_HERE", 
        type="password",
        help="Your secure OpenRouter API gateway passkey."
    )
    
    st.markdown("### 🧠 Neural Core")
    model_choice = st.selectbox(
        "Select Model",
        [
            "deepseek/deepseek-chat", 
            "qwen/qwen-2.5-coder-32b-instruct", 
            "anthropic/claude-3.5-sonnet",
            "google/gemini-flash-1.5"
        ]
    )
    
    st.markdown("### 🎛️ Parameters")
    operation_mode = st.radio(
        "Select Operation Mode",
        ["💻 Full-Stack Coder", "🏗️ System Architect", "🐞 Deep Debugger", "🎨 UI / UX Designer"]
    )
    
    temperature = st.slider("Creativity (Temperature)", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    max_tokens = st.slider("Max Response Length", min_value=500, max_value=4000, value=2000, step=500)
    
    st.markdown("---")
    st.markdown("**VOID Framework v2.0**")

# Main Interface Workspace
col1, col2 = st.columns([2, 1])

with col1:
    user_task = st.text_area(
        "💬 Enter prompt, feature request, or codebase bug description:", 
        height=180, 
        placeholder="E.g., Build a responsive dark-mode music player component in HTML/CSS/JS..."
    )

with col2:
    st.markdown("### 📋 Quick Prompts")
    if st.button("✨ Scaffold React Layout"):
        user_task = "Create a modern, clean React component layout with a sidebar and dynamic dashboard cards."
    if st.button("🛡️ Secure API Endpoint"):
        user_task = "Write a secure Python FastAPI endpoint with rate limiting and error handling."
    if st.button("⚡ Optimize Algorithm"):
        user_task = "Review this logic for performance bottlenecks and rewrite it for maximum speed."

# Execution Trigger
if st.button("⚡ EXECUTE OPERATION", type="primary", use_container_width=True):
    if not api_key_input or api_key_input == "PASTE_YOUR_KEY_HERE":
        st.warning("⚠️ Please insert a valid OpenRouter API key in the sidebar configuration.")
    elif not user_task:
        st.warning("⚠️ Please input a task or instructions into the prompt workspace.")
    else:
        # Tailor system prompt based on chosen operation mode
        system_prompts = {
            "💻 Full-Stack Coder": "You are an elite software engineer. Write clean, modular, production-ready code.",
            "🏗️ System Architect": "You are a master systems architect. Outline file structures, data flow, and tech stacks.",
            "🐞 Deep Debugger": "You are an expert debugger. Isolate flaws, explain the root cause, and provide fixed code patches.",
            "🎨 UI / UX Designer": "You are a world-class frontend designer. Focus heavily on aesthetic layouts, color grading, CSS styles, and smooth user experiences."
        }
        
        current_system_prompt = system_prompts[operation_mode]

        with st.spinner(f"⚡ Running [{operation_mode}] via {model_choice}..."):
            headers = {
                "Authorization": f"Bearer {api_key_input.strip()}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://void-ai-hub.streamlit.app",
                "X-Title": "VOID AI Control Panel"
            }
            
            data = {
                "model": model_choice,
                "messages": [
                    {"role": "system", "content": current_system_prompt},
                    {"role": "user", "content": user_task}
                ],
                "temperature": temperature,
                "max_tokens": max_tokens
            }
            
            try:
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
                
                if response.status_code == 200:
                    result_json = response.json()
                    ai_response = result_json["choices"][0]["message"]["content"]
                    
                    st.success("✨ OPERATION SUCCESSFUL")
                    st.markdown("### 🖥️ Output Results:")
                    st.markdown(ai_response)
                else:
                    st.error(f"❌ Gateway Error ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"❌ Connection Failed: {e}")
