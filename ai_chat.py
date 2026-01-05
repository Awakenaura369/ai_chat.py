import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة والستايل (أسود وأحمر)
st.set_page_config(page_title="AGORAM AI", page_icon="🤖")
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stChatFloatingInputContainer { background-color: #0E1117; }
    .stChatMessage { border-radius: 10px; border: 1px solid #333; }
    </style>
""", unsafe_allow_html=True)

st.title("AGORAM AI 🤖")

# الربط مع Google Gemini باستخدام Secrets
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال السؤال
if prompt := st.chat_input("Message AGORAM AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تعليمات الشخصية (System Prompt) مدمجة في الطلب
            full_prompt = f"You are AGORAM AI, a wise and technical assistant. Speak in Moroccan Darija and English. Answer this: {prompt}"
            response = model.generate_content(full_prompt)
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Matrix Error: {e}")
