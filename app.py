import streamlit as st
import requests

# Minimalist configuration
st.set_page_config(page_title="VOID // AI Hub", page_icon="⚡", layout="centered")

st.title("VOID // AI Hub")
st.caption("Minimalist Coding & Design Assistant")
st.markdown("---")

# PERMANENTLY BAKED-IN CONFIGURATION (No input box errors)
API_KEY = "sk-or-v1-YOUR_ACTUAL_KEY_HERE"  # <-- sk-or-v1-cb27a917f5a6c9d4ae1b2f6cc0bde95f6088f895c992679268a0f75a36130e60Paste your exact OpenRouter key here inside the quotes

# Sidebar options
with st.sidebar:
    st.subheader("Settings")
    model = st.selectbox(
        "Model",
        [
            "deepseek/deepseek-chat:free",
            "qwen/qwen-2.5-coder-32b-instruct:free",
            "google/gemini-2.5-flash:free"
        ]
    )
    mode = st.selectbox(
        "Mode",
        ["Coder", "Architect", "Debugger", "UI Designer"]
    )

# Main Prompt Area
prompt = st.text_area("Enter your prompt or task:", height=130, placeholder="Write a clean Python script for...")

if st.button("Generate", type="primary", use_container_width=True):
    if API_KEY == "sk-or-v1-YOUR_ACTUAL_KEY_HERE" or not API_KEY.startswith("sk-or-v1-"):
        st.warning("⚠️ Please edit app.py on GitHub and insert your actual OpenRouter API key into the API_KEY variable.")
    elif not prompt:
        st.warning("⚠️ Please enter a prompt.")
    else:
        system_prompts = {
            "Coder": "You are an elite software engineer. Write clean, production-ready code.",
            "Architect": "You are a systems architect. Outline structure and logic clearly.",
            "Debugger": "You are an expert debugger. Isolate flaws and provide fixed code.",
            "UI Designer": "You are a frontend designer. Focus on aesthetic layouts and CSS styling."
        }
        
        with st.spinner("Processing request..."):
            headers = {
                "Authorization": f"Bearer {API_KEY.strip()}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://void-ai-hub.streamlit.app",
                "X-Title": "VOID AI Hub"
            }
            
            data = {
                "model": model,
                "messages": [
                    {"role": "system", "content": system_prompts[mode]},
                    {"role": "user", "content": prompt}
                ]
            }
            
            try:
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
                
                if response.status_code == 200:
                    result = response.json()["choices"][0]["message"]["content"]
                    st.markdown("### Output")
                    st.markdown(result)
                else:
                    st.error(f"API Error ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")
