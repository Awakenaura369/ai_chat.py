import streamlit as st
import time

# إعدادات الصفحة
st.set_page_config(
    page_title="AGORAM AI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded" # القائمة الجانبية كتبان من الدقة الأولى
)

# تصميم الـ CSS لتعديل الألوان والواجهة
st.markdown("""
    <style>
    /* تغيير لون العنوان الرئيسي للأزرق الفاتح */
    .main-title {
        font-size: 2.5rem;
        font-weight: bold;
        color: #00CCFF; /* اللون الأزرق الفاتح */
        text-align: center;
        margin-top: -50px;
        margin-bottom: 25px;
        text-shadow: 2px 2px 5px rgba(0,0,0,0.3);
    }
    
    /* تحسين شكل القائمة الجانبية */
    [data-testid="stSidebar"] {
        background-color: #111b21; /* لون داكن احترافي */
        border-right: 1px solid #00CCFF; /* خط أزرق خفيف في الجنب */
    }

    /* تعديل مساحة المحتوى */
    [data-testid="stAppViewBlockContainer"] {
        padding-top: 3rem !important;
        max-width: 900px !important;
        margin: auto;
    }

    /* شكل فقاعات الدردشة */
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712035.png", width=100) # أيقونة اختيارية
    st.title("الإعدادات")
    st.info("مرحباً بك في AGORAM AI. يمكنك مسح المحادثة أو تغيير الإعدادات من هنا.")
    if st.button("🗑️ مسح المحادثة"):
        st.session_state.messages = []
        st.rerun()

# --- واجهة التطبيق الرئيسية ---
st.markdown('<div class="main-title">AGORAM AI 🤖</div>', unsafe_allow_html=True)

# تهيئة سجل الرسائل إذا كان فارغاً
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# استقبال رسالة المستخدم
if prompt := st.chat_input("كيف يمكنني مساعدتك اليوم؟"):
    # إضافة رسالة المستخدم للسجل
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # محاكاة رد الذكاء الاصطناعي (أورام AI)
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        # هنا يمكنك ربط الكود بـ API الخاص بـ Gemini أو أي نموذج آخر
        assistant_response = f"أنا AGORAM AI، قمت باستلام رسالتك: '{prompt}'. كيف يمكنني تطوير خدمتي لك؟"
        
        for chunk in assistant_response.split():
            full_response += chunk + " "
            time.sleep(0.05)
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)
    
    # إضافة رد المساعد للسجل
    st.session_state.messages.append({"role": "assistant", "content": full_response})
