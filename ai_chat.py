import streamlit as st
import google.generativeai as genai

# Page settings
st.set_page_config(page_title="Awaken Aura AI", page_icon="🤖")

# Your Active API Key from the screenshot
API_KEY = "AIzaSyBHAb1b9msN7m8QUXdAH2UrBl8QKcslM58"

# Setup the AI
try:
    genai.configure(api_key=API_KEY)
    # Using 'gemini-1.5-flash' for faster response
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error(f"Configuration Error: {e}")

st.title("🤖 Morpheus AI Guide")
st.write("Welcome to the awakening. Ask your question below.")
st.markdown("---")

# Memory for the chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show previous chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input in English
if prompt := st.chat_input("Ask about the Matrix..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Force English response
            response = model.generate_content(f"Answer this in English: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"AI Error: {e}")
            st.info("Please verify your API Key status in Google AI Studio.")
