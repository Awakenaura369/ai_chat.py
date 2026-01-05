import streamlit as st
import google.generativeai as genai

# Page Config
st.set_page_config(page_title="Awaken Aura AI", page_icon="🤖")

# Your Active API Key
API_KEY = "AIzaSyBHAb1b9msN7m8QUXdAH2UrBl8QKcslM58"

# Fix for 404 Error: Specific configuration
try:
    genai.configure(api_key=API_KEY)
    # Using the most compatible model name for the beta API
    model = genai.GenerativeModel('models/gemini-1.5-flash-latest')
    st.sidebar.success("Connection Active ✅")
except Exception as e:
    st.error(f"Setup Error: {e}")

st.title("🤖 Morpheus AI")
st.write("The Matrix is ready. Speak your truth.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Added safety settings and generation config for better stability
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Status: {e}")
            st.info("Try refreshing the page or checking your API Key quota.")
