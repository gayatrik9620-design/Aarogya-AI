"""MedCheck: Dose-Timing & Meal/Side-Effect Check-In Assistant. Run: streamlit run app.py"""
from datetime import date, time

import streamlit as st
import streamlit.components.v1 as components

import agent
import charts
import database as db
from config import APP_NAME, DISCLAIMER, FOOD_RULES, GOOGLE_API_KEY, MEAL_OPTIONS, SYMPTOMS

st.set_page_config(page_title=APP_NAME, page_icon="🩺", layout="wide")
db.init_db()

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Nunito+Sans:wght@400;600;700;800&family=Outfit:wght@600;700;800&display=swap');
:root { --ink:#12343f; --soft:#35606b; --teal:#0d9488; --teal2:#14b8a6; --coral:#fb7185; }
.stApp, .stApp p, .stApp label, .stApp li, .stApp input, .stApp textarea, [data-baseweb] {
  font-family: 'Nunito Sans', sans-serif; color: var(--ink); font-size: 1.05rem; }
.stApp { background:
  radial-gradient(900px 500px at 8% -5%, rgba(20,184,166,.28) 0%, transparent 60%),
  radial-gradient(800px 500px at 100% 0%, rgba(251,113,133,.16) 0%, transparent 55%),
  linear-gradient(160deg, #f0fdfa 0%, #e0f2fe 55%, #ecfeff 100%); background-attachment: fixed; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 1.6rem; max-width: 1150px; position: relative; z-index: 1; }
.stApp h1, .stApp h2, .stApp h3 { font-family: 'Outfit', sans-serif; color: var(--ink); font-weight: 700; }
.hero { display: flex; align-items: center; gap: 16px; flex-wrap: wrap; }
.hero .logo { width: 54px; height: 54px; border-radius: 16px; display: grid; place-items: center;
  background: linear-gradient(135deg, #0d9488, #14b8a6); box-shadow: 0 8px 20px rgba(13,148,136,.35); }
.stApp .hero .title { font-family: 'Outfit', sans-serif; font-size: 2.4rem; font-weight: 800; color: var(--ink); line-height: 1; }
.ecg path { fill: none; stroke: var(--teal); stroke-width: 2.5; stroke-linecap: round; stroke-linejoin: round;
  stroke-dasharray: 30 70; animation: ecg 2.6s linear infinite; }
@keyframes ecg { from { stroke-dashoffset: 100; } to { stroke-dashoffset: 0; } }
.glass { background: rgba(255,255,255,.68); border: 1px solid rgba(13,148,136,.22); border-radius: 20px;
  padding: 1.1rem 1.3rem; backdrop-filter: blur(14px); -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 8px 28px rgba(13,148,136,.14); margin-bottom: .9rem; }
.stApp .metric-label { font-size: .92rem; color: var(--soft); font-weight: 600; }
.stApp .metric-value { font-family: 'Outfit', sans-serif; font-size: 2.2rem; font-weight: 800; line-height: 1.15; color: var(--teal); }
.stApp .pill { display: inline-block; padding: 2px 12px; border-radius: 999px; font-size: .8rem; font-weight: 800; }
.stApp .pill.taken { background: #ccfbf1; color: #0f766e; } .stApp .pill.pending { background: #e0f2fe; color: #075985; }
.stApp .pill.skipped { background: #fef3c7; color: #92400e; } .stApp .pill.missed { background: #ffe4e6; color: #9f1239; }
.stApp .banner { border-radius: 14px; padding: .75rem 1rem; margin: .4rem 0 .8rem; font-weight: 600; border-left: 5px solid; }
.stApp .banner.ok { background: #ccfbf1; border-color: #0d9488; color: #0f4f4a; }
.stApp .banner.info { background: #e0f2fe; border-color: #0284c7; color: #0c4a6e; }
.stApp .banner.warn { background: #fef3c7; border-color: #f59e0b; color: #78350f; }
.stTabs [data-baseweb="tab-list"] { gap: 6px; background: rgba(255,255,255,.75); padding: 6px; border-radius: 16px;
  border: 1px solid rgba(13,148,136,.2); }
.stTabs [data-baseweb="tab"] { border-radius: 12px; padding: 8px 16px; height: auto; }
.stTabs [data-baseweb="tab"] p { color: #2f5d68; font-weight: 700; }
.stTabs [aria-selected="true"] { background: linear-gradient(135deg, #0d9488, #14b8a6); }
.stTabs [aria-selected="true"] p { color: #fff; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }
.stButton > button, .stDownloadButton > button, .stFormSubmitButton > button {
  background: linear-gradient(135deg, #0d9488, #14b8a6); border: 0; border-radius: 12px;
  box-shadow: 0 4px 14px rgba(13,148,136,.3); transition: transform .15s; }
.stButton > button:hover, .stDownloadButton > button:hover, .stFormSubmitButton > button:hover { transform: translateY(-1px); }
.stButton button p, .stDownloadButton button p, .stFormSubmitButton button p { color: #fff; font-weight: 800; }
.stButton > button:focus-visible { outline: 3px solid #12343f; }
[data-testid="stSidebar"] { display: none; }
.stApp .disclaimer { font-size: .85rem; color: var(--soft); text-align: center; margin-top: 1.5rem; }
div[data-testid="stElementContainer"]:has(iframe[height="0"]) { height: 0; margin: 0; overflow: hidden; }
.floaters i, .floaters b { position: fixed; bottom: -80px; left: var(--x); opacity: .30; pointer-events: none; z-index: 0;
  animation: drift var(--d) linear infinite; animation-delay: var(--delay, 0s); }
.floaters i { width: var(--s); height: calc(var(--s) * .42); border-radius: 999px;
  background: linear-gradient(90deg, #0d9488 50%, #fb7185 50%); }
.floaters b { width: var(--s); height: var(--s); background:
  linear-gradient(#14b8a6,#14b8a6) center/30% 100% no-repeat, linear-gradient(#14b8a6,#14b8a6) center/100% 30% no-repeat; }
@keyframes drift { from { transform: translateY(0) rotate(0deg); } to { transform: translateY(-120vh) rotate(360deg); } }
@media (prefers-reduced-motion: reduce) { .floaters, .ecg path { animation: none; display: none; } }
/* ---- Readability guard: force dark text on light surfaces whatever theme Streamlit/the browser uses ---- */
.stApp { color-scheme: light; }
[data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stMainBlockContainer"] { background: transparent; }
.stApp :is(h1,h2,h3,h4,h5,h6,p,span,label,li,small,strong,b,em,td,th,legend,summary) { color: var(--ink); }
.stApp [data-testid="stWidgetLabel"] *, .stApp label * { color: var(--ink); font-weight: 700; }
.stApp [data-testid="stCaptionContainer"] * { color: var(--soft); }
.stApp [data-testid="stSlider"] div { color: var(--ink); }
header[data-testid="stHeader"] * { color: var(--ink); }
.stApp input, .stApp textarea, .stApp [data-baseweb="select"] *, .stApp [data-baseweb="input"],
.stApp [data-baseweb="base-input"], .stApp [data-baseweb="textarea"], .stApp [data-testid="stNumberInput"] button {
  background-color: #fff; color: var(--ink); -webkit-text-fill-color: var(--ink); }
.stApp input::placeholder, .stApp textarea::placeholder { color: #6b8a93; -webkit-text-fill-color: #6b8a93; }
.stApp [data-baseweb="select"] > div, .stApp [data-baseweb="input"], .stApp [data-baseweb="textarea"] {
  border: 1px solid rgba(13,148,136,.4); border-radius: 10px; }
[data-baseweb="popover"], [data-baseweb="popover"] > div, [data-baseweb="popover"] ul, [data-baseweb="menu"],
[data-baseweb="calendar"], [data-baseweb="calendar"] div { background: #fff; color: var(--ink); }
[data-baseweb="popover"] li, [data-baseweb="popover"] li *, [data-baseweb="popover"] [role="option"],
[data-baseweb="popover"] [role="option"] * { background: #fff; color: var(--ink); font-weight: 600; }
[data-baseweb="popover"] li:hover, [data-baseweb="popover"] li:hover *,
[data-baseweb="popover"] [aria-selected="true"], [data-baseweb="popover"] [aria-selected="true"] * { background: #ccfbf1; }
[data-baseweb="calendar"] [aria-selected="true"], [data-baseweb="calendar"] [aria-selected="true"] * { background: #0d9488; color: #fff; }
</style>
<div class="floaters">
  <i style="--x:6%;--s:38px;--d:34s"></i><i style="--x:28%;--s:28px;--d:42s;--delay:-14s"></i>
  <b style="--x:47%;--s:26px;--d:38s;--delay:-6s"></b><i style="--x:66%;--s:34px;--d:46s;--delay:-22s"></i>
  <b style="--x:82%;--s:30px;--d:36s;--delay:-18s"></b><i style="--x:94%;--s:26px;--d:40s;--delay:-3s"></i>
</div>
"""
st.markdown(CSS, unsafe_allow_html=True)
CURSOR_JS = """<script>
(function () {
  const win = window.parent, doc = win.document;
  if (doc.getElementById('mc-cursor')) return;
  if (win.matchMedia('(prefers-reduced-motion: reduce)').matches || win.matchMedia('(pointer: coarse)').matches) return;
  const st = doc.createElement('style');
  st.textContent = `
  html.mc-on, html.mc-on * { cursor: none !important; }
  #mc-cursor{position:fixed;top:0;left:0;width:30px;height:13px;margin:-6.5px 0 0 -15px;border-radius:999px;
    pointer-events:none;z-index:99999;opacity:0;transition:opacity .15s;will-change:transform;
    background:linear-gradient(90deg,#0d9488 50%,#fb7185 50%);
    box-shadow:0 3px 10px rgba(13,148,136,.45),inset 0 0 0 1.5px rgba(255,255,255,.85)}
  #mc-cursor::after{content:"";position:absolute;left:50%;top:0;bottom:0;width:1.5px;margin-left:-.75px;background:rgba(255,255,255,.85)}
  .mc-plus{position:fixed;pointer-events:none;z-index:99998;width:12px;height:12px;margin:-6px 0 0 -6px;
    background:linear-gradient(#14b8a6,#14b8a6) center/30% 100% no-repeat,linear-gradient(#14b8a6,#14b8a6) center/100% 30% no-repeat;
    animation:mcfade .9s ease-out forwards}
  @keyframes mcfade{from{opacity:.9;transform:translateY(0) scale(1)}to{opacity:0;transform:translateY(-22px) scale(.4)}}`;
  doc.head.appendChild(st);
  const pill = doc.createElement('div'); pill.id = 'mc-cursor'; doc.body.appendChild(pill);
  const root = doc.documentElement;
  const CLICKABLE = 'button,a,[role="tab"],[role="button"],[data-baseweb="select"],input,textarea,label,summary';
  let x = 0, y = 0, ang = -35, target = -35, scale = 1, lx = 0, ly = 0, pe = 0;
  doc.addEventListener('mousemove', e => {
    if (!root.classList.contains('mc-on')) { root.classList.add('mc-on'); lx = e.clientX; ly = e.clientY; }
    pill.style.opacity = 1;
    const dx = e.clientX - x, dy = e.clientY - y;
    if (Math.hypot(dx, dy) > 3) target = Math.atan2(dy, dx) * 180 / Math.PI;   // face the direction of travel
    x = e.clientX; y = e.clientY;
    scale = e.target.closest && e.target.closest(CLICKABLE) ? 1.35 : 1;          // grows over clickable things
    if (Math.hypot(x - lx, y - ly) > 45) {                                        // drop a small "+" along the path
      lx = x; ly = y;
      const p = doc.createElement('div'); p.className = 'mc-plus';
      p.style.left = x + 'px'; p.style.top = y + 'px'; doc.body.appendChild(p);
      setTimeout(() => p.remove(), 900);
    }
  });
  doc.addEventListener('mouseleave', () => { pill.style.opacity = 0; });
  doc.addEventListener('mousedown', () => { scale = 0.85; });
  doc.addEventListener('mouseup', () => { scale = 1; });
  (function loop() {
    let d = ((target - ang + 540) % 360) - 180; ang += d * 0.15;                  // smooth turning
    pill.style.transform = `translate(${x}px,${y}px) rotate(${ang}deg) scale(${scale})`;
    win.requestAnimationFrame(loop);
  })();
})();
</script>
"""
components.html(CURSOR_JS, height=0)


def metric(label, value, sub=""):
    st.markdown(f'<div class="glass"><div class="metric-label">{label}</div>'
                f'<div class="metric-value">{value}</div><div class="metric-label">{sub}</div></div>',
                unsafe_allow_html=True)


_MAP = {"#8b5cf6": "#0d9488", "#c4b5fd": "#14b8a6", "#f0abfc": "#fb7185"}   # old violet -> teal/coral
_STATUS = {"taken": "#0d9488", "skipped": "#f59e0b", "missed": "#fb7185"}


def _recolor(fig):
    """Keep every chart in the teal/coral palette, even if charts.py is an older copy."""
    for t in fig.data:
        if t.type == "pie":
            t.marker.colors = [_STATUS.get(str(label), "#0d9488") for label in t.labels]
            continue
        if isinstance(t.marker.color, str):
            t.marker.color = _MAP.get(t.marker.color.lower(), t.marker.color)
        if t.type == "scatter":
            if isinstance(t.line.color, str):
                t.line.color = _MAP.get(t.line.color.lower(), t.line.color)
            if t.fillcolor and "139,92,246" in t.fillcolor:
                t.fillcolor = "rgba(13,148,136,0.22)"


def show_chart(container, fig, key):
    """Draw a Plotly chart with dark readable text and enough margin so no label is cut off."""
    ink, grid = "#12343f", "rgba(18,52,63,0.12)"
    _recolor(fig)
    fig.update_layout(font=dict(color=ink, size=13), title_font=dict(color=ink, size=16),
                      legend=dict(font=dict(color=ink)), paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      margin=dict(l=24, r=24, t=64, b=24), height=340)
    fig.update_xaxes(tickfont=dict(color=ink), title_text="", gridcolor=grid, linecolor=grid, automargin=True)
    fig.update_yaxes(tickfont=dict(color=ink), title_text="", gridcolor=grid, linecolor=grid, automargin=True)
    fig.update_traces(textfont_color=ink, selector=dict(type="bar"))
    container.plotly_chart(fig, use_container_width=True, theme=None, key=key, config={"displayModeBar": False})


def banner(level, msg):
    """Readable status message (ok / info / warn)."""
    import re as _re
    html = _re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", msg)
    st.markdown(f'<div class="banner {level}">{html}</div>', unsafe_allow_html=True)


def flash(level, msg):
    banner(level, msg)


# ---------- Header ----------
mode = " - Gemini AI assistant on" if GOOGLE_API_KEY else ""
st.markdown(f"""<div class="hero"><div class="logo"><svg width="30" height="30" viewBox="0 0 24 24" fill="#fff">
<path d="M9 2h6v7h7v6h-7v7H9v-7H2V9h7z"/></svg></div><div class="title">{APP_NAME}</div>
<svg class="ecg" width="240" height="44" viewBox="0 0 240 44"><path pathLength="100" d="M0 24H70L80 24L90 6L104 40L116 16L124 24H240"/></svg></div>""",
            unsafe_allow_html=True)
st.caption(f"Dose timing, meal and side-effect check-ins{mode}")

tabs = st.tabs(["Overview", "Today's doses", "Check-in", "Wellness", "Medicines", "Assistant", "Export"])
sched = db.today_schedule()

# ---------- Overview ----------
with tabs[0]:
    taken = int((sched["status"] == "taken").sum())
    wl = db.get_wellness(1)
    today_row = wl[wl["log_date"] == str(date.today())]
    steps = int(today_row["steps"].iloc[0]) if not today_row.empty else 0
    c1, c2, c3, c4 = st.columns(4)
    with c1: metric("7-day adherence", f"{db.adherence_pct(7)}%", "doses taken on record")
    with c2: metric("Today", f"{taken}/{len(sched)}", "doses taken")
    with c3: metric("Steps today", f"{steps:,}", "log them in Wellness")
    with c4: metric("Medicines", len(sched), "active")
    a, b = st.columns([3, 2])
    show_chart(a, charts.adherence_by_day(), "pc1")
    show_chart(b, charts.status_mix(), "pc2")
    a, b = st.columns(2)
    show_chart(a, charts.adherence_by_med(), "pc3")
    show_chart(b, charts.steps_chart(), "pc4")

# ---------- Today's doses ----------
with tabs[1]:
    st.subheader("Today's schedule")
    if sched.empty:
        banner("info", "No medicines yet. Add one in the Medicines tab.")
    for _, r in sched.iterrows():
        st.markdown(f'<div class="glass"><b>{r["schedule_time"]} · {r["name"]}</b> {r["dose"]} '
                    f'<span class="pill {r["status"]}">{r["status"]}</span><br>'
                    f'<span class="metric-label">{FOOD_RULES.get(r["food_rule"], "Any time")}. {r["notes"] or ""}</span></div>',
                    unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns([2, 1, 1, 3])
        meal = c1.selectbox("Food context", MEAL_OPTIONS, key=f"meal{r['id']}", label_visibility="collapsed")
        if c2.button("Taken", key=f"t{r['id']}", use_container_width=True):
            db.log_dose(int(r["id"]), "taken", meal)
            st.session_state[f"msg{r['id']}"] = agent.timing_check(r["food_rule"], meal, r["schedule_time"])
            st.rerun()
        if c3.button("Skipped", key=f"s{r['id']}", use_container_width=True):
            db.log_dose(int(r["id"]), "skipped")
            st.session_state[f"msg{r['id']}"] = ("info", "Skipped dose logged. Ask your doctor what to do if you skip often.")
            st.rerun()
        if f"msg{r['id']}" in st.session_state:
            flash(*st.session_state[f"msg{r['id']}"])
        c4.caption(f"Note: {agent.med_note(r['name'])}")

# ---------- Check-in ----------
with tabs[2]:
    st.subheader("How are you feeling?")
    meds = db.get_meds()
    with st.form("checkin", clear_on_submit=True):
        c1, c2 = st.columns(2)
        med_name = c1.selectbox("Medicine", ["General"] + list(meds["name"]))
        meal = c2.selectbox("Meal timing", MEAL_OPTIONS)
        symptom = c1.selectbox("Comfort or side effect", SYMPTOMS)
        severity = c2.slider("How strong? (1 mild, 5 severe)", 1, 5, 1)
        note = st.text_input("Note (optional)")
        if st.form_submit_button("Save check-in"):
            mid = None if med_name == "General" else int(meds[meds["name"] == med_name]["id"].iloc[0])
            db.add_checkin(mid, meal, symptom, severity, note)
            banner("ok", "Check-in saved.")
            if symptom != "None":
                flash("warn" if severity >= 3 else "info", agent.severity_advice(severity))
    a, b = st.columns([3, 2])
    a.dataframe(db.get_checkins(20), use_container_width=True, hide_index=True)
    show_chart(b, charts.symptom_chart(), "pc5")

# ---------- Wellness ----------
with tabs[3]:
    st.subheader("Daily wellness log")
    with st.form("wellness"):
        c1, c2, c3, c4 = st.columns(4)
        day = c1.date_input("Date", date.today())
        steps_in = c2.number_input("Steps", 0, 100000, 5000, 500)
        water = c3.number_input("Water (ml)", 0, 10000, 2000, 250)
        sleep = c4.number_input("Sleep (hrs)", 0.0, 24.0, 7.0, 0.5)
        notes = st.text_input("Health notes")
        if st.form_submit_button("Save log"):
            db.save_wellness(day, steps_in, water, sleep, notes)
            banner("ok", "Wellness log saved.")
    a, b = st.columns(2)
    show_chart(a, charts.steps_chart(), "pc6")
    show_chart(b, charts.sleep_water_chart(), "pc7")
    st.dataframe(db.get_wellness(30).sort_values("log_date", ascending=False), use_container_width=True, hide_index=True)

# ---------- Medicines ----------
with tabs[4]:
    st.subheader("Your medicines")
    with st.form("addmed", clear_on_submit=True):
        c1, c2, c3, c4 = st.columns(4)
        name = c1.text_input("Name")
        dose = c2.text_input("Dose", placeholder="500 mg")
        t = c3.time_input("Time", time(8, 0))
        rule = c4.selectbox("Food rule", list(FOOD_RULES), format_func=FOOD_RULES.get)
        notes = st.text_input("Notes (optional)")
        if st.form_submit_button("Add medicine"):
            if name.strip():
                db.add_med(name, dose, t.strftime("%H:%M"), rule, notes)
                st.rerun()
            else:
                banner("warn", "Enter a medicine name.")
    for _, r in db.get_meds().iterrows():
        c1, c2 = st.columns([5, 1])
        c1.markdown(f'<div class="glass"><b>{r["name"]}</b> {r["dose"]} at {r["schedule_time"]} · '
                    f'{FOOD_RULES.get(r["food_rule"], "Any time")}</div>', unsafe_allow_html=True)
        if c2.button("Remove", key=f"rm{r['id']}"):
            db.remove_med(int(r["id"]))
            st.rerun()

# ---------- Assistant ----------
with tabs[5]:
    st.subheader("Ask the health assistant")
    quick = ["Should I take metformin before or after food?", "What if I miss a dose?", "Why might I feel drowsy after medicines?"]
    cols = st.columns(len(quick))
    for col, text in zip(cols, quick):
        if col.button(text, key=text):
            st.session_state["question"] = text
    question = st.text_area("Your question", key="question", placeholder="e.g. Can I take vitamin D3 on an empty stomach?")
    if st.button("Ask") and question.strip():
        with st.spinner("Thinking..."):
            answer, used = agent.ask_assistant(question, db.get_meds(), db.adherence_pct(7))
        st.markdown(f'<div class="glass"><span class="pill taken">{used}</span><br><br>{answer}</div>', unsafe_allow_html=True)

# ---------- Export ----------
with tabs[6]:
    st.subheader("Export your data")
    for kind, label in [("doses", "Medication history"), ("wellness", "Wellness logs"), ("checkins", "Side-effect check-ins")]:
        c1, c2, c3 = st.columns([3, 1, 1])
        c1.markdown(f"**{label}**")
        c2.download_button("CSV", db.export_data(kind, "csv"), f"{kind}.csv", "text/csv", key=f"{kind}c")
        c3.download_button("JSON", db.export_data(kind, "json"), f"{kind}.json", "application/json", key=f"{kind}j")

st.markdown(f'<div class="disclaimer">⚕️ {DISCLAIMER}</div>', unsafe_allow_html=True)