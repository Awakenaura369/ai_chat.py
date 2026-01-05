import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Morpheus AI", page_icon="👁️")

# 2. إعداد مفتاح API
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Matrix Error: API Key missing.")

# 3. واجهة المستخدم
st.title("👁️ Morpheus AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطقة الإدخال والرد (بدون صور نهائياً)
if prompt := st.chat_input("Ask Morpheus..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # رجعنا للموديل القديم والمستقر gemini-pro
            model = genai.GenerativeModel('gemini-pro')
            
            # تعليمات بسيطة مدمجة
            instruction = "You are Morpheus from 'Escape the Matrix'. Use a mysterious and philosophical tone."
            full_prompt = f"{instruction}\n\nUser Question: {prompt}"
            
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Glitch: {e}")
