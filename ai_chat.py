import streamlit as st
from groq import Groq
from supabase import create_client, Client

# 1. إعدادات Supabase و Groq
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# إعداد الصفحة لتكون مهيبة
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="centered")

# --- وظائف قاعدة البيانات ---
def load_history():
    try:
        res = supabase.table("chat_history").select("*").order("created_at").execute()
        return res.data
    except: return []

def save_to_db(u_msg, a_res):
    try:
        supabase.table("chat_history").insert({"message": u_msg, "response": a_res}).execute()
    except: pass

# --- واجهة المستخدم المهيبة (التصميم الأصلي) ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stChatMessage { border-radius: 15px; margin-bottom: 10px; }
    .title-text {
        text-align: center;
        color: #00CCFF;
        font-size: 50px;
        font-weight: bold;
        text-shadow: 2px 2px 10px #00CCFF;
        margin-bottom: 5px;
    }
    .sub-text {
        text-align: center;
        color: #888;
        font-size: 18px;
        margin-bottom: 30px;
    }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<h1 class="title-text">AGORAM AI 🤖</h1>', unsafe_allow_html=True)
st.markdown('<p class="sub-text">The Most Powerful AI in Your Hands</p>', unsafe_allow_html=True)

# زر "قهيوة" (Buy Me a Coffee)
st.markdown("""
    <div style="text-align: center; margin-bottom: 20px;">
        <a href="https://www.buymeacoffee.com/yourlink" target="_blank">
            <img src="https://cdn.buymeacoffee.com/buttons/v2/default-yellow.png" alt="Buy Me A Coffee" style="height: 40px !important;width: 145px !important;" >
        </a>
    </div>
    """, unsafe_allow_html=True)

# --- منطق المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    # تحميل الهضرة من الداتابايز عند أول دخول
    db_history = load_history()
    for item in db_history:
        st.session_state.messages.append({"role": "user", "content": item["message"]})
        st.session_state.messages.append({"role": "assistant", "content": item["response"]})

# عرض المحادثات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال ميساج جديد
if prompt := st.chat_input("Ask AGORAM anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        completion = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are AGORAM AI. Answer concisely."}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        response = completion.choices[0].message.content
        st.markdown(response)
        
        # حفظ فـ Supabase
        save_to_db(prompt, response)
        st.session_state.messages.append({"role": "assistant", "content": response})
