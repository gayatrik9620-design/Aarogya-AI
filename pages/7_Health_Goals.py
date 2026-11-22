import os
import sys
import sqlite3
import importlib.util
import pandas as pd
import streamlit as st

# =========================================================
# EXPLICIT ROOT PATH & Ui.py LOADER (pages/7_Health_Goals.py)
# =========================================================

_auto_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_local_root = r"C:\Users\nehab\aarogya-ai"

if any(os.path.isfile(os.path.join(_auto_root, c)) for c in ("Ui.py", "ui.py")):
    ROOT_DIR = _auto_root
elif any(os.path.isfile(os.path.join(_local_root, c)) for c in ("Ui.py", "ui.py")):
    ROOT_DIR = _local_root
else:
    ROOT_DIR = _auto_root

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

_ui_loaded = False
for _candidate in ("Ui.py", "ui.py"):
    _ui_path = os.path.join(ROOT_DIR, _candidate)
    if os.path.isfile(_ui_path):
        try:
            _spec = importlib.util.spec_from_file_location("Ui", _ui_path)
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
.purple-goals-title {
    font-size: 20px;
    font-weight: 800;
    color: #2E1065;
    letter-spacing: -0.3px;
    margin: 24px 0 12px 0;
}

.gloss-goal-card {
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
    margin-bottom: 10px;
}

.gloss-goal-card:hover {
    transform: translateY(-4px);
    border-color: #C084FC;
    box-shadow:
        0 18px 34px rgba(126, 34, 206, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 1);
}

.gloss-goal-label {
    font-size: 12px;
    font-weight: 700;
    color: #6D28D9;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 6px;
}

.gloss-goal-val {
    font-size: 28px;
    font-weight: 800;
    color: #1E1035;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}

.gloss-goal-target {
    font-size: 13px;
    font-weight: 600;
    color: #5B21B6;
    margin-bottom: 8px;
}

.gloss-goal-pct {
    font-size: 14px;
    font-weight: 800;
    color: #7E22CE;
}

.gloss-status-pill {
    border-radius: 16px;
    padding: 15px 20px;
    margin: 10px 0;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.95) 0%, rgba(243, 232, 255, 0.80) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(216, 180, 254, 0.80);
    border-left: 5px solid #7E22CE;
    color: #2E1065;
    font-size: 14px;
    line-height: 1.55;
    box-shadow: 0 8px 20px rgba(109, 40, 217, 0.07);
}

