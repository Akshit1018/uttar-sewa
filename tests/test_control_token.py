from fastapi.testclient import TestClient

from backend.server import app


def test_control_writes_open_when_token_unset(monkeypatch):
    monkeypatch.delenv("CONTROL_TOKEN", raising=False)
    client = TestClient(app)
    response = client.post("/api/process/ingest", json={})
    assert response.status_code == 400


def test_control_writes_require_token_when_set(monkeypatch):
    monkeypatch.setenv("CONTROL_TOKEN", "sewa-secret")
    client = TestClient(app)
    denied = client.put("/api/control/keys", json={"youtube": "AIzaSyBlockedKeyXX"})
    assert denied.status_code == 401
    denied_ingest = client.post("/api/process/ingest", json={"video_ids": ["abc123"]})
    assert denied_ingest.status_code == 401
    allowed = client.put(
        "/api/control/keys",
        json={"youtube": "AIzaSyAllowedKeyYY"},
        headers={"X-Control-Token": "sewa-secret"},
    )
    assert allowed.status_code == 200
    assert "AIzaSyAllowedKeyYY" not in str(allowed.json())
