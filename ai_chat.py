import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة الأساسية
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="wide")

# 2. كود الـ CSS المطور (إظهار السهم بلون أزرق + تنسيق العنوان)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    
    /* تنسيق العنوان الأزرق الفاتح */
    .main-title {
        font-size: 2.8rem;
        font-weight: bold;
        color: #00CCFF; 
        text-align: center;
        margin-top: -60px;
        margin-bottom: 10px;
        text-shadow: 0 0 15px rgba(0, 204, 255, 0.4);
    }

    /* جعل السايدبار يظهر غصب عنه في الموبيل */
    [data-testid="stSidebarNav"] { display: block !important; }
    
    /* تحسين شكل المدخلات (Selectbox) */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #161b22 !important;
        border: 1px solid #00CCFF !important;
        border-radius: 10px;
    }

    /* توسيع الصفحة */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        padding: 1.5rem !important;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. عرض العنوان بالأزرق
st.markdown('<div class="main-title">AGORAM AI 🤖</div>', unsafe_allow_html=True)

# --- الخطوة السحرية: حط الموديلات وسط الصفحة باش يبانو ليك ديما ---
# اختيار الموديل (دابا غيبان ليك تحت العنوان نيشان)
model_option = st.selectbox(
    "🤖 اختر عقل الذكاء الاصطناعي:",
    ("Llama 3.3 70B (الأقوى)", "Qwen 2.5 32B (برمجة)", "Llama 3.2 Vision (صور)", "Whisper (صوت)"),
    index=0
)

model_mapping = {
    "Llama 3.3 70B (الأقوى)": "llama-3.3-70b-versatile",
    "Qwen 2.5 32B (برمجة)": "qwen-2.5-32b",
    "Llama 3.2 Vision (صور)": "llama-3.2-11b-vision-preview",
    "Whisper (صوت)": "whisper-large-v3"
}
selected_model = model_mapping[model_option]

# السايدبار نخليه فقط للأشياء الثانوية كاحتياط
with st.sidebar:
    st.header("إعدادات إضافية")
    st.write(f"الموديل النشط: {selected_model}")
    st.divider()
    st.markdown('<a href="https://paypal.me/aipromptmoney" style="display:block; background:#0070ba; color:white; padding:12px; border-radius:10px; text-align:center; text-decoration:none; font-weight:bold;">☕ دعم مشروع أݣورام</a>', unsafe_allow_html=True)

# 4. محرك الدردشة (Groq)
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
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are AGORAM AI. Professional & Smart."},
                          *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]],
                model=selected_model,
            )
            ans = res.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Error: {e}")