.gloss-motivation-banner {
    position: relative;
    overflow: hidden;
    border-radius: 24px;
    padding: 26px 30px;
    background: linear-gradient(130deg, #2E1065 0%, #5B21B6 50%, #7E22CE 100%);
    border: 1px solid rgba(255, 255, 255, 0.30);
    box-shadow:
        0 18px 38px rgba(76, 29, 149, 0.22),
        inset 0 1px 0 rgba(255, 255, 255, 0.42);
    color: #FFFFFF;
    text-align: center;
    margin: 20px 0;
}
</style>
""", unsafe_allow_html=True)

render_page_banner(
    symbol="💊",
    title="Health Goals & Habits",
    subtitle="Set daily wellness targets and monitor your progress using your recorded health data.",
    badge="🧬 Aarogya-AI Habit & Goal Tracker",
)


# =========================================================
# DATABASE
# =========================================================

DB_PATH = os.path.join(ROOT_DIR, "health_data.db")


@st.cache_data(ttl=60)
def _load_goals_data(db_path: str):
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
            "SELECT date, weight, steps, sleep FROM health_data ORDER BY date ASC",
            conn
        )
        return loaded_df
    except Exception:
        return pd.DataFrame()
    finally:
        if conn is not None:
            conn.close()


df = _load_goals_data(DB_PATH)


# =========================================================
# GOAL SETTINGS
# =========================================================

st.markdown('<div class="purple-goals-title anim-1">🩺 Set Your Wellness Goals</div>', unsafe_allow_html=True)

with st.container(border=True):
    gc1, gc2, gc3 = st.columns(3)

    with gc1:
        steps_goal = st.number_input(
            "🩺 Daily Steps Goal",
            min_value=100, max_value=100000,
            value=5000, step=500
        )

    with gc2:
        sleep_goal = st.number_input(
            "💤 Sleep Goal (hours)",
            min_value=1.0, max_value=24.0,
            value=7.0, step=0.5
        )

    with gc3:
        weight_goal = st.number_input(
            "⚖️ Weight Tracking Value (kg)",
            min_value=1.0, max_value=300.0,
            value=40.0, step=0.1
        )


# =========================================================
# NO DATA STATE
# =========================================================

if df.empty:
    render_gloss_card(
        title="No Health Data Yet",
        body="Add your weight, steps, and sleep data from the Health Data page to start tracking your daily goals.",
        symbol="🫀",
        anim_class="anim-2"
    )
    render_medical_disclaimer()
    st.stop()


# =========================================================
# DATA PREP
# =========================================================

df = df.copy()
df["date"] = pd.to_datetime(df["date"], errors="coerce")
for col, default_val in (("weight", 0.0), ("steps", 0), ("sleep", 0.0)):
    df[col] = pd.to_numeric(df[col], errors="coerce").fillna(default_val)

df = df.dropna(subset=["date"])

if df.empty:
    st.warning("⚠️ No valid health records available.")
    render_medical_disclaimer()
    st.stop()

df = df.sort_values("date").reset_index(drop=True)
latest = df.iloc[-1]

current_steps = float(latest["steps"])
current_sleep = float(latest["sleep"])
current_weight = float(latest["weight"])

steps_progress = min(current_steps / max(float(steps_goal), 1.0), 1.0)
sleep_progress = min(current_sleep / max(float(sleep_goal), 0.1), 1.0)
steps_pct = min(int(steps_progress * 100), 100)
sleep_pct = min(int(sleep_progress * 100), 100)


# =========================================================
# GOAL CARDS
# =========================================================

st.markdown('<div class="purple-goals-title anim-1">🧬 Current Progress</div>', unsafe_allow_html=True)

pg1, pg2, pg3 = st.columns(3)

with pg1:
    st.markdown(f"""
    <div class="gloss-goal-card anim-1">
        <div class="gloss-goal-label"><span class="med-float">🩺</span> Daily Steps</div>
        <div class="gloss-goal-val">{int(current_steps):,}</div>
        <div class="gloss-goal-target">Goal: {int(steps_goal):,} steps</div>
        <div class="gloss-goal-pct">{steps_pct}% of goal</div>
    </div>""", unsafe_allow_html=True)
    st.progress(steps_progress)

with pg2:
    st.markdown(f"""
    <div class="gloss-goal-card anim-2">
        <div class="gloss-goal-label"><span class="med-float">💤</span> Sleep</div>
        <div class="gloss-goal-val">{current_sleep:.1f} hrs</div>
        <div class="gloss-goal-target">Goal: {sleep_goal:.1f} hours</div>
        <div class="gloss-goal-pct">{sleep_pct}% of goal</div>
    </div>""", unsafe_allow_html=True)
    st.progress(sleep_progress)

with pg3:
    st.markdown(f"""
    <div class="gloss-goal-card anim-3">
        <div class="gloss-goal-label"><span class="med-float">⚖️</span> Weight Tracking</div>
        <div class="gloss-goal-val">{current_weight:.1f} kg</div>
        <div class="gloss-goal-target">Reference: {weight_goal:.1f} kg</div>
        <div class="gloss-goal-pct">Active Monitoring</div>
    </div>""", unsafe_allow_html=True)
    st.caption("Weight shown for tracking purposes.")


# =========================================================
# GOAL STATUS
# =========================================================

st.markdown('<div class="purple-goals-title anim-2">🫀 Goal Status</div>', unsafe_allow_html=True)

if current_steps >= steps_goal:
    st.markdown("""
    <div class="gloss-status-pill anim-2">
        <span class="med-float">🩺</span> <b>Steps Goal Reached:</b> You have met your selected daily steps target.
    </div>""", unsafe_allow_html=True)
else:
    remaining = int(steps_goal - current_steps)
    st.markdown(f"""
    <div class="gloss-status-pill anim-2">
        <span class="med-float">🩺</span> <b>Steps Progress:</b> {remaining:,} more steps needed to reach today's goal.
    </div>""", unsafe_allow_html=True)

if current_sleep >= sleep_goal:
    st.markdown("""
    <div class="gloss-status-pill anim-3">
        <span class="med-float">💤</span> <b>Sleep Goal Reached:</b> Your latest recorded sleep meets the selected target.
    </div>""", unsafe_allow_html=True)
else:
    remaining_sleep = sleep_goal - current_sleep
    st.markdown(f"""
    <div class="gloss-status-pill anim-3">
        <span class="med-float">💤</span> <b>Sleep Progress:</b> {remaining_sleep:.1f} more hours needed to reach the selected goal.
    </div>""", unsafe_allow_html=True)


# =========================================================
# MOTIVATION
# =========================================================

if steps_pct >= 100 and sleep_pct >= 100:
    st.markdown("""
    <div class="gloss-motivation-banner anim-3">
        <div class="med-float" style="font-size: 38px; margin-bottom: 8px;">🧬</div>
        <div style="font-size: 19px; font-weight: 800; margin-bottom: 6px;">Outstanding — Both Core Goals Reached</div>
        <div style="font-size: 14px; color: #E9D5FF; line-height: 1.6;">
            Your latest recorded daily movement and sleep duration both meet your selected targets.
        </div>
    </div>""", unsafe_allow_html=True)

elif steps_pct >= 75 or sleep_pct >= 75:
    st.markdown("""
    <div class="gloss-motivation-banner anim-3">
        <div class="med-float" style="font-size: 38px; margin-bottom: 8px;">💊</div>
        <div style="font-size: 19px; font-weight: 800; margin-bottom: 6px;">Strong Momentum — Keep Going</div>
        <div style="font-size: 14px; color: #E9D5FF; line-height: 1.6;">
            You are making steady progress toward your selected daily wellness targets.
        </div>
    </div>""", unsafe_allow_html=True)

else:
    st.markdown("""
    <div class="gloss-motivation-banner anim-3">
        <div class="med-float" style="font-size: 38px; margin-bottom: 8px;">🩺</div>
        <div style="font-size: 19px; font-weight: 800; margin-bottom: 6px;">Steady Habit Building</div>
        <div style="font-size: 14px; color: #E9D5FF; line-height: 1.6;">
            Consistent daily logging helps build sustainable activity and sleep routines over time.
        </div>
    </div>""", unsafe_allow_html=True)


# =========================================================
# PROGRESS CHARTS
# =========================================================

st.markdown('<div class="purple-goals-title anim-2">🧬 Progress History</div>', unsafe_allow_html=True)

with st.container(border=True):
    st.markdown("**🩺 Steps History**")
    st.line_chart(df.set_index("date")[["steps"]], height=220, color=["#7E22CE"], use_container_width=True)

with st.container(border=True):
    st.markdown("**💤 Sleep History**")
    st.line_chart(df.set_index("date")[["sleep"]], height=220, color=["#5B21B6"], use_container_width=True)

with st.container(border=True):
    st.markdown("**⚖️ Weight History**")
    st.line_chart(df.set_index("date")[["weight"]], height=220, color=["#6D28D9"], use_container_width=True)


# =========================================================
# RECORDS
# =========================================================

st.markdown('<div class="purple-goals-title anim-3">📋 Recorded Progress</div>', unsafe_allow_html=True)

display_df = df.copy()
display_df["date"] = display_df["date"].dt.strftime("%Y-%m-%d")
display_df = display_df.rename(columns={
    "date": "Date",
    "weight": "Weight (kg)",
    "steps": "Steps",
    "sleep": "Sleep (hrs)"
})
st.dataframe(display_df, use_container_width=True, hide_index=True)


# =========================================================
# SAFETY
# =========================================================

render_medical_disclaimer()