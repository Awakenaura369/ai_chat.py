import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Morpheus AI", page_icon="🤖")

# الساروت الجديد ديالك
API_KEY = "AIzaSyDxa-fSTMCILT9PT4vz_S7K1WoTUUQdhdw"

try:
    genai.configure(api_key=API_KEY)
    
    # هاد السطر كايجبد كاع الموديلات اللي خدامين عندك وكايختار أول واحد كايقبل توليد المحتوى
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if available_models:
        model_to_use = available_models[0]
        model = genai.GenerativeModel(model_to_use)
        st.sidebar.success(f"System Online")
    else:
        st.error("No compatible models found in your account.")
except Exception as e:
    st.error(f"Connection Error: {e}")

st.title("🤖 Morpheus AI Guide")
st.write("Ask your question in English.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("What do you want to know?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"AI Error: {e}")
