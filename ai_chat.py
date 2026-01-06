import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة والأيقونة
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="wide")

# 2. Meta Tags للأيقونة والـ PWA
st.markdown("""
    <head>
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/4712/4712035.png">
        <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/4712/4712035.png">
        <meta name="mobile-web-app-capable" content="yes">
    </head>
""", unsafe_allow_html=True)

# 3. CSS المطور للعنوان وزر الدعم
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .main-title {
        font-size: 3rem; font-weight: bold; color: #00CCFF; 
        text-align: center; margin-top: -60px; margin-bottom: 5px;
        text-shadow: 0 0 15px rgba(0, 204, 255, 0.4);
    }
    .beta-text {
        text-align: center; color: #8892b0; font-size: 1rem; 
        margin-bottom: 30px; font-style: italic;
    }
    .support-btn {
        display: block; background: #FFDD00; color: #000000 !important; 
        padding: 10px; border-radius: 10px; text-align: center; 
        text-decoration: none; font-weight: bold; margin-top: 20px;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNav"] { display: block !important; }
    </style>
""", unsafe_allow_html=True)

# 4. القائمة الجانبية (Sidebar)
with st.sidebar:
    st.markdown('<h2 style="color: #00CCFF;">AGORAM AI 🤖</h2>', unsafe_allow_html=True)
    st.write("---")
    # اختيار الموديل
    model_option = st.selectbox(
        "Select AI Brain:",
        ("Llama 3.3 70B (Versatile)", "Qwen 2.5 32B (Coder)", "Llama 3.2 11B (Vision)"),
        index=0
    )
    
    st.write("---")
    st.write("☕ **Support the Creator**")
    st.markdown('<a href="https://paypal.me/aipromptmoney" class="support-btn">Buy me a Coffee ☕</a>', unsafe_allow_html=True)
    st.caption("Help us keep AGORAM AI free and fast!")

# 5. الواجهة الرئيسية
st.markdown('<div class="main-title">AGORAM AI 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="beta-text">🚀 <b>Beta Version:</b> Currently testing our AI models. More features coming soon!</div>', unsafe_allow_html=True)

# 6. إعدادات Groq والشات
model_mapping = {
    "Llama 3.3 70B (Versatile)": "llama-3.3-70b-versatile",
    "Qwen 2.5 32B (Coder)": "qwen-2.5-32b",
    "Llama 3.2 11B (Vision)": "llama-3.2-11b-vision-preview"
}
selected_model = model_mapping[model_option]

client = Groq(api_key=st.secrets["GROQ_API_KEY"])
if "messages" not in st.session_state: st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]): st.markdown(message["content"])

if prompt := st.chat_input("Ask AGORAM anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        try:
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are AGORAM AI. Answer concisely."},
                          *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]],
                model=selected_model,
            )
            ans = res.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e: st.error(f"Error: {e}")
