import os
import sys
import sqlite3
import importlib.util
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import streamlit as st

# =========================================================
# EXPLICIT ROOT PATH & Ui.py LOADER (pages/4_Health_Analysis.py)
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
            _spec = importlib.util.spec_from_file_location(
                "aarogya_health_analysis_ui",
                _ui_path
            )

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
.purple-heading {
    font-size: 20px;
    font-weight: 800;
    color: #2E1065;
    letter-spacing: -0.3px;
    margin: 24px 0 12px 0;
}

.gloss-kpi-card {
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

.gloss-kpi-card:hover {
    transform: translateY(-4px);
    border-color: #C084FC;
    box-shadow:
        0 16px 32px rgba(126, 34, 206, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 1);
}

.gloss-kpi-label {
    font-size: 13px;
    font-weight: 700;
    color: #5B21B6;
    margin-bottom: 6px;
}

.gloss-kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #1E1035;
    letter-spacing: -0.5px;
    margin-bottom: 4px;
}

.gloss-kpi-sub {
    font-size: 12.5px;
    font-weight: 600;
    color: #6D28D9;
}

.gloss-insight-box {
    border-radius: 18px;
    padding: 16px 20px;
    margin: 12px 0;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.94) 0%, rgba(243, 232, 255, 0.78) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(216, 180, 254, 0.78);
    border-left: 4px solid #7E22CE;
    color: #2E1065;
    font-size: 14px;
    line-height: 1.6;
    box-shadow: 0 8px 20px rgba(109, 40, 217, 0.06);
}

.gloss-insight-box.good {
    border-left-color: #6D28D9;
    background: linear-gradient(155deg, rgba(250, 245, 255, 0.96) 0%, rgba(237, 233, 254, 0.86) 100%);
}

.gloss-insight-box.warn {
    border-left-color: #9333EA;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.95) 0%, rgba(245, 208, 254, 0.45) 100%);
}
</style>
""", unsafe_allow_html=True)

render_page_banner(
    symbol="🧬",
    title="Health Analysis & Trends",
    subtitle="Understand your wellness patterns through clinical data insights and longitudinal trend charts.",
    badge="🧬 Aarogya-AI Analytics Engine",
)


# =========================================================
# DATABASE (ALWAYS FRESH READ)
# =========================================================

DB_PATH = os.path.join(ROOT_DIR, "health_data.db")


def _load_analysis_data(db_path: str):
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
            "SELECT * FROM health_data ORDER BY id ASC",
            conn
        )
        return loaded_df
    except Exception as e:
        st.error(f"Database read error: {e}")
        return None
    finally:
        if conn is not None:
            conn.close()


df = _load_analysis_data(DB_PATH)
if df is None:
    st.stop()


# =========================================================
# MATPLOTLIB STYLE
# =========================================================

def apply_premium_style(ax, fig):
    fig.patch.set_facecolor("#FAF7FF")
    ax.set_facecolor("#FFFFFF")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#DDD6FE")
    ax.spines["bottom"].set_color("#DDD6FE")
    ax.tick_params(axis="both", colors="#4C1D95", labelsize=9)
    ax.tick_params(axis="x", rotation=35)
    for label in ax.get_xticklabels():
        label.set_ha("right")
    ax.xaxis.label.set_color("#4C1D95")
    ax.yaxis.label.set_color("#4C1D95")
    ax.title.set_color("#2E1065")


# =========================================================
# NO DATA
# =========================================================

if df.empty:
    render_gloss_card(
        title="No Health Data Available",
        body="Please add your health measurements from the Health Data page to unlock trend analytics and wellness insights.",
        symbol="🩺",
        anim_class="anim-2"
    )
    render_medical_disclaimer()
    st.stop()


# =========================================================
# DATA PREP (SAFE PER-COLUMN CONVERSION)
# =========================================================

df = df.copy()

for required_col, default_val in (("weight", 0.0), ("steps", 0), ("sleep", 0.0)):
    if required_col not in df.columns:
        df[required_col] = default_val
    df[required_col] = pd.to_numeric(df[required_col], errors="coerce").fillna(default_val)

if "date" not in df.columns:
    df["date"] = pd.Timestamp.today().strftime("%Y-%m-%d")

df["parsed_date"] = pd.to_datetime(df["date"], errors="coerce")
df["parsed_date"] = df["parsed_date"].fillna(pd.Timestamp.today())
df = df.sort_values(["parsed_date"]).reset_index(drop=True)

latest = df.iloc[-1]
avg_weight = float(df["weight"].mean())
avg_steps = float(df["steps"].mean())
avg_sleep = float(df["sleep"].mean())


# =========================================================
# RECORD COUNT BANNER
# =========================================================

st.markdown(f"""
<div class="gloss-insight-box anim-1">
    <span class="med-float">🧬</span> <b>{len(df)}</b> health record(s) available for analysis.
    &nbsp;·&nbsp; Data range: <b>{df["parsed_date"].min().strftime("%d %b %Y")}</b>
    &nbsp;→&nbsp; <b>{df["parsed_date"].max().strftime("%d %b %Y")}</b>
