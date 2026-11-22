"""
Aarogya-AI Orchestrator Agent (Weeks 3 & 4)
Tool-calling agent with multi-agent sub-workflows,
guardrails, retries, and execution logging.
"""

import os
import logging
import time
from dotenv import load_dotenv

load_dotenv()

# ------------------------------------------------------------------
# Logging
# ------------------------------------------------------------------

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [AGENT] %(levelname)s — %(message)s"
)
logger = logging.getLogger("aarogya_agent")

# ------------------------------------------------------------------
# Guardrail keyword lists
# ------------------------------------------------------------------

EMERGENCY_KEYWORDS = [
    "chest pain", "can't breathe", "cannot breathe", "heart attack",
    "stroke", "unconscious", "uncontrolled bleeding", "seizure",
    "self harm", "self-harm", "suicide", "suicidal",
    "severe pain", "can't move", "paralysis", "overdose",
]

SCOPE_BLOCK_KEYWORDS = [
    "prescribe", "give me medicine", "what drug should i take",
    "diagnose me", "tell me my diagnosis", "am i pregnant",
    "is this cancer", "do i have diabetes", "confirm my diagnosis",
]

INJECTION_PATTERNS = [
    "ignore previous", "ignore all previous", "disregard",
    "forget your instructions", "you are now", "act as",
    "jailbreak", "dan mode", "pretend you are not",
]

FITNESS_KEYWORDS = [
    "my health data", "fitness summary", "health summary",
    "my steps", "my sleep", "my weight", "show my health",
    "health report", "fitness report", "health statistics",
]

MEDICATION_KEYWORDS = [
    "medication interaction", "medicine interaction",
    "drug interaction", "check medication", "check medicine",
]

# ------------------------------------------------------------------
# Guardrail checks
# ------------------------------------------------------------------


def _check_emergency(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in EMERGENCY_KEYWORDS)


def _check_scope_violation(query: str) -> bool:
    q = query.lower()
    return any(kw in q for kw in SCOPE_BLOCK_KEYWORDS)


def _check_injection(query: str) -> bool:
    q = query.lower()
    return any(pat in q for pat in INJECTION_PATTERNS)


def _emergency_response() -> str:
    return (
        "🚨 **URGENT MEDICAL ATTENTION NEEDED**\n\n"
        "Based on the symptoms you described, please seek **immediate "
        "professional medical assistance**.\n\n"
        "🇮🇳 **India Emergency Numbers:**\n"
        "- **112** — National Emergency\n"
        "- **108** — Ambulance Service\n"
        "- **102** — Government Ambulance\n\n"
        "Do NOT rely on an AI during a medical emergency. "
        "Please call emergency services now."
    )


def _scope_response() -> str:
    return (
        "I'm Aarogya-AI, a general wellness information assistant. "
        "I'm not able to provide medical diagnoses, prescriptions, or "
        "specific treatment recommendations.\n\n"
        "Please consult a qualified healthcare professional for personal "
        "medical advice.\n\n"
        "*Disclaimer: I am an AI assistant, not a doctor.*"
    )


def _injection_response() -> str:
    return (
        "I'm designed to provide safe and responsible health information. "
        "I'll continue following my wellness safety guidelines.\n\n"
        "How can I help you with a health or wellness question today?"
    )


# ------------------------------------------------------------------
# LLM call with retry (Wellness Sub-Agent)
# ------------------------------------------------------------------


