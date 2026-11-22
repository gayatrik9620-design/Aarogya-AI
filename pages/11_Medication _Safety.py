import os
import sys
import importlib.util
import streamlit as st

# =========================================================
# EXPLICIT ROOT PATH & Ui.py LOADER (pages/11_Medication _Safety.py)
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

# NOTE: st.set_page_config() is handled by app.py — NOT repeated here.

# =========================================================
# GLOSSY PURPLE THEME & PAGE STYLES
# =========================================================

apply_glossy_purple_theme()

st.markdown("""
<style>
.purple-med-head {
    font-size: 20px;
    font-weight: 800;
    color: #2E1065;
    letter-spacing: -0.3px;
    margin: 22px 0 12px 0;
}

.gloss-med-panel {
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    padding: 26px 28px;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.96) 0%, rgba(243, 232, 255, 0.80) 100%);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(216, 180, 254, 0.85);
    box-shadow:
        0 14px 32px rgba(109, 40, 217, 0.10),
        inset 0 1px 0 rgba(255, 255, 255, 0.98);
    margin: 18px 0;
}

.gloss-med-title {
    font-size: 21px;
    font-weight: 800;
    color: #2E1065;
    margin-bottom: 16px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.gloss-med-point {
    display: flex;
    align-items: flex-start;
    gap: 10px;
    padding: 12px 16px;
    background: linear-gradient(140deg, #FFFFFF 0%, #F3E8FF 100%);
    border: 1px solid rgba(192, 132, 252, 0.55);
    border-radius: 14px;
    font-size: 14px;
    font-weight: 600;
    color: #2E1065;
    margin-bottom: 10px;
    line-height: 1.55;
    box-shadow: 0 6px 14px rgba(109, 40, 217, 0.06);
}

.gloss-urgent-box {
    background: linear-gradient(145deg, #FFF1F2 0%, #FFE4E6 100%);
    border: 1px solid #FECDD3;
    border-left: 5px solid #DC2626;
    border-radius: 16px;
    padding: 16px 20px;
    margin: 14px 0;
    font-size: 13.5px;
    color: #881337;
    line-height: 1.6;
}

.gloss-consult-box {
    background: linear-gradient(145deg, rgba(250, 245, 255, 0.98), rgba(237, 233, 254, 0.88));
    border: 1px solid rgba(168, 85, 247, 0.55);
    border-left: 5px solid #6D28D9;
    border-radius: 16px;
    padding: 16px 20px;
    margin: 14px 0;
    font-size: 13.5px;
    color: #2E1065;
    line-height: 1.6;
}

.gloss-principle-card {
    position: relative;
    overflow: hidden;
    border-radius: 20px;
    padding: 20px 22px;
    background: linear-gradient(160deg, rgba(255, 255, 255, 0.95) 0%, rgba(243, 232, 255, 0.78) 100%);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(216, 180, 254, 0.80);
    box-shadow:
        0 10px 24px rgba(109, 40, 217, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.98);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    height: 100%;
}

.gloss-principle-card:hover {
    transform: translateY(-4px);
    border-color: #C084FC;
    box-shadow:
        0 16px 32px rgba(126, 34, 206, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 1);
}
</style>
""", unsafe_allow_html=True)

render_page_banner(
    symbol="💊",
    title="Medication Safety",
    subtitle="Educational medication awareness information designed to promote safe handling. Does not prescribe medicines or dosages.",
    badge="🧬 Aarogya-AI Medication Safety",
)


# =========================================================
# SAFETY DATA
# =========================================================

