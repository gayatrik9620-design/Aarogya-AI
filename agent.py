"""Medication helper tools and the LangChain + Gemini assistant (with demo fallback)."""
from datetime import datetime
from config import DISCLAIMER, GEMINI_MODEL, GOOGLE_API_KEY, FOOD_RULES

RULE_TO_CONTEXT = {"before": "Before meal", "after": "After meal", "with": "With meal"}

# Small, general reminders only. Not a complete interaction database.
GENERAL_NOTES = {
    "metformin": "Usually taken with or after meals to reduce stomach upset. Ask your doctor about alcohol.",
    "atorvastatin": "Avoid large amounts of grapefruit juice. Report unexplained muscle pain to your doctor.",
    "ibuprofen": "Take with food. Check with your doctor if you also take blood thinners or have kidney or stomach issues.",
    "paracetamol": "Do not exceed the daily limit on the label. Check other cold or flu products for paracetamol.",
    "vitamin d3": "Best absorbed with a meal that contains some fat.",
    "levothyroxine": "Usually taken on an empty stomach. Keep a gap from calcium or iron supplements.",
}


def timing_check(food_rule, meal_context, scheduled_time):
    """Return (level, message) where level is 'ok', 'warn' or 'info'."""
    msgs, level = [], "ok"
    expected = RULE_TO_CONTEXT.get(food_rule)
    if expected and meal_context == "Not sure":
        level = "info"
        msgs.append(f"This medicine is usually taken **{expected.lower()}**. Double-check the label.")
    elif expected and meal_context != expected:
        level = "warn"
        msgs.append(f"Logged **{meal_context.lower()}**, but this medicine is usually taken **{expected.lower()}**. "
                    "Please confirm with your pharmacist.")
    try:
        h, m = map(int, scheduled_time.split(":"))
        late = (datetime.now() - datetime.now().replace(hour=h, minute=m, second=0)).total_seconds() / 3600
        if late > 2:
            level = "warn"
            msgs.append(f"This dose is about {late:.0f} hours late. Do not double up on the next dose unless your doctor says so.")
    except ValueError:
        pass
    return level, " ".join(msgs) or "Timing looks good. Nice work."


def med_note(name):
    for key, note in GENERAL_NOTES.items():
        if key in name.lower():
            return note
    return "No quick note on file. Ask your pharmacist about food, timing and interactions."


def severity_advice(severity):
    if severity >= 4:
        return "Strong symptoms: please contact your doctor today. If severe or sudden, seek urgent care."
    if severity == 3:
        return "Moderate symptoms: keep logging and mention this to your doctor at the next chance."
    return "Mild symptoms: keep an eye on it and note what you ate."


def _context(meds_df, adherence):
    meds = "; ".join(f"{r['name']} {r['dose']} at {r['schedule_time']} ({FOOD_RULES.get(r['food_rule'], 'Any time')})"
                     for _, r in meds_df.iterrows())
    return f"Medicines: {meds or 'none'}. 7-day adherence: {adherence}%."


def _demo_answer(question, meds_df):
    ql = question.lower()
    for key, note in GENERAL_NOTES.items():
        if key.split()[0] in ql:
            return f"**{key.title()}**: {note}"
    if "miss" in ql or "forgot" in ql:
        return ("If you miss a dose, read the leaflet. Many medicines can be taken when you remember unless the next dose is close. "
                "Never double up without asking your pharmacist.")
    if "food" in ql or "meal" in ql or "empty" in ql:
        names = ", ".join(meds_df["name"]) if not meds_df.empty else "your medicines"
        return f"Food rules differ per medicine. Your schedule ({names}) lists each one. Check the label or ask your pharmacist."
    if "acid" in ql or "nausea" in ql or "drows" in ql:
        return "Mild stomach upset or sleepiness is a common side effect for some medicines. Log it in Check-in and tell your doctor if it persists."
    return "I can answer common questions about medicine timing, missed doses and side effects. Try asking about metformin, a missed dose or food timing."


def ask_assistant(question, meds_df, adherence):
    """Return (answer, mode). Falls back to demo mode on any problem."""
    if GOOGLE_API_KEY:
        try:
            from langchain_core.output_parsers import StrOutputParser
            from langchain_core.prompts import ChatPromptTemplate
            from langchain_google_genai import ChatGoogleGenerativeAI
            prompt = ChatPromptTemplate.from_messages([
                ("system", "You are MedCheck, a careful medication-tracking helper for patients in India. "
                           "Give short, plain-language, general information. Never diagnose or change doses. "
                           "Suggest a doctor or pharmacist for anything serious. Patient context: {context}"),
                ("human", "{question}")])
            llm = ChatGoogleGenerativeAI(model=GEMINI_MODEL, google_api_key=GOOGLE_API_KEY, temperature=0.3)
            text = (prompt | llm | StrOutputParser()).invoke({"context": _context(meds_df, adherence), "question": question})
            return text + f"\n\n_{DISCLAIMER}_", "Gemini"
        except Exception as exc:  # network, quota, bad key, missing package
            return _demo_answer(question, meds_df) + f"\n\n_(AI unavailable: {type(exc).__name__}. Showing a basic answer.)_", "Basic"
    return _demo_answer(question, meds_df) + f"\n\n_{DISCLAIMER}_", "Basic"