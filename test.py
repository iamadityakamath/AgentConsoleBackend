import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

import requests


BASE_URL = "http://localhost:8000/api/v1"
OUTPUT_FILE = Path("api_responses.json")
TIMEOUT_SECONDS = 20
MEMBER_ID = "MBR-10001"


def fetch_json(url: str) -> Dict[str, Any]:
    """Fetch one URL and return a structured response payload."""
    try:
        response = requests.get(url, timeout=TIMEOUT_SECONDS)
        payload: Dict[str, Any] = {
            "url": url,
            "status_code": response.status_code,
            "ok": response.ok,
        }

        try:
            payload["data"] = response.json()
        except ValueError:
            payload["data"] = response.text

        return payload
    except Exception as exc:
        return {
            "url": url,
            "status_code": None,
            "ok": False,
            "error": str(exc),
        }


def main() -> None:
    responses: Dict[str, Any] = {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "base_url": BASE_URL,
        "routes": {},
    }

    responses["member_id_used"] = MEMBER_ID

    member_routes = {
        "patient_by_member_id": f"{BASE_URL}/patients/{MEMBER_ID}",
        "care_gaps_by_member_id": f"{BASE_URL}/care-gaps/{MEMBER_ID}",
        "lab_results_by_member_id": f"{BASE_URL}/lab-results/{MEMBER_ID}",
        "medications_by_member_id": f"{BASE_URL}/medications/{MEMBER_ID}",
        "prior_auth_by_member_id": f"{BASE_URL}/prior-auth/{MEMBER_ID}",
        "ehr_notes_by_member_id": f"{BASE_URL}/ehr-notes/{MEMBER_ID}",
    }

    for key, url in member_routes.items():
        responses["routes"][key] = fetch_json(url)

    OUTPUT_FILE.write_text(json.dumps(responses, indent=2), encoding="utf-8")
    print(f"Saved API responses to {OUTPUT_FILE.resolve()}")


if __name__ == "__main__":
    main()
