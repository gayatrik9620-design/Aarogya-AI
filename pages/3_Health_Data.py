import os
import sys
import sqlite3
from datetime import date
import importlib.util
from pathlib import Path

import pandas as pd
import streamlit as st


# =========================================================
# EXPLICIT ROOT PATH & UI LOADER (LOCAL + CLOUD SAFE)
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
            _spec = importlib.util.spec_from_file_location(
                "aarogya_health_data_ui",
                str(_ui_path)
            )

            if _spec is None or _spec.loader is None:
                raise ImportError("Could not load UI module.")

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
    st.error(f"Could not find Ui.py in {ROOT_DIR}")
    st.stop()


# NOTE: st.set_page_config() is handled by app.py.


# =========================================================
# DATABASE PATH
# =========================================================

DB_PATH = ROOT_DIR / "health_data.db"


# =========================================================
# GLOSSY PURPLE THEME & HEADER
# =========================================================

apply_glossy_purple_theme()

st.markdown("""
<style>
.purple-subhead {
    font-size: 20px;
    font-weight: 800;
    color: #2E1065;
    letter-spacing: -0.3px;
    margin: 24px 0 12px 0;
}

.gloss-metric-box {
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

.gloss-metric-box:hover {
    transform: translateY(-4px);
    border-color: #C084FC;
    box-shadow:
        0 16px 32px rgba(126, 34, 206, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 1);
}

.gloss-metric-label {
    font-size: 13px;
    font-weight: 700;
    color: #5B21B6;
    margin-bottom: 6px;
}

.gloss-metric-val {
    font-size: 28px;
    font-weight: 800;
    color: #1E1035;
    letter-spacing: -0.5px;
}

.gloss-empty-panel {
    text-align: center;
    padding: 46px 28px;
    border-radius: 22px;
    background: linear-gradient(160deg, rgba(255, 255, 255, 0.92) 0%, rgba(243, 232, 255, 0.75) 100%);
    border: 1px dashed rgba(168, 85, 247, 0.55);
    box-shadow: 0 10px 24px rgba(109, 40, 217, 0.06);
    margin: 18px 0;
}
</style>
""", unsafe_allow_html=True)


render_page_banner(
    symbol="🫀",
    title="Your Health Data & Vitals",
    subtitle="Track your daily wellness measurements — body mass, activity steps, and recovery sleep.",
    badge="🧬 Aarogya-AI Vitals Tracker",
)


# =========================================================
# DATABASE CONNECTION
# =========================================================

try:
    conn = sqlite3.connect(
        str(DB_PATH),
        check_same_thread=False
    )

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

except sqlite3.Error as e:
    st.error(f"Database connection error: {e}")
    st.stop()


# =========================================================
# LOAD DATA
# =========================================================

def load_data():
    return pd.read_sql_query(
        """
        SELECT date, weight, steps, sleep
        FROM health_data
        ORDER BY date DESC, id DESC
        """,
        conn
    )


try:
    df = load_data()

except Exception as e:
    st.error(f"Unable to load health records: {e}")
    conn.close()
    st.stop()


# =========================================================
# LATEST METRICS
# =========================================================

if not df.empty:

    latest = df.iloc[0]

    st.markdown(
        '<div class="purple-subhead anim-1">🩺 Latest Clinical &amp; Wellness Snapshot</div>',
        unsafe_allow_html=True
    )

    mc1, mc2, mc3, mc4 = st.columns(4)

    with mc1:
        st.markdown(f"""
        <div class="gloss-metric-box anim-1">
            <div class="gloss-metric-label"><span class="med-float">⚖️</span> Latest Weight</div>
            <div class="gloss-metric-val">{latest['weight']:.1f} kg</div>
        </div>
        """, unsafe_allow_html=True)

    with mc2:
        st.markdown(f"""
        <div class="gloss-metric-box anim-2">
            <div class="gloss-metric-label"><span class="med-float">🩺</span> Latest Steps</div>
            <div class="gloss-metric-val">{int(latest['steps']):,}</div>
        </div>
        """, unsafe_allow_html=True)

    with mc3:
        st.markdown(f"""
        <div class="gloss-metric-box anim-3">
            <div class="gloss-metric-label"><span class="med-float">💤</span> Latest Sleep</div>
            <div class="gloss-metric-val">{latest['sleep']:.1f} hrs</div>
        </div>
        """, unsafe_allow_html=True)

    with mc4:
        st.markdown(f"""
        <div class="gloss-metric-box anim-4">
            <div class="gloss-metric-label"><span class="med-float">🧬</span> Total Records</div>
            <div class="gloss-metric-val">{len(df)}</div>
        </div>
        """, unsafe_allow_html=True)


