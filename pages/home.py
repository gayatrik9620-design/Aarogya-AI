import os
import sqlite3
import streamlit as st

# =========================================================
# AAROGYA-AI GLOSSY PURPLE DASHBOARD (pages/home.py)
# =========================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

.stApp {
    background:
        radial-gradient(circle at 10% 12%, rgba(139, 92, 246, 0.20), transparent 42%),
        radial-gradient(circle at 90% 15%, rgba(192, 132, 252, 0.18), transparent 40%),
        radial-gradient(circle at 50% 92%, rgba(99, 102, 241, 0.14), transparent 48%),
        linear-gradient(155deg, #FAF7FF 0%, #F3ECFF 48%, #EDE9FE 100%);
    font-family: 'Plus Jakarta Sans', sans-serif;
    color: #1E1035;
}

/* Smooth Keyframe Animations */
@keyframes violetEntrance {
    0% {
        opacity: 0;
        transform: translateY(20px) scale(0.985);
    }
    100% {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

@keyframes glassSweep {
    0% {
        transform: translateX(-140%) skewX(-22deg);
    }
    55%, 100% {
        transform: translateX(250%) skewX(-22deg);
    }
}

@keyframes medFloat {
    0%, 100% {
        transform: translateY(0px) rotate(0deg);
    }
    50% {
        transform: translateY(-6px) rotate(2deg);
    }
}

@keyframes pulseViolet {
    0% {
        box-shadow: 0 0 0 0 rgba(168, 85, 247, 0.6);
    }
    70% {
        box-shadow: 0 0 0 11px rgba(168, 85, 247, 0);
    }
    100% {
        box-shadow: 0 0 0 0 rgba(168, 85, 247, 0);
    }
}

.anim-1 { animation: violetEntrance 0.55s cubic-bezier(0.22, 1, 0.36, 1) both; }
.anim-2 { animation: violetEntrance 0.62s cubic-bezier(0.22, 1, 0.36, 1) 0.08s both; }
.anim-3 { animation: violetEntrance 0.62s cubic-bezier(0.22, 1, 0.36, 1) 0.16s both; }
.anim-4 { animation: violetEntrance 0.62s cubic-bezier(0.22, 1, 0.36, 1) 0.24s both; }

.med-float {
    animation: medFloat 3.5s ease-in-out infinite;
}

/* Glossy Purple Hero Banner */
.purple-hero {
    position: relative;
    overflow: hidden;
    border-radius: 26px;
    padding: 36px 40px;
    background: linear-gradient(130deg, #2E1065 0%, #5B21B6 48%, #7E22CE 100%);
    border: 1px solid rgba(255, 255, 255, 0.32);
    box-shadow:
        0 22px 48px rgba(76, 29, 149, 0.26),
        inset 0 1px 0 rgba(255, 255, 255, 0.50);
    color: #FFFFFF;
    margin-bottom: 26px;
}

.purple-hero::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 45%;
    height: 100%;
    background: linear-gradient(
        90deg,
        rgba(255, 255, 255, 0) 0%,
        rgba(255, 255, 255, 0.22) 50%,
        rgba(255, 255, 255, 0) 100%
    );
    animation: glassSweep 5.8s ease-in-out infinite;
    pointer-events: none;
}

.purple-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    padding: 6px 15px;
    border-radius: 999px;
    font-size: 12px;
    font-weight: 700;
    letter-spacing: 0.4px;
    color: #F3E8FF;
    background: rgba(255, 255, 255, 0.15);
    backdrop-filter: blur(10px);
    -webkit-backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.30);
    margin-bottom: 14px;
}

.violet-dot {
    width: 8px;
    height: 8px;
    border-radius: 50%;
    background: #E879F9;
    animation: pulseViolet 2.2s infinite;
}

.purple-hero-title {
    font-size: 40px;
    font-weight: 800;
    letter-spacing: -0.7px;
    line-height: 1.15;
    margin: 0 0 8px 0;
    color: #FFFFFF;
    text-shadow: 0 2px 16px rgba(24, 9, 58, 0.35);
}

.purple-hero-sub {
    font-size: 17px;
    font-weight: 600;
    color: #E9D5FF;
    margin-bottom: 10px;
}

.purple-hero-desc {
    font-size: 15px;
    line-height: 1.65;
    color: rgba(250, 245, 255, 0.92);
    max-width: 740px;
    margin: 0;
}

/* Section Headers */
.purple-section {
    font-size: 21px;
    font-weight: 800;
    color: #2E1065;
    letter-spacing: -0.3px;
    margin: 26px 0 14px 0;
}

/* Glossy Purple KPI Cards */
.gloss-purple-kpi {
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    padding: 22px;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.94) 0%, rgba(245, 240, 255, 0.78) 100%);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(216, 180, 254, 0.75);
    box-shadow:
        0 12px 28px rgba(109, 40, 217, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.98);
    transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.28s ease, border-color 0.28s ease;
}

