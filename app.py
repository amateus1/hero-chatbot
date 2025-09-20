import re
import streamlit as st
import time
from me_chatbot import Me

# 🌐 Layout
st.set_page_config(
    page_title="Meet Hero — Canine Model & Brand Ambassador",
    layout="wide"
)

# 🎨 Style
st.markdown("""
    <style>
    .main .block-container {
        max-width: 1000px;
        padding-top: 1.5rem;
        padding-bottom: 2rem;
        margin: auto;
    }
    h1, h2, h3, h4 {
        font-size: 1.2rem !important;
    }
    p, li {
        font-size: 0.95rem !important;
        line-height: 1.6;
    }
    .message-container {
        display: flex;
        justify-content: flex-end;
        align-items: center;
        gap: 0.5rem;
    }
    .user-bubble {
        background-color: #f0f8ff;
        padding: 12px 16px;
        border-radius: 16px;
        font-size: 16px;
        line-height: 1.6;
        max-width: 85%;
        text-align: right;
        word-break: break-word;
    }
    </style>
""", unsafe_allow_html=True)

# 🌍 Language options
language_options = {
    "中文 (Chinese)": {
        "title": "🐶 认识 Hero —— 狗狗模特与品牌大使",
        "desc": (
            "👋 欢迎！我是 **Hero（黄黄）** —— 一半是幸存者，一半是影响者，100% 永远摇尾巴的乐观派。  \n\n"
            "我经历过从 **三条腿的流浪狗** 克服遗弃与艰辛…  \n\n"
            "…到成为 **专业模特与代言人** 的历程，合作品牌包括 **皇家狗粮、Halo 狗粮、平安宠物保险，以及懂车帝 App**。  \n\n"
            "好奇从哪里开始？可以问我关于品牌合作、媒体报道、最爱的食物，或者我从街头到聚光灯下的生命感悟。  \n\n"
            "如果你只想听有趣的事 — 没问题！我会告诉你关于挠肚子、埋骨头，或者三条腿狗狗去土耳其旅行的经历。🌍🐾"
        ),
        "input_placeholder": "问 Hero 点什么吧…",
    },
    "English": {
        "title": "🐶 Meet Hero — Canine Model & Brand Ambassador",
        "desc": (
            "👋 Welcome! I’m **Hero (黄黄)** — part survivor, part influencer, and 100% tail-wagging optimist.  \n\n"
            "I’ve been trained on my journey from a **three-legged rescue dog** who overcame abandonment…  \n\n"
            "…to becoming a **professional model and spokesperson** for brands like **Royal Dog Food, Halo, Ping An Pet Insurance, and Dangchedi App**.  \n\n"
            "Curious where to start? Ask me about my brand collaborations, press coverage, favorite foods, or my life lessons from the streets to the spotlight.  \n\n"
            "And if you just want the fun stuff — yes, I’ll happily tell you about belly rubs, hiding bones, or what it’s like to travel to Turkey on three legs. 🌍🐾"
        ),
        "input_placeholder": "Ask Hero something...",
    }
}

# 🌐 Language select
selected_lang = st.selectbox(
    "🌐 Language / 语言",
    list(language_options.keys()),
    index=0  # 👈 ensures 中文 (Chinese) is default
)
ui = language_options[selected_lang]
# 🧠 Session state
if "lang_prev" not in st.session_state:
    st.session_state.lang_prev = selected_lang
if st.session_state.lang_prev != selected_lang:
    st.session_state.history = []
    st.session_state.lang_prev = selected_lang

if "history" not in st.session_state:
    st.session_state.history = []

if "user_input" not in st.session_state:
    st.session_state.user_input = ""

if "prompt_count" not in st.session_state:
    st.session_state.prompt_count = 0

# >>> START CHANGE 1: add flags for email tracking <<<
if "email" not in st.session_state:
    st.session_state.email = None
if "email_prompt_shown" not in st.session_state:
    st.session_state.email_prompt_shown = False
# >>> END CHANGE 1 <<<

# 🤖 Load bot
me = Me()

# 🧢 Header
st.markdown(f"## {ui['title']}")
st.markdown(ui["desc"])

# 💬 History rendering
for user, bot in st.session_state.history:
    with st.chat_message("user", avatar="🧑"):
        st.markdown(
            f"""
            <div class="message-container">
                <div class="user-bubble">
                    {user}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )
    with st.chat_message("assistant", avatar="🤖"):
        st.markdown(bot, unsafe_allow_html=True)

# 🧾 Input box
user_input = st.chat_input(ui["input_placeholder"])

if st.session_state.user_input:
    user_input = st.session_state.user_input
    st.session_state.user_input = ""

if user_input:
    st.session_state.prompt_count += 1
    display_input = user_input

    contact_keywords = ["contact", "reach", "connect", "talk", "email", "get in touch"]

    # 📧 Capture email typed directly in chat
    email_match = re.search(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", user_input)
    if email_match and not st.session_state.get("email"):
        from me_chatbot import send_email_alert
        user_email = email_match.group(0)
        try:
            send_email_alert(user_email)
            st.success(f"✅ Thanks! Hero's Team has been notified of your email: {user_email}")
            st.session_state.email = user_email
        except Exception as e:
            st.error(f"❌ Failed to send email: {e}")

    # ---- multilingual transform after we’ve done any email capture ----
    if selected_lang == "中文 (Chinese)":
        user_input = f"请始终用中文回答：{user_input}"
    elif selected_lang == "English":
        user_input = f"Please respond only in English: {user_input}"


    # ---- show email input ONCE if conditions match and we don't have an email yet ----
    should_suggest_email = (
        (st.session_state.prompt_count >= 3 or any(
            kw in display_input.lower() for kw in contact_keywords
        ))
        and not st.session_state.email
        and not st.session_state.get("email_prompt_shown", False)
    )

    if should_suggest_email:
        st.markdown(ui["consult_prompt"])
        st.session_state.email_prompt_shown = True  # ✅ only show once
            

    # ✅ Right-aligned user bubble
    with st.chat_message("user", avatar="🧑"):
        st.markdown(
            f"""
            <div class="message-container">
                <div class="user-bubble">
                    {display_input}
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

    # 🧠 Generate assistant response
    response = me.chat(user_input, [])

    # 📡 Stream assistant response
    with st.chat_message("assistant", avatar="🤖"):
        stream_box = st.empty()
        full_response = ""
        for char in response:
            full_response += char
            stream_box.markdown(full_response + "▌")   # ✅ no unsafe_allow_html
            time.sleep(0.01)
        stream_box.markdown(response)  # ✅ final clean render with Markdown

    # 💾 Save to history
    st.session_state.history.append((display_input, response))
