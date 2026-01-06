import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة - جعل السايدبار مفتوح افتراضياً
st.set_page_config(
    page_title="AGORAM AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. تصميم الـ CSS (العنوان بالأزرق الفاتح والواجهة)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    
    /* العنوان بالأزرق الفاتح */
    .main-title {
        font-size: 2.8rem;
        font-weight: bold;
        color: #00CCFF; 
        text-align: center;
        margin-top: -50px;
        margin-bottom: 20px;
        text-shadow: 2px 2px 10px rgba(0, 204, 255, 0.3);
    }

    /* توسيع الحاوية لتملأ الشاشة */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        width: 100% !important;
        padding: 1.5rem !important;
    }

    /* إظهار سهم السايدبار في الموبيل */
    [data-testid="stSidebarNav"] { display: block !important; }

    /* زر PayPal الاحترافي */
    .support-btn {
        display: block; width: 100%; text-align: center; background-color: #0070ba; 
        color: white !important; padding: 12px; border-radius: 10px; 
        text-decoration: none; font-weight: bold; margin: 10px 0;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- القائمة الجانبية (Sidebar) ودمج الموديلات من Groq ---
with st.sidebar:
    st.markdown('<h1 style="color: #00CCFF;">AGORAM AI 🤖</h1>', unsafe_allow_html=True)
    st.header("⚙️ الإعدادات الذكية")
    
    # دمج الموديلات اللي ظهرت في صورة Groq
    model_option = st.selectbox(
        "اختر عقل الذكاء الاصطناعي:",
        (
            "Llama 3.3 70B (الأقوى والأسرع)", 
            "Qwen 2.5 32B (خبير البرمجة)", 
            "Llama 3.2 11B Vision (رؤية الصور)",
            "Whisper Large v3 (تحويل الصوت لنص)"
        )
    )
    
    # ربط الاختيارات بأسماء النماذج الحقيقية في Groq
    model_mapping = {
        "Llama 3.3 70B (الأقوى والأسرع)": "llama-3.3-70b-versatile",
        "Qwen 2.5 32B (خبير البرمجة)": "qwen-2.5-32b",
        "Llama 3.2 11B Vision (رؤية الصور)": "llama-3.2-11b-vision-preview",
        "Whisper Large v3 (تحويل الصوت لنص)": "whisper-large-v3"
    }
    selected_model = model_mapping[model_option]
    
    st.divider()
    st.markdown("### دعم استمرارية المشروع")
    st.markdown('<a href="https://paypal.me/aipromptmoney" target="_blank" class="support-btn">☕ دعم عبر PayPal</a>', unsafe_allow_html=True)

# عرض العنوان الرئيسي بالأزرق الفاتح
st.markdown('<div class="main-title">AGORAM AI 🤖</div>', unsafe_allow_html=True)

# 3. الربط مع Groq API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 4. معالجة الدردشة
if prompt := st.chat_input("سول أݣورام أو اطلب مساعدة..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تعليمات النظام لضمان ذكاء أݣورام
            system_msg = "You are AGORAM AI. Answer concisely in the user's language. Be smart and professional."
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_msg},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                model=selected_model, # الموديل المختار من القائمة
            )
            
            ans = chat_completion.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Error: {e}")
