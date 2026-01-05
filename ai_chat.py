import streamlit as st
import google.generativeai as genai

# 1. إعدادات الهوية البصرية (الأسود والأحمر)
st.set_page_config(page_title="AGORAM AI", page_icon="🤖")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stChatFloatingInputContainer { background-color: #0E1117; }
    .stChatMessage { border-radius: 10px; border: 1px solid #333; }
    /* ستايل مخصص للردود */
    .stChatMessage[data-testid="stChatMessageAssistant"] { border-left: 4px solid #ff4b4b; background-color: #1a1a1a; }
    </style>
""", unsafe_allow_html=True)

# عنوان التطبيق مع اسم الموديل
st.title("AGORAM AI 🤖")
st.caption("Powered by: Gemini 1.5 Flash") # هنا فين زدنا سميت النمودج

# 2. الربط مع الساروت اللي عطيتيني
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-1.5-flash')

# 3. نظام الذاكرة والشخصية
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. استقبال ومعالجة الهضرة
if prompt := st.chat_input("Message AGORAM AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تعليمات الشخصية المغربية الحكيمة
            system_instruction = "You are AGORAM AI. Answer in Moroccan Darija and English. Be wise, technical, and helpful."
            response = model.generate_content(f"{system_instruction}\n\nUser: {prompt}")
            
            full_response = response.text
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
        except Exception as e:
            st.error(f"Matrix Error: {str(e)}")
