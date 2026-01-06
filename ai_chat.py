import streamlit as st
from groq import Groq

# 1. هادي هي أهم حاجة: لازم تكون أول سطر برمجي باش يتحل السايدبار
st.set_page_config(
    page_title="AGORAM AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded" 
)

# 2. تصميم الواجهة (العنوان بالأزرق الفاتح + تحسين المسافات)
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    
    /* ستايل العنوان الأزرق اللي عجبك */
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #00CCFF; 
        text-align: center;
        margin-top: -60px;
        margin-bottom: 30px;
        text-shadow: 0 0 15px rgba(0, 204, 255, 0.5);
    }

    /* توسيع المحتوى باش ميبقاش رقيق */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        width: 100% !important;
        padding: 1.5rem !important;
    }

    /* زر بايبال احترافي فالسيدبار */
    .support-btn {
        display: block; width: 100%; text-align: center; background-color: #0070ba; 
        color: white !important; padding: 12px; border-radius: 10px; 
        text-decoration: none; font-weight: bold; margin: 10px 0;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. القائمة الجانبية (Sidebar) ودمج موديلات Groq
with st.sidebar:
    st.markdown('<h1 style="color: #00CCFF;">AGORAM AI 🤖</h1>', unsafe_allow_html=True)
    st.header("⚙️ الموديلات المتاحة")
    
    # الموديلات اللي عندك في Groq بظبط
    model_option = st.selectbox(
        "اختر الموديل:",
        (
            "Llama 3.3 70B (قوي جداً)", 
            "Qwen 2.5 32B (برمجة)", 
            "Llama 3.2 11B (رؤية)",
            "Whisper (صوت)"
        )
    )
    
    model_mapping = {
        "Llama 3.3 70B (قوي جداً)": "llama-3.3-70b-versatile",
        "Qwen 2.5 32B (برمجة)": "qwen-2.5-32b",
        "Llama 3.2 11B (رؤية)": "llama-3.2-11b-vision-preview",
        "Whisper (صوت)": "whisper-large-v3"
    }
    selected_model = model_mapping[model_option]
    
    st.divider()
    st.markdown('<a href="https://paypal.me/aipromptmoney" target="_blank" class="support-btn">☕ دعم المشروع</a>', unsafe_allow_html=True)

# عرض العنوان الرئيسي بالأزرق
st.markdown('<div class="main-title">AGORAM AI 🤖</div>', unsafe_allow_html=True)

# 4. الربط الحقيقي مع Groq API
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# معالجة الشات
if prompt := st.chat_input("سول أݣورام..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تعليمات الذكاء
            system_msg = "You are AGORAM AI. Professional assistant. Respond in user language."
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_msg},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                model=selected_model, # الموديل اللي اختاريتي من السايدبار
            )
            
            ans = chat_completion.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Error: {e}")
