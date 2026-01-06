import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="wide")

# 2. تصميم الواجهة الاحترافية
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .blue-title {
        color: #00CCFF; font-size: 2.8rem; font-weight: bold;
        text-align: center; margin-top: -50px;
        text-shadow: 0 0 15px rgba(0, 204, 255, 0.4);
    }
    /* جعل السايدبار والموديلات باينين */
    [data-testid="stSidebarNav"] { display: block !important; }
    [data-testid="stAppViewBlockContainer"] { max-width: 100% !important; padding: 1rem !important; }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="blue-title">AGORAM AI 🤖</div>', unsafe_allow_html=True)

# 3. دمج الموديلات من صورتك فـ Groq
with st.sidebar:
    st.markdown('<h2 style="color: #00CCFF;">إعدادات التطبيق</h2>', unsafe_allow_html=True)
    model_option = st.selectbox(
        "اختر الموديل:",
        ("Llama 3.3 70B", "Qwen 2.5 32B", "Llama 3.2 Vision", "Whisper Large")
    )
    model_mapping = {
        "Llama 3.3 70B": "llama-3.3-70b-versatile",
        "Qwen 2.5 32B": "qwen-2.5-32b",
        "Llama 3.2 Vision": "llama-3.2-11b-vision-preview",
        "Whisper Large": "whisper-large-v3"
    }
    selected_model = model_mapping[model_option]
    st.divider()
    st.markdown('<a href="https://paypal.me/aipromptmoney" style="display:block; background:#0070ba; color:white; padding:10px; border-radius:10px; text-align:center; text-decoration:none;">☕ دعم المشروع</a>', unsafe_allow_html=True)

# 4. محرك الشات
client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if "messages" not in st.session_state: st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

if prompt := st.chat_input("سول أݣورام..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are AGORAM AI."},
                          *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]],
                model=selected_model,
            )
            ans = res.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e: st.error(f"Error: {e}")
