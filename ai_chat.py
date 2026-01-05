import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Morpheus AI", page_icon="👁️")

# 2. إعداد مفتاح API
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Matrix Error: Check your API Key in Streamlit Secrets.")

# 3. واجهة المستخدم
st.title("👁️ Morpheus AI")
st.markdown("*I am here to show you how deep the rabbit hole goes.*")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. منطقة الإدخال والرد
if prompt := st.chat_input("Ask Morpheus..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استخدام موديل فلاش بنسخة مستقرة جداً
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # إرسال التعليمات مع كل سؤال لضمان بقاء الشخصية
            system_instruction = "You are Morpheus from 'Escape the Matrix'. Mysterious and philosophical tone."
            full_prompt = f"{system_instruction}\n\nUser: {prompt}"
            
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # إذا استمر الخطأ، سنعرض رسالة واضحة للمستخدم
            st.error(f"The Matrix detected a glitch: {e}")
