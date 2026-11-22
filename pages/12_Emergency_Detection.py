import sys
import importlib.util
from pathlib import Path
import streamlit as st

# =========================================================
# PROJECT ROOT & UI LOADER
# =========================================================

ROOT_DIR = Path(r"C:\Users\nehab\aarogya-ai")

if not ROOT_DIR.is_dir():
    st.error(f"Project folder not found: {ROOT_DIR}")
    st.stop()

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

ui_path = None

for filename in ("Ui.py", "ui.py"):
    candidate = ROOT_DIR / filename
    if candidate.is_file():
        ui_path = candidate
        break

if ui_path is None:
    st.error(f"Could not find Ui.py in: {ROOT_DIR}")
    st.stop()

try:
    spec = importlib.util.spec_from_file_location("Ui", str(ui_path))

    if spec is None or spec.loader is None:
        raise ImportError("Unable to load Ui.py")

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

# NOTE: st.set_page_config() is handled by app.py.


# =========================================================
# GLOSSY PURPLE THEME & EMERGENCY STYLES
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
    background: linear-gradient(
        155deg,
        rgba(255,255,255,0.96) 0%,
        rgba(243,232,255,0.80) 100%
    );
    border: 1px solid rgba(216,180,254,0.85);
    box-shadow: 0 14px 30px rgba(109,40,217,0.10);
}

.gloss-helpline-card {
    background: linear-gradient(
        150deg,
        #FFFFFF 0%,
        #F3E8FF 100%
    );
    border: 1.5px solid rgba(192,132,252,0.65);
    border-bottom: 4px solid #DC2626;
    border-radius: 18px;
    padding: 18px 16px;
    text-align: center;
    box-shadow: 0 8px 20px rgba(109,40,217,0.08);
    transition: transform 0.22s ease;
}

.gloss-helpline-card:hover {
    transform: translateY(-4px);
}

.gloss-helpline-num {
    font-size: 28px;
    font-weight: 900;
    color: #B91C1C;
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
    background: linear-gradient(
        150deg,
        #FFF1F2 0%,
        #FFE4E6 60%,
        #F3E8FF 100%
    );
    border: 2px solid #DC2626;
    box-shadow: 0 14px 32px rgba(220,38,38,0.14);
}

.gloss-symp-badge {
    display: flex;
    align-items: center;
    gap: 10px;
    padding: 11px 15px;
    background: rgba(255,255,255,0.95);
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
    background: linear-gradient(
        155deg,
        rgba(255,255,255,0.96) 0%,
        rgba(243,232,255,0.84) 100%
    );
    border: 1.5px solid rgba(168,85,247,0.65);
    box-shadow: 0 12px 26px rgba(109,40,217,0.09);
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HEADER
# =========================================================

render_page_banner(
    symbol="🚨",
    title="Emergency Detection & Urgent Care Guide",
    subtitle=(
        "Learn about symptoms that may require urgent medical "
        "attention. General awareness only — call 112 in emergencies."
    ),
    badge="🧬 Aarogya-AI Triage & Safety",
)


# =========================================================
# EMERGENCY NUMBERS
# =========================================================

st.markdown(
    '<div class="purple-emg-head">🩺 India Emergency Numbers</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="gloss-emg-numbers-panel">',
    unsafe_allow_html=True
)

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
    <div class="gloss-helpline-lbl">🩺 {label}</div>
</div>
""", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)


# =========================================================
# AWARENESS NOTICE
# =========================================================

render_gloss_card(
    title="Awareness Tool Only",
    body=(
        "This tool supports general symptom awareness. "
        "It cannot diagnose an emergency or replace emergency "
        "medical services. If someone is in immediate danger, "
        "call 112 right away."
    ),
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
    "Sudden severe headache",
    "Signs of stroke (face drooping, arm weakness, speech difficulty)",
]

st.markdown(
    '<div class="purple-emg-head">💊 Select Symptoms</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    selected_symptoms = st.multiselect(
        "Select any symptoms you notice:",
        emergency_symptoms,
        label_visibility="collapsed",
        placeholder="Choose one or more symptoms..."
    )

    check_clicked = st.button(
        "🚨 Check Emergency Status",
        use_container_width=True,
        type="primary"
    )


# =========================================================
# EMERGENCY STATUS
# =========================================================

if check_clicked:

    if selected_symptoms:

        symptom_items = "".join(
            f'<div class="gloss-symp-badge">🚨 {s}</div>'
            for s in selected_symptoms
        )

        # HTML starts at column zero to prevent Markdown code blocks.
        alert_html = f"""<div class="gloss-urgent-alert">
<div style="
    font-size:20px;
    font-weight:900;
    color:#B91C1C;
    margin-bottom:10px;
">
    🚨 URGENT MEDICAL ATTENTION MAY BE REQUIRED
</div>

<div style="
    font-size:14.5px;
    color:#7F1D1D;
    line-height:1.65;
    margin-bottom:14px;
">
    The selected symptoms may indicate a serious
    medical condition. Please seek urgent professional
    medical assistance immediately.
    Do not delay emergency care while using this app.
</div>

<div style="
    margin-bottom:10px;
    font-weight:800;
    color:#881337;
">
    Selected symptoms:
</div>

{symptom_items}
</div>"""

        st.markdown(alert_html, unsafe_allow_html=True)

        with st.container(border=True):

            st.markdown("**📞 Emergency Services**")

            ec1, ec2 = st.columns(2)

            with ec1:
                st.markdown("""
<div class="gloss-helpline-card">
    <div class="gloss-helpline-num">112</div>
    <div class="gloss-helpline-lbl">
        National Emergency
    </div>
</div>
""", unsafe_allow_html=True)

            with ec2:
                st.markdown("""
<div class="gloss-helpline-card">
    <div class="gloss-helpline-num">108</div>
    <div class="gloss-helpline-lbl">
        Ambulance Service
    </div>
</div>
""", unsafe_allow_html=True)

        st.warning(
            "Do not delay professional medical care. "
            "This application cannot diagnose emergency conditions."
        )

    else:

        st.markdown("""
<div class="gloss-clear-banner">
    <div style="font-size:44px;margin-bottom:10px;">
        🧬
    </div>

    <div style="
        font-size:18px;
        font-weight:800;
        color:#2E1065;
        margin-bottom:6px;
    ">
        No symptoms selected
    </div>

    <div style="
        font-size:14px;
        color:#4C1D95;
        line-height:1.6;
    ">
        No symptoms were selected.
        If severe or rapidly worsening symptoms develop,
        seek urgent medical help immediately.
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# MEDICAL DISCLAIMER
# =========================================================

render_medical_disclaimer()