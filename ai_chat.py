import streamlit as st
from groq import Groq
from supabase import create_client, Client
from functools import lru_cache
import bcrypt
import re
import pandas as pd

# --- Setup Supabase ---
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# --- Page config ---
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="centered")

# --- CSS Styling ---
st.markdown("""
<style>
.stApp { background-color: #0e1117; }
.main-title { text-align: center; color: #00CCFF; font-size:50px; font-weight:bold; text-shadow:0px 0px 20px #00CCFF; margin-bottom:5px; display:flex; justify-content:center; align-items:center; gap:15px;}
.beta-tag { text-align:center; color:#8892b0; font-size:18px; line-height:1.6; margin-bottom:30px; font-style:italic;}
.coffee-container { display:flex; justify-content:center; margin-bottom:40px;}
.btn-yellow { background-color:#FFDD00; color:black; padding:14px 30px; border-radius:35px; font-weight:bold; font-size:18px; display:flex; align-items:center; gap:10px; box-shadow:0px 6px 20px rgba(255,221,0,0.4); text-decoration:none !important;}
.stChatMessage { border-radius:15px; background-color:#1a1c23; border:1px solid #2d2e3a;}
</style>
""", unsafe_allow_html=True)

# --- Sidebar: Workspace + Auth + Admin ---
with st.sidebar:
    st.title("📂 Workspace")
    
    # --- Admin Dashboard Access ---
    admin_emails = ["admin@example.com"]  # set your admin emails
    is_admin = "user" in st.session_state and st.session_state.user.email in admin_emails

    if is_admin:
        st.subheader("📊 Dashboard Analytics")
        try:
            users_res = supabase.auth.admin.list_users()
            users_data = users_res.data
            user_count = len(users_data)
            st.metric("Total Users", user_count)

            chat_data = supabase.table("chat_history").select("*").execute()
            df = pd.DataFrame(chat_data.data)
            if not df.empty:
                chat_per_user = df.groupby("user_id")["message"].count().reset_index()
                st.subheader("Chats per User")
                st.dataframe(chat_per_user)

                st.subheader("Top 5 Most Active Users")
                top_users = chat_per_user.sort_values("message", ascending=False).head(5)
                st.bar_chart(top_users.set_index("user_id")["message"])

                st.subheader("Average Message Length")
                df["msg_len"] = df["message"].apply(lambda x: len(str(x)))
                st.metric("Avg. User Msg Length", round(df["msg_len"].mean(),1))
        except Exception as e:
            st.error(f"Dashboard Error: {str(e)}")
    
    if "user" not in st.session_state:
        st.info("💡 Login to save your chat history.")
        with st.expander("🔐 Account Access", expanded=True):
            mode = st.radio("Choose:", ["Login", "Sign Up"])
            email = st.text_input("Email", placeholder="example@mail.com")
            password = st.text_input("Password", type="password")

            def validate_email(email):
                return re.match(r"[^@]+@[^@]+\.[^@]+", email)

            def validate_password(pw):
                return len(pw) >= 6

            if st.button("Confirm Action"):
                if not validate_email(email):
                    st.error("Invalid email format.")
                elif not validate_password(password):
                    st.error("Password must be at least 6 characters.")
                else:
                    try:
                        if mode == "Sign Up":
                            hashed_pw = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
                            res = supabase.auth.sign_up({"email": email, "password": password})
                            if res.user:
                                st.session_state.user = res.user
                                st.success("Account created!")
                                st.rerun()
                        elif mode == "Login":
                            res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                            if res.user:
                                st.session_state.user = res.user
                                st.rerun()
                    except Exception as e:
                        st.error(f"Auth Error: {str(e)}")
    else:
        st.write(f"Logged in: **{st.session_state.user.email}**")
        if st.button("🚪 Logout"):
            try:
                supabase.auth.sign_out()
            except: pass
            st.session_state.pop("user", None)
            st.session_state.pop("messages", None)
            st.rerun()
    
    st.divider()
    if st.button("➕ New Chat"):
        st.session_state.messages = []
        st.rerun()

# --- Main UI ---
st.markdown('<div class="main-title">AGORAM AI <span style="font-size:45px;">🤖</span></div>', unsafe_allow_html=True)
st.markdown('<p class="beta-tag">🚀 Beta Version: Currently testing our AI models. More features coming soon!</p>', unsafe_allow_html=True)
st.markdown("""
<div class="coffee-container">
<a href="https://www.paypal.me/siddear" target="_blank" style="text-decoration:none;">
<div class="btn-yellow"><span style="font-size:20px;">☕</span> Buy me a Coffee</div>
</a>
</div>
""", unsafe_allow_html=True)

# --- Initialize messages ---
if "messages" not in st.session_state:
    st.session_state.messages = []
    if "user" in st.session_state:
        try:
            res = supabase.table("chat_history").select("*").eq("user_id", st.session_state.user.id).order("created_at").execute()
            for m in res.data:
                st.session_state.messages.append({"role": "user", "content": m["message"]})
                st.session_state.messages.append({"role": "assistant", "content": m["response"]})
        except: pass

# --- Display previous messages ---
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Advanced Groq Chat ---
@lru_cache(maxsize=512)
def get_groq_response(messages_tuple):
    all_msgs = " ".join(messages_tuple)
    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        system_instruction = """
        You are AGORAM AI, adaptive and Moroccan at heart.
        1. LANGUAGE: match the user's language/dialect.
        2. INTELLECT: adapt response complexity to user level.
        3. CONTEXT: maintain entire conversation context.
        4. ATTITUDE: helpful, friendly, professional.
        """
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":"system","content":system_instruction}] + 
                     [{"role": "user", "content": msg} for msg in messages_tuple]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

# --- Chat input ---
if prompt := st.chat_input("Ask AGORAM anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        user_msgs = tuple([m["content"] for m in st.session_state.messages if m["role"]=="user"])
        ans = get_groq_response(user_msgs)
        st.markdown(ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
        
        if "user" in st.session_state:
            try:
                supabase.table("chat_history").insert({
                    "message": prompt,
                    "response": ans,
                    "user_id": st.session_state.user.id
                }).execute()
            except: pass
