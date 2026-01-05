import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة (Design Black & Red)
st.set_page_config(page_title="AGORAM AI", page_icon="🤖")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    /* تنسيق الرسائل باش ما تبقاش لاصقة فـ الجناب */
    .stChatMessage { 
        border-radius: 15px; 
        margin: 10px 5%; 
        border: 1px solid #333; 
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] { 
        border-left: 5px solid #ff4b4b; 
        background-color: #1a1a1a; 
    }
    /* تحسين شكل الكتابة */
    .stMarkdown p { font-size: 1.1rem; line-height: 1.6; }
    </style>
""", unsafe_allow_html=True)

st.title("AGORAM AI 🤖")
st.caption("Multilingual Edition: Darija & English | Powered by Llama 3.3")

# 2. الربط مع الساروت (Groq)
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error(f"Secret Key Error: {e}")

# 3. نظام الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. معالجة الهضرة (الدارجة + الإنجليزية)
if prompt := st.chat_input("Ask AGORAM AI anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تعليمات صارمة للموديل باش يجاوب بجوج لغات ديما
            system_instruction = """
            You are AGORAM AI. You must ALWAYS provide your answer in two parts:
            1. Response in Moroccan Darija (Maghrebi Arabic).
            2. A 'Technical Summary' in English.
            Use horizontal lines (---) to separate them clearly.
            """
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                model="llama-3.3-70b-versatile", # أحدث موديل شغال حالياً
            )
            
            full_response = chat_completion.choices[0].message.content
            st.markdown(full_response)
            st.session_state.messages.append({"role": "assistant", "content": full_response})
            
        except Exception as e:
            st.error(f"Matrix Error: {str(e)}")
