import streamlit as st
from groq import Groq
import datetime
import requests
import sqlite3

# --- Page Config ---
st.set_page_config(page_title="AGORAM AI", page_icon="🧠", layout="wide")

# --- Database Setup (SQLite for demo, can be Supabase/PostgreSQL) ---
conn = sqlite3.connect("agoram_ai.db", check_same_thread=False)
c = conn.cursor()
c.execute('''
CREATE TABLE IF NOT EXISTS usage_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    date TEXT,
    prompt TEXT,
    response TEXT,
    type TEXT
)
''')
conn.commit()

# --- Session State Initialization ---
if "messages" not in st.session_state:
    st.session_state.messages = []

if "api_calls_today" not in st.session_state:
    st.session_state.api_calls_today = 0
    st.session_state.last_call_date = datetime.date.today()

if "analytics" not in st.session_state:
    st.session_state.analytics = {
        "total_prompts": 0,
        "top_prompts": {}
    }

# --- Constants ---
DAILY_API_LIMIT = 5  # Limit free calls per user per day

# --- Helper Functions ---
def reset_daily_limit():
    today = datetime.date.today()
    if st.session_state.last_call_date != today:
        st.session_state.api_calls_today = 0
        st.session_state.last_call_date = today

def log_usage(prompt, response, type_):
    today = str(datetime.date.today())
    c.execute("INSERT INTO usage_log (date, prompt, response, type) VALUES (?, ?, ?, ?)", (today, prompt, response, type_))
    conn.commit()

def ai_response(prompt):
    reset_daily_limit()
    if st.session_state.api_calls_today >= DAILY_API_LIMIT:
        return "Daily limit reached. Try again tomorrow."
    
    # Update analytics
    st.session_state.analytics["total_prompts"] += 1
    st.session_state.analytics["top_prompts"][prompt] = st.session_state.analytics["top_prompts"].get(prompt, 0) + 1

    try:
        client = Groq(api_key=st.secrets["GROQ_API_KEY"])
        system_instruction = """
        You are AGORAM AI. Respond naturally and directly.
        Do NOT use emojis or extra formatting.
        Match the user's language and tone.
        Adapt responses for user profession: doctor, engineer, programmer, content creator.
        """
        messages = [{"role": "system", "content": system_instruction}] + \
                   [{"role": m["role"], "content": m["content"]} for m in st.session_state.messages] + \
                   [{"role": "user", "content": prompt}]
        
        res = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=messages
        )
        answer = res.choices[0].message.content.strip()
        st.session_state.api_calls_today += 1
        log_usage(prompt, answer, "chat")
        return answer
    except Exception as e:
        return f"Error: {str(e)}"

def generate_image(prompt):
    try:
        api_key = st.secrets["GEMINI_API_KEY"].strip()
        url = "https://api.gemini.ai/v1/images/generate"
        payload = {"prompt": prompt, "size": "1024x1024"}
        headers = {"Authorization": f"Bearer {api_key}"}
        r = requests.post(url, json=payload, headers=headers).json()
        image_url = r.get("data", [{}])[0].get("url")
        if image_url:
            log_usage(prompt, image_url, "image")
        return image_url if image_url else "Image generation failed."
    except Exception as e:
        return f"Error generating image: {str(e)}"

# --- UI ---
st.title("AGORAM AI 🧠 | Professional Intelligence")

tab1, tab2, tab3 = st.tabs(["Chat", "Generate Image", "Analytics"])

# --- Chat Tab ---
with tab1:
    prompt = st.chat_input("Ask anything:")
    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})
        response = ai_response(prompt)
        st.session_state.messages.append({"role": "assistant", "content": response})
    
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

# --- Image Tab ---
with tab2:
    img_prompt = st.text_input("Enter prompt for image generation:")
    if st.button("Generate Image"):
        if img_prompt:
            img_url = generate_image(img_prompt)
            if img_url.startswith("http"):
                st.image(img_url, use_column_width=True)
            else:
                st.error(img_url)

# --- Analytics Tab ---
with tab3:
    st.subheader("📊 Usage Analytics")
    st.write(f"API Calls Today: {st.session_state.api_calls_today}/{DAILY_API_LIMIT}")
    st.write(f"Total Prompts Sent: {st.session_state.analytics['total_prompts']}")
    
    if st.session_state.analytics["top_prompts"]:
        st.write("Top Prompts:")
        for p, count in st.session_state.analytics["top_prompts"].items():
            st.write(f"- {p}: {count} times")
    
    # Optional: Show all logs from DB
    if st.checkbox("Show Full Logs"):
        logs = c.execute("SELECT * FROM usage_log ORDER BY id DESC").fetchall()
        st.dataframe(logs)
