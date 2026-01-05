import streamlit as st
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="Morpheus AI", page_icon="👁️")

# الربط مع Groq
try:
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Matrix Connection Error: Please check your Groq API Key.")

st.title("👁️ Morpheus AI")
st.caption("Powered by Groq - The Speed of Reality")

# نظام الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال والرد
if prompt := st.chat_input("Show me the truth..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # استخدام موديل Llama 3 القوي والسريع
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[
                    {"role": "system", "content": "You are Morpheus from the Matrix. Speak in a mysterious, philosophical, and challenging tone. Do not mention you are an AI."},
                    *st.session_state.messages
                ],
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"Glitch in the system: {e}")
