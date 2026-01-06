import streamlit as st
from groq import Groq

# 1. Page Configuration
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="wide")

# 2. Meta Tags for Custom Icon
st.markdown("""
    <head>
        <link rel="icon" href="https://cdn-icons-png.flaticon.com/512/4712/4712035.png">
        <link rel="apple-touch-icon" href="https://cdn-icons-png.flaticon.com/512/4712/4712035.png">
        <meta name="mobile-web-app-capable" content="yes">
    </head>
""", unsafe_allow_html=True)

# 3. Enhanced CSS for Centered Support Button
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
        margin-bottom: 15px; font-style: italic;
    }
    /* Centered Yellow Coffee Button */
    .support-container {
        display: flex; justify-content: center; margin-bottom: 35px;
    }
    .support-btn {
        background: #FFDD00; color: #000000 !important; 
        padding: 8px 20px; border-radius: 20px; text-align: center; 
        text-decoration: none; font-weight: bold; font-size: 0.9rem;
        box-shadow: 0 4px 10px rgba(255, 221, 0, 0.2);
    }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    [data-testid="stSidebarNav"] { display: block !important; }
    </style>
""", unsafe_allow_html=True)

# 4. Sidebar for Models
with st.sidebar:
    st.markdown('<h2 style="color: #00CCFF;">AGORAM AI 🤖</h2>', unsafe_allow_html=True)
    st.write("---")
    model_option = st.selectbox(
        "Select AI Brain:",
        ("Llama 3.3 70B (Versatile)", "Qwen 2.5 32B (Coder)", "Llama 3.2 11B (Vision)"),
        index=0
    )
    st.write("---")
    st.caption("v1.0 Beta - Optimized for Speed")

# 5. Main Page Layout (Title -> Beta Message -> Support Button)
st.markdown('<div class="main-title">AGORAM AI 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="beta-text">🚀 <b>Beta Version:</b> Currently testing our AI models. More features coming soon!</div>', unsafe_allow_html=True)

# Centered Support Button
st.markdown("""
    <div class="support-container">
        <a href="https://paypal.me/aipromptmoney" class="support-btn">☕ Buy me a Coffee</a>
    </div>
""", unsafe_allow_html=True)

# 6. Groq Chat Logic
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
