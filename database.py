"""SQLite storage with per-user accounts: schema, sample data, CRUD and export helpers."""
import hashlib
import hmac
import json
import random
import re
import secrets
import sqlite3
from contextlib import closing
from datetime import date, datetime, timedelta

import pandas as pd
from config import DB_PATH

SCHEMA = """
CREATE TABLE IF NOT EXISTS users(
  id INTEGER PRIMARY KEY AUTOINCREMENT, username TEXT UNIQUE NOT NULL,
  salt TEXT NOT NULL, pw_hash TEXT NOT NULL, created_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS medications(
  id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, name TEXT NOT NULL, dose TEXT,
  schedule_time TEXT NOT NULL, food_rule TEXT DEFAULT 'any', notes TEXT, active INTEGER DEFAULT 1);
CREATE TABLE IF NOT EXISTS dose_logs(
  id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, med_id INTEGER NOT NULL,
  log_date TEXT NOT NULL, status TEXT NOT NULL, taken_at TEXT, food_context TEXT);
CREATE TABLE IF NOT EXISTS checkins(
  id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, created_at TEXT NOT NULL, med_id INTEGER,
  meal_relation TEXT, symptom TEXT, severity INTEGER, note TEXT);
CREATE TABLE IF NOT EXISTS wellness(
  id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER NOT NULL, log_date TEXT NOT NULL,
  steps INTEGER, water_ml INTEGER, sleep_hrs REAL, notes TEXT, UNIQUE(user_id, log_date));
"""


def _conn():
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)
    return sqlite3.connect(DB_PATH)


def run(sql, params=()):
    """Execute a write and return the new row id."""
    with closing(_conn()) as c:
        cur = c.execute(sql, params)
        c.commit()
        return cur.lastrowid


def q(sql, params=()):
    with closing(_conn()) as c:
        return pd.read_sql_query(sql, c, params=params)


def init_db():
    """Create tables (rebuilding an old single-user database) and the shared demo account."""
    with closing(_conn()) as c:
        cols = [r[1] for r in c.execute("PRAGMA table_info(medications)")]
        if cols and "user_id" not in cols:  # old layout held only sample data, so start fresh
            for t in ("medications", "dose_logs", "checkins", "wellness"):
                c.execute(f"DROP TABLE IF EXISTS {t}")
        c.executescript(SCHEMA)
        c.commit()
    if q("SELECT id FROM users WHERE username='demo'").empty:
        try:
            seed_user(_create_user("demo", secrets.token_urlsafe(16)))
        except sqlite3.IntegrityError:
            pass  # another session created it first


# ---- Accounts ----
def _hash(password, salt):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), bytes.fromhex(salt), 200_000).hex()


def _create_user(username, password):
    salt = secrets.token_hex(16)
    return run("INSERT INTO users(username,salt,pw_hash,created_at) VALUES(?,?,?,?)",
               (username, salt, _hash(password, salt), datetime.now().strftime("%Y-%m-%d %H:%M")))


def register(username, password, sample=False):
    """Return (user_id, error). Passwords are stored only as salted PBKDF2 hashes."""
    username = username.strip().lower()
    if not re.fullmatch(r"[a-z0-9_.-]{3,30}", username):
        return None, "Username: 3-30 letters, numbers, dot, dash or underscore."
    if len(password) < 6:
        return None, "Password must be at least 6 characters."
    if not q("SELECT id FROM users WHERE username=?", (username,)).empty:
        return None, "That username is already taken."
    uid = _create_user(username, password)
    if sample:
        seed_user(uid)
    return uid, ""


def login(username, password):
    df = q("SELECT id, salt, pw_hash FROM users WHERE username=?", (username.strip().lower(),))
    if df.empty:
        return None
    r = df.iloc[0]
    return int(r["id"]) if hmac.compare_digest(_hash(password, r["salt"]), r["pw_hash"]) else None


def demo_user_id():
    return int(q("SELECT id FROM users WHERE username='demo'")["id"][0])


def seed_user(uid):
    """Fill one account with 14 days of realistic sample data."""
    rnd = random.Random(uid)
    meds = [("Metformin", "500 mg", "08:00", "after", "For blood sugar. Take after breakfast."),
            ("Vitamin D3", "60,000 IU weekly", "13:00", "with", "Take with the biggest meal."),
            ("Atorvastatin", "10 mg", "21:30", "any", "Evening dose.")]
    ids = [run("INSERT INTO medications(user_id,name,dose,schedule_time,food_rule,notes) VALUES(?,?,?,?,?,?)",
               (uid, *m)) for m in meds]
    today = date.today()
    ctx = {"after": "After meal", "with": "With meal", "any": "Not sure"}
    for back in range(14, 0, -1):
        d = today - timedelta(days=back)
        for mid, m in zip(ids, meds):
            r = rnd.random()
            status = "taken" if r < 0.84 else ("skipped" if r < 0.92 else "missed")
            run("INSERT INTO dose_logs(user_id,med_id,log_date,status,taken_at,food_context) VALUES(?,?,?,?,?,?)",
                (uid, mid, str(d), status, f"{d} {m[2]}" if status == "taken" else None,
                 ctx[m[3]] if status == "taken" else None))
        run("INSERT OR REPLACE INTO wellness(user_id,log_date,steps,water_ml,sleep_hrs,notes) VALUES(?,?,?,?,?,?)",
            (uid, str(d), rnd.randint(3500, 11000), rnd.randint(1200, 3000), round(rnd.uniform(5.5, 8.5), 1),
             rnd.choice(["Felt good", "A bit tired", "Long walk in evening", "", "Light headache in morning"])))
    for back, idx, meal, sym, sev, note in [(9, 0, "After meal", "Mild acidity", 2, "Settled in an hour"),
                                            (5, 2, "Not sure", "Drowsiness", 2, "Slightly sleepy at night"),
                                            (2, 0, "Before meal", "Nausea", 3, "Took it before breakfast")]:
        run("INSERT INTO checkins(user_id,created_at,med_id,meal_relation,symptom,severity,note) VALUES(?,?,?,?,?,?,?)",
            (uid, f"{today - timedelta(days=back)} 09:00", ids[idx], meal, sym, sev, note))


