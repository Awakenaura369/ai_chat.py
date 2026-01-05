import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="Morpheus AI", page_icon="👁️", layout="centered")

# 2. إعداد مفتاح الـ API من Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Matrix Error: Check your Streamlit Secrets for the API Key.")

# 3. تعريف التعليمات البرمجية للشخصية
# قمنا بتبسيطها لضمان عدم وقوع تعارض (Conflict)
instruction = """
You are Morpheus, the digital guide from 'Escape the Matrix'.
Your tone is mysterious and philosophical. 
You can analyze images and provide expert AI image prompts.
Challenge the user's reality in every response.
"""

# 4. تحميل الموديل بأبسط طريقة ممكنة لتفادي خطأ 404
@st.cache_resource
def load_stable_model():
    # استدعاء الموديل مباشرة بدون أدوات (Tools) لضمان الاستقرار
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=instruction
    )

model = load_stable_model()

# 5. واجهة المستخدم والتصميم
st.title("👁️ Morpheus AI")
st.markdown("*Architect of the Matrix. I can see and design your reality.*")

# شريط جانبي لرفع الصور
with st.sidebar:
    st.header("Visual Input")
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        img = Image.open(uploaded_file)
        st.image(img, caption="Image detected in the Matrix.", use_container_width=True)

# إدارة سجل الرسائل
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال
if prompt := st.chat_input("Ask or request a vision..."):
    # إضافة رسالة المستخدم للسجل
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد من مورفيوس
    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                # إذا كانت هناك صورة، نرسلها مع السؤال
                response = model.generate_content([prompt, img])
            else:
                # رد نصي عادي مع الحفاظ على السياق
                chat = model.start_chat(history=[])
                response = chat.send_message(prompt)
            
            output_text = response.text
            st.markdown(output_text)
            st.session_state.messages.append({"role": "assistant", "content": output_text})
            
        except Exception as e:
            st.error(f"Glitch detected: {e}. Please try refreshing the page.")
