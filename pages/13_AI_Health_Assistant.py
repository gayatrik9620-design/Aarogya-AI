import os
import sys
import importlib.util
from pathlib import Path
import streamlit as st

# =========================================================
# PROJECT ROOT DETECTION & UI LOADER
# =========================================================

CURRENT_FILE = Path(__file__).resolve()

ROOT_DIR = None

# Find the folder containing Ui.py
for parent in CURRENT_FILE.parents:
    if (parent / "Ui.py").is_file():
        ROOT_DIR = parent
        break
    if (parent / "ui.py").is_file():
        ROOT_DIR = parent
        break

if ROOT_DIR is None:
    st.error(
        "Could not locate Ui.py. "
        f"Current file location: {CURRENT_FILE}"
    )
    st.stop()

ROOT_DIR = str(ROOT_DIR)

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# Load UI module
_ui_path = None

for candidate in ("Ui.py", "ui.py"):
    possible_path = os.path.join(ROOT_DIR, candidate)

    if os.path.isfile(possible_path):
        _ui_path = possible_path
        break

if _ui_path is None:
    st.error(f"UI file not found in: {ROOT_DIR}")
    st.stop()

try:
    _spec = importlib.util.spec_from_file_location(
        "aarogya_ui", _ui_path
    )

    if _spec is None or _spec.loader is None:
        raise ImportError("Could not create UI module loader.")

    _ui_mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_ui_mod)

    apply_glossy_purple_theme = (
        _ui_mod.apply_glossy_purple_theme
    )
    render_page_banner = _ui_mod.render_page_banner
    render_gloss_card = _ui_mod.render_gloss_card
    render_medical_disclaimer = (
        _ui_mod.render_medical_disclaimer
    )

except Exception as e:
    st.error(f"Error loading Ui.py: {e}")
    st.stop()

from src.chatbot import get_chatbot_response

# NOTE: Page configuration is handled by app.py.


# =========================================================
# GLOSSY PURPLE THEME & CHAT STYLES
# =========================================================

apply_glossy_purple_theme()

st.markdown("""
<style>
.purple-chat-label {
    font-size: 12.5px;
    font-weight: 800;
    color: #4C1D95;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 10px;
}

.gloss-feat-pill {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: linear-gradient(145deg, #FFFFFF 0%, #F3E8FF 100%);
    border: 1px solid rgba(192, 132, 252, 0.65);
    border-radius: 20px;
    padding: 8px 16px;
    font-size: 13px;
    font-weight: 700;
    color: #2E1065;
    margin-right: 8px;
    margin-bottom: 8px;
    box-shadow: 0 6px 16px rgba(109, 40, 217, 0.08);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.gloss-feat-pill:hover {
    transform: translateY(-2px);
    box-shadow: 0 10px 22px rgba(126, 34, 206, 0.14);
}
</style>
""", unsafe_allow_html=True)


# =========================================================
# PAGE HEADER
# =========================================================

render_page_banner(
    symbol="🩺",
    title="Your AI Health Assistant",
    subtitle="Ask questions about general wellness, lifestyle habits, and health awareness. Educational guidance only.",
    badge="🧬 Aarogya-AI • Conversational Wellness",
)


# =========================================================
# SAFETY DISCLAIMER
# =========================================================

render_gloss_card(
    title="Medical Safety Notice",
    body="Aarogya-AI provides general health and wellness information only. It does not diagnose diseases or prescribe medications. For personal medical concerns, consult a qualified healthcare professional. In an emergency, call 112.",
    symbol="🫀",
    anim_class="anim-2"
)


# =========================================================
# FEATURE PILLS
# =========================================================

st.markdown("""
<div class="anim-2">
    <span class="gloss-feat-pill">🩺 Natural Language</span>
    <span class="gloss-feat-pill">🧬 AI-Powered Insights</span>
    <span class="gloss-feat-pill">💊 Safety-First Design</span>
    <span class="gloss-feat-pill">🫀 Health-Aware Context</span>
</div>
""", unsafe_allow_html=True)

st.markdown(
    '<div style="height:14px"></div>',
    unsafe_allow_html=True
)


# =========================================================
# QUICK PROMPTS
# =========================================================

st.markdown(
    '<div class="purple-chat-label anim-2">💡 Quick Prompts</div>',
    unsafe_allow_html=True
)

qp_col1, qp_col2, qp_col3, qp_col4 = st.columns(4)

quick_prompts = [
    "How can I improve my sleep?",
    "Give me healthy lifestyle tips",
    "How can I stay hydrated?",
    "How to improve daily activity?",
]

if "health_messages" not in st.session_state:
    st.session_state.health_messages = []

prompt_clicked = None

with qp_col1:
    if st.button("💤 Sleep Tips", use_container_width=True):
        prompt_clicked = quick_prompts[0]

with qp_col2:
    if st.button("🧬 Lifestyle Tips", use_container_width=True):
        prompt_clicked = quick_prompts[1]

with qp_col3:
    if st.button("💧 Hydration Tips", use_container_width=True):
        prompt_clicked = quick_prompts[2]

with qp_col4:
    if st.button("🩺 Activity Tips", use_container_width=True):
        prompt_clicked = quick_prompts[3]

st.markdown(
    '<div style="height:10px"></div>',
    unsafe_allow_html=True
)


# =========================================================
# CLEAR CHAT
# =========================================================

clear_col, _ = st.columns([1, 5])

with clear_col:
    if st.button("🗑️ Clear Chat", use_container_width=True):
        st.session_state.health_messages = []
        st.rerun()


# =========================================================
# CHAT HISTORY
# =========================================================

with st.container(border=True):

    if not st.session_state.health_messages:
        st.caption(
            "Start a conversation below or click one "
            "of the quick wellness prompts above."
        )

    for message in st.session_state.health_messages:

        with st.chat_message(
            message["role"],
            avatar="🩺" if message["role"] == "assistant" else "🧑"
        ):
            st.markdown(message["content"])


# =========================================================
# USER INPUT
# =========================================================

user_query = st.chat_input(
    "💬 Ask Aarogya-AI a health or wellness question..."
)

if prompt_clicked:
    user_query = prompt_clicked


# =========================================================
# AI RESPONSE
# =========================================================

if user_query:

    st.session_state.health_messages.append({
        "role": "user",
        "content": user_query
    })

    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_query)

    with st.chat_message("assistant", avatar="🩺"):

        with st.spinner("🧬 Aarogya-AI is thinking..."):

            try:
                response = get_chatbot_response(user_query)

                st.markdown(response)

            except Exception as e:
                response = (
                    "I'm unable to process your question right now. "
                    "Please check your API key configuration and try again."
                )

                st.error(response)
                print(f"Chatbot error: {e}")

    st.session_state.health_messages.append({
        "role": "assistant",
        "content": response
    })


# =========================================================
# SAFETY DISCLAIMER & FOOTER
# =========================================================

render_medical_disclaimer()