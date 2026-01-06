import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة - ضروري تكون أول سطر
st.set_page_config(page_title="AGORAM AI", layout="wide")

# 2. كود CSS قوي لإظهار السايدبار وتنسيق العنوان الأزرق
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    
    /* جعل العنوان الأزرق يظهر بوضوح */
    .blue-title {
        color: #00CCFF;
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin-top: -50px;
        text-shadow: 0 0 10px rgba(0, 204, 255, 0.4);
    }

    /* إظهار سهم السايدبار في الموبيل بزز */
    [data-testid="stSidebarNav"] { display: block !important; }
    button[kind="headerNoPadding"] { display: block !important; color: #00CCFF !important; }

    /* تحسين العرض الكامل */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        padding: 1rem !important;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. واجهة اختيار الموديلات (دابا غاتبان فوق الشات نيشان باش ما تدوخش)
st.markdown('<div class="blue-title">AGORAM AI 🤖</div>', unsafe_allow_html=True)

# اختيار الموديل من القائمة (مباشرة في الصفحة)
col1, col2 = st.columns([1, 1])
with col1:
    model_option = st.selectbox(
        "🧠 اختر العقل الذكي:",
        ("Llama 3.3 70B", "Qwen 2.5 32B", "Llama 3.2 Vision", "Whisper Large"),
        label_visibility="collapsed"
    )

# ربط الموديلات بـ Groq
model_mapping = {
    "Llama 3.3 70B": "llama-3.3-70b-versatile",
    "Qwen 2.5 32B": "qwen-2.5-32b",
    "Llama 3.2 Vision": "llama-3.2-11b-vision-preview",
    "Whisper Large": "whisper-large-v3"
}
selected_model = model_mapping[model_option]

# 4. السايدبار كاحتياط فيه زر الدعم
with st.sidebar:
    st.title("Settings")
    st.write(f"الموديل الحالي: {selected_model}")
    st.markdown('<a href="https://paypal.me/aipromptmoney" style="display:block; background:#0070ba; color:white; padding:10px; border-radius:10px; text-align:center; text-decoration:none; font-weight:bold;">☕ Buy me a Coffee</a>', unsafe_allow_html=True)

# 5. نظام الشات
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("سول أݣورام..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are AGORAM AI. Concise and smart."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                model=selected_model,
            )
            ans = chat_completion.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Error: {e}")
