from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


LIST_ENDPOINTS = [
    "/",
    "/api/v1/health",
    "/api/v1/care-gaps",
    "/api/v1/ehr-notes",
    "/api/v1/insurance-claims",
    "/api/v1/lab-results",
    "/api/v1/medications",
    "/api/v1/patients",
    "/api/v1/pharmacy-claims",
    "/api/v1/prior-auth",
]


DETAIL_ENDPOINTS = [
    ("/api/v1/care-gaps", "member_id"),
    ("/api/v1/ehr-notes", "member_id"),
    ("/api/v1/insurance-claims", "claim_id"),
    ("/api/v1/lab-results", "member_id"),
    ("/api/v1/medications", "member_id"),
    ("/api/v1/patients", "member_id"),
    ("/api/v1/pharmacy-claims", "rx_claim_id"),
    ("/api/v1/prior-auth", "member_id"),
]


def test_all_list_endpoints_return_200() -> None:
    for endpoint in LIST_ENDPOINTS:
        response = client.get(endpoint)
        assert response.status_code == 200, f"Failed endpoint: {endpoint}, body: {response.text}"


def test_all_detail_endpoints_return_200_for_existing_records() -> None:
    for base_endpoint, id_field in DETAIL_ENDPOINTS:
        list_response = client.get(base_endpoint)
        assert list_response.status_code == 200, (
            f"List failed for {base_endpoint}, body: {list_response.text}"
        )

        data = list_response.json()
        assert isinstance(data, list), f"Expected list response for {base_endpoint}"
        assert len(data) > 0, f"Expected non-empty data for {base_endpoint}"

        record_id = data[0].get(id_field)
        assert record_id is not None, f"Missing ID field '{id_field}' in {base_endpoint}"

        detail_response = client.get(f"{base_endpoint}/{record_id}")
        assert detail_response.status_code == 200, (
            f"Detail failed for {base_endpoint}/{record_id}, body: {detail_response.text}"
        )
