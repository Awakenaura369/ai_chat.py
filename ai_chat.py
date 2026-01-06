import streamlit as st
from groq import Groq

# إعدادات الصفحة - Wide Layout باش يظهر السايدبار فالموبيل
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="wide")

# ستايل CSS احترافي لضبط القياسات واتجاه النص
st.markdown("""
    <style>
    /* خلفية داكنة وتنسيق النصوص */
    .stApp { background-color: #0E1117; color: white; }
    
    /* فرض ظهور السهم ديال السايدبار فالموبيل */
    [data-testid="stSidebarNav"] { display: block !important; }
    
    /* توسيع الحاوية باش تعمر الشاشة وتحيد الرقة */
    [data-testid="stAppViewBlockContainer"] {
        max-width: 100% !important;
        width: 100% !important;
        padding: 1rem !important;
    }

    /* تحسين شكل الرسائل */
    .stChatMessage { border-radius: 12px; margin: 8px 0; border: 1px solid #2d2d2d; }
    .stChatMessage[data-testid="stChatMessageAssistant"] { border-left: 4px solid #ff4b4b; background-color: #161b22; }

    /* ستايل زر بايبال */
    .support-btn {
        display: block; width: 100%; text-align: center; background-color: #0070ba; 
        color: white !important; padding: 12px; border-radius: 10px; 
        text-decoration: none; font-weight: bold; margin: 10px 0;
    }
    
    /* إخفاء الزوائد لزيادة الاحترافية */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# القائمة الجانبية (Settings & Support)
with st.sidebar:
    st.title("AGORAM AI 🤖")
    st.header("⚙️ Settings")
    
    # اختيار الموديل من القائمة
    model_option = st.selectbox(
        "Choose AI Intelligence:",
        ("Llama 3.3 70B (Fast & Smart)", "Qwen 2.5 32B (Coding)", "Llama 3.2 Vision")
    )
    
    model_mapping = {
        "Llama 3.3 70B (Fast & Smart)": "llama-3.3-70b-versatile",
        "Qwen 2.5 32B (Coding)": "qwen-2.5-32b",
        "Llama 3.2 Vision": "llama-3.2-11b-vision-preview"
    }
    selected_model = model_mapping[model_option]
    
    st.divider()
    st.markdown("### Support the Project")
    st.markdown('<a href="https://paypal.me/aipromptmoney" target="_blank" class="support-btn">☕ Support via PayPal</a>', unsafe_allow_html=True)
    st.caption("دعمك كيخلينا نستمروا فالتطوير.")

# إدارة المحادثة
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("سول أݣورام..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # عقلية ذكية مرنة لغوياً
            system_instruction = "You are AGORAM AI. Answer in the user's language. Be smart and concise."
            
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_instruction},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                model=selected_model,
            )
            
            ans = chat_completion.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Error: {e}")
