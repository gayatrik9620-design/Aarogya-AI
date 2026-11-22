import os
import sys
import sqlite3
import importlib.util
from datetime import datetime
import pandas as pd
import streamlit as st

# =========================================================
# EXPLICIT ROOT PATH & Ui.py LOADER (pages/5_Health_Report.py)
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
.purple-sec-title {
    font-size: 20px;
    font-weight: 800;
    color: #2E1065;
    letter-spacing: -0.3px;
    margin: 24px 0 12px 0;
}

.gloss-meta-bar {
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    padding: 22px 28px;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.95) 0%, rgba(243, 232, 255, 0.78) 100%);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(216, 180, 254, 0.80);
    box-shadow:
        0 12px 26px rgba(109, 40, 217, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.98);
    display: flex;
    gap: 32px;
    align-items: center;
    flex-wrap: wrap;
    margin-bottom: 22px;
}

.gloss-meta-item {
    display: flex;
    flex-direction: column;
    gap: 3px;
}

.gloss-meta-label {
    font-size: 11px;
    font-weight: 700;
    color: #6D28D9;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.gloss-meta-val {
    font-size: 16px;
    font-weight: 800;
    color: #1E1035;
}

.gloss-kpi-box {
    position: relative;
    overflow: hidden;
    border-radius: 20px;
    padding: 20px;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.95) 0%, rgba(243, 232, 255, 0.78) 100%);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(216, 180, 254, 0.80);
    box-shadow:
        0 10px 24px rgba(109, 40, 217, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.98);
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
}

.gloss-kpi-box:hover {
    transform: translateY(-4px);
    border-color: #C084FC;
    box-shadow:
        0 16px 32px rgba(126, 34, 206, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 1);
}

.gloss-kpi-lbl {
    font-size: 13px;
    font-weight: 700;
    color: #5B21B6;
    margin-bottom: 6px;
}

.gloss-kpi-num {
    font-size: 28px;
    font-weight: 800;
    color: #1E1035;
    letter-spacing: -0.5px;
}
</style>
""", unsafe_allow_html=True)

render_page_banner(
    symbol="🩺",
    title="Your Health Report",
    subtitle="A comprehensive clinical & wellness overview of your recorded health measurements.",
    badge="🧬 Aarogya-AI Clinical Summary",
)


# =========================================================
# DATABASE
# =========================================================

DB_PATH = os.path.join(ROOT_DIR, "health_data.db")


@st.cache_data(ttl=60)
def _load_report_data(db_path: str):
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
            "SELECT date, weight, steps, sleep FROM health_data ORDER BY date DESC",
            conn
        )
        return loaded_df
    except Exception:
        return None
    finally:
        if conn is not None:
            conn.close()


_df_result = _load_report_data(DB_PATH)
if _df_result is None:
    st.error("Unable to load health data.")
    st.stop()
df = _df_result


# =========================================================
# NO DATA
# =========================================================

if df.empty:
    render_gloss_card(
        title="No Health Data Available",
        body="Please add your health records from the Health Data page to generate a wellness summary report.",
        symbol="🫀",
        anim_class="anim-2"
    )
    render_medical_disclaimer()
    st.stop()


# =========================================================
# DATA PROCESSING
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

df = df.sort_values("date", ascending=False).reset_index(drop=True)
latest = df.iloc[0]

avg_weight = float(df["weight"].mean())
avg_steps = float(df["steps"].mean())
avg_sleep = float(df["sleep"].mean())

generated_time = datetime.now().strftime("%d %B %Y, %I:%M %p")


# =========================================================
# REPORT INFO BAR
# =========================================================

st.markdown(f"""
<div class="gloss-meta-bar anim-1">
    <div class="gloss-meta-item">
        <div class="gloss-meta-label">📅 Report Generated</div>
        <div class="gloss-meta-val">{generated_time}</div>
    </div>
    <div class="gloss-meta-item">
        <div class="gloss-meta-label">🧬 Total Records</div>
        <div class="gloss-meta-val">{len(df)}</div>
    </div>
    <div class="gloss-meta-item">
        <div class="gloss-meta-label">🗓️ Date Range</div>
        <div class="gloss-meta-val">{df["date"].min().strftime("%d %b %Y")} → {df["date"].max().strftime("%d %b %Y")}</div>
    </div>
    <div class="gloss-meta-item">
        <div class="gloss-meta-label">🩺 Powered By</div>
        <div class="gloss-meta-val">Aarogya-AI</div>
    </div>