.gloss-purple-kpi:hover {
    transform: translateY(-5px);
    border-color: #C084FC;
    box-shadow:
        0 20px 38px rgba(126, 34, 206, 0.18),
        inset 0 1px 0 rgba(255, 255, 255, 1);
}

.gloss-kpi-label {
    font-size: 13px;
    font-weight: 700;
    color: #5B21B6;
    margin-bottom: 8px;
}

.gloss-kpi-value {
    font-size: 30px;
    font-weight: 800;
    color: #1E1035;
    letter-spacing: -0.6px;
    margin-bottom: 4px;
}

.gloss-kpi-accent {
    font-size: 12px;
    font-weight: 700;
    color: #7E22CE;
}

/* Glossy Quick Access Cards */
.gloss-purple-qa {
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    padding: 22px;
    min-height: 156px;
    background: linear-gradient(160deg, rgba(255, 255, 255, 0.95) 0%, rgba(243, 232, 255, 0.75) 100%);
    backdrop-filter: blur(14px);
    -webkit-backdrop-filter: blur(14px);
    border: 1px solid rgba(216, 180, 254, 0.80);
    box-shadow:
        0 10px 24px rgba(109, 40, 217, 0.07),
        inset 0 1px 0 rgba(255, 255, 255, 0.98);
    transition: transform 0.28s cubic-bezier(0.22, 1, 0.36, 1), box-shadow 0.28s ease, border-color 0.28s ease;
}

.gloss-purple-qa:hover {
    transform: translateY(-6px);
    border-color: #A855F7;
    box-shadow:
        0 20px 36px rgba(126, 34, 206, 0.18),
        inset 0 1px 0 rgba(255, 255, 255, 1);
}

