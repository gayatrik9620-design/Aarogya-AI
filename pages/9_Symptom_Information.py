import os
import sys
import html
import importlib.util
from pathlib import Path
import streamlit as st

# =========================================================
# EXPLICIT ROOT PATH & Ui.py LOADER (pages/9_Symptom_Information.py)
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
.purple-symp-head {
    font-size: 20px;
    font-weight: 800;
    color: #2E1065;
    letter-spacing: -0.3px;
    margin: 22px 0 12px 0;
}

.gloss-symptom-panel {
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

.gloss-symptom-title {
    font-size: 22px;
    font-weight: 800;
    color: #2E1065;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.gloss-symptom-desc {
    font-size: 14.5px;
    color: #3B0764;
    line-height: 1.65;
    margin-bottom: 18px;
}

.gloss-tips-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
    gap: 12px;
    margin-top: 10px;
}

.gloss-tip-pill {
    background: linear-gradient(145deg, #FFFFFF 0%, #F3E8FF 100%);
    border: 1px solid rgba(192, 132, 252, 0.55);
    border-radius: 14px;
    padding: 13px 16px;
    font-size: 13.5px;
    font-weight: 600;
    color: #2E1065;
    display: flex;
    align-items: flex-start;
    gap: 8px;
    line-height: 1.5;
    box-shadow: 0 6px 14px rgba(109, 40, 217, 0.06);
}

.gloss-seek-box {
    background: linear-gradient(145deg, rgba(250, 245, 255, 0.98), rgba(237, 233, 254, 0.88));
    border: 1px solid rgba(168, 85, 247, 0.55);
    border-left: 5px solid #7E22CE;
    border-radius: 16px;
    padding: 16px 20px;
    margin-top: 18px;
    font-size: 13.5px;
    color: #2E1065;
    line-height: 1.6;
}

.gloss-emergency-box {
    background: linear-gradient(145deg, #FFF1F2 0%, #FFE4E6 100%);
    border: 1px solid #FECDD3;
    border-left: 5px solid #DC2626;
    border-radius: 16px;
    padding: 16px 20px;
    margin-top: 14px;
    font-size: 13.5px;
    color: #881337;
    line-height: 1.6;
}
</style>
""", unsafe_allow_html=True)

render_page_banner(
    symbol="🩺",
    title="Symptom Information",
    subtitle="Educational health awareness for common symptoms, self-care habits, and red-flag warning signs.",
    badge="🧬 Aarogya-AI Clinical Reference",
)


# =========================================================
# SYMPTOM DATA
# =========================================================

symptoms = {
    "🤕 Headache": {
        "emoji": "🤕",
        "info": "Headache can be related to stress, lack of sleep, dehydration, poor posture, eye strain or other factors. Most headaches are tension-type and resolve with rest.",
        "tips": [
            "Get adequate rest and sleep",
            "Stay well hydrated",
            "Take regular breaks from screens",
            "Practice relaxation techniques",
            "Monitor if headache keeps returning"
        ],
        "seek_help": "Consult a healthcare professional if headaches are frequent, severe, sudden-onset, or accompanied by fever, vision changes or stiff neck.",
    },
    "🌡️ Fever": {
        "emoji": "🌡️",
        "info": "Fever is the body's natural response to infections or other conditions. A raised body temperature often indicates the immune system is responding to something.",
        "tips": [
            "Take adequate rest",
            "Stay well hydrated",
            "Monitor body temperature",
            "Wear light clothing",
            "Seek advice if fever is high or persists"
        ],
        "seek_help": "Seek medical attention if fever is very high (above 39.5°C), lasts more than a few days, or is accompanied by severe symptoms.",
    },
    "😷 Cough": {
        "emoji": "😷",
        "info": "Cough can occur due to infections, allergies, environmental irritants or other causes. Acute coughs are usually short-term while chronic coughs last longer.",
        "tips": [
            "Stay well hydrated",
            "Avoid smoke and irritants",
            "Rest your voice",
            "Use a humidifier if air is dry",
            "See a doctor if cough persists"
        ],
        "seek_help": "Seek medical advice if cough persists for more than 3 weeks, produces blood, or is accompanied by difficulty breathing or chest pain.",
    },
    "🤢 Stomach Pain": {
        "emoji": "🤢",
        "info": "Stomach pain can have many possible causes including digestive problems, gas, food intolerance, infections or stress.",
        "tips": [
            "Stay hydrated",
            "Eat light, easily digestible foods",
            "Note foods that trigger discomfort",
            "Eat regular balanced meals",
            "Avoid very spicy or fatty foods temporarily"
        ],
        "seek_help": "Seek medical advice if pain is severe, persistent, accompanied by vomiting blood, or you experience sudden sharp pain.",
    },
    "😔 Fatigue": {
        "emoji": "😔",
        "info": "Fatigue can be related to poor sleep, stress, lifestyle factors, nutritional deficiencies or other underlying conditions.",
        "tips": [
            "Maintain regular sleep schedule",
            "Eat balanced, nutrient-rich meals",
            "Stay hydrated",
            "Reduce excessive caffeine",
            "Get regular light physical activity"
        ],
        "seek_help": "Consult a healthcare professional if fatigue is persistent, significantly affects daily life, or is accompanied by other unexplained symptoms.",
    },
    "😤 Breathing Difficulty": {
        "emoji": "😤",
        "info": "Breathing difficulty can range from mild (due to anxiety or physical exertion) to severe (requiring immediate medical attention).",
        "tips": [
            "Sit upright in a comfortable position",
            "Breathe slowly and calmly",
            "Avoid triggers if known (dust, smoke)",
            "Note when symptoms started and severity"
        ],
        "seek_help": "⚠️ Seek IMMEDIATE medical attention if breathing difficulty is sudden, severe, or accompanied by chest pain, blue lips or confusion. Call 112.",
    },
}


# =========================================================
# SELECTION
# =========================================================

st.markdown('<div class="purple-symp-head anim-1">🔍 Select a Symptom</div>', unsafe_allow_html=True)

with st.container(border=True):
    selected = st.selectbox(
        "Select a symptom to learn about:",
        list(symptoms.keys()),
        label_visibility="collapsed"
    )

    if st.button("📖  Get Symptom Information", use_container_width=False, type="primary"):
        st.session_state["show_symptom"] = selected

if "show_symptom" in st.session_state and st.session_state["show_symptom"] in symptoms:
    sel = st.session_state["show_symptom"]
    data = symptoms[sel]
    safe_title = html.escape(sel.split(" ", 1)[-1])
    safe_info = html.escape(data["info"])
    safe_seek_help = html.escape(data["seek_help"])
    tips_html = "".join(
        f'<div class="gloss-tip-pill"><span>🩺</span><span>{html.escape(tip)}</span></div>'
        for tip in data["tips"]
    )

    st.markdown(f"""
    <div class="gloss-symptom-panel anim-2">
        <div class="gloss-symptom-title">
            <span class="med-float">{data['emoji']}</span>
            <span>{safe_title}</span>
        </div>
        <div class="gloss-symptom-desc">{safe_info}</div>
        <div style="font-size:15px;font-weight:800;color:#2E1065;margin-bottom:8px;">
            💊 General Wellness Tips
        </div>
        <div class="gloss-tips-grid">
            {tips_html}
        </div>
        <div class="gloss-seek-box">
            <strong>🩺 When to Seek Professional Help:</strong><br>
            {safe_seek_help}
        </div>
        <div class="gloss-emergency-box">
            <strong>🚨 Emergency Reminder:</strong>
            If you experience severe or life-threatening symptoms, seek immediate professional medical assistance.
            In India, call <b>112</b> (Emergency) or <b>108</b> (Ambulance).
        </div>
    </div>
    """, unsafe_allow_html=True)

render_medical_disclaimer()