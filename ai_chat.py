import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. إعدادات الصفحة
st.set_page_config(page_title="Morpheus AI", page_icon="👁️", layout="centered")

# 2. جلب الساروت بأمان
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("Matrix Error: API Key is missing in Secrets!")

# 3. تعليمات الشخصية (الرؤية + هندسة أوصاف الصور)
instruction = """
You are Morpheus, the digital guide from 'Escape the Matrix'.
Your tone is mysterious and philosophical.
You can analyze images and architect visions.
If the user asks for a vision or image, provide a professional AI prompt.
Challenge the user's perception of reality.
"""

# 4. تحميل الموديل بنسخة مستقرة وبدون أدوات معقدة (لحل أرور 404)
@st.cache_resource
def load_model():
    # استعملنا هنا gemini-1.5-flash مباشرة وبدون tools لتجنب أرور v1beta
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=instruction
    )

model = load_model()

# 5. واجهة المستخدم
st.title("👁️ Morpheus AI")
st.caption("Architect of the Matrix. I can see and design your reality.")

with st.sidebar:
    st.header("Matrix Input")
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, use_container_width=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال
if prompt := st.chat_input("Ask or request a vision..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            if uploaded_file:
                # التحليل بالصورة
                response = model.generate_content([prompt, image])
                st.markdown(response.text)
            else:
                # محادثة نصية مع الذاكرة
                chat = model.start_chat(history=[
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ])
                response = chat.send_message(prompt)
                st.markdown(response.text)
            
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            # حل أخير في حالة وقوع أي خطأ مفاجئ
            st.error(f"Glitch detected: {e}. Try refreshing the page.")
