"""
Aarogya-AI Medication Awareness Tool (Week 3)
General medication safety information — NOT prescriptions or diagnoses.
"""

from typing import List

MED_INFO = {
    "aspirin": "Common pain reliever and anti-inflammatory. Not recommended for children under 12. May irritate the stomach.",
    "ibuprofen": "NSAID (e.g., Brufen). Take with food. Avoid in kidney disease or with blood thinners.",
    "paracetamol": "Used for pain and fever (Crocin, Dolo). Do not exceed recommended dose. Liver damage risk with overdose.",
    "metformin": "Used for type 2 diabetes. Requires prescription. Take with meals to reduce GI side effects.",
    "omeprazole": "Proton pump inhibitor for acidity/GERD. Take before meals. Long-term use needs monitoring.",
    "amoxicillin": "Penicillin antibiotic. Complete the full prescribed course. Inform doctor of penicillin allergy.",
    "amlodipine": "Calcium channel blocker for blood pressure. Do not stop suddenly without medical advice.",
    "atorvastatin": "Statin for cholesterol. Report muscle pain to your doctor immediately.",
    "cetirizine": "Antihistamine for allergies. May cause drowsiness. Avoid alcohol.",
    "azithromycin": "Macrolide antibiotic. Requires prescription. Complete the full course.",
}

KNOWN_INTERACTIONS = [
    ({"aspirin", "ibuprofen"}, "Both are NSAIDs — combining may increase risk of GI bleeding."),
    ({"aspirin", "warfarin"}, "May significantly increase bleeding risk. Medical supervision required."),
    ({"metformin", "alcohol"}, "Alcohol with metformin may increase risk of lactic acidosis."),
    ({"cetirizine", "alcohol"}, "Alcohol may intensify drowsiness from cetirizine."),
    ({"amlodipine", "grapefruit"}, "Grapefruit may increase amlodipine blood levels."),
]


def check_medication_interaction(medications: List[str]) -> str:
    meds_clean = [m.strip().lower() for m in medications if m.strip()]
    meds_set = set(meds_clean)

    if not meds_clean:
        return "Please provide at least one medication name."

    lines = [
        "💊 **Medication Safety Information**",
        f"\nChecking: {', '.join(meds_clean)}", "",
        "---", "**General Awareness Notes:**",
    ]

    for med in meds_clean:
        info = MED_INFO.get(med)
        if info:
            lines.append(f"\n• **{med.title()}:** {info}")
        else:
            lines.append(f"\n• **{med.title()}:** No specific info available. Consult your pharmacist or doctor.")

    found = [note for combo, note in KNOWN_INTERACTIONS if combo.issubset(meds_set)]

    lines += ["", "---"]
    if found:
        lines.append("⚠️ **Potential Interaction Awareness:**")
        lines += [f"• {n}" for n in found]
    else:
        lines += [
            "No common interactions found in our database for these medications.",
            "This does not mean no interactions exist — always consult your doctor or pharmacist.",
        ]

    lines += [
        "", "---",
        "🛡️ **Important:** This information is for general awareness only.",
        "Never start, stop, or change medications without consulting a qualified healthcare professional.",
        "",
        "*Disclaimer: I am an AI assistant, not a doctor. Please consult a medical professional for advice.*"
    ]
    return "\n".join(lines)