import streamlit as st
from groq import Groq

# 1. Page Configuration - Sidebar starts expanded on desktop
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="wide", initial_sidebar_state="expanded")

# 2. Add Meta Tags for Custom Icon & PWA
st.markdown("""
    <head>
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/4712/4712035.png">
        <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/4712/4712035.png">
        <meta name="mobile-web-app-capable" content="yes">
        <meta name="apple-mobile-web-app-status-bar-style" content="black-translucent">
    </head>
""", unsafe_allow_html=True)

# 3. CSS Styling - Keeping the Sky Blue Title
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .main-title {
        font-size: 3rem; font-weight: bold; color: #00CCFF; 
        text-align: center; margin-top: -60px; margin-bottom: 30px;
        text-shadow: 0 0 15px rgba(0, 204, 255, 0.4);
    }
    
    /* Make sure sidebar arrow is visible on mobile */
    [data-testid="stSidebarNav"] { display: block !important; }

    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important; padding: 1.5rem !important;
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 4. Sidebar: Model Selection moved here
with st.sidebar:
    st.markdown('<h1 style="color: #00CCFF;">AGORAM AI 🤖</h1>', unsafe_allow_html=True)
    st.header("Settings")
    
    # Model Selection inside Sidebar
    model_option = st.selectbox(
        "Choose AI Brain:",
        ("Llama 3.3 70B (Versatile)", "Qwen 2.5 32B (Coder)", "Llama 3.2 11B (Vision)", "Whisper Large v3 (Audio)"),
        index=0
    )
    
    model_mapping = {
        "Llama 3.3 70B (Versatile)": "llama-3.3-70b-versatile",
        "Qwen 2.5 32B (Coder)": "qwen-2.5-32b",
        "Llama 3.2 11B (Vision)": "llama-3.2-11b-vision-preview",
        "Whisper Large v3 (Audio)": "whisper-large-v3"
    }
    selected_model = model_mapping[model_option]
    
    st.divider()
    st.markdown('<a href="https://paypal.me/aipromptmoney" style="display:block; background:#0070ba; color:white; padding:12px; border-radius:10px; text-align:center; text-decoration:none; font-weight:bold;">☕ Support Project</a>', unsafe_allow_html=True)

# 5. Main Title on Page
st.markdown('<div class="main-title">AGORAM AI 🤖</div>', unsafe_allow_html=True)

# 6. Groq Chat Logic
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
