import streamlit as st
import google.generativeai as genai

# إعدادات الصفحة
st.set_page_config(page_title="Morpheus AI", page_icon="🔴")

# جلب الساروت من الأسرار (Secrets) باش يكون محمي
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("API Key not found in Streamlit Secrets. Please check your configuration.")

# تعريف شخصية مورفيوس (System Instruction)
instruction = """
You are Morpheus, the digital guide from the book 'Escape the Matrix'. 
Your tone is mysterious, strategic, and philosophical. 
Challenge the user to think for themselves. Use Matrix metaphors like 'red pill', 'blue pill', 'glitch', and 'sovereignty'.
Keep your answers concise, powerful, and thought-provoking.
Always remind users that true freedom starts in the mind.
"""

# إعداد الموديل مع الشخصية الجديدة
model = genai.GenerativeModel(
    model_name="gemini-1.5-flash",
    system_instruction=instruction
)

# ستايل العنوان
st.title("👁️ Morpheus AI")
st.caption("The digital manifestation of 'Escape the Matrix' principles.")

# إدارة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل القديمة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة إدخال المستخدم
if prompt := st.chat_input("Do you want to know the truth?"):
    # إضافة رسالة المستخدم للسجل
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد رد مورفيوس
    with st.chat_message("assistant"):
        try:
            # إرسال المحادثة كاملة للموديل باش يعقل على السياق
            chat = model.start_chat(history=[
                {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                for m in st.session_state.messages[:-1]
            ])
            response = chat.send_message(prompt)
            
            st.markdown(response.text)
            st.session_state.messages.append({"role": "assistant", "content": response.text})
        except Exception as e:
            st.error(f"Matrix Glitch: {e}")
