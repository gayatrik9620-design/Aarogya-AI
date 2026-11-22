import os
import sys
import importlib.util
from pathlib import Path
import streamlit as st

# =========================================================
# EXPLICIT ROOT PATH & Ui.py LOADER (pages/8_Risk_Assesment.py)
# =========================================================

_auto_root = Path(__file__).resolve().parents[1]
_local_root = Path(r"C:\Users\nehab\aarogya-ai")

if (_auto_root / "Ui.py").is_file() or (_auto_root / "ui.py").is_file():
    ROOT_DIR = _auto_root
elif (_local_root / "Ui.py").is_file() or (_local_root / "ui.py").is_file():
    ROOT_DIR = _local_root
else:
    ROOT_DIR = _auto_root

if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

_ui_loaded = False
for _candidate in ("Ui.py", "ui.py"):
    _ui_path = ROOT_DIR / _candidate
    if _ui_path.is_file():
        try:
            _spec = importlib.util.spec_from_file_location("Ui", str(_ui_path))
            if _spec is None or _spec.loader is None:
                raise ImportError("Unable to create UI module loader.")
            _ui_mod = importlib.util.module_from_spec(_spec)
            _spec.loader.exec_module(_ui_mod)
            apply_glossy_purple_theme = _ui_mod.apply_glossy_purple_theme
            render_page_banner = _ui_mod.render_page_banner
            render_gloss_card = _ui_mod.render_gloss_card
            render_medical_disclaimer = _ui_mod.render_medical_disclaimer
            _ui_loaded = True
            break
        except Exception as e:
            st.error(f"Error loading Ui.py: {e}")
            st.stop()

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
.purple-risk-head {
    font-size: 20px;
    font-weight: 800;
    color: #2E1065;
    letter-spacing: -0.3px;
    margin: 22px 0 12px 0;
}

.gloss-risk-banner {
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    padding: 22px 26px;
    margin: 12px 0 18px 0;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.96) 0%, rgba(243, 232, 255, 0.82) 100%);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(216, 180, 254, 0.85);
    border-left: 6px solid #7E22CE;
    box-shadow:
        0 12px 28px rgba(109, 40, 217, 0.10),
        inset 0 1px 0 rgba(255, 255, 255, 0.98);
    color: #1E1035;
}

.gloss-risk-tier {
    font-size: 20px;
    font-weight: 800;
    color: #2E1065;
    margin-bottom: 6px;
}

.gloss-risk-desc {
    font-size: 14px;
    line-height: 1.6;
    color: #3B0764;
    margin: 0;
}

.gloss-warning-item {
    border-radius: 16px;
    padding: 13px 18px;
    margin: 8px 0;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.94) 0%, rgba(243, 232, 255, 0.78) 100%);
    border: 1px solid rgba(216, 180, 254, 0.78);
    border-left: 4px solid #6D28D9;
    color: #2E1065;
    font-size: 14px;
    font-weight: 600;
}
</style>
""", unsafe_allow_html=True)

render_page_banner(
    symbol="🫀",
    title="Health Risk Assessment",
    subtitle="Evaluate lifestyle and wellness risk indicators from your daily habits. For general wellness information only.",
    badge="🧬 Aarogya-AI Risk Screening",
)

render_gloss_card(
    title="Wellness Screening Scope",
    body="This tool provides a general wellness risk check based on sleep, activity steps, hydration, and stress inputs. It does not provide a medical diagnosis.",
    symbol="🩺",
    anim_class="anim-2"
)

# =========================================================
# INPUT FORM
# =========================================================

st.markdown('<div class="purple-risk-head anim-1">📋 Enter Your Information</div>', unsafe_allow_html=True)

with st.container(border=True):
    c1, c2 = st.columns(2)

    with c1:
        age = st.number_input(
            "🧬 Age",
            min_value=1,
            max_value=120,
            value=20,
            step=1
        )

        sleep = st.number_input(
            "💤 Average sleep per day (hours)",
            min_value=0.0,
            max_value=24.0,
            value=7.0,
            step=0.5
        )

        steps = st.number_input(
            "🩺 Average daily steps",
            min_value=0,
            max_value=100000,
            value=5000,
            step=100
        )

    with c2:
        water = st.number_input(
            "💧 Approximate water intake (litres/day)",
            min_value=0.0,
            max_value=10.0,
            value=2.0,
            step=0.5
        )

        stress = st.slider(
            "💊 Stress level (1 = Low, 10 = High)",
            min_value=1,
            max_value=10,
            value=5
        )

    assess_clicked = st.button("🔍 Assess My Wellness Risk", use_container_width=True)

# =========================================================
# ASSESSMENT LOGIC & RESULTS
# =========================================================

if assess_clicked:
    risk_score = 0
    warnings = []

    # Sleep assessment
    if sleep < 6:
        risk_score += 2
        warnings.append("Your average sleep is quite low.")
    elif sleep < 7:
        risk_score += 1
        warnings.append("You may benefit from getting more sleep.")

    # Physical activity
    if steps < 3000:
        risk_score += 2
        warnings.append("Your daily activity level appears low.")
    elif steps < 5000:
        risk_score += 1
        warnings.append("Try to gradually increase your daily activity.")

    # Hydration
    if water < 1.5:
        risk_score += 2
        warnings.append("Your reported water intake is relatively low.")

    # Stress
    if stress >= 8:
        risk_score += 2
        warnings.append("Your reported stress level is high.")
    elif stress >= 6:
        risk_score += 1
        warnings.append("Your reported stress level is moderately high.")

    st.markdown('<div class="purple-risk-head anim-2">🫀 Assessment Result</div>', unsafe_allow_html=True)

    if risk_score <= 2:
        tier_label = "🟢 Lower Wellness Risk"
        tier_desc = (
            f"At age {int(age)}, your entered lifestyle habits show few wellness risk indicators "
            f"(Wellness Risk Index: {risk_score}/8)."
        )
    elif risk_score <= 5:
        tier_label = "🟡 Moderate Wellness Risk"
        tier_desc = (
            f"At age {int(age)}, some daily habits may need attention "
            f"(Wellness Risk Index: {risk_score}/8). Consider reviewing sleep, steps, hydration, or stress."
        )
    else:
        tier_label = "🔴 Higher Wellness Risk"
        tier_desc = (
            f"At age {int(age)}, several wellness indicators warrant closer attention "
            f"(Wellness Risk Index: {risk_score}/8). Consider speaking with a qualified healthcare professional."
        )

    st.markdown(f"""
    <div class="gloss-risk-banner anim-2">
        <div class="gloss-risk-tier"><span class="med-float">🩺</span> {tier_label}</div>
        <p class="gloss-risk-desc">{tier_desc}</p>
    </div>
    """, unsafe_allow_html=True)

    if warnings:
        st.markdown('<div class="purple-risk-head anim-3">💊 Areas to Pay Attention To</div>', unsafe_allow_html=True)
        for warning in warnings:
            st.markdown(f"""
            <div class="gloss-warning-item anim-3">
                <span class="med-float">🩺</span> {warning}
            </div>
            """, unsafe_allow_html=True)
    else:
        render_gloss_card(
            title="Balanced Daily Indicators",
            body="No major wellness warning indicators were detected from the values you entered.",
            symbol="🧬",
            anim_class="anim-3"
        )

render_medical_disclaimer()