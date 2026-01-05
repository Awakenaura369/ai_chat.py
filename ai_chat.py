import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Awaken Aura AI", page_icon="🤖")

# Your Gemini API Key
genai.configure(api_key="AIzaSyBHAb1b9msN7m8QUXdAH2UrBl8QKcslM58")

# Using the stable 'gemini-pro' model
model = genai.GenerativeModel('gemini-pro')

st.title("🤖 Awaken Aura AI")
st.subheader("Your Strategic Guide to Reality")
st.markdown("---")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input Section
if prompt := st.chat_input("Ask me anything about the Matrix..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Explicitly asking for English response
            response = model.generate_content(f"Respond to this in English: {prompt}")
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error("Connection Error: Please verify your API Key or Network.")
