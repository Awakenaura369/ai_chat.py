import streamlit as st
from openai import OpenAI

# 1. إعدادات الصفحة والهوية البصرية
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="centered")

# CSS المطور للون الأسود والأحمر وحماية الواجهة
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; border: 1px solid #333; }
    .stChatInputContainer { border-top: 1px solid #ff4b4b !important; }
    /* ستايل الماتريكس للأخطاء */
    .stAlert { background-color: #1a0a0a; border: 1px solid #ff4b4b; color: #ff4b4b; }
    </style>
""", unsafe_allow_html=True)

st.title("AGORAM AI 🤖")
st.caption("Universal Intelligence: Technical Precision & Philosophical Wisdom")

# 2. الربط مع OpenAI
client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

# 3. نظام الذاكرة والشخصية
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": "You are AGORAM AI. You are a wise, technical, and philosophical assistant. You speak in Moroccan Darija and English. You provide deep insights and avoid Matrix errors."}
    ]

# عرض الرسائل (بلا ما نبينو الـ System Prompt)
for message in st.session_state.messages:
    if message["role"] != "system":
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

# 4. إضافة ميزة رفع الصور (باش يولي كامل مكمول)
uploaded_file = st.file_uploader("Upload an image for analysis...", type=["jpg", "png", "jpeg"])

# 5. معالجة المدخلات
if prompt := st.chat_input("Message AGORAM AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استخدام موديل gpt-4o المتطور
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=st.session_state.messages,
                max_tokens=1000
            )
            full_response = response.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Matrix Error: {str(e)}")
