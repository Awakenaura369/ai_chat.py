import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# 1. إعداد الصفحة وستايل الماتريكس
st.set_page_config(page_title="Morpheus AI Ultra", page_icon="👁️", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stChatMessage { background-color: #0a0a0a !important; border: 1px solid #00FF41; border-radius: 10px; margin-bottom: 10px; }
    h1, h2, h3, p, span { color: #00FF41 !important; text-shadow: 0 0 8px #00FF41; }
    .stTextInput>div>div>input { background-color: #0d0d0d; color: #00FF41; border: 1px solid #00FF41; }
    </style>
    """, unsafe_allow_html=True)

# 2. إعداد الاتصال بـ Groq
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
except:
    st.error("Matrix Secrets Missing! Check your API Keys.")
    st.stop()

# دالة البحث في الويب
def web_search(query):
    try:
        results = DDGS().text(query, max_results=3)
        return "\n".join([f"Source: {r['href']} - {r['body']}" for r in results])
    except:
        return ""

st.title("👁️ MORPHEUS AI ULTRA")
st.caption("Dynamic Intelligence System: Professional Tech Expert + Philosophical Guide.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message: st.image(message["image"])

# 3. منطق الاستجابة الذكي
if prompt := st.chat_input("Ask a tech question or seek the truth..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # تحليل نوع السؤال (Dynamic Analysis)
    tech_keywords = ["كيفاش", "برمجة", "كود", "ثمن", "تقنية", "سعر", "شحال", "how", "code", "price", "tech", "fix", "news", "أخبار"]
    is_tech_or_fact = any(word in prompt.lower() for word in tech_keywords)

    with st.chat_message("assistant"):
        context = ""
        image_url = None
        
        # أ - البحث في الويب إذا كان السؤال تقني أو إخباري
        if is_tech_or_fact:
            with st.spinner("Accessing Matrix Data Streams..."):
                context = web_search(prompt)
        
        # ب - توليد صورة إذا طلب المستخدم
        if any(word in prompt.lower() for word in ["صورة", "تخيل", "draw", "imagine", "vision"]):
            with st.spinner("Rendering Vision..."):
                clean_prompt = prompt.replace(" ", "%20")
                image_url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024&model=flux"
                st.image(image_url)

        # ج - تحديد الشخصية بناءً على التحليل
        if is_tech_or_fact:
            # نمط الخبير التقني المباشر
            system_instruction = "You are a professional tech expert. Be direct, concise, and provide accurate facts or code. Use Moroccan Darija if the user does. Avoid any mysterious or philosophical talk."
            current_temp = 0.2 # دقة عالية
        else:
            # نمط مورفيوس الفلسفي
            system_instruction = "You are Morpheus from the Matrix. Speak in a deep, mysterious, and philosophical tone. Use metaphors about reality, awakening, and the Matrix."
            current_temp = 0.8 # إبداع عالي

        try:
            # دمج سياق الويب إذا وجد
            user_input = f"Web Context: {context}\n\nUser Question: {prompt}" if context else prompt
            
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_instruction},
                    *st.session_state.messages[:-1], # الذاكرة
                    {"role": "user", "content": user_input}
                ],
                temperature=current_temp
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            
            # حفظ في الذاكرة
            msg_save = {"role": "assistant", "content": response}
            if image_url: msg_save["image"] = image_url
            st.session_state.messages.append(msg_save)
            
        except Exception as e:
            st.error(f"Matrix Glitch: {str(e)}")
