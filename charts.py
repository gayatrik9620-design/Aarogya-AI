"""Plotly charts in a violet theme."""
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from database import dose_history, get_checkins, get_wellness

TEAL, MINT, CORAL, MUTED, INK = "#0d9488", "#5eead4", "#fb7185", "rgba(18,52,63,0.10)", "#12343f"


def _style(fig, h=300):
    fig.update_layout(height=h, margin=dict(l=24, r=24, t=64, b=24), paper_bgcolor="rgba(0,0,0,0)",
                      plot_bgcolor="rgba(0,0,0,0)", font=dict(color=INK, size=13), title_font=dict(color=INK, size=16), legend_title_text="")
    fig.update_xaxes(gridcolor=MUTED, showline=False, automargin=True)
    fig.update_yaxes(gridcolor=MUTED, showline=False, automargin=True)
    fig.update_xaxes(title_text="")
    fig.update_yaxes(title_text="")
    return fig


def _empty(msg):
    fig = go.Figure()
    fig.add_annotation(text=msg, showarrow=False, font=dict(color="#35606b", size=14))
    return _style(fig, 200)


def adherence_by_day(uid, days=14):
    df = dose_history(uid, days)
    if df.empty:
        return _empty("No dose logs yet")
    d = df.groupby("log_date")["status"].apply(lambda s: 100 * (s == "taken").mean()).reset_index(name="pct")
    fig = px.area(d, x="log_date", y="pct", title="Daily adherence (%)", markers=True)
    fig.update_traces(line_color=TEAL, fillcolor="rgba(13,148,136,0.22)")
    fig.update_yaxes(range=[0, 105])
    return _style(fig)


def adherence_by_med(uid, days=14):
    df = dose_history(uid, days)
    if df.empty:
        return _empty("No dose logs yet")
    d = df.groupby("medication")["status"].apply(lambda s: round(100 * (s == "taken").mean())).reset_index(name="pct")
    fig = px.bar(d, x="medication", y="pct", title="Adherence by medicine (%)", text="pct")
    fig.update_traces(marker_color=TEAL, textposition="outside")
    fig.update_yaxes(range=[0, 115])
    return _style(fig)


def status_mix(uid, days=14):
    df = dose_history(uid, days)
    if df.empty:
        return _empty("No dose logs yet")
    d = df["status"].value_counts().reset_index()
    d.columns = ["status", "count"]
    fig = px.pie(d, names="status", values="count", hole=0.6, title="Dose outcomes",
                 color="status", color_discrete_map={"taken": TEAL, "skipped": "#f59e0b", "missed": CORAL})
    return _style(fig)


def steps_chart(uid, days=14):
    df = get_wellness(uid, days)
    if df.empty:
        return _empty("No wellness logs yet")
    fig = px.bar(df, x="log_date", y="steps", title="Daily steps")
    fig.update_traces(marker_color="#14b8a6")
    return _style(fig)


def sleep_water_chart(uid, days=14):
    df = get_wellness(uid, days)
    if df.empty:
        return _empty("No wellness logs yet")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["log_date"], y=df["sleep_hrs"], name="Sleep (hrs)", line=dict(color=TEAL, width=3)))
    fig.add_trace(go.Scatter(x=df["log_date"], y=df["water_ml"] / 1000, name="Water (L)", line=dict(color=CORAL, width=3)))
    fig.update_layout(title="Sleep and water")
    return _style(fig)


def symptom_chart(uid):
    df = get_checkins(uid, 200)
    df = df[df["symptom"] != "None"] if not df.empty else df
    if df.empty:
        return _empty("No side-effect check-ins yet")
    d = df.groupby("symptom")["severity"].agg(["count", "mean"]).reset_index()
    fig = px.bar(d, x="symptom", y="count", title="Check-ins by symptom", hover_data={"mean": ":.1f"})
    fig.update_traces(marker_color=CORAL)
    return _style(fig)