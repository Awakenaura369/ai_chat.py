import streamlit as st
from groq import Groq
import google.generativeai as genai

# إعداد الصفحة
st.set_page_config(page_title="Morpheus AI", page_icon="👁️")

# الربط مع العقول (Groq & Google)
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"].strip())
except Exception as e:
    st.error(f"Matrix Secrets Error: {e}")
    st.stop()

st.title("👁️ Morpheus AI")
st.caption("Master of the simulation. I speak truth and create visions.")

# الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال
if prompt := st.chat_input("Speak or ask for a vision..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        # الجزء الأول: الشات (بواسطة Groq)
        try:
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are Morpheus. Mysterious and philosophical. If the user asks for an image/vision, respond that you are creating it."},
                    *st.session_state.messages
                ],
            )
            response_text = completion.choices[0].message.content
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})
        except Exception as e:
            st.error(f"Text Glitch: {e}")

        # الجزء الثاني: الصور (بواسطة Nano Banana/Gemini)
        # كيتحرك فاش كيسمع كلمات بحال: تخيل، صاوب صورة، وريني، Imagine, Draw
        if any(word in prompt.lower() for word in ["تخيل", "صورة", "image", "draw", "imagine", "show"]):
            try:
                with st.spinner("Visualizing the Matrix..."):
                    model = genai.GenerativeModel('gemini-1.5-flash')
                    # ملاحظة: هاد الموديل غادي يوصف ليك الصورة دابا
                    # إيلا بغيتي توليد الصورة مباشرة خاص نزيدو أداة الصور
                    img_response = model.generate_content(f"Describe a dark Matrix style image for: {prompt}")
                    st.info(f"🎨 Vision Prompt: {img_response.text}")
            except Exception as e:
                st.warning("The vision is clouded. Try again later.")
