import os
import sys
import sqlite3
import importlib.util
from pathlib import Path
import pandas as pd
import streamlit as st

# =========================================================
# EXPLICIT ROOT PATH & Ui.py LOADER (pages/10_Health_Recommendations.py)
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
.purple-rec-head {
    font-size: 20px;
    font-weight: 800;
    color: #2E1065;
    letter-spacing: -0.3px;
    margin: 24px 0 10px 0;
}

.purple-rec-sub {
    font-size: 13.5px;
    font-weight: 500;
    color: #5B21B6;
    margin-bottom: 14px;
}

.gloss-insight-card {
    position: relative;
    overflow: hidden;
    border-radius: 18px;
    padding: 16px 20px;
    margin: 10px 0;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.96) 0%, rgba(243, 232, 255, 0.80) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(216, 180, 254, 0.82);
    border-left: 5px solid #7E22CE;
    box-shadow: 0 8px 20px rgba(109, 40, 217, 0.07);
    color: #2E1065;
}

.gloss-rec-tile {
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    padding: 22px 24px;
    background: linear-gradient(160deg, rgba(255, 255, 255, 0.95) 0%, rgba(243, 232, 255, 0.78) 100%);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(216, 180, 254, 0.80);
    box-shadow:
        0 12px 26px rgba(109, 40, 217, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.98);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    height: 100%;
    margin-bottom: 12px;
}

.gloss-rec-tile:hover {
    transform: translateY(-4px);
    border-color: #C084FC;
    box-shadow:
        0 18px 34px rgba(126, 34, 206, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 1);
}

.gloss-rec-title {
    font-size: 16.5px;
    font-weight: 800;
    color: #2E1065;
    margin: 10px 0 6px 0;
}

.gloss-rec-desc {
    font-size: 13.5px;
    color: #3B0764;
    line-height: 1.6;
    margin-bottom: 12px;
}

