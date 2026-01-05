import streamlit as st
from groq import Groq

# ستايل "أݣورام" (أسود وأحمر)
st.set_page_config(page_title="AGORAM AI", page_icon="🤖")
st.markdown("<style>.stApp { background-color: #0E1117; color: white; }</style>", unsafe_allow_html=True)

st.title("AGORAM AI 🤖")
st.caption("Powered by: Groq (Llama 3.1)")

# الربط مع الساروت
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Message AGORAM AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            chat_completion = client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are AGORAM AI. Answer in Moroccan Darija and English. Be wise and technical."},
                    *[{"role": m["role"], "content": m["content"]} for m in st.session_state.messages]
                ],
                model="llama-3.1-70b-versatile",
            )
            ans = chat_completion.choices[0].message.content
            st.markdown(ans)
            st.session_state.messages.append({"role": "assistant", "content": ans})
        except Exception as e:
            st.error(f"Groq Matrix Error: {e}")
