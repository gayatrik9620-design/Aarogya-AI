import streamlit as st


def apply_glossy_purple_theme():
    """Applies glossy purple gradient styling, glassmorphism cards, and animations."""
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

    /* Keyframe Animations */
    @keyframes violetEntrance {
        0% {
            opacity: 0;
            transform: translateY(18px) scale(0.985);
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
        display: inline-block;
        animation: medFloat 3.5s ease-in-out infinite;
    }

    /* Glossy Purple Banner */
    .ui-purple-banner {
        position: relative;
        overflow: hidden;
        border-radius: 24px;
        padding: 30px 36px;
        background: linear-gradient(130deg, #2E1065 0%, #5B21B6 48%, #7E22CE 100%);
        border: 1px solid rgba(255, 255, 255, 0.32);
        box-shadow:
            0 20px 44px rgba(76, 29, 149, 0.24),
            inset 0 1px 0 rgba(255, 255, 255, 0.48);
        color: #FFFFFF;
        margin-bottom: 24px;
    }

    .ui-purple-banner::before {
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

    .ui-badge-pill {
        display: inline-flex;
        align-items: center;
        gap: 8px;
        padding: 5px 14px;
        border-radius: 999px;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 0.3px;
        color: #F3E8FF;
        background: rgba(255, 255, 255, 0.15);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.30);
        margin-bottom: 12px;
    }

    .ui-pulse-dot {
        width: 8px;
        height: 8px;
        border-radius: 50%;
        background: #E879F9;
        animation: pulseViolet 2.2s infinite;
    }

    .ui-banner-title {
        font-size: 34px;
        font-weight: 800;
        letter-spacing: -0.6px;
        line-height: 1.15;
        margin: 0 0 6px 0;
        color: #FFFFFF;
    }

    .ui-banner-sub {
        font-size: 15px;
        color: #E9D5FF;
        margin: 0;
        line-height: 1.55;
    }

    /* Glossy Purple Card */
    .ui-gloss-card {
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
        margin-bottom: 18px;
        transition: transform 0.26s ease, box-shadow 0.26s ease, border-color 0.26s ease;
    }

    .ui-gloss-card:hover {
        transform: translateY(-4px);
        border-color: #C084FC;
        box-shadow:
            0 18px 34px rgba(126, 34, 206, 0.15),
            inset 0 1px 0 rgba(255, 255, 255, 1);
    }

    .ui-card-head {
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 17px;
        font-weight: 800;
        color: #2E1065;
        margin-bottom: 8px;
    }

    .ui-icon-chip {
        width: 38px;
        height: 38px;
        border-radius: 12px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 19px;
        background: linear-gradient(135deg, #FFFFFF 0%, #EDE9FE 100%);
        border: 1px solid rgba(192, 132, 252, 0.55);
        box-shadow: 0 5px 12px rgba(109, 40, 217, 0.10);
    }

    .ui-card-body {
        font-size: 14px;
        line-height: 1.6;
        color: #3B0764;
        margin: 0;
    }

    /* Streamlit Input & Button Gloss Polish */
    div.stButton > button {
        border-radius: 14px;
        font-weight: 700;
        border: 1px solid rgba(168, 85, 247, 0.45);
        background: linear-gradient(135deg, #6D28D9 0%, #7E22CE 100%);
        color: #FFFFFF;
        box-shadow: 0 8px 18px rgba(109, 40, 217, 0.20);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 12px 24px rgba(126, 34, 206, 0.30);
        color: #FFFFFF;
    }

    /* Glossy Medical Safety Notice */
    .ui-purple-safety {
        border-radius: 18px;
        padding: 15px 20px;
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


def render_page_banner(
    symbol: str,
    title: str,
    subtitle: str,
    badge: str = "🧬 Aarogya-AI Wellness Suite",
):
    """Renders an animated glossy purple top banner with a medical symbol."""
    st.markdown(
        f"""
    <div class="ui-purple-banner anim-1">
        <div class="ui-badge-pill">
            <span class="ui-pulse-dot"></span>
            {badge}
        </div>
        <div class="ui-banner-title"><span class="med-float">{symbol}</span> {title}</div>
        <p class="ui-banner-sub">{subtitle}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_gloss_card(
    title: str, body: str, symbol: str = "🩺", anim_class: str = "anim-2"
):
    """Renders a glossy purple card with a medical icon badge."""
    st.markdown(
        f"""
    <div class="ui-gloss-card {anim_class}">
        <div class="ui-card-head">
            <span class="ui-icon-chip med-float">{symbol}</span>
            <span>{title}</span>
        </div>
        <p class="ui-card-body">{body}</p>
    </div>
    """,
        unsafe_allow_html=True,
    )


def render_medical_disclaimer():
    """Renders the standard medical safety footer across pages."""
    st.markdown(
        """
    <div class="ui-purple-safety anim-3">
        <strong>🩺 Medical Safety Notice:</strong> Aarogya-AI provides general wellness information and educational support.
        It does not replace professional medical advice, diagnosis, or treatment.
    </div>
    """,
        unsafe_allow_html=True,
    )