import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة
st.set_page_config(page_title="Morpheus AI", page_icon="👁️")

# 2. إعداد مفتاح API وفرض النسخة المستقرة v1
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    # فرض استخدام النسخة v1 المستقرة لتجنب أرور 404
    genai.configure(api_key=API_KEY, transport='rest') 
except:
    st.error("Matrix Error: API Key missing.")

# 3. تعليمات الشخصية
instruction = "You are Morpheus from 'Escape the Matrix'. Mysterious and philosophical tone."

# 4. استدعاء الموديل بأبسط طريقة وبدون أي إضافات
@st.cache_resource
def load_model():
    # استخدام gemini-1.5-flash كاسم مباشر
    return genai.GenerativeModel(model_name="gemini-1.5-flash")

model = load_model()

# 5. واجهة المستخدم
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
            # إرسال الرسالة مع التعليمات يدوياً لضمان الاستقرار
            full_prompt = f"{instruction}\n\nUser: {prompt}"
            response = model.generate_content(full_prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Glitch detected: {e}. Try again in a moment.")
