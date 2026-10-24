import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="VOID // AI Hub", page_icon="⚡", layout="centered")

# Minimalist Chat Styling
st.markdown("""
    <style>
    .stChatMessage {
        border-radius: 8px;
        padding: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.title("VOID // AI Hub")
st.caption("Shared Elite Coding & Design Assistant")
st.markdown("---")

# Securely load your API key from Streamlit Secrets
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    API_KEY = ""

# Sidebar Settings & Customization Controls
with st.sidebar:
    st.subheader("⚙️ Configuration")
    
    model = st.selectbox(
        "Choose Model",
        [
            "google/gemini-2.5-flash",
            "deepseek/deepseek-chat",
            "qwen/qwen-2.5-coder-32b-instruct"
        ]
    )
    
    mode = st.selectbox(
        "Operation Mode",
        ["Coder", "Architect", "Debugger", "UI Designer"]
    )
    
    st.markdown("---")
    st.subheader("🎛️ Fine-Tuning")
    
    # Customization sliders for control
    temperature = st.slider("Temperature (Creativity)", min_value=0.0, max_value=1.0, value=0.2, step=0.1)
    max_tokens = st.slider("Max Response Tokens", min_value=250, max_value=4000, value=1000, step=250)
    
    # Preset base instructions mapped to modes
    system_prompts = {
        "Coder": "You are an elite software engineer. Write clean, production-ready code.",
        "Architect": "You are a systems architect. Outline structure and logic clearly.",
        "Debugger": "You are an expert debugger. Isolate flaws and provide fixed code.",
        "UI Designer": "You are a frontend designer. Focus on aesthetic layouts and CSS styling."
    }
    
    # Allow customizing the system prompt dynamically
    custom_system_prompt = st.text_area("System Persona Prompt", value=system_prompts[mode], height=100)
    
    st.markdown("---")
    
    # Chat History Management (Save / Clear feature)
    if st.button("🗑️ Clear Chat History", use_container_width=True):
        st.session_state.messages = []
        st.rerun()
        
    st.markdown("🔒 **Protected Session**<br>Powered by VOID Framework", unsafe_allow_html=True)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat history messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input bar at the bottom
if prompt := st.chat_input("Ask for code, architecture, or design layout..."):
    if not API_KEY:
        st.error("⚠️ API Key is missing in app secrets. Please configure it in Streamlit settings.")
    else:
        # Add user message to state and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Prepare API payload
        headers = {
            "Authorization": f"Bearer {API_KEY.strip()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://void-ai-hub.streamlit.app",
            "X-Title": "VOID AI Hub"
        }
        
        # Send customized system prompt + user chat history
        messages_payload = [{"role": "system", "content": custom_system_prompt}]
        for m in st.session_state.messages:
            messages_payload.append({"role": m["role"], "content": m["content"]})
            
        data = {
            "model": model,
            "messages": messages_payload,
            "temperature": temperature,
            "max_tokens": max_tokens
        }

        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Synthesizing..."):
                try:
                    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
                    
                    if response.status_code == 200:
                        result = response.json()["choices"][0]["message"]["content"]
                        st.markdown(result)
                        # Save assistant response to history state
                        st.session_state.messages.append({"role": "assistant", "content": result})
                    else:
                        st.error(f"API Error ({response.status_code}): {response.text}")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")
