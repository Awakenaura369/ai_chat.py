import streamlit as st
from groq import Groq
import google.generativeai as genai
from PIL import Image
import io

# 1. إعدادات الصفحة المتقدمة
st.set_page_config(page_title="Morpheus AI Pro", page_icon="👁️", layout="wide")

# ستايل الماتريكس المتطور
st.markdown("""
    <style>
    .main { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stChatMessage { background-color: #0a0a0a !important; border: 1px solid #00FF41; border-radius: 15px; }
    .stSidebar { background-color: #050505 !important; border-right: 1px solid #00FF41; }
    h1, h2, h3 { color: #00FF41 !important; text-shadow: 0 0 10px #00FF41; }
    .stFileUploader { border: 1px dashed #00FF41; border-radius: 10px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# 2. إدارة المفاتيح
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"].strip())
except:
    st.error("Missing API Keys in Secrets!")
    st.stop()

# 3. الشريط الجانبي (Sidebar) للتحكم الاحترافي
with st.sidebar:
    st.title("⚙️ Control Panel")
    model_option = st.selectbox("Choose Brain:", ["Llama-3.3-70b (Fast)", "Gemini-1.5-Flash (Vision)"])
    temp = st.slider("Creativity Level:", 0.0, 1.0, 0.7)
    
    st.markdown("---")
    uploaded_file = st.file_uploader("Upload Image or Document:", type=["pdf", "txt", "png", "jpg", "jpeg"])
    
    if st.button("🗑️ Clear Matrix Memory"):
        st.session_state.messages = []
        st.rerun()

st.title("👁️ MORPHEUS AI PRO")
st.caption("The ultimate interface to the real world.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message: st.image(message["image"])

# 4. منطق الإدخال والرد الاحترافي
if prompt := st.chat_input("Enter your command..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        full_response = ""
        image_url = None
        
        # أ - معالجة الصور إيلا ترفعات
        if uploaded_file and model_option == "Gemini-1.5-Flash (Vision)":
            with st.spinner("Analyzing data..."):
                img = Image.open(uploaded_file)
                model_v = genai.GenerativeModel('gemini-1.5-flash')
                res = model_v.generate_content([prompt, img])
                full_response = res.text
        
        # ب - توليد الصور (Pollinations)
        elif any(word in prompt.lower() for word in ["صورة", "تخيل", "draw", "imagine"]):
            with st.spinner("Visualizing..."):
                clean_prompt = prompt.replace(" ", "%20")
                image_url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024&model=flux"
                st.image(image_url)
                full_response = "I have visualized your request from the Matrix data streams."

        # ج - الرد النصي العادي (Groq)
        else:
            try:
                chat_completion = groq_client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "You are Morpheus Pro. Expert, philosophical, and highly capable."}, *st.session_state.messages],
                    temperature=temp
                )
                full_response = chat_completion.choices[0].message.content
            except Exception as e:
                full_response = f"Glitch detected: {str(e)}"

        st.markdown(full_response)
        
        # حفظ في الذاكرة
        msg_data = {"role": "assistant", "content": full_response}
        if image_url: msg_data["image"] = image_url
        st.session_state.messages.append(msg_data)