.med-icon-box {
    width: 44px;
    height: 44px;
    border-radius: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 21px;
    background: linear-gradient(135deg, #FFFFFF 0%, #EDE9FE 100%);
    border: 1px solid rgba(192, 132, 252, 0.55);
    box-shadow: 0 6px 14px rgba(109, 40, 217, 0.10);
    margin-bottom: 12px;
}

.gloss-qa-title {
    font-size: 16px;
    font-weight: 800;
    color: #1E1035;
    margin-bottom: 6px;
}

.gloss-qa-desc {
    font-size: 13px;
    line-height: 1.55;
    color: #4C1D95;
    margin: 0;
}

/* Glossy Wellness Insight Cards */
.gloss-purple-insight {
    border-radius: 20px;
    padding: 20px;
    background: linear-gradient(155deg, rgba(255, 255, 255, 0.92) 0%, rgba(245, 243, 255, 0.80) 100%);
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(216, 180, 254, 0.75);
    border-left: 4px solid #7E22CE;
    box-shadow:
        0 8px 20px rgba(109, 40, 217, 0.06),
        inset 0 1px 0 rgba(255, 255, 255, 0.95);
    transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.gloss-purple-insight:hover {
    transform: translateY(-3px);
    box-shadow: 0 14px 26px rgba(109, 40, 217, 0.12);
}

.gloss-insight-title {
    font-size: 15px;
    font-weight: 800;
    color: #2E1065;
    margin-bottom: 6px;
}

.gloss-insight-body {
    font-size: 13.5px;
    line-height: 1.55;
    color: #3B0764;
    margin: 0;
}

/* Glossy AI Intelligence Box */
.gloss-purple-ai {
    border-radius: 22px;
    padding: 18px 22px;
    background: linear-gradient(120deg, rgba(243, 232, 255, 0.95), rgba(224, 231, 255, 0.92));
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid rgba(192, 132, 252, 0.70);
    box-shadow:
        0 10px 24px rgba(109, 40, 217, 0.08),
        inset 0 1px 0 rgba(255, 255, 255, 0.98);
    color: #1E1035;
    font-size: 14px;
    line-height: 1.6;
}

/* Glossy Medical Safety Notice */
.gloss-purple-safety {
    border-radius: 18px;
    padding: 16px 20px;
    background: linear-gradient(120deg, rgba(250, 245, 255, 0.96), rgba(243, 232, 255, 0.88));
    border: 1px solid rgba(192, 132, 252, 0.65);
    border-left: 5px solid #6D28D9;
    color: #2E1065;
    font-size: 13.5px;
    line-height: 1.55;
    margin-top: 24px;
    box-shadow: 0 8px 18px rgba(109, 40, 217, 0.08);
}
</style>
""",
    unsafe_allow_html=True,
)


# =========================================================
# DATABASE
# =========================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


@st.cache_data(ttl=30)
def get_health_data():
  data = {"weight": None, "steps": None, "sleep": None}

  db_path = os.path.join(BASE_DIR, "health_data.db")
  if not os.path.exists(db_path):
    return data

  try:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    cursor.execute("""
            SELECT name
            FROM sqlite_master
            WHERE type='table'
        """)
    tables = [row[0] for row in cursor.fetchall()]

    for table in tables:
      try:
        safe_table = table.replace('"', '""')
        cursor.execute(f'PRAGMA table_info("{safe_table}")')
        columns_info = cursor.fetchall()
        columns = [str(column[1]).lower() for column in columns_info]

        if not columns:
          continue

        cursor.execute(
            f'SELECT * FROM "{safe_table}" ORDER BY rowid DESC LIMIT 1'
        )
        row = cursor.fetchone()

        if row:
          for index, column in enumerate(columns):
            value = row[index]
            if value is None:
              continue

            if "weight" in column:
              data["weight"] = value
            elif "step" in column:
              data["steps"] = value
            elif "sleep" in column or "rest" in column:
              data["sleep"] = value
      except Exception:
        continue

    conn.close()
  except Exception:
    pass

  return data


health = get_health_data()


# =========================================================
# HERO
# =========================================================

st.markdown(
    """
<div class="purple-hero anim-1">
    <div class="purple-pill">
        <span class="violet-dot"></span>
        🧬 Aarogya-AI Clinical Wellness Suite
    </div>
    <div class="purple-hero-title">🩺 Aarogya-AI</div>
    <div class="purple-hero-sub">Your Intelligent Wellness &amp; Health Monitoring Companion</div>
    <p class="purple-hero-desc">
        Monitor your health data, understand wellness trends, explore health insights
        and interact with your AI-powered health assistant — all from one place.
    </p>
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# HEALTH OVERVIEW
# =========================================================

st.markdown(
    '<div class="purple-section anim-1">🫀 Health Overview</div>',
    unsafe_allow_html=True,
)

weight_display = (
    f"{health['weight']} kg" if health["weight"] is not None else "No data"
)
steps_display = (
    f"{health['steps']:,}" if health["steps"] is not None else "No data"
)
sleep_display = (
    f"{health['sleep']} hrs" if health["sleep"] is not None else "No data"
)

c1, c2, c3 = st.columns(3)

with c1:
  st.markdown(
      f"""
    <div class="gloss-purple-kpi anim-2">
        <div class="gloss-kpi-label">⚖️ Body Mass / Weight</div>
        <div class="gloss-kpi-value">{weight_display}</div>
        <div class="gloss-kpi-accent">Latest recorded measurement</div>
    </div>
    """,
      unsafe_allow_html=True,
  )

with c2:
  st.markdown(
      f"""
    <div class="gloss-purple-kpi anim-3">
        <div class="gloss-kpi-label">🩺 Daily Activity Steps</div>
        <div class="gloss-kpi-value">{steps_display}</div>
        <div class="gloss-kpi-accent">Active movement log</div>
    </div>
    """,
      unsafe_allow_html=True,
  )

with c3:
  st.markdown(
      f"""
    <div class="gloss-purple-kpi anim-4">
        <div class="gloss-kpi-label">💤 Recovery Sleep</div>
        <div class="gloss-kpi-value">{sleep_display}</div>
        <div class="gloss-kpi-accent">Recent rest duration</div>
    </div>
    """,
      unsafe_allow_html=True,
  )


# =========================================================
# QUICK ACCESS
# =========================================================

st.markdown(
    '<div class="purple-section anim-1">🩺 Quick Access Modules</div>',
    unsafe_allow_html=True,
)

q1, q2, q3, q4 = st.columns(4)

with q1:
  st.markdown(
      """
    <div class="gloss-purple-qa anim-2">
        <div class="med-icon-box med-float">🩺</div>
        <div class="gloss-qa-title">AI Assistant</div>
        <p class="gloss-qa-desc">Get general wellness guidance from your AI assistant.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

with q2:
  st.markdown(
      """
    <div class="gloss-purple-qa anim-3">
        <div class="med-icon-box med-float">🫀</div>
        <div class="gloss-qa-title">Health Data</div>
        <p class="gloss-qa-desc">Record and review your health measurements.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

with q3:
  st.markdown(
      """
    <div class="gloss-purple-qa anim-4">
        <div class="med-icon-box med-float">🧬</div>
        <div class="gloss-qa-title">Analysis</div>
        <p class="gloss-qa-desc">Explore your health trends and insights.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )

with q4:
  st.markdown(
      """
    <div class="gloss-purple-qa anim-4">
        <div class="med-icon-box med-float">💊</div>
        <div class="gloss-qa-title">Health Goals</div>
        <p class="gloss-qa-desc">Track your wellness objectives and progress.</p>
    </div>
    """,
      unsafe_allow_html=True,
  )


# =========================================================
# WELLNESS INSIGHTS
# =========================================================

st.markdown(
    '<div class="purple-section anim-1">🧬 Wellness Insights</div>',
    unsafe_allow_html=True,
)

i1, i2, i3 = st.columns(3)

with i1:
  st.markdown(
      """
    <div class="gloss-purple-insight anim-2">
        <div class="gloss-insight-title">🩺 Activity Overview</div>
        <p class="gloss-insight-body">
            Keep your daily activity records updated to understand your wellness patterns over time.
        </p>
    </div>
    """,
      unsafe_allow_html=True,
  )

with i2:
  st.markdown(
      """
    <div class="gloss-purple-insight anim-3">
        <div class="gloss-insight-title">💤 Sleep Tracking</div>
        <p class="gloss-insight-body">
            Regular sleep tracking helps you observe changes in your personal wellness routine.
        </p>
    </div>
    """,
      unsafe_allow_html=True,
  )

with i3:
  st.markdown(
      """
    <div class="gloss-purple-insight anim-4">
        <div class="gloss-insight-title">📋 Tracking Status</div>
        <p class="gloss-insight-body">
            Your health tracking data is being monitored through the available health records.
        </p>
    </div>
    """,
      unsafe_allow_html=True,
  )


# =========================================================
# AI FEATURE
# =========================================================

st.markdown(
    '<div class="purple-section anim-1">🧬 Aarogya-AI Intelligence</div>',
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="gloss-purple-ai anim-2">
    <strong>✨ Smarter wellness, powered by AI.</strong><br>
    Aarogya-AI combines health tracking, wellness insights, AI assistance and safety-focused features in one platform.
</div>
""",
    unsafe_allow_html=True,
)


# =========================================================
# SAFETY NOTICE
# =========================================================

st.markdown(
    """
<div class="gloss-purple-safety anim-3">
    <strong>🛡️ Safety Notice:</strong> Aarogya-AI provides general wellness information and educational support.
    It does not replace professional medical advice, diagnosis or treatment.
</div>
""",
    unsafe_allow_html=True,
)