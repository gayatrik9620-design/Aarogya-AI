import os
import time
from pathlib import Path

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI

from src.fitness_tool import get_fitness_summary


# =========================================================
# LOAD PROJECT ROOT .ENV FILE
# =========================================================

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = PROJECT_ROOT / ".env"

load_dotenv(dotenv_path=ENV_PATH, override=True)

DEFAULT_MODEL = "gemini-3.8-flash"


def get_model_name() -> str:
    # Reload .env with override=True so updates to .env are respected on restart
    load_dotenv(dotenv_path=ENV_PATH, override=True)
    raw_model = os.getenv("GEMINI_MODEL", DEFAULT_MODEL)
    cleaned_model = (raw_model or "").strip().strip('"').strip("'")
    return cleaned_model or DEFAULT_MODEL


def get_api_key() -> str:
    load_dotenv(dotenv_path=ENV_PATH)

    try:
        import streamlit as st
        raw_key = st.secrets.get("GOOGLE_API_KEY", "")
    except Exception:
        raw_key = ""

    if not raw_key:
        raw_key = os.getenv("GOOGLE_API_KEY", "")

    return (raw_key or "").strip().strip('"').strip("'")


# =========================================================
# SAFETY SYSTEM PROMPT
# =========================================================

SAFETY_SYSTEM_PROMPT = """
You are Aarogya AI, a helpful and safe personal healthcare assistant.

Rules:
1. Give general health and wellness information only.
2. Never provide a definite medical diagnosis.
3. Never prescribe medicines or dosages.
4. For serious or persistent symptoms, recommend consulting a doctor.
5. For chest pain, severe breathing difficulty, sudden numbness,
   uncontrolled bleeding, or immediate danger, advise urgent medical
   care and calling India emergency number 112.
6. End health guidance with:
Disclaimer: I am an AI assistant, not a doctor.
Please consult a medical professional for advice.

User Query: {user_query}

Response:
"""


# =========================================================
# FITNESS KEYWORDS
# =========================================================

FITNESS_KEYWORDS = (
    "fitness summary",
    "my health data",
    "my steps",
    "my sleep",
    "my weight",
    "health report",
    "fitness report",
    "health summary",
    "show my health",
    "show fitness",
    "health statistics",
)


# =========================================================
# BUILD GEMINI CHAIN
# =========================================================

def _build_chain(api_key: str, model_name: str):

    llm = ChatGoogleGenerativeAI(
        model=model_name,
        google_api_key=api_key,
        temperature=0.3,
        timeout=60,
        max_retries=3,
    )

    prompt = PromptTemplate(
        input_variables=["user_query"],
        template=SAFETY_SYSTEM_PROMPT,
    )

    return prompt | llm | StrOutputParser()


# =========================================================
# STREAMLIT CACHING
# =========================================================

try:
    import streamlit as st

    @st.cache_resource(show_spinner=False)
    def _get_cached_chain(api_key: str, model_name: str):
        return _build_chain(api_key, model_name)

    @st.cache_data(ttl=300, show_spinner=False)
    def _invoke_cached_query(normalized_query: str, model_name: str) -> str:

        api_key = get_api_key()

        if not api_key:
            return "Error: GOOGLE_API_KEY missing in .env file."

        chain = _get_cached_chain(api_key, model_name)

        return chain.invoke({
            "user_query": normalized_query
        })


except Exception:

    _FALLBACK_CHAINS = {}

    def _invoke_cached_query(normalized_query: str, model_name: str) -> str:

        api_key = get_api_key()

        if not api_key:
            return "Error: GOOGLE_API_KEY missing in .env file."

        key = (api_key, model_name)

        if key not in _FALLBACK_CHAINS:
            _FALLBACK_CHAINS[key] = _build_chain(
                api_key,
                model_name
            )

        return _FALLBACK_CHAINS[key].invoke({
            "user_query": normalized_query
        })


# =========================================================
# STREAMING CHATBOT RESPONSE
# =========================================================

def stream_chatbot_response(user_query: str):

    if not user_query or not user_query.strip():
        yield "Please enter a health or wellness question."
        return

    cleaned_query = " ".join(user_query.strip().split())
    lowered_query = cleaned_query.lower()

    if any(keyword in lowered_query for keyword in FITNESS_KEYWORDS):
        yield get_fitness_summary()
        return

    api_key = get_api_key()

    if not api_key:
        yield "Error: GOOGLE_API_KEY missing in .env file."
        return

    model_name = get_model_name()
    print(f"[Aarogya-AI] STREAM MODEL IN USE: {model_name}")

    try:

        chain = _build_chain(api_key, model_name)

        for chunk in chain.stream({
            "user_query": cleaned_query
        }):
            if chunk:
                yield chunk

    except Exception as e:

        print(f"[Aarogya-AI] Streaming error (model={model_name}): {e}")

        yield f"Unable to get chatbot response: {e}"


# =========================================================
# NORMAL CHATBOT RESPONSE
# =========================================================

def get_chatbot_response(user_query: str) -> str:

    t0 = time.perf_counter()

    if not user_query or not user_query.strip():
        return "Please enter a health or wellness question."

    cleaned_query = " ".join(user_query.strip().split())
    lowered_query = cleaned_query.lower()

    # Fitness tool
    if any(keyword in lowered_query for keyword in FITNESS_KEYWORDS):

        t_fit = time.perf_counter()

        result = get_fitness_summary()

        print(
            f"[Aarogya-AI] fitness_tool took "
            f"{(time.perf_counter() - t_fit):.2f}s"
        )

        return result

    # API key
    api_key = get_api_key()

    if not api_key:
        return "Error: GOOGLE_API_KEY missing in .env file."

    # Model configuration
    model_name = get_model_name()

    print(f"[Aarogya-AI] MODEL IN USE: {model_name}")

    try:

        result = _invoke_cached_query(
            lowered_query,
            model_name
        )

        print(
            f"[Aarogya-AI] LLM response took "
            f"{(time.perf_counter() - t0):.2f}s "
            f"(model={model_name})"
        )

        return result

    except Exception as e:

        print(
            f"[Aarogya-AI] LLM error after "
            f"{(time.perf_counter() - t0):.2f}s (model={model_name}): {e}"
        )

        return f"Unable to get chatbot response: {e}"