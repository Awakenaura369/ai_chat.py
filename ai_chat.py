import streamlit as st
from groq import Groq
from supabase import create_client, Client

# 1. الربط مع Supabase
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="centered")

# --- الستايل المهيب (CSS) لإعادة تصميم الواجهة ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    
    /* العنوان بستايل النيون واللوغو */
    .main-title {
        text-align: center;
        color: #00CCFF;
        font-size: 50px;
        font-weight: bold;
        text-shadow: 0px 0px 20px #00CCFF;
        margin-bottom: 5px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
    }
    
    /* نص البيتا */
    .beta-tag {
        text-align: center;
        color: #8892b0;
        font-size: 18px;
        line-height: 1.6;
        margin-bottom: 30px;
    }
    
    /* ستايل الميساجات */
    .stChatMessage { border-radius: 15px; background-color: #1a1c23; border: 1px solid #2d2e3a; }
    
    /* إخفاء سهم السايدبار الافتراضي لتعويضه بوضوح */
    section[data-testid="stSidebar"] { background-color: #11141b; }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.title("📂 Workspace")
    if "user" not in st.session_state:
        st.info("Login to save your chat history.")
        with st.expander("🔐 Login / Sign Up"):
            mode = st.radio("Choose:", ["Login", "Sign Up"])
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Confirm"):
                try:
                    if mode == "Login":
                        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = res.user
                    else:
                        supabase.auth.sign_up({"email": email, "password": password})
                        st.success("Check your email to confirm!")
                    st.rerun()
                except: st.error("Authentication failed.")
    else:
        st.write(f"Logged in: **{st.session_state.user.email}**")
        if st.button("🚪 Logout"):
            supabase.auth.sign_out()
            del st.session_state.user
            st.session_state.messages = []
            st.rerun()
    
    st.divider()
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

# --- الواجهة الرئيسية (بحال الصورة بالضبط) ---

# 1. العنوان واللوغو
st.markdown('<div class="main-title">AGORAM AI <span style="font-size: 45px;">🤖</span></div>', unsafe_allow_html=True)

# 2. نص البيتا
st.markdown('<p class="beta-tag">🚀 <i>Beta Version: Currently testing our AI models. More features coming soon!</i></p>', unsafe_allow_html=True)

# 3. زر القهيوة المربوط بـ PayPal (siddear)
st.markdown("""
    <div style="display: flex; justify-content: center; margin-bottom: 40px;">
        <a href="https://www.paypal.me/siddear" target="_blank" style="text-decoration: none;">
            <div style="background-color: #FFDD00; color: black; padding: 14px 30px; border-radius: 35px; font-weight: bold; font-size: 18px; display: flex; align-items: center; gap: 10px; box-shadow: 0px 6px 20px rgba(255, 221, 0, 0.4); transition: 0.3s;">
                <span style="font-size: 20px;">☕</span> Buy me a Coffee
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# --- نظام المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    if "user" in st.session_state:
        try:
            res = supabase.table("chat_history").select("*").eq("user_id", st.session_state.user.id).order("created_at").execute()
            for m in res.data:
                st.session_state.messages.append({"role": "user", "content": m["message"]})
                st.session_state.messages.append({"role": "assistant", "content": m["response"]})
        except: pass

# عرض الميساجات
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# شريط الإدخال
if prompt := st.chat_input("Ask AGORAM anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are AGORAM AI, a helpful assistant."}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        ans = res.choices[0].message.content
        st.markdown(ans)
        
        # حفظ فالداتابايز إيلا كان المستخدم مسجل
        if "user" in st.session_state:
            try:
                supabase.table("chat_history").insert({
                    "message": prompt, 
                    "response": ans, 
                    "user_id": st.session_state.user.id
                }).execute()
            except: pass
        st.session_state.messages.append({"role": "assistant", "content": ans})
