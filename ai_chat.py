import streamlit as st
from groq import Groq
from supabase import create_client, Client

# 1. جلب السوارت من Streamlit Secrets
url: str = st.secrets["SUPABASE_URL"]
key: str = st.secrets["SUPABASE_KEY"]
supabase: Client = create_client(url, key)

# إعداد الصفحة
st.set_page_config(page_title="AGORAM AI 🤖", layout="wide")

# 2. وظيفة لجلب التاريخ من الداتابايز
def load_chat_history():
    try:
        # كنجيبو كاع الميساجات مرتبين من القديم للجديد
        response = supabase.table("chat_history").select("*").order("created_at").execute()
        return response.data
    except Exception as e:
        st.error(f"Error loading history: {e}")
        return []

# 3. وظيفة لحفظ الميساج الجديد فـ Supabase
def save_message(user_msg, ai_res):
    try:
        supabase.table("chat_history").insert({
            "message": user_msg, 
            "response": ai_res
        }).execute()
    except Exception as e:
        st.warning(f"Note: Database not saved: {e}")

# واجهة التطبيق
st.markdown('<h1 style="text-align: center; color: #00CCFF;">AGORAM AI 🤖</h1>', unsafe_allow_html=True)
st.markdown('<p style="text-align: center;">الذكاء الاصطناعي بذاكرة قوية</p>', unsafe_allow_html=True)

# 4. تحميل التاريخ فـ البداية
if "messages" not in st.session_state:
    st.session_state.messages = []
    db_messages = load_chat_history()
    if db_messages:
        for m in db_messages:
            st.session_state.messages.append({"role": "user", "content": m["message"]})
            st.session_state.messages.append({"role": "assistant", "content": m["response"]})

# عرض المحادثات السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# إدخال ميساج جديد
if prompt := st.chat_input("Ask AGORAM anything..."):
    # عرض ميساج المستخدم
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # طلب الرد من Groq
    with st.chat_message("assistant"):
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        res = client.chat.completions.create(
            messages=[
                {"role": "system", "content": "You are AGORAM AI. Always respond in the same language as the user."},
                *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
            ],
            model="llama-3.3-70b-versatile",
        )
        ans = res.choices[0].message.content
        st.markdown(ans)
        
        # 5. الحفظ فـ الداتابايز باش المرة الجاية تلقاها
        save_message(prompt, ans)
        st.session_state.messages.append({"role": "assistant", "content": ans})
