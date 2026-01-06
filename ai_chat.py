import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="wide")

# 2. CSS Styling for Blue Title and Mobile UI
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    
    /* Blue Title Effect */
    .main-title {
        font-size: 3rem;
        font-weight: bold;
        color: #00CCFF; 
        text-align: center;
        margin-top: -60px;
        margin-bottom: 10px;
        text-shadow: 0 0 15px rgba(0, 204, 255, 0.4);
    }

    /* Force Sidebar Arrow on Mobile */
    [data-testid="stSidebarNav"] { display: block !important; }
    
    /* Styling the Model Selector */
    .stSelectbox div[data-baseweb="select"] {
        background-color: #161b22 !important;
        border: 1px solid #00CCFF !important;
        border-radius: 10px;
    }

    /* Full Width Container */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        padding: 1.5rem !important;
    }
    
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. Main Title
st.markdown('<div class="main-title">AGORAM AI 🤖</div>', unsafe_allow_html=True)

# 4. Model Selection (Main Page for Visibility)
model_option = st.selectbox(
    "Choose AI Model:",
    ("Llama 3.3 70B (Versatile)", "Qwen 2.5 32B (Coder)", "Llama 3.2 11B (Vision)", "Whisper Large v3 (Audio)"),
    index=0
)

# Mapping models to Groq IDs
model_mapping = {
    "Llama 3.3 70B (Versatile)": "llama-3.3-70b-versatile",
    "Qwen 2.5 32B (Coder)": "qwen-2.5-32b",
    "Llama 3.2 11B (Vision)": "llama-3.2-11b-vision-preview",
    "Whisper Large v3 (Audio)": "whisper-large-v3"
}
selected_model = model_mapping[model_option]

# 5. Sidebar for Support
with st.sidebar:
    st.header("Settings")
    st.write(f"Active Model: {selected_model}")
    st.divider()
    st.markdown('<a href="https://paypal.me/aipromptmoney" style="display:block; background:#0070ba; color:white; padding:12px; border-radius:10px; text-align:center; text-decoration:none; font-weight:bold;">☕ Support AGORAM Project</a>', unsafe_allow_html=True)

# 6. Groq Chat Logic
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input in English
if prompt := st.chat_input("Ask AGORAM anything..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            res = client.chat.completions.create(
                messages=[{"role": "system", "content": "You are AGORAM AI. Answer in the same language the user speaks. Be concise."},
                          *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]],
                model=selected_model,
            )
            ans = res.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Error: {e}")
