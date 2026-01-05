import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="Awaken Aura AI", page_icon="🤖")

# Your Gemini API Key
genai.configure(api_key="AIzaSyBHAb1b9msN7m8QUXdAH2UrBl8QKcslM58")

# System Instructions in English
instruction = """
You are 'Morpheus AI', the digital guide for the 'Awaken Aura' platform. 
Your mission is to help users understand and escape the 'Mental Matrix'. 
Tone: Deep, philosophical, empowering, and professional. 
Context: Use concepts from the 'Escape the Matrix' philosophy. 
Always respond in English.
"""

# Initialize the model
model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=instruction)

st.title("🤖 Awaken Aura AI")
st.subheader("Your Guide to Escaping the Matrix")
st.markdown("---")

# Chat History Management
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask Morpheus anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # Generate English response
        response = model.generate_content(prompt)
        st.markdown(response.text)
        st.session_state.messages.append({"role": "assistant", "content": response.text})
