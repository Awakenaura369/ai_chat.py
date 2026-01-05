import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# 1. Global Page Configuration
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="wide")

# 2. Professional Dark Theme (ChatGPT Inspired)
st.markdown("""
    <style>
    .main { background-color: #212121; color: #ececf1; font-family: sans-serif; }
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #2f2f2f !important; border-radius: 15px; color: #ececf1 !important;
    }
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: transparent !important; color: #ececf1 !important;
    }
    p, span, div, label { color: #ececf1 !important; }
    h1 { color: #ffffff !important; text-align: center; font-weight: 600; }
    .stCaption { color: #b4b4b4 !important; text-align: center; }
    .stTextInput>div>div>input { background-color: #353541; color: white; border: 1px solid #565869; border-radius: 10px; }
    [data-testid="stSidebar"] { background-color: #171717; }
    .coffee-btn {
        background-color: #10a37f; color: white !important; padding: 12px; border-radius: 8px;
        text-align: center; text-decoration: none; display: block; font-weight: 600;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Core Engine
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
except:
    st.error("Authentication Error: Check your secrets.")
    st.stop()

def web_search(query):
    try:
        results = DDGS().text(query, max_results=3)
        return "\n".join([f"Source: {r['href']} - {r['body']}" for r in results])
    except: return ""

# 4. Sidebar
with st.sidebar:
    st.title("AGORAM Settings")
    st.markdown("---")
    paypal_url = "https://paypal.me/aipromptmoney"
    st.markdown(f'<a href="{paypal_url}" target="_blank" class="coffee-btn">⚡ Support AGORAM</a>', unsafe_allow_html=True)
    st.markdown("---")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# 5. UI Header
st.title("AGORAM AI")
st.caption("Universal Intelligence: Helpful, Clear & Wise")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message: st.image(message["image"])

# 6. Logic Turn
if prompt := st.chat_input("How can I help you today?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # التحقق من نوع السؤال لضبط الشخصية
    greetings = ["سلام", "لباس", "مرحبا", "hi", "hello", "hey"]
    tech_keywords = ["how", "code", "fix", "price", "news", "كيفاش", "برمجة", "كود", "ثمن"]
    
    is_general_or_tech = any(word in prompt.lower() for word in (greetings + tech_keywords))

    with st.chat_message("assistant"):
        context = ""
        image_url = None
        
        if any(word in prompt.lower() for word in tech_keywords):
            with st.spinner("Searching..."): context = web_search(prompt)
        
        if any(word in prompt.lower() for word in ["image", "draw", "imagine", "صورة"]):
            with st.spinner("Visualizing..."):
                image_url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&model=flux"
                st.image(image_url)

        # التبديل بين المساعد العادي والحكيم
        if is_general_or_tech:
            sys_msg = "You are AGORAM AI, a helpful and direct assistant. Respond naturally and clearly in the user's language."
            temp = 0.5
        else:
            sys_msg = "You are AGORAM AI, a wise guide. Provide deep and philosophical insights."
            temp = 0.8

        try:
            full_input = f"Context: {context}\n\nQuery: {prompt}" if context else prompt
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}, *st.session_state.messages[:-1], {"role": "user", "content": full_input}],
                temperature=temp
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            
            msg_save = {"role": "assistant", "content": response}
            if image_url: msg_save["image"] = image_url
            st.session_state.messages.append(msg_save)
        except Exception as e:
            st.error(f"Error: {str(e)}")
