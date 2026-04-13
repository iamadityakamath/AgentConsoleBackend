from fastapi.testclient import TestClient

from app.api.routes.ai_routes import undertand_patient_data as understand_route
from app.api.routes.ai_routes import frame_questions as frame_questions_route
from app.main import app


client = TestClient(app)


def test_health_endpoint() -> None:
    response = client.get("/api/v1/health")
    assert response.status_code == 200


def test_ai_route_accepts_patient_data() -> None:
    def fake_chatgpt_response(prepared_prompt: str, api_key: str) -> str:
        assert "PATIENT_INPUT_JSON" in prepared_prompt
        assert api_key
        return '{"clinical_story":"Mock summary"}'

    original_generator = understand_route.generate_chatgpt_response
    understand_route.generate_chatgpt_response = fake_chatgpt_response

    payload = {
        "member_id": "MBR-10002",
        "patient_snapshot": {
            "member_id": "MBR-10002",
            "full_name": "James Thornton",
        },
        "source": "overview-left-panel",
    }
    try:
        response = client.post("/api/v1/ai/undertand_patient_data", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert body == {"chatgpt_response": {"clinical_story": "Mock summary"}}
    finally:
        understand_route.generate_chatgpt_response = original_generator


def test_ai_route_frame_questions_returns_mock_response() -> None:
    def fake_frame_questions_response(prepared_prompt: str, api_key: str) -> str:
        assert "PATIENT_INPUT_JSON" in prepared_prompt
        assert api_key
        return '{"clinical_story":"V2 summary","timeline_events":[],"coordinator_questions":[],"missed_follow_ups":[],"medication_risk_connections":[],"coordinator_alerts":[]}'

    original_generator = frame_questions_route.generate_frame_questions_response
    frame_questions_route.generate_frame_questions_response = fake_frame_questions_response

    payload = {
        "member_id": "MBR-10002",
        "source": "overview-left-panel",
    }
    try:
        response = client.post("/api/v1/ai/frame-questions", json=payload)
        assert response.status_code == 200
        body = response.json()
        assert "chatgpt_response" in body
        assert body["chatgpt_response"]["clinical_story"] == "V2 summary"
        assert isinstance(body["chatgpt_response"]["coordinator_questions"], list)
    finally:
        frame_questions_route.generate_frame_questions_response = original_generator