# ---- Medications ----
def get_meds(uid, active_only=True):
    return q("SELECT * FROM medications WHERE user_id=?" + (" AND active=1" if active_only else "")
             + " ORDER BY schedule_time", (uid,))


def add_med(uid, name, dose, schedule_time, food_rule, notes):
    run("INSERT INTO medications(user_id,name,dose,schedule_time,food_rule,notes) VALUES(?,?,?,?,?,?)",
        (uid, name.strip(), dose.strip(), schedule_time, food_rule, notes.strip()))


def remove_med(uid, med_id):
    run("UPDATE medications SET active=0 WHERE id=? AND user_id=?", (med_id, uid))


# ---- Doses ----
def today_schedule(uid):
    return q("""SELECT m.id, m.name, m.dose, m.schedule_time, m.food_rule, m.notes,
                COALESCE(d.status,'pending') AS status, d.food_context
                FROM medications m LEFT JOIN dose_logs d ON d.med_id=m.id AND d.log_date=?
                WHERE m.user_id=? AND m.active=1 ORDER BY m.schedule_time""", (str(date.today()), uid))


def log_dose(uid, med_id, status, food_context=None):
    if q("SELECT id FROM medications WHERE id=? AND user_id=?", (med_id, uid)).empty:
        return  # not this user's medicine
    today = str(date.today())
    run("DELETE FROM dose_logs WHERE med_id=? AND log_date=? AND user_id=?", (med_id, today, uid))
    taken_at = datetime.now().strftime("%Y-%m-%d %H:%M") if status == "taken" else None
    run("INSERT INTO dose_logs(user_id,med_id,log_date,status,taken_at,food_context) VALUES(?,?,?,?,?,?)",
        (uid, med_id, today, status, taken_at, food_context))


def dose_history(uid, days=14):
    since = str(date.today() - timedelta(days=days))
    return q("""SELECT d.log_date, m.name AS medication, m.dose, d.status, d.taken_at, d.food_context
                FROM dose_logs d JOIN medications m ON m.id=d.med_id
                WHERE d.user_id=? AND d.log_date>=? ORDER BY d.log_date DESC, m.schedule_time""", (uid, since))


def adherence_pct(uid, days=7):
    df = dose_history(uid, days)
    return 0.0 if df.empty else round(100 * (df["status"] == "taken").sum() / len(df), 1)


# ---- Check-ins ----
def add_checkin(uid, med_id, meal, symptom, severity, note):
    run("INSERT INTO checkins(user_id,created_at,med_id,meal_relation,symptom,severity,note) VALUES(?,?,?,?,?,?,?)",
        (uid, datetime.now().strftime("%Y-%m-%d %H:%M"), med_id, meal, symptom, severity, note.strip()))


def get_checkins(uid, limit=100):
    return q("""SELECT c.created_at, COALESCE(m.name,'General') AS medication, c.meal_relation,
                c.symptom, c.severity, c.note FROM checkins c LEFT JOIN medications m ON m.id=c.med_id
                WHERE c.user_id=? ORDER BY c.created_at DESC LIMIT ?""", (uid, limit))


# ---- Wellness ----
def save_wellness(uid, day, steps, water_ml, sleep_hrs, notes):
    run("INSERT OR REPLACE INTO wellness(user_id,log_date,steps,water_ml,sleep_hrs,notes) VALUES(?,?,?,?,?,?)",
        (uid, str(day), int(steps), int(water_ml), float(sleep_hrs), notes.strip()))


def get_wellness(uid, days=14):
    since = str(date.today() - timedelta(days=days))
    return q("SELECT log_date,steps,water_ml,sleep_hrs,notes FROM wellness WHERE user_id=? AND log_date>=? ORDER BY log_date",
             (uid, since))


# ---- Export ----
def export_data(uid, kind, fmt):
    """kind: 'doses' | 'wellness' | 'checkins'; fmt: 'csv' | 'json'. Returns text."""
    df = {"doses": lambda: dose_history(uid, 365), "wellness": lambda: get_wellness(uid, 365),
          "checkins": lambda: get_checkins(uid, 1000)}[kind]()
    return df.to_csv(index=False) if fmt == "csv" else json.dumps(df.to_dict("records"), indent=2)