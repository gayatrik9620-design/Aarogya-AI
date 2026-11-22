import os
import sqlite3
from typing import Any, Dict


def _get_db_path() -> str:
  """Locate health_data.db in the project root if present."""
  root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
  return os.path.join(root_dir, "health_data.db")


def get_fitness_summary(user_id: Any = None) -> Dict[str, Any]:
  """Return a clean fitness & wellness summary without circular imports."""
  summary: Dict[str, Any] = {
      "status": "ok",
      "user_id": user_id,
      "weight_kg": None,
      "bmi": None,
      "steps": None,
      "sleep_hours": None,
      "notes": "No fitness records logged yet.",
  }

  db_path = _get_db_path()
  if not os.path.exists(db_path):
    return summary

  try:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT"
        " LIKE 'sqlite_%'"
    )
    tables = [row["name"] for row in cursor.fetchall()]

    for table in tables:
      cursor.execute(f"PRAGMA table_info({table})")
      cols = [col["name"].lower() for col in cursor.fetchall()]
      if any(k in cols for k in ("weight", "steps", "sleep", "bmi", "heart_rate")):
        cursor.execute(f"SELECT * FROM {table} ORDER BY rowid DESC LIMIT 1")
        latest = cursor.fetchone()
        if latest:
          record = dict(latest)
          summary["latest_record"] = record
          summary["notes"] = f"Loaded latest entry from {table}."
          for key in ("weight", "weight_kg"):
            if key in record and record[key] is not None:
              summary["weight_kg"] = record[key]
              break
          for key in ("steps", "daily_steps"):
            if key in record and record[key] is not None:
              summary["steps"] = record[key]
              break
          for key in ("sleep", "sleep_hours"):
            if key in record and record[key] is not None:
              summary["sleep_hours"] = record[key]
              break
          if "bmi" in record and record[key] is not None:
            summary["bmi"] = record["bmi"]
        break

    conn.close()
  except Exception as exc:
    summary["status"] = "fallback"
    summary["notes"] = f"Unable to read health database cleanly: {exc}"

  return summary