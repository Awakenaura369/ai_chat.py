import streamlit as st
import google.generativeai as genai

st.set_page_config(page_title="Morpheus AI", page_icon="🤖")

# دابا الكود كايجبد الساروت من الأسرار بلا ما يبان فـ GitHub
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
    
    available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
    if available_models:
        model_to_use = available_models[0]
        model = genai.GenerativeModel(model_to_use)
    else:
        st.error("No models found.")
except Exception as e:
    st.error("Please configure the API Key in Streamlit Secrets.")

st.title("🤖 Morpheus AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask Morpheus..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Error: {e}")