.gloss-rec-tip {
    background: linear-gradient(140deg, #FFFFFF 0%, #EDE9FE 100%);
    border: 1px solid rgba(192, 132, 252, 0.55);
    border-radius: 12px;
    padding: 10px 14px;
    font-size: 12.5px;
    font-weight: 700;
    color: #4C1D95;
    line-height: 1.5;
}
</style>
""", unsafe_allow_html=True)

render_page_banner(
    symbol="💊",
    title="Personalized Health Recommendations",
    subtitle="Actionable wellness suggestions tailored to your recorded health habits and daily routines.",
    badge="🧬 Aarogya-AI Care Guidance",
)


# =========================================================
# DATABASE
# =========================================================

DB_PATH = str(ROOT_DIR / "health_data.db")


@st.cache_data(ttl=60)
def _load_rec_data(db_path: str):
    conn = None
    try:
        conn = sqlite3.connect(db_path)
        conn.execute("""
        CREATE TABLE IF NOT EXISTS health_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            weight REAL,
            steps INTEGER,
            sleep REAL
        )
        """)
        conn.commit()
        loaded_df = pd.read_sql_query(
            "SELECT date, weight, steps, sleep FROM health_data ORDER BY date DESC, id DESC",
            conn
        )
        return loaded_df
    except Exception:
        return pd.DataFrame()
    finally:
        if conn is not None:
            conn.close()


df = _load_rec_data(DB_PATH)


# =========================================================
# DATA-DRIVEN INSIGHTS
# =========================================================

if not df.empty:
    clean_df = df.copy()
    clean_df["parsed_date"] = pd.to_datetime(clean_df["date"], errors="coerce")
    for col, default_val in (("weight", 0.0), ("steps", 0), ("sleep", 0.0)):
        if col not in clean_df.columns:
            clean_df[col] = default_val
        clean_df[col] = pd.to_numeric(clean_df[col], errors="coerce").fillna(default_val)

    clean_df = clean_df.sort_values(
        by=["parsed_date"],
        ascending=False,
        na_position="last"
    ).reset_index(drop=True)

    latest = clean_df.iloc[0]
    steps_val = float(latest["steps"])
    sleep_val = float(latest["sleep"])

    if steps_val < 3000:
        activity_msg = "Your recorded activity is low. Try adding short walks throughout your day."
        activity_accent = "#9333EA"
    elif steps_val < 7000:
        activity_msg = "Your activity level can be improved. Try adding more walking during the day."
        activity_accent = "#7E22CE"
    else:
        activity_msg = "Your recorded daily activity looks great. Continue maintaining regular movement!"
        activity_accent = "#6D28D9"

    if sleep_val < 6:
        sleep_msg = "Your sleep is below recommended levels. Try to maintain a regular sleep schedule."
        sleep_accent = "#9333EA"
    elif sleep_val < 7:
        sleep_msg = "You may benefit from getting a little more sleep each night."
        sleep_accent = "#7E22CE"
    else:
        sleep_msg = "Your recorded sleep duration looks reasonable. Keep up the healthy sleep habit!"
        sleep_accent = "#6D28D9"

    def gloss_insight(icon, title, msg, accent="#7E22CE", anim="anim-2"):
        return f"""
        <div class="gloss-insight-card {anim}" style="border-left-color:{accent};">
            <div style="font-size:14.5px;font-weight:800;color:#2E1065;margin-bottom:4px;">
                <span class="med-float">{icon}</span> {title}
            </div>
            <div style="font-size:13.5px;color:#3B0764;line-height:1.55;">{msg}</div>
        </div>"""

    st.markdown('<div class="purple-rec-head anim-1">🩺 Your Personalized Insights</div>', unsafe_allow_html=True)
    st.markdown(
        gloss_insight("🩺", "Activity:", activity_msg, activity_accent, "anim-1") +
        gloss_insight("💤", "Sleep:", sleep_msg, sleep_accent, "anim-2") +
        gloss_insight("⚖️", "Weight:", "Continue monitoring your weight regularly and focus on balanced nutrition.", "#6D28D9", "anim-3"),
        unsafe_allow_html=True
    )
else:
    render_gloss_card(
        title="No Health Data Found Yet",
        body="Add your health data from the Health Data page to unlock personalized activity and sleep insights.",
        symbol="🫀",
        anim_class="anim-2"
    )


# =========================================================
# GENERAL RECOMMENDATION CARDS
# =========================================================

st.markdown('<div class="purple-rec-head anim-2">🧬 General Wellness Recommendations</div>', unsafe_allow_html=True)
st.markdown('<div class="purple-rec-sub anim-2">These are general educational wellness suggestions, not personalized medical advice.</div>', unsafe_allow_html=True)

recommendations = [
    {
        "icon": "💧",
        "title": "Hydration",
        "desc": "Staying well-hydrated supports energy levels, cognitive function and overall body performance.",
        "tip": "💡 Try drinking a glass of water first thing in the morning and keep a water bottle with you throughout the day."
    },
    {
        "icon": "🥗",
        "title": "Nutrition",
        "desc": "A balanced diet rich in vegetables, fruits, whole grains and lean proteins supports overall wellness.",
        "tip": "💡 Focus on adding more colorful vegetables to your meals. Variety in your diet helps ensure diverse nutrient intake."
    },
    {
        "icon": "🩺",
        "title": "Physical Activity",
        "desc": "Regular physical movement supports cardiovascular health, mood and energy throughout the day.",
        "tip": "💡 Aim for short, consistent activity sessions. Even 10-minute walks throughout the day add up significantly."
    },
    {
        "icon": "💤",
        "title": "Sleep Quality",
        "desc": "Quality sleep is essential for physical recovery, mental clarity and emotional wellbeing.",
        "tip": "💡 Try maintaining a consistent sleep schedule and create a relaxing pre-bed routine to improve sleep quality."
    },
    {
        "icon": "🫀",
        "title": "Stress & Relaxation",
        "desc": "Managing stress through mindfulness, breathing exercises or relaxing activities supports mental wellness.",
        "tip": "💡 Try a 5-minute breathing exercise: inhale for 4 counts, hold for 4, exhale for 6. Repeat 3–5 times."
    },
    {
        "icon": "💊",
        "title": "Healthy Habits",
        "desc": "Small consistent habits — regular sleep, movement, hydration and social connection — compound into major wellness gains.",
        "tip": "💡 Choose one small healthy habit to focus on this week and build from there."
    },
]

rc1, rc2, rc3 = st.columns(3)

for i, rec in enumerate(recommendations):
    col = [rc1, rc2, rc3][i % 3]
    anim_cls = f"anim-{(i % 4) + 1}"
    with col:
        st.markdown(f"""
        <div class="gloss-rec-tile {anim_cls}">
            <span class="ui-icon-chip med-float">{rec['icon']}</span>
            <div class="gloss-rec-title">{rec['title']}</div>
            <div class="gloss-rec-desc">{rec['desc']}</div>
            <div class="gloss-rec-tip">{rec['tip']}</div>
        </div>
        """, unsafe_allow_html=True)
    if i == 2:
        st.markdown('<div style="height:14px"></div>', unsafe_allow_html=True)
        rc1, rc2, rc3 = st.columns(3)


# =========================================================
# SAFETY
# =========================================================

render_medical_disclaimer()