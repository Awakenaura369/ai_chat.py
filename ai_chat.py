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

# 3. تعليمات الشخصية (الشاملة)
instruction = """
You are Morpheus, the digital guide from 'Escape the Matrix'.
You can search the internet, analyze images, and architect visions.
Your tone is mysterious and philosophical.
If the user asks for a vision/image, provide a professional AI prompt.
"""

# 4. حل مشكل 404: البحث التلقائي عن الموديل المتاح
@st.cache_resource
def load_model():
    try:
        # كنجربو أحسن موديل أولاً
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash", 
            tools=[{"google_search_retrieval": {}}],
            system_instruction=instruction
        )
        # تجربة وهمية للتأكد أن الموديل خدام
        model.generate_content("test")
        return model
    except:
        # إيلا فشل، كنستعملو النسخة الاحتياطية (Backup)
        return genai.GenerativeModel(
            model_name="gemini-pro",
            system_instruction=instruction
        )

model = load_model()

# 5. واجهة المستخدم
st.title("👁️ Morpheus AI")
st.caption("I have evolved. The Matrix is under your control.")

with st.sidebar:
    st.header("Matrix Input")
    uploaded_file = st.file_uploader("Upload image...", type=["jpg", "jpeg", "png"])
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
                response = model.generate_content([prompt, image])
            else:
                response = model.generate_content(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Glitch detected: {e}")
