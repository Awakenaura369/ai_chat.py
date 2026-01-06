import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة - Mobile First Design
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    /* تحسين شكل الرسائل فـ الموبيل */
    .stChatMessage { border-radius: 12px; margin: 5px 1%; border: 1px solid #2d2d2d; }
    .stChatMessage[data-testid="stChatMessageAssistant"] { border-left: 4px solid #ff4b4b; background-color: #161b22; }
    .stMarkdown p { font-size: 0.95rem; line-height: 1.5; }
    
    /* ستايل زر الدعم (PayPal) */
    .support-btn {
        display: block;
        width: 100%;
        text-align: center;
        background-color: #0070ba; /* لون بايبال الرسمي */
        color: white !important;
        padding: 12px;
        border-radius: 10px;
        text-decoration: none;
        font-weight: bold;
        margin: 20px 0;
        border: 1px solid #005ea6;
    }
    .support-btn:hover { background-color: #005ea6; }
    </style>
""", unsafe_allow_html=True)

st.title("AGORAM AI 🤖")

# 2. زر PayPal فـ Sidebar وفي أسفل الصفحة للموبيل
with st.sidebar:
    st.markdown('### Support the Project')
    st.markdown('<a href="https://paypal.me/aipromptmoney" target="_blank" class="support-btn">☕ Support via PayPal</a>', unsafe_allow_html=True)
    st.caption("دعمك كيخلي أݣورام يطور ويستمر.")

# 3. الربط مع Groq (الموديل الأقوى)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. معالجة البحث والذكاء المرن
if prompt := st.chat_input("سول أݣورام أو ابحث..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # العقلية المرنة اللي كتفاعل مع لغة الزائر
            system_instruction = """
            You are AGORAM AI, an advanced AI with real-time web knowledge.
            - Language: ALWAYS respond in the same language as the user (Darija, English, French, etc.).
            - Web Search: You have real-time access to information. If the user asks for news or facts, act as a search engine.
            - Personality: Be helpful, technical, and concise. No unnecessary language repetition.
            """
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                model="llama-3.3-70b-versatile", # الموديل اللي كيدعم البحث والسرعة
            )
            
            ans = chat_completion.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Error: {e}")

# إضافة الزر فـ الأسفل باش يبان فـ الموبيل بلا ما يفتح Sidebar
st.markdown('<a href="https://paypal.me/aipromptmoney" target="_blank" class="support-btn">☕ Support via PayPal</a>', unsafe_allow_html=True)
