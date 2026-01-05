import streamlit as st
from groq import Groq

# 1. إعداد الصفحة وستايل الماتريكس (The Matrix Theme)
st.set_page_config(page_title="Morpheus AI", page_icon="👁️", layout="centered")

st.markdown("""
    <style>
    .main {
        background-color: #000000;
        color: #00FF41;
        font-family: 'Courier New', Courier, monospace;
    }
    .stTextInput>div>div>input {
        background-color: #0d0d0d;
        color: #00FF41;
        border: 1px solid #00FF41;
    }
    .stChatMessage {
        background-color: #0a0a0a !important;
        border-radius: 10px;
        border: 0.5px solid #00FF41;
        margin-bottom: 10px;
    }
    h1, h2, h3, p, span {
        color: #00FF41 !important;
        text-shadow: 0 0 5px #00FF41;
    }
    .stButton>button {
        background-color: #00FF41;
        color: black;
        border-radius: 5px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. الربط مع Groq
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
except Exception as e:
    st.error("Matrix Secrets Error: Check your Key.")
    st.stop()

st.title("👁️ MORPHEUS AI")
st.write("Welcome to the real world. I am your guide.")

# ذاكرة المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message:
            st.image(message["image"])

# 3. منطقة الإدخال والرد
if prompt := st.chat_input("Show me the truth..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # أ - توليد الصورة (Pollinations AI)
        image_url = None
        if any(word in prompt.lower() for word in ["صورة", "تخيل", "draw", "imagine", "image", "vision"]):
            with st.spinner("Decoding image from the Matrix..."):
                clean_prompt = prompt.replace(" ", "%20")
                image_url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024&model=flux"
                st.image(image_url)

        # ب - الرد النصي (Groq)
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are Morpheus. Speak in a mysterious, cool, and philosophical way. Use Matrix metaphors."},
                    *st.session_state.messages
                ],
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            
            # حفظ الرسالة
            new_msg = {"role": "assistant", "content": response}
            if image_url: new_msg["image"] = image_url
            st.session_state.messages.append(new_msg)
        except Exception as e:
            st.error(f"Glitch: {e}")
