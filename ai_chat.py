import streamlit as st
from groq import Groq
from supabase import create_client, Client

# 1. الربط مع Supabase
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="centered")

# --- الستايل المهيب (نفس اللي فـ الصورة) ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; }
    .main-title {
        text-align: center;
        color: #00CCFF;
        font-size: 50px;
        font-weight: bold;
        text-shadow: 0px 0px 20px #00CCFF;
        margin-bottom: 0px;
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 15px;
    }
    .beta-tag {
        text-align: center;
        color: #8892b0;
        font-size: 18px;
        font-style: italic;
        margin-top: 10px;
        margin-bottom: 30px;
    }
    .coffee-btn {
        display: flex;
        justify-content: center;
        margin-bottom: 40px;
    }
    /* ستايل الميساجات */
    .stChatMessage { border-radius: 15px; background-color: #1a1c23; }
    </style>
    """, unsafe_allow_html=True)

# --- القائمة الجانبية (Sidebar) ---
with st.sidebar:
    st.title("📂 Workspace")
    if "user" not in st.session_state:
        st.info("Login to save history.")
        with st.expander("🔐 Login / Sign Up"):
            mode = st.radio("Choose:", ["Login", "Sign Up"])
            email = st.text_input("Email")
            password = st.text_input("Password", type="password")
            if st.button("Go"):
                try:
                    if mode == "Login":
                        res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                        st.session_state.user = res.user
                    else:
                        supabase.auth.sign_up({"email": email, "password": password})
                        st.success("Check your email!")
                    st.rerun()
                except: st.error("Error! Check info.")
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

# --- الواجهة الرئيسية (نفس الصورة بالضبط) ---

# العنوان مع اللوجو الصغير
st.markdown('<div class="main-title">AGORAM AI <span style="font-size: 40px;">🤖</span></div>', unsafe_allow_html=True)

# نص البيتا
st.markdown('<p class="beta-tag">🚀 Beta Version: Currently testing our AI models. More features coming soon!</p>', unsafe_allow_html=True)

# زر القهيوة الأصفر
st.markdown("""
    <div class="coffee-btn">
        <a href="https://www.buymeacoffee.com/yourlink" target="_blank" style="text-decoration: none;">
            <div style="background-color: #FFDD00; color: black; padding: 12px 25px; border-radius: 30px; font-weight: bold; display: flex; align-items: center; gap: 10px; box-shadow: 0px 4px 15px rgba(255, 221, 0, 0.3);">
                ☕ Buy me a Coffee
            </div>
        </a>
    </div>
    """, unsafe_allow_html=True)

# --- نظام المحادثة ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    if "user" in st.session_state:
        try:
            res = supabase.table("chat_history").select("*").eq("user_id", st.session_state.user.id).execute()
            for m in res.data:
                st.session_state.messages.append({"role": "user", "content": m["message"]})
                st.session_state.messages.append({"role": "assistant", "content": m["response"]})
        except: pass

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if prompt := st.chat_input("Ask AGORAM anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)

    with st.chat_message("assistant"):
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role": "system", "content": "You are AGORAM AI."}] + 
                     [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
        )
        ans = res.choices[0].message.content
        st.markdown(ans)
        
        if "user" in st.session_state:
            try:
                supabase.table("chat_history").insert({"message": prompt, "response": ans, "user_id": st.session_state.user.id}).execute()
            except: pass
        st.session_state.messages.append({"role": "assistant", "content": ans})
