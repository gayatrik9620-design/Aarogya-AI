import importlib.util
import os
import sys
import streamlit as st

# =========================================================
# EXPLICIT ROOT PATH & Ui.py LOADER
# =========================================================

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

_ui_loaded = False
for _candidate in ("Ui.py", "ui.py"):
    _ui_path = os.path.join(ROOT_DIR, _candidate)
    if os.path.exists(_ui_path):
        _spec = importlib.util.spec_from_file_location("Ui", _ui_path)
        _ui_mod = importlib.util.module_from_spec(_spec)
        _spec.loader.exec_module(_ui_mod)
        apply_glossy_purple_theme = _ui_mod.apply_glossy_purple_theme
        render_page_banner = _ui_mod.render_page_banner
        render_gloss_card = _ui_mod.render_gloss_card
        render_medical_disclaimer = _ui_mod.render_medical_disclaimer
        _ui_loaded = True
        break

if not _ui_loaded:
    st.error(f"Could not find Ui.py in {ROOT_DIR}. Please ensure Ui.py is saved in the root aarogya-ai folder.")
    st.stop()

from src.chatbot import get_chatbot_response

# NOTE: st.set_page_config() is handled by app.py — NOT repeated here.

# =========================================================
# GLOSSY PURPLE THEME & PAGE STYLES
# =========================================================

apply_glossy_purple_theme()

st.markdown("""
<style>
.gloss-chat-panel {
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    padding: 20px 22px;
    margin: 14px 0 18px 0;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.96) 0%, rgba(243, 232, 255, 0.82) 100%);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(216, 180, 254, 0.85);
    box-shadow:
        0 12px 28px rgba(109, 40, 217, 0.09),
        inset 0 1px 0 rgba(255, 255, 255, 0.98);
}

@keyframes purplePulseGlow {
    0%, 100% { box-shadow: 0 12px 28px rgba(109, 40, 217, 0.09), inset 0 1px 0 rgba(255, 255, 255, 0.98); }
    50%      { box-shadow: 0 16px 34px rgba(126, 34, 206, 0.16), inset 0 1px 0 rgba(255, 255, 255, 1); }
}

.gloss-chat-panel {
    animation: fadeUp 0.65s ease, purplePulseGlow 4.5s ease-in-out infinite;
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# HEADER BANNER & GUIDANCE CARDS
# =========================================================

render_page_banner(
    symbol="🩺",
    title="Aarogya AI Chatbot",
    subtitle="Your AI-powered healthcare & wellness assistant for general health, sleep, activity, hydration, and healthy habits.",
    badge="🧬 Aarogya-AI • Health Assistant",
)

render_gloss_card(
    title="What You Can Ask",
    body="Ask general questions about health, sleep, physical activity, hydration, and healthy daily habits.",
    symbol="🧬",
    anim_class="anim-2",
)

render_gloss_card(
    title="Important Medical Notice",
    body="This chatbot provides general information only. It cannot diagnose diseases or prescribe medicines. Consult a qualified healthcare professional for personal medical advice, or call 112 in an emergency.",
    symbol="💊",
    anim_class="anim-3",
)

# =========================================================
# CHAT HISTORY & INTERACTION
# =========================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

st.markdown('<div class="gloss-chat-panel">', unsafe_allow_html=True)

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(
        message["role"],
        avatar="🩺" if message["role"] == "assistant" else "🧑",
    ):
        st.markdown(message["content"])

st.markdown('</div>', unsafe_allow_html=True)

# Chat input
question = st.chat_input("🩺 Ask your health question...")

if question:
    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user", avatar="🧑"):
        st.markdown(question)

    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner("🧬 Aarogya AI is thinking..."):
            response = get_chatbot_response(question)

        st.markdown(response)

    st.session_state.messages.append(
        {"role": "assistant", "content": response}
    )

# =========================================================
# FOOTER DISCLAIMER
# =========================================================

render_medical_disclaimer()