import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة والهوية العالمية
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="wide")

# 2. CSS المطور للواجهة والزر المركزي
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: white; }
    .main-title {
        font-size: 3.5rem; font-weight: bold; color: #00CCFF; 
        text-align: center; margin-top: -60px; margin-bottom: 5px;
        text-shadow: 0 0 20px rgba(0, 204, 255, 0.5);
    }
    .beta-text {
        text-align: center; color: #8892b0; font-size: 1.1rem; 
        margin-bottom: 15px; font-style: italic;
    }
    .support-container {
        display: flex; justify-content: center; margin-bottom: 35px;
    }
    .support-btn {
        background: #FFDD00; color: #000000 !important; 
        padding: 10px 25px; border-radius: 25px; text-align: center; 
        text-decoration: none; font-weight: bold; font-size: 1rem;
        box-shadow: 0 4px 15px rgba(255, 221, 0, 0.3);
        transition: transform 0.2s;
    }
    .support-btn:hover { transform: scale(1.05); }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# 3. السايدبار لاختيار الموديلات
with st.sidebar:
    st.markdown('<h2 style="color: #00CCFF;">AGORAM AI 🤖</h2>', unsafe_allow_html=True)
    st.write("---")
    model_option = st.selectbox(
        "Select AI Engine:",
        ("Llama 3.3 70B (Global Leader)", "Qwen 2.5 32B (Coding Pro)", "Llama 3.2 11B (Vision)"),
        index=0
    )
    st.write("---")
    st.caption("Status: Global Beta v1.2")

# 4. الواجهة الرئيسية
st.markdown('<div class="main-title">AGORAM AI 🤖</div>', unsafe_allow_html=True)
st.markdown('<div class="beta-text">🚀 <b>Beta Version:</b> Currently testing our AI models. More features coming soon!</div>', unsafe_allow_html=True)

# زر الدعم المركزي
st.markdown("""
    <div class="support-container">
        <a href="https://paypal.me/aipromptmoney" class="support-btn">☕ Buy me a Coffee</a>
    </div>
""", unsafe_allow_html=True)

# 5. منطق الشات مع إصلاح اللغة
model_mapping = {
    "Llama 3.3 70B (Global Leader)": "llama-3.3-70b-versatile",
    "Qwen 2.5 32B (Coding Pro)": "qwen-2.5-32b",
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
            # System Prompt المطور لضبط اللغة
            res = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are AGORAM AI, a professional global assistant. ALWAYS respond in the EXACT SAME language the user uses. If they speak Arabic, answer only in Arabic. Be concise and smart."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                model=selected_model,
            )
            ans = res.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e: st.error(f"Error: {e}")
