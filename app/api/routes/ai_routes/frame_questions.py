"""AI route to frame questions using OpenAI and v2 prompt instructions."""
import json
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict

from fastapi import APIRouter, Body, HTTPException, status
from starlette.concurrency import run_in_threadpool

from app.core.config import get_settings

try:
    from openai import OpenAI
except ImportError:  # pragma: no cover
    OpenAI = None


router = APIRouter(prefix="/ai", tags=["AI Routes"])


SAVE_FILE = (
    Path(__file__).resolve().parents[4]
    / "received_frame_questions_payload.json"
)

RAW_FILE = (
    Path(__file__).resolve().parents[4]
    / "frame_questions_raw_response.json"
)

PROMPT_FILE = (
    Path(__file__).resolve().parents[4]
    / "prompts"
    / "ai"
    / "undertand_patient_data_v2.prompt.txt"
)


@lru_cache(maxsize=1)
def load_mock_response() -> Dict[str, Any]:
    """Load and cache v2 prompt template for frame questions."""

    return {"prompt": PROMPT_FILE.read_text(encoding="utf-8")}


def build_prompt(payload: Dict[str, Any]) -> str:
    """Build prompt for OpenAI call with input payload."""

    prompt_template = load_mock_response()["prompt"]
    return (
        f"{prompt_template}\n\n"
        "PATIENT_INPUT_JSON:\n"
        f"{json.dumps(payload, indent=2, ensure_ascii=False)}"
    )


def generate_frame_questions_response(prepared_prompt: str, api_key: str) -> str:
    """Call OpenAI and return text response."""

    if OpenAI is None:
        raise RuntimeError("The 'openai' package is not installed.")

    client = OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prepared_prompt}],
        temperature=0.2,
        max_tokens=1400,
        top_p=1,
        stop=None,
    )
    return (completion.choices[0].message.content or "").strip()


def parse_json_if_possible(model_response: str) -> Dict[str, Any] | None:
    """Try to parse JSON response content; return None if parsing fails."""

    cleaned = model_response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.removeprefix("```json").removeprefix("```").strip()
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

    try:
        parsed = json.loads(cleaned)
    except json.JSONDecodeError:
        return None

    return parsed if isinstance(parsed, dict) else None


def build_json_repair_prompt(non_json_response: str) -> str:
    """Build a strict repair prompt to force JSON response."""

    return (
        "Your previous response was not valid JSON. "
        "Rewrite it as a valid JSON object only. "
        "Do not include markdown, code fences, or extra text.\n\n"
        "PREVIOUS_RESPONSE:\n"
        f"{non_json_response}"
    )


def save_raw_output(initial_response: str, repaired_response: str | None = None) -> None:
    """Persist raw OpenAI outputs for troubleshooting."""

    RAW_FILE.write_text(
        json.dumps(
            {
                "initial_response": initial_response,
                "repaired_response": repaired_response,
            },
            indent=2,
            ensure_ascii=False,
        ),
        encoding="utf-8",
    )


@router.post(
    "/frame-questions",
    response_model=Dict[str, Any],
    status_code=status.HTTP_200_OK,
)
async def frame_questions(payload: Dict[str, Any] = Body(...)) -> Dict[str, Any]:
    """Accept payload and return OpenAI-generated framed questions JSON."""

    SAVE_FILE.write_text(
        json.dumps({"received": True, "payload": payload}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )

    settings = get_settings()
    api_key = settings.openai_api_key.strip()
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="OpenAI API key is not configured. Set OPENAI_API_KEY (or API_KEY) in .env.",
        )

    prepared_prompt = build_prompt(payload)
    try:
        model_response = await run_in_threadpool(generate_frame_questions_response, prepared_prompt, api_key)
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail=f"OpenAI request failed: {exc}",
        ) from exc

    save_raw_output(model_response)
    parsed_response = parse_json_if_possible(model_response)

    if parsed_response is None:
        repair_prompt = build_json_repair_prompt(model_response)
        try:
            repaired_response = await run_in_threadpool(generate_frame_questions_response, repair_prompt, api_key)
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"OpenAI JSON repair request failed: {exc}",
            ) from exc

        save_raw_output(model_response, repaired_response)
        parsed_response = parse_json_if_possible(repaired_response)

    if parsed_response is None:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="OpenAI did not return valid JSON after retry.",
        )

    return {
        "chatgpt_response": parsed_response,
    }
