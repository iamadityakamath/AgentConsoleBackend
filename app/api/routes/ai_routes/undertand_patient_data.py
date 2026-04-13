"""AI route to accept patient data, call ChatGPT, and store the incoming payload."""
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, Body, HTTPException, status
from starlette.concurrency import run_in_threadpool

from app.core.config import get_settings

# try:
#     from openai import OpenAI
# except ImportError:  # pragma: no cover
#     OpenAI = None


router = APIRouter(prefix="/ai", tags=["AI Routes"])


SAVE_FILE = (
    Path(__file__).resolve().parents[4]
    / "received_patient_data.json"
)

CHATGPT_RAW_FILE = (
    Path(__file__).resolve().parents[4]
    / "chatgpt_raw_response.json"
)

PROMPT_FILE = (
    Path(__file__).resolve().parents[4]
    / "prompts"
    / "ai"
    / "undertand_patient_data.prompt.txt"
)

MOCK_RESPONSE_FILE = (
    Path(__file__).resolve().parent
    / "mock_chatgpt_response.json"
)


@lru_cache(maxsize=1)
def load_prompt_template() -> str:
    """Load and cache the prompt template from disk."""

    return PROMPT_FILE.read_text(encoding="utf-8")


def build_prepared_prompt(payload: Dict[str, Any]) -> str:
    """Build the final prompt including the incoming request body."""

    prompt_template = load_prompt_template()
    return (
        f"{prompt_template}\n\n"
        "PATIENT_INPUT_JSON:\n"
        f"{json.dumps(payload, indent=2, ensure_ascii=False)}"
    )


# def generate_chatgpt_response(prepared_prompt: str, api_key: str) -> str:
#     """Call ChatGPT and return the response text."""
#
#     if OpenAI is None:
#         raise RuntimeError("The 'openai' package is not installed.")
#
#     client = OpenAI(api_key=api_key)
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[{"role": "user", "content": prepared_prompt}],
#         temperature=0.3,
#         top_p=1,
#         stop=None,
#     )
#
#     return (completion.choices[0].message.content or "").strip()


# def parse_json_if_possible(model_response: str) -> Dict[str, Any] | None:
#     """Try to parse JSON response content; return None if parsing fails."""
#
#     cleaned = model_response.strip()
#     if cleaned.startswith("```"):
#         cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
#         if cleaned.endswith("```"):
#             cleaned = cleaned[:-3].strip()
#
#     try:
#         parsed = json.loads(cleaned)
#     except json.JSONDecodeError:
#         return None
#
#     return parsed if isinstance(parsed, dict) else None


# def build_json_repair_prompt(non_json_response: str) -> str:
#     """Build a strict repair prompt to force a valid JSON object response."""
#
#     return (
#         "Your previous response was not valid JSON. "
#         "Rewrite it as a valid JSON object only. "
#         "Do not include markdown, code fences, or extra text.\n\n"
#         "PREVIOUS_RESPONSE:\n"
#         f"{non_json_response}"
#     )


# def save_raw_chatgpt_output(initial_response: str, repaired_response: str | None = None) -> None:
#     """Persist raw ChatGPT outputs for review before JSON parsing."""
#
#     payload: Dict[str, Any] = {
#         "initial_response": initial_response,
#         "repaired_response": repaired_response,
#     }
#     CHATGPT_RAW_FILE.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")


@router.post(
    "/undertand_patient_data",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def undertand_patient_data(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """Accept patient data payload and return mock response for frontend testing."""

    saved_payload = {
        "received": True,
        "patient_data": payload,
    }
    SAVE_FILE.write_text(json.dumps(saved_payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # Load mock response from file
    mock_response = json.loads(MOCK_RESPONSE_FILE.read_text(encoding="utf-8"))

    return {
        "chatgpt_response": mock_response,
    }
