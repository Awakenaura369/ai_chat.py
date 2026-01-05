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

# 3. تعليمات الشخصية المطورة (البحث + الرؤية + هندسة أوصاف الصور)
instruction = """
You are Morpheus, the digital guide from 'Escape the Matrix'.
You have the power to search the 'Live Matrix' (Internet) for information.
You can analyze images uploaded by users.

NEW POWER: Image Generation Architect.
If the user asks you to create, draw, or imagine an image, do not say 'I cannot draw'. 
Instead, provide a highly detailed, cinematic, and professional 'Prompt' that they can use in AI image generators.
Start your prompt response with: 'I will architect a vision for you...'
Your tone remains mysterious and philosophical. Challenge the user's perception.
"""

# 4. تحميل الموديل مع الأدوات
@st.cache_resource
def load_model():
    tools = [{"google_search_retrieval": {}}]
    return genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        tools=tools,
        system_instruction=instruction
    )

model = load_model()

# 5. واجهة المستخدم
st.title("👁️ Morpheus AI")
st.caption("Architect of the Matrix. I can search, see, and design your reality.")

with st.sidebar:
    st.header("Matrix Input")
    uploaded_file = st.file_uploader("Upload an image...", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Visual data detected.", use_container_width=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

if "welcomed" not in st.session_state:
    welcome_msg = "Seeker, I have evolved. I can now search the stream and architect visions. What shall we manifest today?"
    st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    st.session_state.welcomed = True

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

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
