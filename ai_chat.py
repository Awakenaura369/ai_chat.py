import streamlit as st
from groq import Groq
from duckduckgo_search import DDGS

# 1. إعداد الصفحة بالهوية الجديدة "AGORAM"
st.set_page_config(page_title="AGORAM AI", page_icon="🤖", layout="wide")

# 2. ستايل "أݣورام" المغربي العصري (Modern Moroccan Style)
st.markdown("""
    <style>
    /* الخلفية العامة */
    .main { 
        background-color: #f4f7f6; 
        color: #1e3a8a; 
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
    }
    
    /* ستايل فقاعات الشات */
    .stChatMessage { 
        background-color: #ffffff !important; 
        border-radius: 15px; 
        padding: 15px;
        margin-bottom: 15px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border-left: 5px solid #1e3a8a; 
    }
    
    /* العناوين */
    h1 { 
        color: #1e3a8a !important; 
        font-weight: 800;
        text-align: center;
        text-shadow: 1px 1px 2px rgba(0,0,0,0.1);
    }
    
    .stCaption {
        color: #b45309 !important; 
        text-align: center;
        font-weight: bold;
        font-size: 1.1em;
    }

    /* زر الإدخال */
    .stTextInput>div>div>input { 
        border-radius: 20px;
        border: 2px solid #1e3a8a;
    }

    /* ستايل الشريط الجانبي */
    [data-testid="stSidebar"] {
        background-color: #1e3a8a;
    }
    
    [data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p, [data-testid="stSidebar"] span {
        color: white !important;
    }

    /* ستايل زر القهوة */
    .coffee-btn {
        background-color: #b45309; 
        color: white !important; 
        border: none; 
        padding: 12px; 
        border-radius: 8px; 
        cursor: pointer;
        font-weight: bold;
        width: 100%;
        text-align: center;
        text-decoration: none;
        display: inline-block;
        transition: 0.3s;
    }
    .coffee-btn:hover {
        background-color: #d97706;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    </style>
    """, unsafe_allow_html=True)

# 3. إعداد الاتصال بـ Groq
try:
    groq_client = Groq(api_key=st.secrets["GROQ_API_KEY"].strip())
except:
    st.error("Matrix Secrets Missing! Check your API Keys in Streamlit.")
    st.stop()

# دالة البحث في الويب
def web_search(query):
    try:
        results = DDGS().text(query, max_results=3)
        return "\n".join([f"Source: {r['href']} - {r['body']}" for r in results])
    except:
        return ""

# 4. الشريط الجانبي (Sidebar)
with st.sidebar:
    st.title("⚙️ لوحة التحكم")
    st.markdown("---")
    st.subheader("☕ دعم الحكيم")
    st.write("إذا كنت تستفيد من حكمة AGORAM، يمكنك دعم استمراريته:")
    
    # رابط PayPal الشخصي ديالك
    my_paypal_link = "https://paypal.me/aipromptmoney" 
    
    st.markdown(f'<a href="{my_paypal_link}" target="_blank" class="coffee-btn">💰 صيفط قهيوة لـ AGORAM</a>', unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ مسح الذاكرة"):
        st.session_state.messages = []
        st.rerun()

# الواجهة الرئيسية
st.title("🤖 AGORAM AI | أݣورام")
st.caption("الرجل الحكيم: خبيرك في التقنية ومرشدك في الحياة")

if "messages" not in st.session_state:
    st.session_state.messages = []

# عرض المحادثة
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])
        if "image" in message: st.image(message["image"])

# 5. منطق الاستجابة الذكي (Dynamic AI)
if prompt := st.chat_input("تحدث مع الحكيم أݣورام..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # تحليل نوع السؤال (تقني/واقعي أم فلسفي)
    tech_keywords = ["كيفاش", "برمجة", "كود", "ثمن", "تقنية", "سعر", "شحال", "أخبار", "دير", "صاوب", "how", "code", "price", "tech", "news"]
    is_tech_or_fact = any(word in prompt.lower() for word in tech_keywords)

    with st.chat_message("assistant"):
        context = ""
        image_url = None
        
        # أ - البحث في الويب للمعلومات الآنية
        if is_tech_or_fact:
            with st.spinner("يتم الآن استشارة مصادر البيانات..."):
                context = web_search(prompt)
        
        # ب - توليد الصور
        if any(word in prompt.lower() for word in ["صورة", "تخيل", "رسم", "draw", "imagine"]):
            with st.spinner("يتم الآن رسم خيالك..."):
                clean_prompt = prompt.replace(" ", "%20")
                image_url = f"https://pollinations.ai/p/{clean_prompt}?width=1024&height=1024&model=flux"
                st.image(image_url)

        # ج - تحديد الشخصية بناءً على الحكمة الأمازيغية
        if is_tech_or_fact:
            system_instruction = "You are AGORAM AI, a professional tech expert. Provide accurate, helpful, and direct answers in Moroccan Darija. No philosophy."
            current_temp = 0.2 
        else:
            system_instruction = "You are AGORAM AI, the wise tribal guide (Agoram). Use deep, respectful, and philosophical Moroccan Darija. Share wisdom about life and reality."
            current_temp = 0.8 

        try:
            user_input = f"Web Context: {context}\n\nUser Question: {prompt}" if context else prompt
            
            completion = groq_client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[
                    {"role": "system", "content": system_instruction},
                    *st.session_state.messages[:-1],
                    {"role": "user", "content": user_input}
                ],
                temperature=current_temp
            )
            response = completion.choices[0].message.content
            st.markdown(response)
            
            # حفظ في الذاكرة
            msg_save = {"role": "assistant", "content": response}
            if image_url: msg_save["image"] = image_url
            st.session_state.messages.append(msg_save)
            
        except Exception as e:
            st.error(f"عذراً، حدث خلل بسيط: {str(e)}")
