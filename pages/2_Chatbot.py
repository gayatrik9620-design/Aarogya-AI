import os
import sys
import importlib.util
from pathlib import Path
import streamlit as st

# =========================================================
# ROOT DIRECTORY
# =========================================================

ROOT_DIR = Path(__file__).resolve().parent.parent

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

# =========================================================
# LOAD Ui.py
# =========================================================

ui_path = None

for filename in ["Ui.py", "ui.py"]:
    candidate = ROOT_DIR / filename
    if candidate.is_file():
        ui_path = candidate
        break

if ui_path is None:
    st.error("Ui.py file not found!")
    st.write("Expected location:", str(ROOT_DIR))
    st.write("Files available:", [f.name for f in ROOT_DIR.iterdir()])
    st.stop()

try:
    spec = importlib.util.spec_from_file_location("Ui", str(ui_path))

    if spec is None or spec.loader is None:
        raise ImportError("Could not load Ui.py")

    ui_module = importlib.util.module_from_spec(spec)
    sys.modules["Ui"] = ui_module
    spec.loader.exec_module(ui_module)

    apply_glossy_purple_theme = ui_module.apply_glossy_purple_theme
    render_page_banner = ui_module.render_page_banner
    render_gloss_card = ui_module.render_gloss_card
    render_medical_disclaimer = ui_module.render_medical_disclaimer

except Exception as e:
    st.error(f"Ui.py loading error: {e}")
    st.stop()

# =========================================================
# CHATBOT IMPORT
# =========================================================

try:
    from src.chatbot import get_chatbot_response
except Exception as e:
    st.error(f"Chatbot import error: {e}")
    st.stop()

# =========================================================
# THEME
# =========================================================

apply_glossy_purple_theme()

st.markdown("""
<style>
.gloss-chat-panel {
    border-radius: 22px;
    padding: 20px;
    margin: 14px 0;
    background: linear-gradient(
        155deg,
        #FFFFFF 0%,
        #F3E8FF 100%
    );
    border: 1px solid rgba(216,180,254,0.85);
    box-shadow: 0 12px 28px rgba(109,40,217,0.09);
}

.chat-heading {
    color: #4C1D95;
    font-size: 15px;
    font-weight: 800;
    margin-bottom: 10px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER
# =========================================================

render_page_banner(
    symbol="🩺",
    title="Aarogya AI Chatbot",
    subtitle=(
        "Your AI-powered healthcare and wellness assistant "
        "for general health, sleep, activity and healthy habits."
    ),
    badge="🧬 Aarogya-AI • Health Assistant",
)

# =========================================================
# INFORMATION CARDS
# =========================================================

render_gloss_card(
    title="What You Can Ask",
    body=(
        "Ask general questions about health awareness, "
        "sleep, hydration, physical activity and healthy habits."
    ),
    symbol="🧬",
    anim_class="anim-2",
)

render_gloss_card(
    title="Important Medical Notice",
    body=(
        "This chatbot provides general educational information only. "
        "It does not diagnose diseases or prescribe medicines. "
        "Consult a qualified healthcare professional for personal "
        "medical concerns. In an emergency, call 112."
    ),
    symbol="💊",
    anim_class="anim-3",
)

# =========================================================
# SESSION STATE
# =========================================================

if "chatbot_messages" not in st.session_state:
    st.session_state.chatbot_messages = []

# =========================================================
# QUICK PROMPTS
# =========================================================

st.markdown(
    '<div class="chat-heading">💡 Quick Questions</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

prompt = None

with col1:
    if st.button("💤 Sleep Tips", use_container_width=True):
        prompt = "How can I improve my sleep?"

with col2:
    if st.button("💧 Hydration", use_container_width=True):
        prompt = "How can I stay hydrated?"

with col3:
    if st.button("🧬 Healthy Habits", use_container_width=True):
        prompt = "Give me healthy lifestyle tips."

# =========================================================
# CLEAR CHAT
# =========================================================

if st.button("🗑️ Clear Chat"):
    st.session_state.chatbot_messages = []
    st.rerun()

# =========================================================
# DISPLAY CHAT HISTORY
# =========================================================

with st.container(border=True):

    if not st.session_state.chatbot_messages:
        st.caption(
            "Start a conversation below or select a quick question."
        )

    for message in st.session_state.chatbot_messages:

        with st.chat_message(
            message["role"],
            avatar="🩺" if message["role"] == "assistant" else "🧑",
        ):
            st.markdown(message["content"])

# =========================================================
# USER INPUT
# =========================================================

question = st.chat_input("🩺 Ask Aarogya AI your question...")

if prompt:
    question = prompt

# =========================================================
# GENERATE AI RESPONSE
# =========================================================

if question:

    st.session_state.chatbot_messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🩺"):

        with st.spinner("🧬 Aarogya AI is thinking..."):

            try:
                response = get_chatbot_response(question)

                if not response:
                    response = "I could not generate a response. Please try again."

                st.markdown(response)

            except Exception as e:
                response = (
                    "Sorry, I am unable to process your request right now. "
                    "Please check your API configuration and try again."
                )

                st.error(response)
                st.caption(f"Technical details: {e}")

    st.session_state.chatbot_messages.append({
        "role": "assistant",
        "content": response
    })

# =========================================================
# FOOTER
# =========================================================

render_medical_disclaimer()