import streamlit as st
from groq import Groq

# 1. إعدادات الصفحة - Mobile First
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="centered")

# 2. ستايل CSS احترافي لضبط القياسات واتجاه النص
st.markdown("""
    <style>
    /* خلفية داكنة وتنسيق النصوص */
    .stApp { background-color: #0E1117; color: white; }
    
    /* ضبط اتجاه النص تلقائياً (يمين للعربية، يسار للإنجليزية) */
    .stMarkdown div p {
        unicode-bidi: plaintext;
        text-align: start;
        direction: auto;
    }

    /* تحسين حاويات الشات للموبيل */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 5rem !important; /* مساحة للـ input */
        max-width: 100% !important;
    }
    
    .stChatMessage { 
        border-radius: 15px; 
        margin: 8px 2%; 
        border: 1px solid #2d2d2d;
        padding: 10px;
    }
    
    .stChatMessage[data-testid="stChatMessageAssistant"] { 
        border-left: 4px solid #ff4b4b; 
        background-color: #161b22; 
    }

    /* ستايل الأزرار في القائمة الجانبية */
    .support-btn {
        display: block; width: 100%; text-align: center; background-color: #0070ba; 
        color: white !important; padding: 10px; border-radius: 10px; 
        text-decoration: none; font-weight: bold; margin: 10px 0; font-size: 0.9rem;
    }
    
    /* إخفاء شريط Streamlit الفوقاني لزيادة الاحترافية */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

st.title("AGORAM AI 🤖")

# 3. القائمة الجانبية (الاختيارات والدعم)
with st.sidebar:
    st.header("⚙️ Settings")
    
    # اختيار الموديل (Llama 3.3 هو الأفضل حالياً)
    model_option = st.selectbox(
        "AI Intelligence:",
        ("Llama 3.3 70B (Fast & Smart)", "Qwen 2.5 32B (Coding Expert)", "Llama 3.2 Vision (Images)")
    )
    
    model_mapping = {
        "Llama 3.3 70B (Fast & Smart)": "llama-3.3-70b-versatile",
        "Qwen 2.5 32B (Coding Expert)": "qwen-2.5-32b",
        "Llama 3.2 Vision (Images)": "llama-3.2-11b-vision-preview"
    }
    selected_model = model_mapping[model_option]
    
    st.divider()
    st.markdown("### Support the Project")
    st.markdown('<a href="https://paypal.me/aipromptmoney" target="_blank" class="support-btn">☕ Buy me a Coffee</a>', unsafe_allow_html=True)
    st.caption("دعمك كيخلينا نزيدو نطوروا أݣورام.")

# 4. إدارة المحادثة
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("سول أݣورام أو ابحث..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # تعليمات العقلية المرنة والبحث في الويب
            system_instruction = """
            You are AGORAM AI. Respond in the user's language ONLY. 
            If they ask for news or facts, provide real-time information. 
            Keep it professional, concise, and helpful.
            """
            
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

# زر الدعم فـ الأسفل للموبيل
st.markdown('<a href="https://paypal.me/aipromptmoney" target="_blank" class="support-btn">☕ Support via PayPal</a>', unsafe_allow_html=True)