</div>
""", unsafe_allow_html=True)


# =========================================================
# OVERVIEW METRICS
# =========================================================

st.markdown('<div class="purple-heading anim-1">🫀 Latest Health Overview</div>', unsafe_allow_html=True)

oc1, oc2, oc3 = st.columns(3)

with oc1:
    st.markdown(f"""
    <div class="gloss-kpi-card anim-1">
        <div class="gloss-kpi-label"><span class="med-float">⚖️</span> Latest Weight</div>
        <div class="gloss-kpi-value">{float(latest['weight']):.1f} kg</div>
        <div class="gloss-kpi-sub">Avg: {avg_weight:.2f} kg</div>
    </div>""", unsafe_allow_html=True)

with oc2:
    st.markdown(f"""
    <div class="gloss-kpi-card anim-2">
        <div class="gloss-kpi-label"><span class="med-float">🩺</span> Latest Steps</div>
        <div class="gloss-kpi-value">{int(float(latest['steps'])):,}</div>
        <div class="gloss-kpi-sub">Avg: {avg_steps:.0f} steps/day</div>
    </div>""", unsafe_allow_html=True)

with oc3:
    st.markdown(f"""
    <div class="gloss-kpi-card anim-3">
        <div class="gloss-kpi-label"><span class="med-float">💤</span> Latest Sleep</div>
        <div class="gloss-kpi-value">{float(latest['sleep']):.1f} hrs</div>
        <div class="gloss-kpi-sub">Avg: {avg_sleep:.2f} hrs/night</div>
    </div>""", unsafe_allow_html=True)


# =========================================================
# CHARTS
# =========================================================

st.markdown('<div class="purple-heading anim-2">🧬 Health Trends</div>', unsafe_allow_html=True)

DEEP_VIOLET = "#6D28D9"
ROYAL_PURPLE = "#7E22CE"
AMETHYST = "#9333EA"

# ---- Weight ----
with st.container(border=True):
    st.markdown("**⚖️ Weight Trend**")
    fig1, ax1 = plt.subplots(figsize=(9, 3.2))
    ax1.fill_between(df["parsed_date"], df["weight"], alpha=0.14, color=DEEP_VIOLET)
    ax1.plot(df["parsed_date"], df["weight"], color=DEEP_VIOLET, linewidth=2.2, marker="o", markersize=5)
    ax1.set_ylabel("Weight (kg)")
    ax1.set_title("")
    apply_premium_style(ax1, fig1)
    fig1.tight_layout()
    st.pyplot(fig1, use_container_width=True)
    plt.close(fig1)

# ---- Steps ----
with st.container(border=True):
    st.markdown("**🩺 Daily Steps Trend**")
    fig2, ax2 = plt.subplots(figsize=(9, 3.2))
    ax2.fill_between(df["parsed_date"], df["steps"], alpha=0.14, color=ROYAL_PURPLE)
    ax2.plot(df["parsed_date"], df["steps"], color=ROYAL_PURPLE, linewidth=2.2, marker="o", markersize=5)
    ax2.axhline(7000, color="#A855F7", linestyle="--", linewidth=1.3, alpha=0.85, label="7,000 step reference")
    ax2.legend(fontsize=9)
    ax2.set_ylabel("Steps")
    apply_premium_style(ax2, fig2)
    fig2.tight_layout()
    st.pyplot(fig2, use_container_width=True)
    plt.close(fig2)

# ---- Sleep ----
with st.container(border=True):
    st.markdown("**💤 Sleep Duration Trend**")
    fig3, ax3 = plt.subplots(figsize=(9, 3.2))
    ax3.fill_between(df["parsed_date"], df["sleep"], alpha=0.14, color=AMETHYST)
    ax3.plot(df["parsed_date"], df["sleep"], color=AMETHYST, linewidth=2.2, marker="o", markersize=5)
    ax3.axhline(7, color="#7E22CE", linestyle="--", linewidth=1.3, alpha=0.85, label="7-hr reference")
    ax3.legend(fontsize=9)
    ax3.set_ylabel("Sleep (hours)")
    apply_premium_style(ax3, fig3)
    fig3.tight_layout()
    st.pyplot(fig3, use_container_width=True)
    plt.close(fig3)


# =========================================================
# STATISTICS
# =========================================================

st.markdown('<div class="purple-heading anim-2">💊 Health Statistics</div>', unsafe_allow_html=True)

sc1, sc2, sc3 = st.columns(3)

with sc1:
    st.markdown(f"""
    <div class="gloss-kpi-card anim-1">
        <div class="gloss-kpi-label"><span class="med-float">⚖️</span> Average Weight</div>
        <div class="gloss-kpi-value">{avg_weight:.2f} kg</div>
    </div>""", unsafe_allow_html=True)

with sc2:
    st.markdown(f"""
    <div class="gloss-kpi-card anim-2">
        <div class="gloss-kpi-label"><span class="med-float">🩺</span> Average Steps</div>
        <div class="gloss-kpi-value">{avg_steps:.0f}</div>
    </div>""", unsafe_allow_html=True)

with sc3:
    st.markdown(f"""
    <div class="gloss-kpi-card anim-3">
        <div class="gloss-kpi-label"><span class="med-float">💤</span> Average Sleep</div>
        <div class="gloss-kpi-value">{avg_sleep:.2f} hrs</div>
    </div>""", unsafe_allow_html=True)


# =========================================================
# WELLNESS INSIGHTS
# =========================================================

st.markdown('<div class="purple-heading anim-3">🩺 Wellness Insights</div>', unsafe_allow_html=True)

activity_class = "good" if avg_steps >= 7000 else "warn"
activity_msg = (
    "Your recorded activity level shows consistent daily movement. Keep it up!"
    if avg_steps >= 7000
    else "Your recorded activity level may benefit from more regular movement."
)

sleep_class = "good" if avg_sleep >= 7 else "warn"
sleep_msg = (
    "Your recorded average sleep duration is within a commonly recommended range."
    if avg_sleep >= 7
    else "Your recorded average sleep duration is below 7 hours."
)

st.markdown(f"""
<div class="gloss-insight-box {activity_class} anim-2">
    <span class="med-float">🩺</span> <b>Activity Insight:</b> {activity_msg}
</div>
<div class="gloss-insight-box {sleep_class} anim-3">
    <span class="med-float">💤</span> <b>Sleep Insight:</b> {sleep_msg}
</div>
<div class="gloss-insight-box anim-4">
    <span class="med-float">🧬</span> <b>Data Summary:</b> You currently have <b>{len(df)}</b> health record(s) available.
    Continue adding records for richer trend analysis.
</div>
""", unsafe_allow_html=True)


# =========================================================
# DATA TABLE
# =========================================================

st.markdown('<div class="purple-heading anim-3">📋 Recorded Health Data</div>', unsafe_allow_html=True)

display_df = df[["parsed_date", "weight", "steps", "sleep"]].copy()
display_df["parsed_date"] = display_df["parsed_date"].dt.strftime("%Y-%m-%d")
display_df.columns = ["Date", "Weight (kg)", "Steps", "Sleep (hrs)"]
st.dataframe(display_df, use_container_width=True, hide_index=True)


# =========================================================
# SAFETY NOTICE
# =========================================================

render_medical_disclaimer()