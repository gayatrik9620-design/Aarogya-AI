"""App constants, environment handling and disclaimers."""
import os
from pathlib import Path
from dotenv import load_dotenv

BASE_DIR = Path(__file__).parent
load_dotenv(BASE_DIR / ".env")

DB_PATH = BASE_DIR / "data" / "health_agent.db"
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.7-flash").strip()
APP_NAME = "MedCheck"

MEAL_OPTIONS = ["Before meal", "After meal", "With meal", "Not sure"]
FOOD_RULES = {"any": "Any time", "before": "Before meal", "after": "After meal", "with": "With meal"}
SYMPTOMS = ["None", "Mild acidity", "Drowsiness", "Nausea", "Headache", "Dizziness", "Dry mouth", "Other"]

DISCLAIMER = (
    "MedCheck is for informational and tracking purposes only. It is not a substitute for "
    "professional medical advice, diagnosis or treatment. Always talk to your doctor or "
    "pharmacist before changing, skipping or combining medicines. In an emergency, call your "
    "local emergency number (112 in India)."
)