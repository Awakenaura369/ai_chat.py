import streamlit as st
from groq import Groq

# إعداد الصفحة
st.set_page_config(page_title="Morpheus AI", page_icon="👁️")

# الربط مع Groq وتنظيف الساروت
try:
    if "GROQ_API_KEY" in st.secrets:
        # استخدام strip() لمسح أي فراغات خفية قد تسبب خطأ 401
        client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
    else:
        st.error("Matrix Error: GROQ_API_KEY missing in Secrets.")
        st.stop()
except Exception as e:
    st.error(f"Configuration Error: {e}")
    st.stop()

st.title("👁️ Morpheus AI")
st.caption("The simulation is under your command.")

# نظام الذاكرة
if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# منطقة الإدخال والرد (باستخدام الموديل الجديد)
if prompt := st.chat_input("Show me the truth..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # التبديل للموديل الجديد llama-3.3-70b-versatile لضمان الاستقرار
            completion = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": "You are Morpheus from the Matrix. Speak in a mysterious, philosophical tone. You are here to help users wake up from the digital illusion."},
                    *st.session_state.messages
                ],
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
        except Exception as e:
            st.error(f"The Matrix detected a glitch: {e}")
