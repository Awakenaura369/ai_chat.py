import streamlit as st
from groq import Groq

# 1. إعدادات الهوية البصرية (الأسود والأحمر لـ AGORAM AI)
st.set_page_config(page_title="AGORAM AI", page_icon="🤖")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stChatFloatingInputContainer { background-color: #0E1117; }
    .stChatMessage { border-radius: 10px; border: 1px solid #333; }
    /* ستايل مخصص لردود المساعد باللون الأحمر */
    .stChatMessage[data-testid="stChatMessageAssistant"] { 
        border-left: 4px solid #ff4b4b; 
        background-color: #1a1a1a; 
    }
    </style>
""", unsafe_allow_html=True)

# عنوان التطبيق مع الموديل الجديد
st.title("AGORAM AI 🤖")
st.caption("Powered by: Groq (Llama 3.3 70B)") # التحديث الجديد

# 2. الربط مع الساروت (GROQ_API_KEY)
# تأكد أن الساروت في Secrets كيبدا بـ gsk_ صغير
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Configuration Error: {e}")

# 3. نظام الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. استقبال الهضرة ومعالجتها
if prompt := st.chat_input("Message AGORAM AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استدعاء الموديل الجديد llama-3.3-70b-versatile
            chat_completion = client.chat.completions.create(
                messages=[
                    {
                        "role": "system", 
                        "content": "You are AGORAM AI, a wise and technical assistant. Answer in Moroccan Darija and English. Be helpful and direct."
                    },
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                model="llama-3.3-70b-versatile", # هادي هي اللي غاتحل أرور 400
            )
            
            response = chat_completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            # معالجة الأرورات بستايل الماتريكس
            st.error(f"Groq Matrix Error: {str(e)}")
