import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# 1. Global Page Configuration
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="wide")

# 2. Premium Dark UI (ChatGPT Style) - Fixed Visibility
st.markdown("""
    <style>
    .main { background-color: #212121; color: #ffffff; font-family: 'Inter', sans-serif; }
    
    /* User Message Style */
    .stChatMessage[data-testid="stChatMessageUser"] {
        background-color: #2f2f2f !important; border-radius: 15px; padding: 15px; margin-bottom: 10px;
    }

    /* Assistant Message Style */
    .stChatMessage[data-testid="stChatMessageAssistant"] {
        background-color: transparent !important; padding: 15px; margin-bottom: 10px;
    }

    /* Absolute Text Visibility Fix */
    p, span, div, label, .stMarkdown {
        color: #ececf1 !important; 
        font-size: 1.05rem;
        line-height: 1.6;
    }
    
    h1 { color: #ffffff !important; text-align: center; font-weight: 700; font-size: 2.5rem !important; }
    .stCaption { color: #b4b4b4 !important; text-align: center; font-size: 1rem; }

    /* Input Field */
    .stTextInput>div>div>input { 
        background-color: #353541; color: white !important; border: 1px solid #565869; border-radius: 12px; padding: 10px;
    }

    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #171717; border-right: 1px solid #333; }
    
    /* Support Button (ChatGPT Green) */
    .support-btn {
        background-color: #10a37f; color: white !important; padding: 14px; border-radius: 10px;
        text-align: center; text-decoration: none; display: block; font-weight: 700; transition: 0.3s;
    }
    .support-btn:hover { background-color: #1a7f64; transform: scale(1.02); }
    </style>
    """, unsafe_allow_html=True)

# 3. Secure Engine Setup
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
except:
    st.error("Matrix Secrets Error: Please check your configuration.")
    st.stop()

def web_search(query):
    try:
        results = DDGS().text(query, max_results=3)
        return "\n".join([f"Source: {r['href']} - {r['body']}" for r in results])
    except: return ""

# 4. Sidebar Content
with st.sidebar:
    st.title("AGORAM Settings")
    st.markdown("---")
    st.subheader("Support Growth")
    st.write("Help AGORAM evolve with a cup of coffee:")
    paypal_url = "https://paypal.me/aipromptmoney"
    st.markdown(f'<a href="{paypal_url}" target="_blank" class="support-btn">⚡ Support via PayPal</a>', unsafe_allow_html=True)
    st.markdown("---")
    if st.button("Clear History"):
        st.session_state.messages = []
        st.rerun()

# 5. Header Section
st.title("AGORAM AI")
st.caption("Universal Intelligence: Technical Precision & Philosophical Wisdom")

if "messages" not in st.session_state:
    st.session_state.messages = []

# Displaying Chat
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message: st.image(message["image"])

# 6. Interaction & Response Logic
if prompt := st.chat_input("Message AGORAM AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    greetings = ["سلام", "لباس", "مرحبا", "hi", "hello", "hey", "test"]
    tech_keys = ["how", "code", "fix", "price", "news", "كيفاش", "برمجة", "كود", "ثمن"]
    is_general = any(word in prompt.lower() for word in (greetings + tech_keys))

    with st.chat_message("assistant"):
        context = ""
        image_url = None
        
        if any(word in prompt.lower() for word in tech_keys):
            with st.spinner("Searching..."): context = web_search(prompt)
        
        if any(word in prompt.lower() for word in ["image", "draw", "imagine", "صورة"]):
            with st.spinner("Visualizing..."):
                image_url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024&model=flux"
                st.image(image_url)

        # Fixed Temp and Character Control
        if is_general:
            # Low temperature for precision (0.1) prevents mixed characters
            sys_msg = "You are AGORAM AI, a helpful assistant. Use ONLY Arabic letters for Arabic words. No Latin mixing. Be direct and friendly."
            temp = 0.1 
        else:
            sys_msg = "You are AGORAM AI, a wise philosophical guide. Use deep metaphors only for life wisdom. Maintain perfect Arabic script."
            temp = 0.3

        try:
            full_input = f"Web Context: {context}\n\nQuery: {prompt}" if context else prompt
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": sys_msg}, *st.session_state.messages[:-1], {"role": "user", "content": full_input}],
                temperature=temp # Lowered to fix Glitch
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            
            msg_save = {"role": "assistant", "content": response}
            if image_url: msg_save["image"] = image_url
            st.session_state.messages.append(msg_save)
        except Exception as e:
            st.error(f"Matrix Error: {str(e)}")
