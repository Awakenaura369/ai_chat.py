import streamlit as st
import google.generativeai as genai

# 1. إعدادات الصفحة والأيقونة
st.set_page_config(page_title="Morpheus AI", page_icon="👁️")

# 2. جلب الساروت بأمان من Secrets
try:
    API_KEY = st.secrets["GOOGLE_API_KEY"]
    genai.configure(api_key=API_KEY)
except Exception as e:
    st.error("API Key missing! Please add GOOGLE_API_KEY to Streamlit Secrets.")

# 3. تعريف شخصية مورفيوس (System Instruction)
instruction = """
You are Morpheus, the digital guide from the book 'Escape the Matrix'. 
Your tone is mysterious, strategic, and philosophical. 
Challenge the user to think for themselves. 
Use Matrix metaphors (red pill, blue pill, glitches, sovereignty). 
Keep your answers concise and powerful. 
Remind them that you are the digital manifestation of the wisdom found in 'Escape the Matrix'.
"""

# 4. اختيار الموديل المتاح تلقائياً (لتفادي أرور 404)
@st.cache_resource
def load_morpheus_model():
    try:
        # البحث عن الموديلات المتاحة في حسابك
        available_models = [m.name for m in genai.list_models() if 'generateContent' in m.supported_generation_methods]
        # اختيار gemini-1.5-flash كخيار أول، أو أي موديل متاح
        model_name = "models/gemini-1.5-flash" if "models/gemini-1.5-flash" in available_models else available_models[0]
        
        return genai.GenerativeModel(
            model_name=model_name,
            system_instruction=instruction
        )
    except Exception as e:
        st.error(f"Matrix Glitch (Model Load): {e}")
        return None

model = load_morpheus_model()

# 5. واجهة المستخدم (UI)
st.title("👁️ Morpheus AI")
st.markdown("---")

# إدارة سجل المحادثة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض الرسائل السابقة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة إدخال المستخدم
if prompt := st.chat_input("Ask Morpheus..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # توليد الرد
    if model:
        with st.chat_message("assistant"):
            try:
                # إنشاء محادثة تعتمد على السجل (Context)
                chat = model.start_chat(history=[
                    {"role": "user" if m["role"] == "user" else "model", "parts": [m["content"]]}
                    for m in st.session_state.messages[:-1]
                ])
                response = chat.send_message(prompt)
                
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
            except Exception as e:
                st.error(f"Matrix Glitch: {e}")
