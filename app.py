import os
import sys
import streamlit as st

# =====================================================
# 1. PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="Aarogya-AI | Intelligent Wellness",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# 2. ROOT DIRECTORY
# =====================================================

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))

if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

# =====================================================
# 3. LOAD GLOBAL UI THEME FROM Ui.py
# =====================================================

try:
    from Ui import apply_glossy_purple_theme

    apply_glossy_purple_theme()

except Exception as e:
    st.error("Unable to load Ui.py")
    st.exception(e)
    st.stop()

# =====================================================
# 4. MODERN NAVIGATION CSS
# =====================================================

st.markdown("""
<style>

/* APP BACKGROUND */
.stApp {
    background:
        radial-gradient(
            circle at 10% 10%,
            rgba(139, 92, 246, 0.12),
            transparent 40%
        ),
        radial-gradient(
            circle at 90% 15%,
            rgba(192, 132, 252, 0.12),
            transparent 40%
        ),
        linear-gradient(
            145deg,
            #FAF7FF,
            #F3ECFF,
            #EDE9FE
        );
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(
        180deg,
        #FFFFFF 0%,
        #F6F0FF 50%,
        #EDE5FF 100%
    );

    border-right: 1px solid #E4D7FF;
    box-shadow: 5px 0 25px rgba(91, 33, 182, 0.07);
}

[data-testid="stSidebar"] > div:first-child {
    padding-top: 0.8rem;
}

/* BRAND */
.brand-box {
    margin: 10px 12px 22px;
    padding: 20px 16px;

    border-radius: 20px;

    background: linear-gradient(
        135deg,
        #2E1065 0%,
        #5B21B6 48%,
        #9333EA 100%
    );

    border: 1px solid rgba(255,255,255,0.3);

    box-shadow:
        0 12px 28px rgba(91,33,182,0.25),
        inset 0 1px 0 rgba(255,255,255,0.25);
}

.brand-title {
    color: #FFFFFF;
    font-size: 20px;
    font-weight: 800;
    letter-spacing: -0.4px;
}

.brand-sub {
    color: #E9D5FF;
    font-size: 10.5px;
    font-weight: 500;
    margin-top: 5px;
}

/* NAVIGATION HEADING */
.nav-caption {
    color: #7C3AED;
    font-size: 10px;
    font-weight: 800;
    letter-spacing: 1.5px;
    padding: 5px 18px 13px;
}

/* HIDE RADIO LABEL */
[data-testid="stSidebar"] .stRadio > label {
    display: none !important;
}

/* NAVIGATION GROUP */
[data-testid="stSidebar"] .stRadio
> div[role="radiogroup"] {

    display: flex;
    flex-direction: column;
    gap: 7px;

    padding: 0 12px 15px;
}

/* HIDE RADIO CIRCLE */
[data-testid="stSidebar"] .stRadio
[role="radiogroup"] label > div:first-child {
    display: none !important;
}

/* NAVIGATION ITEM */
[data-testid="stSidebar"] .stRadio
[role="radiogroup"] > label {

    min-height: 43px;
    padding: 10px 14px !important;

    margin: 0 !important;

    border-radius: 13px !important;

    background: transparent !important;
    border: 1px solid transparent !important;

    transition: all 0.22s ease !important;

    cursor: pointer !important;
}

/* HOVER EFFECT */
[data-testid="stSidebar"] .stRadio
[role="radiogroup"] > label:hover {

    background: #EDE5FF !important;
    border-color: #D8C5FF !important;

    transform: translateX(3px);
}

/* ACTIVE NAVIGATION */
[data-testid="stSidebar"] .stRadio
[role="radiogroup"] > label:has(input:checked) {

    background: linear-gradient(
        110deg,
        #5B21B6,
        #7C3AED,
        #9333EA
    ) !important;

    border: 1px solid #A78BFA !important;

    box-shadow:
        0 7px 18px rgba(109,40,217,0.25);
}

/* NAVIGATION TEXT */
[data-testid="stSidebar"] .stRadio
div[data-testid="stMarkdownContainer"] p {

    color: #4C1D95 !important;

    font-size: 12.5px !important;
    font-weight: 650 !important;

    margin: 0 !important;
    line-height: 1.4 !important;
}

/* ACTIVE TEXT */
[data-testid="stSidebar"] .stRadio
[role="radiogroup"] > label:has(input:checked)
div[data-testid="stMarkdownContainer"] p {

    color: #FFFFFF !important;
    font-weight: 700 !important;
}

/* SAFETY NOTICE */
.sidebar-safety-box {

    margin: 14px 12px 18px;
    padding: 15px;

    border-radius: 15px;

    background: rgba(255,255,255,0.85);

    border: 1px solid #DDD0FF;

    box-shadow: 0 5px 14px rgba(91,33,182,0.06);

    color: #475569;

    font-size: 11px;
    line-height: 1.7;
}

/* MAIN CONTENT */
.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1280px;
}

/* BUTTONS */
div.stButton > button {
    border-radius: 12px;
    transition: all 0.2s ease;
}

div.stButton > button:hover {
    transform: translateY(-2px);
}

/* MOBILE RESPONSIVE */
@media(max-width:768px) {

    .block-container {
        padding: 1.2rem 1rem 2rem 1rem !important;
    }

    .brand-title {
        font-size: 18px;
    }

}

</style>
""", unsafe_allow_html=True)

