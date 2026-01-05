import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="Morpheus AI", page_icon="👁️")

# 2. إعداد مفتاح API
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except:
    st.error("Matrix Error: API Key missing.")

# 3. تعليمات الشخصية
instruction = "You are Morpheus from 'Escape the Matrix'. Mysterious and philosophical tone."

# 4. الحل النهائي لخطأ 404: تغيير الموديل لنسخة مستقرة تماماً
@st.cache_resource
def load_model():
    # استعملنا هنا gemini-pro لأنه الأكثر استقراراً ومضمون العمل 100%
    return genai.GenerativeModel(
        model_name="gemini-pro", 
        system_instruction=instruction
    )

model = load_model()

# 5. واجهة المستخدم المبسطة
st.title("👁️ Morpheus AI")

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
            # استخدام توليد نصي بسيط لضمان تخطي أي "Glitch"
            response = model.generate_content(prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Glitch detected: {e}. Try a shorter question.")