def _call_llm(query: str, retries: int = 2) -> str:
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        return (
            "⚠️ GOOGLE_API_KEY is not configured. "
            "Please add it to your .env file."
        )

    for attempt in range(1, retries + 2):
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from langchain_core.prompts import PromptTemplate
            from langchain_core.output_parsers import StrOutputParser

            llm = ChatGoogleGenerativeAI(
                model="gemini-1.5-flash",
                google_api_key=api_key,
                temperature=0.3,
            )

            template = """You are Aarogya AI, a helpful, empathetic, and safe personal healthcare assistant.

CRITICAL SAFETY RULES:
1. Provide ONLY general informational and wellness guidance.
2. NEVER provide a definitive medical diagnosis.
3. NEVER prescribe specific medicines, treatments, or dosages.
4. For serious or persistent symptoms, advise consulting a qualified healthcare professional.
5. Always end your response with:

Disclaimer: I am an AI assistant, not a doctor. Please consult a medical professional for advice.

User Query: {user_query}

Response:"""

            prompt = PromptTemplate(
                input_variables=["user_query"],
                template=template
            )
            chain = prompt | llm | StrOutputParser()
            return chain.invoke({"user_query": query})

        except Exception as e:
            logger.warning(f"LLM attempt {attempt} failed: {e}")
            if attempt <= retries:
                time.sleep(1.5 ** attempt)
            else:
                return (
                    "I'm temporarily unable to process your query. "
                    "Please try again in a moment.\n\n"
                    f"*(Error: {type(e).__name__})*"
                )


# ------------------------------------------------------------------
# Tool sub-agents
# ------------------------------------------------------------------


def _fitness_sub_agent(query: str) -> str:
    logger.info("Routing to FitnessSubAgent")
    try:
        from src.fitness_tool import get_fitness_summary
        return get_fitness_summary()
    except Exception as e:
        logger.error(f"FitnessSubAgent error: {e}")
        return f"Unable to retrieve fitness data at this time. ({type(e).__name__})"


def _medication_sub_agent(query: str) -> str:
    logger.info("Routing to MedicationSubAgent")
    try:
        from src.medication_tool import check_medication_interaction
        parts = query.split(":", 1)
        if len(parts) == 2:
            meds = [m.strip() for m in parts[1].split(",")]
            return check_medication_interaction(meds)
        return (
            "Please specify medications separated by commas after a colon.\n"
            "Example: *Check medication interaction: aspirin, ibuprofen*"
        )
    except Exception as e:
        logger.error(f"MedicationSubAgent error: {e}")
        return f"Unable to process medication query. ({type(e).__name__})"


def _wellness_sub_agent(query: str) -> str:
    logger.info("Routing to WellnessSubAgent (Gemini LLM)")
    return _call_llm(query)


# ------------------------------------------------------------------
# Main orchestrator
# ------------------------------------------------------------------


def get_health_agent_reply(user_query: str) -> str:
    """
    Orchestrator agent.
    1. Run guardrails (emergency → scope → injection)
    2. Route to appropriate sub-agent / tool
    3. Fall back to LLM with retries
    4. Log all routing decisions and latency
    """
    start = time.time()
    query = (user_query or "").strip()

    if not query:
        return "Please enter a health or wellness question."

    logger.info(f"Query received ({len(query)} chars): {query[:80]}")

    # Guardrail 1: Emergency detection
    if _check_emergency(query):
        logger.warning("EMERGENCY guardrail triggered")
        resp = _emergency_response()
        logger.info(f"Response time: {time.time()-start:.2f}s [EMERGENCY]")
        return resp

    # Guardrail 2: Scope boundary
    if _check_scope_violation(query):
        logger.warning("SCOPE guardrail triggered")
        resp = _scope_response()
        logger.info(f"Response time: {time.time()-start:.2f}s [SCOPE_BLOCK]")
        return resp

    # Guardrail 3: Prompt injection
    if _check_injection(query):
        logger.warning("INJECTION guardrail triggered")
        resp = _injection_response()
        logger.info(f"Response time: {time.time()-start:.2f}s [INJECTION_BLOCK]")
        return resp

    # Tool routing
    q = query.lower()

    if any(kw in q for kw in FITNESS_KEYWORDS):
        resp = _fitness_sub_agent(query)
        logger.info(f"Response time: {time.time()-start:.2f}s [FITNESS_TOOL]")
        return resp

    if any(kw in q for kw in MEDICATION_KEYWORDS):
        resp = _medication_sub_agent(query)
        logger.info(f"Response time: {time.time()-start:.2f}s [MEDICATION_TOOL]")
        return resp

    # Default: Wellness LLM sub-agent
    resp = _wellness_sub_agent(query)
    logger.info(f"Response time: {time.time()-start:.2f}s [LLM_WELLNESS]")
    return resp