</div>
""", unsafe_allow_html=True)


# =========================================================
# LATEST METRICS
# =========================================================

st.markdown('<div class="purple-sec-title anim-1">🫀 Latest Health Summary</div>', unsafe_allow_html=True)

lc1, lc2, lc3 = st.columns(3)

with lc1:
    st.markdown(f"""
    <div class="gloss-kpi-box anim-1">
        <div class="gloss-kpi-lbl"><span class="med-float">⚖️</span> Latest Weight</div>
        <div class="gloss-kpi-num">{float(latest['weight']):.1f} kg</div>
    </div>""", unsafe_allow_html=True)

with lc2:
    st.markdown(f"""
    <div class="gloss-kpi-box anim-2">
        <div class="gloss-kpi-lbl"><span class="med-float">🩺</span> Latest Steps</div>
        <div class="gloss-kpi-num">{int(float(latest['steps'])):,}</div>
    </div>""", unsafe_allow_html=True)

with lc3:
    st.markdown(f"""
    <div class="gloss-kpi-box anim-3">
        <div class="gloss-kpi-lbl"><span class="med-float">💤</span> Latest Sleep</div>
        <div class="gloss-kpi-num">{float(latest['sleep']):.1f} hrs</div>
    </div>""", unsafe_allow_html=True)


# =========================================================
# AVERAGE METRICS
# =========================================================

st.markdown('<div class="purple-sec-title anim-2">🧬 Overall Statistics</div>', unsafe_allow_html=True)

sc1, sc2, sc3 = st.columns(3)

with sc1:
    st.metric("⚖️ Average Weight", f"{avg_weight:.2f} kg")

with sc2:
    st.metric("🩺 Average Steps", f"{avg_steps:.0f}")

with sc3:
    st.metric("💤 Average Sleep", f"{avg_sleep:.2f} hrs")


# =========================================================
# REPORT SUMMARY
# =========================================================

st.markdown('<div class="purple-sec-title anim-2">💊 Report Summary</div>', unsafe_allow_html=True)

summary_text = (
    f"Latest recorded weight: <b>{float(latest['weight']):.1f} kg</b> · "
    f"Latest activity: <b>{int(float(latest['steps'])):,} steps</b> · "
    f"Latest sleep: <b>{float(latest['sleep']):.1f} hrs</b><br><br>"
    f"Overall averages across <b>{len(df)}</b> record(s): "
    f"<b>{avg_weight:.2f} kg</b> weight, "
    f"<b>{avg_steps:.0f}</b> daily steps, and "
    f"<b>{avg_sleep:.2f} hrs</b> sleep per night."
)

render_gloss_card(
    title="Health Data Summary",
    body=summary_text,
    symbol="🩺",
    anim_class="anim-2"
)


# =========================================================
# COMPLETE RECORDS
# =========================================================

st.markdown('<div class="purple-sec-title anim-3">📋 Complete Health Records</div>', unsafe_allow_html=True)

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
# DOWNLOAD
# =========================================================

st.markdown('<div class="purple-sec-title anim-3">📥 Download Report</div>', unsafe_allow_html=True)

render_gloss_card(
    title="Export Health Report",
    body="Download your complete recorded health data as a CSV file for personal reference or sharing with a healthcare professional.",
    symbol="💊",
    anim_class="anim-3"
)

csv_data = display_df.to_csv(index=False).encode("utf-8")

dl1, _ = st.columns([2, 5])
with dl1:
    st.download_button(
        label="📄  Download Health Report (CSV)",
        data=csv_data,
        file_name="Aarogya_AI_Health_Report.csv",
        mime="text/csv",
        use_container_width=True
    )


# =========================================================
# SAFETY NOTICE
# =========================================================

render_medical_disclaimer()
