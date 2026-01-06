import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة والديكور
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .stChatMessage { border-radius: 12px; margin: 5px 1%; border: 1px solid #2d2d2d; }
    .stChatMessage[data-testid="stChatMessageAssistant"] { border-left: 4px solid #ff4b4b; background-color: #161b22; }
    .support-btn {
        display: block; width: 100%; text-align: center; background-color: #0070ba; 
        color: white !important; padding: 12px; border-radius: 10px; 
        text-decoration: none; font-weight: bold; margin: 10px 0;
    }
    </style>
""", unsafe_allow_html=True)

st.title("AGORAM AI 🤖")

# 2. القائمة الجانبية لاختيار الموديل ودعم PayPal
with st.sidebar:
    st.header("Settings")
    
    # اختيار الموديل من النماذج اللي شفتي فـ Groq
    model_option = st.selectbox(
        "Choose AI Model:",
        ("Llama 3.3 70B (Best)", "Llama 3.2 11B Vision", "Qwen 2.5 32B")
    )
    
    # تحويل الاختيار لـ Model ID الحقيقي
    model_mapping = {
        "Llama 3.3 70B (Best)": "llama-3.3-70b-versatile",
        "Llama 3.2 11B Vision": "llama-3.2-11b-vision-preview",
        "Qwen 2.5 32B": "qwen-2.5-32b"
    }
    selected_model = model_mapping[model_option]
    
    st.divider()
    st.markdown('<a href="https://paypal.me/aipromptmoney" target="_blank" class="support-btn">☕ Support via PayPal</a>', unsafe_allow_html=True)

# 3. الربط مع Groq
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. معالجة المحادثة
if prompt := st.chat_input("سول أݣورام..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            system_instruction = "You are AGORAM AI. Answer ONLY in the user's language. Be concise and smart."
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                model=selected_model, # الموديل كيتبدل على حسب شنو اختار المستخدم
            )
            
            ans = chat_completion.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Error: {e}")

st.markdown('<a href="https://paypal.me/aipromptmoney" target="_blank" class="support-btn">☕ Support via PayPal</a>', unsafe_allow_html=True)
