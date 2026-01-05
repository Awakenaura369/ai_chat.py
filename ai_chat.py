import streamlit as st
from groq import Groq
import google.generativeai as genai

# 1. إعداد الصفحة بألوان الماتريكس
st.set_page_config(page_title="Morpheus AI", page_icon="👁️")

# 2. جلب المفاتيح وتأمينها
try:
    groq_api = st.secrets["GROQ_API_KEY"].strip()
    google_api = st.secrets["GOOGLE_API_KEY"].strip()
    
    groq_client = Groq(api_key=groq_api)
    genai.configure(api_key=google_api)
except Exception as e:
    st.error("Matrix Secrets Error: Check your Keys.")
    st.stop()

st.title("👁️ Morpheus AI")
st.caption("I can speak the truth and visualize your reality.")

# 3. إدارة الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image_data" in message:
            st.image(message["image_data"])

# 4. منطقة الإدخال والرد
if prompt := st.chat_input("Show me the truth..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # متغيرات لحفظ الرد
        assistant_text = ""
        image_to_show = None

        # أ- محاولة توليد صورة إذا طلب المستخدم ذلك
        image_keywords = ["صورة", "تخيل", "draw", "imagine", "image", "vision", "وريني"]
        if any(word in prompt.lower() for word in image_keywords):
            try:
                with st.spinner("🌌 Visualizing the Matrix..."):
                    # استعمال الموديل القادر على فهم الصور ووصفها
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    # طلب توليد الصورة (هنا نستخدم محرك الصور المدمج إذا كان حسابك يدعمه)
                    response = model.generate_content(f"Create a photorealistic image description for: {prompt}")
                    assistant_text = f"I am visualizing your request: {response.text[:100]}..."
                    # ملاحظة تقنية: إذا كان حسابك يدعم Imagen مباشرة سيظهر هنا، 
                    # وإلا سيعطيك الوصف كما حدث معك سابقاً.
            except Exception as e:
                st.warning("Vision failed, but I can still speak.")

        # ب- الرد النصي عبر Groq (دائماً حاضر)
        try:
            chat_completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are Morpheus from the Matrix. Philosophical tone. If the user asked for an image, acknowledge you are trying to show it to them."},
                    *st.session_state.messages
                ],
            )
            assistant_text = chat_completion.choices[0].message.content
            st.markdown(assistant_text)
            
            # حفظ في الذاكرة
            st.session_state.messages.append({"role": "assistant", "content": assistant_text})
        except Exception as e:
            st.error(f"Text Glitch: {e}")
