import os
import sys
import importlib.util
import streamlit as st

# =========================================================
# EXPLICIT ROOT PATH & Ui.py LOADER (pages/12_Emergency_Detection.py)
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
# GLOSSY PURPLE THEME & EMERGENCY ACCENT STYLES
# =========================================================

apply_glossy_purple_theme()

st.markdown("""
<style>
.purple-emg-head {
    font-size: 20px;
    font-weight: 800;
    color: #2E1065;
    letter-spacing: -0.3px;
    margin: 22px 0 12px 0;
}

.gloss-emg-numbers-panel {
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    padding: 24px 26px;
    margin-bottom: 20px;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.96) 0%, rgba(243, 232, 255, 0.80) 100%);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(216, 180, 254, 0.85);
    box-shadow:
        0 14px 30px rgba(109, 40, 217, 0.10),
        inset 0 1px 0 rgba(255, 255, 255, 0.98);
}

.gloss-helpline-card {
    background: linear-gradient(150deg, #FFFFFF 0%, #F3E8FF 100%);
    border: 1.5px solid rgba(192, 132, 252, 0.65);
    border-bottom: 4px solid #DC2626;
    border-radius: 18px;
    padding: 18px 16px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(109, 40, 217, 0.08);
    transition: transform 0.22s ease, box-shadow 0.22s ease;
}

.gloss-helpline-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 14px 28px rgba(126, 34, 206, 0.16);
}

.gloss-helpline-num {
    font-size: 28px;
    font-weight: 900;
    color: #B91C1C;
    letter-spacing: -0.4px;
}

.gloss-helpline-lbl {
    font-size: 12.5px;
    font-weight: 700;
    color: #2E1065;
    margin-top: 5px;
}

.gloss-urgent-alert {
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    padding: 24px 28px;
    margin: 16px 0;
    background: linear-gradient(150deg, #FFF1F2 0%, #FFE4E6 60%, #F3E8FF 100%);
    border: 2px solid #DC2626;
    box-shadow: 0 14px 32px rgba(220, 38, 38, 0.14);
}

.gloss-symp-badge {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 11px 15px;
    background: rgba(255, 255, 255, 0.95);
    border: 1px solid #FECDD3;
    border-left: 4px solid #DC2626;
    border-radius: 12px;
    font-size: 14px;
    font-weight: 700;
    color: #881337;
    margin-bottom: 8px;
}

.gloss-clear-banner {
    border-radius: 22px;
    padding: 26px 28px;
    margin: 16px 0;
    text-align: center;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.96) 0%, rgba(243, 232, 255, 0.84) 100%);
    border: 1.5px solid rgba(168, 85, 247, 0.65);
    box-shadow: 0 12px 26px rgba(109, 40, 217, 0.09);
}
</style>
""", unsafe_allow_html=True)

render_page_banner(
    symbol="🚨",
    title="Emergency Detection & Urgent Care Guide",
    subtitle="Identify symptoms that may require urgent medical attention. General awareness only — call 112 immediately for emergencies.",
    badge="🧬 Aarogya-AI Triage & Safety",
)


# =========================================================
# EMERGENCY NUMBERS — ALWAYS VISIBLE
# =========================================================

st.markdown('<div class="purple-emg-head anim-1">🩺 India Emergency Numbers — Always Available</div>', unsafe_allow_html=True)

st.markdown('<div class="gloss-emg-numbers-panel anim-1">', unsafe_allow_html=True)

nc1, nc2, nc3, nc4 = st.columns(4)

numbers = [
    ("112", "National Emergency"),
    ("108", "Ambulance Service"),
    ("102", "Government Ambulance"),
    ("1800-180-1104", "Health Helpline"),
]

for col, (num, label) in zip([nc1, nc2, nc3, nc4], numbers):
    with col:
        st.markdown(f"""
        <div class="gloss-helpline-card">
            <div class="gloss-helpline-num">{num}</div>
            <div class="gloss-helpline-lbl"><span class="med-float">🩺</span> {label}</div>
        </div>""", unsafe_allow_html=True)