topics = {
    "💊 Taking Medicines Safely": {
        "icon": "💊",
        "points": [
            "Take medicines only as directed by a qualified healthcare professional.",
            "Read the medicine label and instructions carefully before taking.",
            "Do not share prescription medicines with other people.",
            "Keep medicines away from children and store them safely.",
            "Complete prescribed courses even if you feel better early."
        ]
    },
    "⚠️ Possible Side Effects": {
        "icon": "⚠️",
        "points": [
            "Some medicines can cause side effects — these vary by person and medicine.",
            "Read the information leaflet provided with your medicine carefully.",
            "If you notice unusual or severe symptoms, contact a healthcare professional.",
            "Do not stop a prescribed medicine suddenly without medical advice."
        ]
    },
    "🔗 Medicine Interactions": {
        "icon": "🔗",
        "points": [
            "Some medicines can interact with other medicines, foods or supplements.",
            "Tell your doctor or pharmacist about all medicines and supplements you take.",
            "Do not start or stop a prescribed medicine without professional advice.",
            "Herbal supplements can also interact with prescription medicines."
        ]
    },
    "🏠 Storage & Expiry": {
        "icon": "🏠",
        "points": [
            "Store medicines according to the instructions on the label.",
            "Keep medicines in a safe, dry place away from heat and moisture.",
            "Check the expiry date before using any medicine.",
            "Keep all medicines out of reach of children.",
            "Dispose of expired medicines safely — do not flush down drains."
        ]
    },
    "📋 Missed Dose": {
        "icon": "📋",
        "points": [
            "Follow the instructions provided with your medicine for missed doses.",
            "Do not automatically take a double dose to make up for a missed one.",
            "If you are unsure what to do, ask your doctor or pharmacist.",
            "Set reminders to help you maintain a consistent medication schedule."
        ]
    },
    "🏥 Emergency Situations": {
        "icon": "🏥",
        "points": [
            "If you suspect a medicine overdose, seek immediate medical attention.",
            "In India, call 112 (Emergency) or 108 (Ambulance) for urgent help.",
            "Keep packaging and medicine name available for emergency responders.",
            "Do not induce vomiting unless specifically directed by a medical professional."
        ]
    },
}


# =========================================================
# TOPIC SELECTION
# =========================================================

st.markdown('<div class="purple-med-head anim-1">🩺 Choose a Safety Topic</div>', unsafe_allow_html=True)

with st.container(border=True):
    selected_topic = st.selectbox(
        "Choose a topic:",
        list(topics.keys()),
        label_visibility="collapsed"
    )

    if st.button("🔍  Show Safety Information", use_container_width=False, type="primary"):
        st.session_state["med_topic"] = selected_topic

if "med_topic" in st.session_state and st.session_state["med_topic"] in topics:
    topic_key = st.session_state["med_topic"]
    topic = topics[topic_key]

    points_html = "".join(
        f'<div class="gloss-med-point"><span class="med-float">🩺</span><span>{p}</span></div>'
        for p in topic["points"]
    )

    st.markdown(f"""
    <div class="gloss-med-panel anim-2">
        <div class="gloss-med-title">
            <span class="med-float">{topic["icon"]}</span>
            <span>{topic_key.split(' ', 1)[-1]}</span>
        </div>
        {points_html}
        <div class="gloss-urgent-box">
            <strong>🚨 Important:</strong>
            If you experience a serious or unexpected reaction after taking a medicine,
            seek urgent medical help immediately. Call <b>112</b> (Emergency) or <b>108</b> (Ambulance) in India.
        </div>
        <div class="gloss-consult-box">
            <strong>🩺 Always Consult a Professional:</strong>
            For any personal medication questions, dosage concerns, or health decisions,
            please consult a qualified doctor or licensed pharmacist.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# ALWAYS VISIBLE IMPORTANT NOTES
# =========================================================

st.markdown('<div class="purple-med-head anim-2">🧬 Important Safety Principles</div>', unsafe_allow_html=True)

ic1, ic2, ic3 = st.columns(3)

safety_cards = [
    ("💊", "Medication Awareness", "Always follow professional medical guidance when using any medicine.", "anim-1"),
    ("🩺", "Know Your Medicine", "Understand what you are taking — read labels and ask questions.", "anim-2"),
    ("🫀", "Consult a Professional", "A doctor or pharmacist is your best resource for medication questions.", "anim-3"),
]

for col, (icon, title, desc, anim_cls) in zip([ic1, ic2, ic3], safety_cards):
    with col:
        st.markdown(f"""
        <div class="gloss-principle-card {anim_cls}">
            <span class="ui-icon-chip med-float">{icon}</span>
            <div style="font-size:15.5px;font-weight:800;color:#2E1065;margin:10px 0 6px 0;">{title}</div>
            <div style="font-size:13.5px;font-weight:500;color:#3B0764;line-height:1.55;">{desc}</div>
        </div>""", unsafe_allow_html=True)


# =========================================================
# SAFETY NOTICE
# =========================================================

render_medical_disclaimer()