import streamlit as st
from groq import Groq

# إعدادات الصفحة للموبيل (Mobile First)
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    /* تحسين الألوان وتصغير المساحات للموبيل */
    .stApp { background-color: #0E1117; color: white; }
    .stChatMessage { 
        border-radius: 12px; 
        margin: 5px 1%; 
        border: 1px solid #2d2d2d; 
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] { 
        border-left: 4px solid #ff4b4b; 
        background-color: #161b22; 
    }
    /* تصغير الخط باش ما يعمرش الشاشة */
    .stMarkdown p { font-size: 0.95rem !important; line-height: 1.5; }
    h1 { font-size: 1.4rem !important; text-align: center; }
    </style>
""", unsafe_allow_html=True)

st.title("AGORAM AI 🤖")

# الربط مع Groq بالساروت اللي عندك
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Check your API Key in Secrets.")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask me anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # هادي هي "العقلية" اللي طلبتي: كيتفاعل مع لغة السائل
            system_instruction = """
            You are AGORAM AI, a highly intelligent and flexible assistant. 
            Instruction: Respond in the SAME language the user uses. 
            - If they speak Darija, answer in Darija. 
            - If they speak English, answer in English. 
            - Match their tone and professional level (Engineer, Doctor, Creator, etc.).
            Be concise and don't repeat the answer in other languages unless asked.
            """
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                model="llama-3.3-70b-versatile", # الموديل الأقوى حالياً
            )
            
            ans = chat_completion.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Error: {e}")
