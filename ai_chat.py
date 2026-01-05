import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Morpheus AI", page_icon="👁️")

# 2. الربط مع Google (أبسط طريقة)
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Matrix Error: API Key missing in Streamlit Secrets.")

st.title("👁️ Morpheus AI")
st.markdown("---")

# 3. نظام الذاكرة (Session State)
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطق الرد
if prompt := st.chat_input("Speak, seeker..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استعمال الموديل الخام بدون أي تعقيدات
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # تعليمات الشخصية مدمجة فالسؤال
            instruction = "You are Morpheus from 'Escape the Matrix'. Mysterious tone."
            response = model.generate_content(f"{instruction}\nUser: {prompt}")
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Glitch: {e}")
