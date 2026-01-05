import streamlit as st
import google.generativeai as genai

# Page settings
st.set_page_config(page_title="Awaken Aura AI", page_icon="🤖")

# Your API Key from the screenshot
API_KEY = "AIzaSyBHAb1b9msN7m8QUXdAH2UrBl8QKcslM58"

# Setup AI with the stable model
try:
    genai.configure(api_key=API_KEY)
    # Changed from 'gemini-1.5-flash' to 'gemini-pro' to fix the 404 error
    model = genai.GenerativeModel('gemini-pro')
except Exception as e:
    st.error(f"Setup Error: {e}")

st.title("🤖 Morpheus AI Guide")
st.write("The connection is stable now. Ask your question.")
st.markdown("---")

# Memory for chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
if prompt := st.chat_input("Ask about the Matrix..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Simple and direct request
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"System Error: {e}")