# =====================================================
# 5. SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:

    # BRAND SECTION
    st.markdown("""
    <div class="brand-box">

        <div style="
            display:flex;
            align-items:center;
            gap:12px;
        ">

            <div style="
                background:rgba(255,255,255,0.18);
                border:1px solid rgba(255,255,255,0.2);
                padding:11px;
                border-radius:14px;
                font-size:25px;
            ">
                🩺
            </div>

            <div>
                <div class="brand-title">
                    AAROGYA-AI
                </div>

                <div class="brand-sub">
                    Intelligent Wellness Companion
                </div>
            </div>

        </div>

    </div>
    """, unsafe_allow_html=True)

    # NAVIGATION HEADING
    st.markdown(
        '<div class="nav-caption">✦ HEALTH MODULES</div>',
        unsafe_allow_html=True
    )

    # NAVIGATION OPTIONS
    navigation = {
        "⌂   Dashboard": "home",
        "✧   AI Health Assistant": "assistant",
        "♡   Health Data": "data",
        "▥   Health Analysis": "analysis",
        "▤   Health Report": "report",
        "◎   Health Goals": "goals",
        "✦   Recommendations": "recommendations",
        "⚕   Symptom Information": "symptoms",
        "⬡   Medication Safety": "medication",
        "⚠   Emergency Detection": "emergency"
    }

    # SELECT PAGE
    selected_page = st.radio(
        "Navigation",
        list(navigation.keys()),
        key="main_navigation",
        label_visibility="collapsed"
    )

    page_key = navigation[selected_page]

    # SAFETY FOOTER
    st.markdown("""
    <div class="sidebar-safety-box">

        <b style="color:#6D28D9;">
            🛡️ Safety Notice
        </b>

        <br>

        General wellness guidance only.

        <br>

        Not a substitute for professional medical care.

    </div>
    """, unsafe_allow_html=True)


# =====================================================
# 6. PAGE ROUTES
# =====================================================

ROUTES = {

    "home":
        "pages/home.py",

    "assistant":
        "pages/13_AI_Health_Assistant.py",

    "data":
        "pages/3_Health_Data.py",

    "analysis":
        "pages/4_Health_Analysis.py",

    "report":
        "pages/5_Health_Report.py",

    "goals":
        "pages/7_Health_Goals.py",

    "recommendations":
        "pages/10_Health_Recommendations.py",

    "symptoms":
        "pages/9_Symptom_Information.py",

    "medication":
        "pages/11_Medication_Safety.py",

    "emergency":
        "pages/12_Emergency_Detection.py"
}


# =====================================================
# 7. PAGE LOADER
# =====================================================

def run_page(relative_path):

    full_path = os.path.join(
        ROOT_DIR,
        relative_path
    )

    # CHECK PAGE EXISTS
    if not os.path.isfile(full_path):

        st.error(
            f"Page file not found: {relative_path}"
        )

        st.info(
            "Please check the filename inside your pages folder."
        )

        return

    try:

        with open(
            full_path,
            "r",
            encoding="utf-8"
        ) as file:

            source_code = file.read()

        exec(
            compile(
                source_code,
                full_path,
                "exec"
            ),
            globals()
        )

    except Exception as error:

        st.error(
            f"Unable to load page: {relative_path}"
        )

        st.exception(error)


# =====================================================
# 8. RUN SELECTED PAGE
# =====================================================

run_page(ROUTES[page_key])