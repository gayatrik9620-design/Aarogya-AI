"""SQLite storage: schema, sample data, CRUD and export helpers."""
import json
import random
import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta

import pandas as pd
from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS medications(
  id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, dose TEXT,
  schedule_time TEXT NOT NULL, food_rule TEXT DEFAULT 'any', notes TEXT, active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS dose_logs(
  id INTEGER PRIMARY KEY AUTOINCREMENT, med_id INTEGER NOT NULL, log_date TEXT NOT NULL,
  status TEXT NOT NULL, taken_at TEXT, food_context TEXT);
CREATE TABLE IF NOT EXISTS checkins(
  id INTEGER PRIMARY KEY AUTOINCREMENT, created_at TEXT NOT NULL, med_id INTEGER,
  meal_relation TEXT, symptom TEXT, severity INTEGER, note TEXT);
CREATE TABLE IF NOT EXISTS wellness(
  id INTEGER PRIMARY KEY AUTOINCREMENT, log_date TEXT UNIQUE NOT NULL,
  steps INTEGER, water_ml INTEGER, sleep_hrs REAL, notes TEXT);
"""


def _conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def run(sql, params=()):
    with closing(_conn()) as c:
        c.execute(sql, params)
        c.commit()


def q(sql, params=()):
    with closing(_conn()) as c:
        return pd.read_sql_query(sql, c, params=params)


def init_db():
    """Create tables and seed sample data on first run."""
    with closing(_conn()) as c:
        c.executescript(SCHEMA)
        c.commit()
    if q("SELECT COUNT(*) n FROM medications")["n"][0] == 0:
        _seed()


def _seed():
    rnd = random.Random(42)
    meds = [("Metformin", "500 mg", "08:00", "after", "For blood sugar. Take after breakfast."),
            ("Vitamin D3", "60,000 IU weekly", "13:00", "with", "Take with the biggest meal."),
            ("Atorvastatin", "10 mg", "21:30", "any", "Evening dose.")]
    for m in meds:
        run("INSERT INTO medications(name,dose,schedule_time,food_rule,notes) VALUES(?,?,?,?,?)", m)
    today = date.today()
    ctx = {"after": "After meal", "with": "With meal", "any": "Not sure"}
    for back in range(14, 0, -1):
        d = today - timedelta(days=back)
        for i, m in enumerate(meds, start=1):
            r = rnd.random()
            status = "taken" if r < 0.84 else ("skipped" if r < 0.92 else "missed")
            taken_at = f"{d} {m[2]}" if status == "taken" else None
            run("INSERT INTO dose_logs(med_id,log_date,status,taken_at,food_context) VALUES(?,?,?,?,?)",
                (i, str(d), status, taken_at, ctx[m[3]] if status == "taken" else None))
        run("INSERT OR REPLACE INTO wellness(log_date,steps,water_ml,sleep_hrs,notes) VALUES(?,?,?,?,?)",
            (str(d), rnd.randint(3500, 11000), rnd.randint(1200, 3000), round(rnd.uniform(5.5, 8.5), 1),
             rnd.choice(["Felt good", "A bit tired", "Long walk in evening", "", "Light headache in morning"])))
    for back, med, meal, sym, sev, note in [(9, 1, "After meal", "Mild acidity", 2, "Settled in an hour"),
                                            (5, 3, "Not sure", "Drowsiness", 2, "Slightly sleepy at night"),
                                            (2, 1, "Before meal", "Nausea", 3, "Took it before breakfast")]:
        run("INSERT INTO checkins(created_at,med_id,meal_relation,symptom,severity,note) VALUES(?,?,?,?,?,?)",
            (f"{today - timedelta(days=back)} 09:00", med, meal, sym, sev, note))


# ---- Medications ----
def get_meds(active_only=True):
    return q("SELECT * FROM medications" + (" WHERE active=1" if active_only else "") + " ORDER BY schedule_time")


def add_med(name, dose, schedule_time, food_rule, notes):
    run("INSERT INTO medications(name,dose,schedule_time,food_rule,notes) VALUES(?,?,?,?,?)",
        (name.strip(), dose.strip(), schedule_time, food_rule, notes.strip()))


def remove_med(med_id):
    run("UPDATE medications SET active=0 WHERE id=?", (med_id,))


# ---- Doses ----
def today_schedule():
    return q("""SELECT m.id, m.name, m.dose, m.schedule_time, m.food_rule, m.notes,
                COALESCE(d.status,'pending') AS status, d.food_context
                FROM medications m LEFT JOIN dose_logs d ON d.med_id=m.id AND d.log_date=?
                WHERE m.active=1 ORDER BY m.schedule_time""", (str(date.today()),))


def log_dose(med_id, status, food_context=None):
    today = str(date.today())
    run("DELETE FROM dose_logs WHERE med_id=? AND log_date=?", (med_id, today))
    taken_at = datetime.now().strftime("%Y-%m-%d %H:%M") if status == "taken" else None
    run("INSERT INTO dose_logs(med_id,log_date,status,taken_at,food_context) VALUES(?,?,?,?,?)",
        (med_id, today, status, taken_at, food_context))


def dose_history(days=14):
    since = str(date.today() - timedelta(days=days))
    return q("""SELECT d.log_date, m.name AS medication, m.dose, d.status, d.taken_at, d.food_context
                FROM dose_logs d JOIN medications m ON m.id=d.med_id
                WHERE d.log_date>=? ORDER BY d.log_date DESC, m.schedule_time""", (since,))


def adherence_pct(days=7):
    df = dose_history(days)
    return 0.0 if df.empty else round(100 * (df["status"] == "taken").sum() / len(df), 1)


# ---- Check-ins ----
def add_checkin(med_id, meal, symptom, severity, note):
    run("INSERT INTO checkins(created_at,med_id,meal_relation,symptom,severity,note) VALUES(?,?,?,?,?,?)",
        (datetime.now().strftime("%Y-%m-%d %H:%M"), med_id, meal, symptom, severity, note.strip()))


def get_checkins(limit=100):
    return q("""SELECT c.created_at, COALESCE(m.name,'General') AS medication, c.meal_relation,
                c.symptom, c.severity, c.note FROM checkins c LEFT JOIN medications m ON m.id=c.med_id
                ORDER BY c.created_at DESC LIMIT ?""", (limit,))


# ---- Wellness ----
def save_wellness(day, steps, water_ml, sleep_hrs, notes):
    run("INSERT OR REPLACE INTO wellness(log_date,steps,water_ml,sleep_hrs,notes) VALUES(?,?,?,?,?)",
        (str(day), int(steps), int(water_ml), float(sleep_hrs), notes.strip()))


def get_wellness(days=14):
    since = str(date.today() - timedelta(days=days))
    return q("SELECT log_date,steps,water_ml,sleep_hrs,notes FROM wellness WHERE log_date>=? ORDER BY log_date", (since,))


# ---- Export ----
def export_data(kind, fmt):
    """kind: 'doses' | 'wellness' | 'checkins'; fmt: 'csv' | 'json'. Returns text."""
    df = {"doses": lambda: dose_history(365), "wellness": lambda: get_wellness(365),
          "checkins": lambda: get_checkins(1000)}[kind]()
    return df.to_csv(index=False) if fmt == "csv" else json.dumps(df.to_dict("records"), indent=2)