st.markdown('</div>', unsafe_allow_html=True)


# =========================================================
# AWARENESS NOTICE
# =========================================================

render_gloss_card(
    title="Awareness Tool Only",
    body="This tool supports general symptom awareness and cannot diagnose an emergency or replace emergency medical services. If you or someone else is in immediate danger, call 112 right away.",
    symbol="🫀",
    anim_class="anim-2"
)


# =========================================================
# SYMPTOM SELECTION
# =========================================================

emergency_symptoms = [
    "Chest pain or pressure",
    "Severe difficulty breathing",
    "Sudden loss of consciousness",
    "Severe bleeding that does not stop",
    "Sudden weakness or numbness",
    "Sudden confusion or disorientation",
    "Seizure or convulsions",
    "Severe allergic reaction",
    "Thoughts of self-harm or suicide",
    "Sudden severe headache",
    "Signs of stroke (face drooping, arm weakness, speech difficulty)",
]

st.markdown('<div class="purple-emg-head anim-2">💊 Select Symptoms You Are Experiencing</div>', unsafe_allow_html=True)

with st.container(border=True):
    selected_symptoms = st.multiselect(
        "Select any symptoms you notice:",
        emergency_symptoms,
        label_visibility="collapsed",
        placeholder="Choose one or more symptoms from the list…"
    )

    check_clicked = st.button("🚨  Check Emergency Status", use_container_width=False, type="primary")

if check_clicked:
    if len(selected_symptoms) > 0:
        symptom_items = "".join(
            f'<div class="gloss-symp-badge"><span class="med-float">🚨</span><span>{s}</span></div>'
            for s in selected_symptoms
        )

        st.markdown(f"""
        <div class="gloss-urgent-alert anim-2">
            <div style="font-size:20px;font-weight:900;color:#B91C1C;margin-bottom:10px;">
                <span class="med-float">🚨</span> URGENT MEDICAL ATTENTION MAY BE REQUIRED
            </div>
            <div style="font-size:14.5px;color:#7F1D1D;line-height:1.65;margin-bottom:14px;">
                You have selected symptoms that can indicate a serious medical condition.
                <b>Please seek urgent professional medical assistance immediately.</b>
                Do not delay emergency care while using this application.
            </div>
            <div style="margin-bottom:10px;font-weight:800;font-size:14px;color:#881337;">
                Selected symptoms:
            </div>
            {symptom_items}
        </div>
        """, unsafe_allow_html=True)

        with st.container(border=True):
            st.markdown("**📞 Call Emergency Services NOW**")
            ec1, ec2 = st.columns(2)
            with ec1:
                st.markdown("""
                <div class="gloss-helpline-card">
                    <div class="gloss-helpline-num">112</div>
                    <div class="gloss-helpline-lbl">National Emergency</div>
                </div>""", unsafe_allow_html=True)
            with ec2:
                st.markdown("""
                <div class="gloss-helpline-card">
                    <div class="gloss-helpline-num">108</div>
                    <div class="gloss-helpline-lbl">Ambulance Service</div>
                </div>""", unsafe_allow_html=True)

        st.warning(
            "🛑 **Do not delay professional medical care while using this tool.** "
            "This application cannot diagnose an emergency condition."
        )

    else:
        st.markdown("""
        <div class="gloss-clear-banner anim-2">
            <div class="med-float" style="font-size:44px;margin-bottom:10px;">🧬</div>
            <div style="font-size:18px;font-weight:800;color:#2E1065;margin-bottom:6px;">No emergency symptoms selected</div>
            <div style="font-size:14px;color:#4C1D95;line-height:1.6;">
                No concerning symptoms were selected at this time.<br>
                If you develop severe or rapidly worsening symptoms, seek urgent medical help immediately.
            </div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# DISCLAIMER
# =========================================================

render_medical_disclaimer()