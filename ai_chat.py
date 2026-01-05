import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# 1. إعداد الصفحة (Matrix Pro Max)
st.set_page_config(page_title="Morpheus Web-AI", page_icon="🌐", layout="wide")

# ستايل الماتريكس
st.markdown("""
    <style>
    .main { background-color: #000000; color: #00FF41; font-family: 'Courier New', monospace; }
    .stChatMessage { background-color: #0a0a0a !important; border: 1px solid #00FF41; border-radius: 10px; }
    h1, p { color: #00FF41 !important; text-shadow: 0 0 5px #00FF41; }
    </style>
    """, unsafe_allow_html=True)

# 2. إعداد العقل (Groq)
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
except:
    st.error("Matrix Secrets Missing!")
    st.stop()

# دالة البحث في الويب
def web_search(query):
    try:
        results = DDGS().text(query, max_results=3)
        return "\n".join([f"Source: {r['href']} - {r['body']}" for r in results])
    except:
        return "Search failed."

st.title("👁️ MORPHEUS WEB-INTELLIGENCE")
st.caption("I am now connected to the real-time data streams of the Matrix.")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الشات
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message: st.image(message["image"])

# 3. معالجة الطلب
if prompt := st.chat_input("Ask anything, even about today's news..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        context = ""
        image_url = None
        
        # أ - واش السؤال كيحتاج بحث في الإنترنت؟
        search_keywords = ["أخبار", "اليوم", "نتائج", "سعر", "جديد", "news", "today", "search"]
        if any(word in prompt.lower() for word in search_keywords):
            with st.spinner("Searching the Web Matrix..."):
                context = web_search(prompt)
                st.info("🌐 Web Data Retrieved.")

        # ب - واش محتاج صورة؟
        if any(word in prompt.lower() for word in ["صورة", "تخيل", "draw", "imagine"]):
            with st.spinner("Generating Vision..."):
                clean_prompt = prompt.replace(" ", "%20")
                image_url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024&model=flux"
                st.image(image_url)

        # ج - الرد النهائي (Groq + الويب إيلا كاين)
        try:
            # دمج معلومات الويب مع السؤال
            final_prompt = f"Web Context: {context}\n\nUser Question: {prompt}" if context else prompt
            
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are Morpheus. Use the provided Web Context if available to give up-to-date answers. Keep your mysterious tone."},
                    {"role": "user", "content": final_prompt}
                ]
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            
            # حفظ
            msg_data = {"role": "assistant", "content": response}
            if image_url: msg_data["image"] = image_url
            st.session_state.messages.append(msg_data)
        except Exception as e:
            st.error(f"Matrix Glitch: {e}")
