import streamlit as st
import requests

# Page Configuration
st.set_page_config(page_title="Void AI Coding Hub", page_icon="🚀", layout="wide")

st.title("🚀 Void AI Coding Hub")
st.markdown("A lightweight coding & design assistant for the crew. Enter your OpenRouter API key below to start.")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    api_key_input = st.text_input("OpenRouter API Key", type="password", help="Paste your OpenRouter API key here.")
    
    # Selection of top-tier coding models available on OpenRouter
    model_choice = st.selectbox(
        "Choose Model",
        [
            "deepseek/deepseek-chat", 
            "qwen/qwen-2.5-coder-32b-instruct", 
            "anthropic/claude-3.5-sonnet",
            "google/gemini-flash-1.5"
        ]
    )
    st.markdown("---")
    st.markdown("**Status:** Ready for action ⚡")

# Main Interface for Prompting
prompt = st.text_area("💬 Paste your coding task, design layout, or bug description:", height=150, placeholder="Write a clean Python script for...")

if st.button("Generate Code & Design", type="primary"):
    if not api_key_input:
        st.warning("⚠️ Please enter your OpenRouter API Key in the sidebar first!")
    elif not prompt:
        st.warning("⚠️ Please enter a prompt or coding question.")
    else:
        with st.spinner("🤖 Coding in progress... synthesizing architecture..."):
            headers = {
                "Authorization": f"Bearer {api_key_input}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://void-ai-hub.streamlit.app", # Optional, helps OpenRouter track app
                "X-Title": "Void AI Coding Hub"
            }
            data = {
                "model": model_choice,
                "messages": [{"role": "user", "content": prompt}]
            }
            
            try:
                response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)
                
                if response.status_code == 200:
                    result_json = response.json()
                    ai_response = result_json["choices"][0]["message"]["content"]
                    
                    st.success("✨ Output Generated Successfully!")
                    st.markdown("### Result:")
                    st.markdown(ai_response)
                else:
                    st.error(f"❌ API Error ({response.status_code}): {response.text}")
            except Exception as e:
                st.error(f"❌ Connection Failed: {e}")
