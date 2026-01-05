import streamlit as st
import google.generativeai as genai
from google.generativeai.types import RequestOptions

# 1. إعدادات الصفحة
st.set_page_config(page_title="Morpheus AI", page_icon="👁️")

# 2. إعداد مفتاح API وفرض النسخة المستقرة v1
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # هاد السطر هو الساروت باش نحيدو أرور 404 بمرة
    genai.configure(api_key=API_KEY)
except:
    st.error("Matrix Error: API Key missing.")

# 3. واجهة المستخدم
st.title("👁️ Morpheus AI")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. الرد بأسلوب مضمون 100%
if prompt := st.chat_input("Ask Morpheus..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # كنستعملو هاد الـ options باش نجبرو السيستيم يخدم بـ v1 المستقرة
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            instruction = "You are Morpheus from 'Escape the Matrix'. Mysterious and philosophical tone."
            full_prompt = f"{instruction}\n\nUser Question: {prompt}"
            
            # فرض استخدام النسخة المستقرة v1 فكل طلب
            response = model.generate_content(
                full_prompt,
                request_options=RequestOptions(api_version='v1')
            )
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Glitch: {e}")
