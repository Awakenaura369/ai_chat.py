import streamlit as st
from groq import Groq
from supabase import create_client, Client

# 1. الربط مع Supabase (تأكد أن السوارت محطوطين فـ Streamlit Secrets)
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# إعداد الصفحة
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="centered")

# --- الستايل المهيب (CSS) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .title-text {
        text-align: center;
        color: #00CCFF;
        font-size: 55px;
        font-weight: bold;
        text-shadow: 0px 0px 20px #00CCFF;
        margin-bottom: 5px;
    }
    .beta-text {
        text-align: center;
        color: #8892b0;
        font-size: 18px;
        font-style: italic;
        margin-bottom: 25px;
    }
    /* ستايل الميساجات */
    .stChatMessage { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- نظام تسجيل الدخول (Authentication) ---
if "user" not in st.session_state:
    st.markdown('<h1 class="title-text">AGORAM AI 🤖</h1>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["🔐 Login", "✨ Sign Up"])
    
    with tab1:
        email = st.text_input("Email", placeholder="yourname@example.com")
        password = st.text_input("Password", type="password")
        if st.button("Login"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except: st.error("Login failed. Check your email or password.")
            
    with tab2:
        new_email = st.text_input("New Email", placeholder="yourname@example.com")
        new_password = st.text_input("Create Password", type="password")
        if st.button("Create Account"):
            try:
                supabase.auth.sign_up({"email": new_email, "password": new_password})
                st.success("Account created! Check your email for confirmation link.")
            except: st.error("Signup failed. Try again.")
    st.stop()

# --- واجهة المستخدم بعد الدخول ---
user = st.session_state.user

with st.sidebar:
    st.title("📂 Workspace")
    st.write(f"Logged in: **{user.email}**")
    if st.button("🚪 Logout"):
        supabase.auth.sign_out()
        del st.session_state.user
        st.rerun()
    st.divider()
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

# التصميم المهيب للعنوان
st.markdown('<h1 class="title-text">AGORAM AI 🤖</h1>', unsafe_allow_html=True)
st.markdown('<p class="beta-text">🚀 Beta Version: Currently testing our AI models. More features coming soon!</p>', unsafe_allow_html=True)

# زر القهيوة الأصفر
st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 30px;">
        <a href="https://www.buymeacoffee.com/yourlink" target="_blank">
            <img src="https://img.buymeacoffee.com/button-api/?text=Buy me a Coffee&emoji=☕&slug=yourlink&button_colour=FFDD00&font_colour=000000&font_family=Cookie&outline_colour=000000&coffee_colour=ffffff" alt="Buy me a Coffee">
        </a>
    </div>
    """, unsafe_allow_html=True)

# --- جلب الذاكرة الشخصية من Supabase ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    try:
        # كنجيبو غير الميساجات ديال المستخدم اللي داخل دابا
        db_res = supabase.table("chat_history").select("*").eq("user_id", user.id).order("created_at").execute()
        for m in db_res.data:
            st.session_state.messages.append({"role": "user", "content": m["message"]})
            st.session_state.messages.append({"role": "assistant", "content": m["response"]})
    except: pass

# عرض المحادثة
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# إرسال ميساج جديد
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
        
        # حفظ فـ الداتابايز مع user_id
        try:
            supabase.table("chat_history").insert({
                "message": prompt, 
                "response": response, 
                "user_id": user.id
            }).execute()
        except: pass
        st.session_state.messages.append({"role": "assistant", "content": response})
