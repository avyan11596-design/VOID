import streamlit as st
import requests

st.set_page_config(page_title="VOID // AI Hub", page_icon="⚡", layout="centered")

st.title("VOID // AI Hub")
st.caption("Minimalist Coding & Design Assistant")
st.markdown("---")

with st.sidebar:
    st.subheader("Settings")
    # Leave this blank by default so it forces a clean entry
    api_key = st.text_input("OpenRouter API Key", type="password", placeholder="sk-or-v1-...")
    
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

prompt = st.text_area("Enter your prompt or task:", height=130, placeholder="Write a clean Python script for...")

if st.button("Generate", type="primary", use_container_width=True):
    if not api_key:
        st.warning("Please paste your OpenRouter API key into the sidebar.")
    elif not prompt:
        st.warning("Please enter a prompt.")
    else:
        system_prompts = {
            "Coder": "You are an elite software engineer. Write clean, production-ready code.",
            "Architect": "You are a systems architect. Outline structure and logic clearly.",
            "Debugger": "You are an expert debugger. Isolate flaws and provide fixed code.",
            "UI Designer": "You are a frontend designer. Focus on aesthetic layouts and CSS styling."
        }
        
        with st.spinner("Processing..."):
            headers = {
                "Authorization": f"Bearer {api_key.strip()}",
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
                    st.error(f"Error ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"Connection Failed: {e}")