# =========================================================
# RECORD FORM
# =========================================================

st.markdown(
    '<div class="purple-subhead anim-2">💊 Record Today\'s Health Data</div>',
    unsafe_allow_html=True
)

with st.container(border=True):

    st.markdown("**📋 Enter your measurements below**")

    with st.form("health_entry_form"):

        fc1, fc2 = st.columns(2)

        with fc1:

            health_date = st.date_input(
                "📅 Date",
                value=date.today()
            )

            weight = st.number_input(
                "⚖️ Weight (kg)",
                min_value=0.0,
                max_value=500.0,
                value=50.0,
                step=0.1,
                format="%.1f"
            )

        with fc2:

            steps = st.number_input(
                "🩺 Daily Steps",
                min_value=0,
                max_value=200000,
                value=0,
                step=100
            )

            sleep = st.number_input(
                "💤 Sleep (hours)",
                min_value=0.0,
                max_value=24.0,
                value=7.0,
                step=0.5,
                format="%.1f"
            )

        submitted = st.form_submit_button(
            "💾  Save Health Data",
            use_container_width=True,
            type="primary"
        )

        if submitted:

            try:
                conn.execute(
                    """
                    INSERT INTO health_data
                    (date, weight, steps, sleep)
                    VALUES (?, ?, ?, ?)
                    """,
                    (
                        str(health_date),
                        weight,
                        int(steps),
                        sleep
                    )
                )

                conn.commit()

                st.success(
                    "✅ Health data saved successfully! "
                    "Your record has been added."
                )

                conn.close()
                st.rerun()

            except sqlite3.Error as e:
                st.error(f"Unable to save health data: {e}")


# =========================================================
# REFRESH DATA
# =========================================================

try:
    df = load_data()

except Exception as e:
    st.error(f"Unable to refresh health records: {e}")
    conn.close()
    st.stop()


# =========================================================
# CHARTS + RECORDS
# =========================================================

if not df.empty:

    render_gloss_card(
        title="Tracking Insight",
        body="Regularly recording weight, daily movement, and sleep helps reveal consistent patterns in your personal wellness routine.",
        symbol="🧬",
        anim_class="anim-2"
    )

    chart_df = df.copy()

    chart_df["date"] = pd.to_datetime(
        chart_df["date"],
        errors="coerce"
    )

    chart_df = chart_df.dropna(subset=["date"])
    chart_df = chart_df.sort_values("date")

    st.markdown(
        '<div class="purple-subhead anim-2">🧬 Wellness Trends</div>',
        unsafe_allow_html=True
    )

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:

        with st.container(border=True):

            st.markdown("**🩺 Activity Trend — Daily Steps**")

            st.line_chart(
                chart_df.set_index("date")["steps"],
                height=250,
                color="#7E22CE"
            )

    with chart_col2:

        with st.container(border=True):

            st.markdown("**💤 Sleep Trend — Hours per Day**")

            st.line_chart(
                chart_df.set_index("date")["sleep"],
                height=250,
                color="#5B21B6"
            )

    with st.container(border=True):

        st.markdown("**⚖️ Weight Trend — kg over Time**")

        st.line_chart(
            chart_df.set_index("date")["weight"],
            height=240,
            color="#6D28D9"
        )

    st.markdown(
        '<div class="purple-subhead anim-3">📋 Health Records</div>',
        unsafe_allow_html=True
    )

    display_df = df.copy()

    display_df.columns = [
        "Date",
        "Weight (kg)",
        "Steps",
        "Sleep (hrs)"
    ]

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.markdown(
        '<div class="purple-subhead anim-3">📥 Export Your Data</div>',
        unsafe_allow_html=True
    )

    csv_data = df.to_csv(index=False).encode("utf-8")

    dl1, dl2 = st.columns([2, 5])

    with dl1:

        st.download_button(
            label="📄  Download Health Report (CSV)",
            data=csv_data,
            file_name="aarogya_health_report.csv",
            mime="text/csv",
            use_container_width=True
        )

else:

    st.markdown("""
    <div class="gloss-empty-panel anim-2">
        <div class="med-float" style="font-size: 56px; margin-bottom: 12px;">🩺</div>
        <div style="font-size: 18px; font-weight: 800; color: #2E1065; margin-bottom: 6px;">No health records yet</div>
        <div style="font-size: 14px; color: #5B21B6;">
            Add your first health record using the form above to start<br>
            building your personal wellness history.
        </div>
    </div>
    """, unsafe_allow_html=True)


# =========================================================
# SAFETY NOTICE
# =========================================================

render_medical_disclaimer()

conn.close()