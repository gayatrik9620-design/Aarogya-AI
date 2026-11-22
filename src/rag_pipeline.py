"""
Aarogya-AI RAG Pipeline (Week 2)
Inline health knowledge base → FAISS vector index → retrieval.
Graceful keyword fallback if faiss/sentence-transformers not installed.
"""

import logging
from typing import List

logger = logging.getLogger("aarogya_rag")

HEALTH_KNOWLEDGE: List[str] = [
    "Sleep: Adults need 7–9 hours per night. Poor sleep is linked to obesity, diabetes, and cardiovascular disease. Tips: consistent schedule, avoid screens 1 hour before bed, keep bedroom cool and dark.",
    "Physical Activity: WHO recommends 150 minutes of moderate aerobic activity per week. 10,000 steps/day is a popular goal. Regular exercise improves mood and lowers chronic disease risk.",
    "Hydration: General recommendation is 2 litres (8 glasses) of water per day. Needs vary by body size, activity, and climate. Signs of dehydration: dark urine, dry mouth, fatigue.",
    "Nutrition: A balanced diet includes fruits, vegetables, whole grains, lean proteins, and healthy fats. ICMR recommends at least 5 portions of fruits and vegetables daily.",
    "Mental Health: Chronic stress, anxiety, and depression affect physical health. Mindfulness, yoga, regular exercise, and social connection are evidence-based wellness strategies.",
    "BMI: Body Mass Index = weight(kg) / height(m)². Healthy range: 18.5–24.9. Overweight: 25–29.9. Obese: ≥30. BMI is a screening tool, not a diagnostic measure.",
    "Heart Health: Risk factors for cardiovascular disease include high blood pressure, high cholesterol, smoking, obesity, and inactivity. Regular blood pressure monitoring is key.",
    "Diabetes Prevention: Type 2 diabetes risk can be reduced by healthy weight, regular exercise, and a diet low in refined carbohydrates. Regular blood glucose screening is recommended for at-risk individuals.",
    "Medication Safety: Never take prescription medications without a doctor's prescription. Store medicines away from heat, moisture, and children. Never share prescription drugs.",
    "Emergency Signs: Call 112 immediately for chest pain, difficulty breathing, sudden numbness, uncontrolled bleeding, loss of consciousness, seizures, or stroke signs (FAST: Face drooping, Arm weakness, Speech difficulty, Time to call).",
    "Cancer Screening: Early detection saves lives. Recommended screenings: mammography, Pap smear, colonoscopy, PSA test. Consult your doctor for a screening schedule.",
    "Respiratory Health: Avoid smoking and secondhand smoke. Use masks in high-pollution environments. Practice deep breathing exercises. COPD and asthma require professional management.",
]

_index = None
_chunks: List[str] = []
_embedder = None
_faiss_available = False


def _build_index() -> None:
    global _index, _chunks, _embedder, _faiss_available
    try:
        import faiss
        import numpy as np
        from sentence_transformers import SentenceTransformer

        _embedder = SentenceTransformer("all-MiniLM-L6-v2")
        _chunks = HEALTH_KNOWLEDGE
        embeddings = _embedder.encode(_chunks, convert_to_numpy=True)
        dim = embeddings.shape[1]
        _index = faiss.IndexFlatL2(dim)
        _index.add(embeddings)
        _faiss_available = True
        logger.info(f"RAG FAISS index built: {len(_chunks)} chunks, dim={dim}")
    except ImportError as e:
        logger.warning(f"RAG deps not available ({e}). Using keyword fallback.")
        _faiss_available = False
    except Exception as e:
        logger.error(f"RAG index build failed: {e}")
        _faiss_available = False


def get_rag_context(query: str, top_k: int = 3) -> str:
    """Retrieve top-k relevant health knowledge chunks for a query."""
    global _index, _faiss_available

    if _index is None:
        _build_index()

    if _faiss_available and _index is not None:
        try:
            import numpy as np
            query_emb = _embedder.encode([query], convert_to_numpy=True)
            distances, indices = _index.search(query_emb, top_k)
            results = [HEALTH_KNOWLEDGE[i] for i in indices[0] if i < len(HEALTH_KNOWLEDGE)]
            return "\n\n".join(results)
        except Exception as e:
            logger.error(f"RAG retrieval error: {e}")

    # Keyword fallback
    q = query.lower()
    matches = [c for c in HEALTH_KNOWLEDGE if any(w in c.lower() for w in q.split() if len(w) > 3)]
    return "\n\n".join(matches[:top_k]) if matches else HEALTH_KNOWLEDGE[0]


def get_health_info_by_topic(topic: str) -> str:
    """Return health info for a specific topic (used by /api/rag/health-info)."""
    topic_map = {
        "sleep": 0, "activity": 1, "hydration": 2, "nutrition": 3,
        "mental": 4, "bmi": 5, "heart": 6, "diabetes": 7,
        "medication": 8, "emergency": 9, "cancer": 10, "respiratory": 11,
    }
    t = topic.lower().strip()
    for key, idx in topic_map.items():
        if key in t:
            return HEALTH_KNOWLEDGE[idx]
    return get_rag_context(topic, top_k=2)
