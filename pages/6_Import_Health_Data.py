import os
import sys
import json
import sqlite3
import importlib.util
import pandas as pd
import streamlit as st

# =========================================================
# EXPLICIT ROOT PATH & Ui.py LOADER (pages/6_Import_Health_Data.py)
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
.purple-sec-head {
    font-size: 20px;
    font-weight: 800;
    color: #2E1065;
    letter-spacing: -0.3px;
    margin: 24px 0 12px 0;
}

.gloss-stat-box {
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

.gloss-stat-box:hover {
    transform: translateY(-4px);
    border-color: #C084FC;
    box-shadow:
        0 16px 32px rgba(126, 34, 206, 0.16),
        inset 0 1px 0 rgba(255, 255, 255, 1);
}

.gloss-stat-label {
    font-size: 12.5px;
    font-weight: 700;
    color: #5B21B6;
    margin-bottom: 6px;
}

.gloss-stat-val {
    font-size: 24px;
    font-weight: 800;
    color: #1E1035;
    letter-spacing: -0.4px;
    word-break: break-word;
}
</style>
""", unsafe_allow_html=True)

render_page_banner(
    symbol="🧬",
    title="Import Health Data",
    subtitle="Upload, inspect, and export your health and wellness measurements in CSV or JSON format.",
    badge="🧬 Aarogya-AI Data Ingestion",
)

# =========================================================
# FILE UPLOADER & DATA PREVIEW
# =========================================================

render_gloss_card(
    title="Supported Health Data Formats",
    body="Select a CSV or JSON file containing wellness logs (such as date, weight, steps, or sleep) to preview rows, view numeric summaries, and export a clean CSV.",
    symbol="🩺",
    anim_class="anim-2"
)

with st.container(border=True):
    uploaded_file = st.file_uploader(
        "🧬 Choose a CSV or JSON file",
        type=["csv", "json"]
    )

if uploaded_file is not None:
    try:
        if uploaded_file.name.lower().endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.lower().endswith(".json"):
            df = pd.read_json(uploaded_file)

        st.success("✅ File uploaded successfully!")

        st.markdown('<div class="purple-sec-head anim-1">🩺 File Information</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f"""
            <div class="gloss-stat-box anim-1">
                <div class="gloss-stat-label"><span class="med-float">📋</span> File Name</div>
                <div class="gloss-stat-val">{uploaded_file.name}</div>
            </div>
            """, unsafe_allow_html=True)

        with col2:
            st.markdown(f"""
            <div class="gloss-stat-box anim-2">
                <div class="gloss-stat-label"><span class="med-float">🧬</span> Total Rows</div>
                <div class="gloss-stat-val">{len(df):,}</div>
            </div>
            """, unsafe_allow_html=True)

        with col3:
            st.markdown(f"""
            <div class="gloss-stat-box anim-3">
                <div class="gloss-stat-label"><span class="med-float">💊</span> Total Columns</div>
                <div class="gloss-stat-val">{len(df.columns)}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown('<div class="purple-sec-head anim-2">🫀 Health Data Preview</div>', unsafe_allow_html=True)
        st.dataframe(df, use_container_width=True)

        st.markdown('<div class="purple-sec-head anim-2">🧬 Basic Statistics</div>', unsafe_allow_html=True)
        numeric_columns = df.select_dtypes(include=["number"]).columns

        if len(numeric_columns) > 0:
            st.dataframe(df[numeric_columns].describe(), use_container_width=True)
        else:
            st.info("No numerical health data found.")

        st.markdown('<div class="purple-sec-head anim-3">💾 Download Data</div>', unsafe_allow_html=True)
        csv_data = df.to_csv(index=False)

        st.download_button(
            label="⬇️ Download as CSV",
            data=csv_data,
            file_name="health_data_export.csv",
            mime="text/csv"
        )

    except Exception as e:
        st.error(f"Error while reading file: {str(e)}")

else:
    st.info("Please upload a CSV or JSON health data file.")

    st.markdown('<div class="purple-sec-head anim-2">📋 Example CSV Format</div>', unsafe_allow_html=True)

    example_data = pd.DataFrame({
        "date": ["2026-10-25", "2026-10-26"],
        "weight": [40, 40.2],
        "steps": [5000, 6500],
        "sleep": [7, 7.5]
    })

    st.dataframe(example_data, use_container_width=True)

render_medical_disclaimer()