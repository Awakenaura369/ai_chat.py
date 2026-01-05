import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Morpheus AI", page_icon="👁️")

# 2. إعداد مفتاح API
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    st.error("Matrix Error: API Key missing in Secrets.")

# 3. واجهة المستخدم
st.title("👁️ Morpheus AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. الرد (أبسط طريقة ممكنة لتجنب 404)
if prompt := st.chat_input("Ask Morpheus..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استخدام الموديل بدون أي إعدادات إضافية لضمان العمل
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            # إرسال النص مباشرة
            response = model.generate_content(f"You are Morpheus. Answer this: {prompt}")
            
            if response.text:
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # محاولة أخيرة بموديل مختلف إذا فشل الأول
            try:
                model_backup = genai.GenerativeModel('gemini-pro')
                response = model_backup.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e2:
                st.error(f"Matrix Glitch: {e2}")
