from app.main import app


def test_status_endpoint_returns_200():
    client = app.test_client()
    response = client.get("/")
    assert response.status_code == 200


def test_status_payload_contains_service_name():
    client = app.test_client()
    response = client.get("/")
    data = response.get_json()
    assert data["service"] == "CloudPulse Telemetry API"
    assert data["status"] == "ONLINE"
