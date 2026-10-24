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

# Securely load your API key from Streamlit Secrets (Friends cannot see or access this)
try:
    API_KEY = st.secrets["OPENROUTER_API_KEY"]
except Exception:
    API_KEY = ""

# Sidebar settings for model selection
with st.sidebar:
    st.subheader("⚙️ Settings")
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
    st.markdown("🔒 **Protected Session**<br>Powered by VOID Framework", unsafe_allow_html=True)

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display prior chat history messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input bar at the bottom (just like ChatGPT)
if prompt := st.chat_input("Ask for code, architecture, or design layout..."):
    if not API_KEY:
        st.error("⚠️ API Key is missing in app secrets. Please configure it in Streamlit settings.")
    else:
        # Add user message to state and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Define system prompts based on mode
        system_prompts = {
            "Coder": "You are an elite software engineer. Write clean, production-ready code.",
            "Architect": "You are a systems architect. Outline structure and logic clearly.",
            "Debugger": "You are an expert debugger. Isolate flaws and provide fixed code.",
            "UI Designer": "You are a frontend designer. Focus on aesthetic layouts and CSS styling."
        }
        
        # Prepare API payload
        headers = {
            "Authorization": f"Bearer {API_KEY.strip()}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://void-ai-hub.streamlit.app",
            "X-Title": "VOID AI Hub"
        }
        
        # Send system prompt + user chat history to OpenRouter
        messages_payload = [{"role": "system", "content": system_prompts[mode]}]
        for m in st.session_state.messages:
            messages_payload.append({"role": m["role"], "content": m["content"]})
            
        data = {
            "model": model,
            "messages": messages_payload
        }

        # Generate AI response
        with st.chat_message("assistant"):
            with st.spinner("Synthesizing..."):
                try:
                    response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
                    
                    if response.status_code == 200:
                        result = response.json()["choices"][0]["message"]["content"]
                        st.markdown(result)
                        # Save assistant response to history
                        st.session_state.messages.append({"role": "assistant", "content": result})
                    else:
                        st.error(f"API Error ({response.status_code}): {response.text}")
                except Exception as e:
                    st.error(f"Connection Failed: {e}")
