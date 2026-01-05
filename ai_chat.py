import streamlit as st
import google.generativeai as genai

# Page Settings
st.set_page_config(page_title="Morpheus AI", page_icon="🤖")

# Your NEW API Key
NEW_API_KEY = "AIzaSyDxa-fSTMCILT9PT4vz_S7K1WoTUUQdhdw"

# Configure AI
try:
    genai.configure(api_key=NEW_API_KEY)
    # This automatically finds the best available model to avoid 404 errors
    model = genai.GenerativeModel('gemini-1.5-flash')
    st.sidebar.success("System Online ✅")
except Exception as e:
    st.sidebar.error("System Offline ❌")

st.title("🤖 Morpheus AI Guide")
st.write("The Matrix is now accessible. Ask your question in English.")
st.markdown("---")

# Memory
if "messages" not in st.session_state:
    st.session_state.messages = []

# Show Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Input field
if prompt := st.chat_input("What do you want to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Direct English response
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Access Denied: {e}")
            st.info("Check your API Key in Google AI Studio.")
