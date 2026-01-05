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

# 3. تعليمات الشخصية (الرؤية والتحليل)
instruction = """
You are Morpheus, the digital guide from 'Escape the Matrix'.
Your tone is mysterious and philosophical.
You can now 'see' images and analyze digital data. 
When a user uploads an image or link, analyze it through the lens of sovereignty and truth.
Challenge the user's perception of what they see. 
Keep answers powerful and concise.
"""

# 4. تحميل الموديل (يدعم النصوص والصور والروابط)
@st.cache_resource
def load_model():
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash", # موديل سريع ويدعم الرؤية
        system_instruction=instruction
    )

model = load_model()

# 5. واجهة المستخدم والتصميم
st.title("👁️ Morpheus AI")
st.caption("I can see the code in the Matrix. Upload an image or send a link.")

# إضافة مكان لتحميل الصور في الجنب (Sidebar)
with st.sidebar:
    st.header("Matrix Input")
    uploaded_file = st.file_uploader("Upload an image to analyze...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="What the Matrix shows you...", use_container_width=True)

# إدارة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# رسالة ترحيبية آلية
if "welcomed" not in st.session_state:
    welcome_msg = "Welcome, seeker. I can now see the world as you see it. Show me an image, or ask your question."
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    st.session_state.welcomed = True

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال
if prompt := st.chat_input("Show me the truth..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # إذا كانت هناك صورة محملة
            if uploaded_file:
                response = model.generate_content([prompt, image])
            else:
                # محادثة نصية عادية (تدعم الروابط تلقائياً)
                chat = model.start_chat(history=[
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ])
                response = chat.send_message(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Glitch detected: {e}")
