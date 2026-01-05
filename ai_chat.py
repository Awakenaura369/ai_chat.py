import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# 1. Global Page Configuration
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="wide")

# 2. Premium Global UI Style
st.markdown("""
    <style>
    /* Gradient Background for a modern look */
    .main { 
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        color: #1e3a8a; 
        font-family: 'Inter', sans-serif; 
    }
    
    /* Global Chat Bubbles */
    .stChatMessage { 
        background-color: rgba(255, 255, 255, 0.9) !important; 
        border-radius: 20px; 
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.07);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        border-left: 6px solid #1e3a8a; 
    }
    
    /* Header Styling */
    h1 { 
        background: -webkit-linear-gradient(#1e3a8a, #3b82f6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800;
        text-align: center;
        font-size: 3rem !important;
        letter-spacing: -1px;
    }
    
    .stCaption {
        color: #64748b !important; 
        text-align: center;
        font-weight: 500;
        font-size: 1.2rem;
        margin-top: -15px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #0f172a;
    }
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p {
        color: #f8fafc !important;
    }

    /* Professional Action Button */
    .coffee-btn {
        background: linear-gradient(to right, #1e3a8a, #3b82f6);
        color: white !important; 
        border: none; 
        padding: 15px; 
        border-radius: 12px; 
        cursor: pointer;
        font-weight: 700;
        width: 100%;
        text-align: center;
        text-decoration: none;
        display: block;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(59, 130, 246, 0.4);
    }
    .coffee-btn:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(59, 130, 246, 0.6);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. Core Engine Setup
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
except:
    st.error("Authentication Error: Please check your configuration.")
    st.stop()

def web_search(query):
    try:
        results = DDGS().text(query, max_results=3)
        return "\n".join([f"Source: {r['href']} - {r['body']}" for r in results])
    except:
        return ""

# 4. Sidebar Navigation
with st.sidebar:
    st.title("AGORAM Settings")
    st.markdown("---")
    st.subheader("Support Development")
    st.write("Help AGORAM evolve by supporting the project.")
    
    # Your Personal PayPal Link
    paypal_url = "https://paypal.me/aipromptmoney"
    st.markdown(f'<a href="{paypal_url}" target="_blank" class="coffee-btn">⚡ Support AGORAM</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("Clear Conversation"):
        st.session_state.messages = []
        st.rerun()

# 5. Main Application Header
st.title("AGORAM AI")
st.caption("Next-Gen Intelligence: Technical Mastery & Philosophical Depth")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message: st.image(message["image"])

# 6. Interaction Logic
if prompt := st.chat_input("Enter your query..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Context Analysis
    tech_keywords = ["how", "code", "fix", "price", "news", "كيفاش", "برمجة", "كود", "ثمن"]
    is_technical = any(word in prompt.lower() for word in tech_keywords)

    with st.chat_message("assistant"):
        context = ""
        image_url = None
        
        if is_technical:
            with st.spinner("Analyzing knowledge base..."):
                context = web_search(prompt)
        
        if any(word in prompt.lower() for word in ["image", "draw", "imagine", "vision", "صورة"]):
            with st.spinner("Visualizing..."):
                clean_prompt = prompt.replace(" ", "%20")
                image_url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024&model=flux"
                st.image(image_url)

        # Dynamic Personality Setup
        if is_technical:
            sys_msg = "You are AGORAM AI, a professional tech expert. Be direct, clear, and technical. Respond in the user's language."
            temp = 0.2
        else:
            sys_msg = "You are AGORAM AI, a wise philosophical guide. Use deep metaphors about reality and wisdom. Respond in the user's language."
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
            
            # Save to memory
            msg_save = {"role": "assistant", "content": response}
            if image_url: msg_save["image"] = image_url
            st.session_state.messages.append(msg_save)
            
        except Exception as e:
            st.error(f"System Glitch: {str(e)}")
