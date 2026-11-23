# 💜 MedCheck: Dose-Timing & Meal/Side-Effect Check-In Assistant

A simple Streamlit health-tracking app (Capabl Healthcare Monitoring, Track A).

**Features**
- Today's doses: mark Taken or Skipped, pick before, after or with meal, and get an instant timing check
- Side-effect check-ins (mild acidity, drowsiness, nausea...) with severity guidance
- Adherence % (daily, per medicine, outcome mix) using Plotly charts
- Wellness log: steps, water, sleep and notes
- Medicine information and Q&A via LangChain + Google Gemini, with automatic **Demo Mode** if no key is set
- SQLite storage in `data/health_agent.db`, pre-filled with 14 days of sample data
- CSV and JSON export

> ⚠️ **Disclaimer:** MedCheck is for informational and tracking purposes only. It is not a substitute for professional medical advice, diagnosis or treatment. Never store real patient data while developing.

## Setup in VS Code (open the `medcheck` folder, then Terminal > New Terminal)

**Windows (PowerShell)**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
copy .env.example .env
streamlit run app.py
```
If activation is blocked, run `Set-ExecutionPolicy -Scope Process Bypass` first.

**macOS / Linux**
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
streamlit run app.py
```

The app opens at http://localhost:8501. In VS Code, choose the `.venv` interpreter (Ctrl+Shift+P > "Python: Select Interpreter").

## Enable Gemini (optional)
Get a free key at https://aistudio.google.com/app/apikey, paste it after `GOOGLE_API_KEY=` in `.env`, and restart. Without a key the app runs in Demo Mode.

## Reset sample data
Stop the app, delete `data/health_agent.db`, and run again.

## Files
`app.py` UI and navigation · `config.py` settings and disclaimer · `database.py` SQLite, seed data, exports · `agent.py` timing checks and Gemini assistant · `charts.py` Plotly charts
