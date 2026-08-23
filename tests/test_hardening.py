import re

from fastapi.testclient import TestClient

from backend.models import AskQuery, SearchQuery
from backend.services.control_auth import authorize_control, authorize_cloud
from backend.services.query_safety import escape_regex, clamp_limit
from backend.services.backend_url import resolve_backend_url


def test_search_and_ask_limits_are_capped():
    assert SearchQuery(query="ध्यान", limit=100000).limit == 50
    assert AskQuery(query="ध्यान", limit=0).limit == 1
    assert clamp_limit(999, high=50) == 50


def test_escape_regex_is_literal():
    raw = "(a+)+"
    escaped = escape_regex(raw)
    assert re.search(escaped, "(a+)+")
    assert not re.search(escaped, "aaaaaaaa")


def test_resolve_backend_url_never_undefined():
    assert resolve_backend_url("") == "http://127.0.0.1:8000"
    assert resolve_backend_url("undefined") == "http://127.0.0.1:8000"
    assert resolve_backend_url("https://sewa.example/api/") == "https://sewa.example"
    assert resolve_backend_url("https://sewa.example", origin="https://app.example") == "https://sewa.example"
    assert resolve_backend_url("", origin="https://app.example") == "https://app.example"


def test_cloud_authorize_fails_closed_without_token(monkeypatch):
    monkeypatch.delenv("CONTROL_TOKEN", raising=False)
    assert authorize_cloud(None) is False
    assert authorize_control(None) is True
    monkeypatch.setenv("CONTROL_TOKEN", "secret")
    assert authorize_cloud(None) is False
    assert authorize_cloud("secret") is True
    assert authorize_control(None) is False
    assert authorize_control("secret") is True


def test_cloud_routes_require_token_even_when_unset(monkeypatch):
    monkeypatch.delenv("CONTROL_TOKEN", raising=False)
    client = TestClient(__import__("backend.server", fromlist=["app"]).app)
    assert client.post("/api/cloud/restore").status_code == 401
    assert client.post("/api/cloud/backup").status_code == 401


def test_feedback_rejects_huge_payload():
    from backend.server import app

    client = TestClient(app)
    response = client.post("/api/feedback", json={"message": "x" * 20000})
    assert response.status_code in (400, 422)


def test_health_ready_tracks_database():
    from backend.server import app

    client = TestClient(app)
    body = client.get("/api/health").json()
    assert body["ready"] == body["database"]
    assert "ok" in body


def test_search_handler_is_lexical_only():
    import inspect

    from backend.server import search_questions

    source = inspect.getsource(search_questions)
    assert "enhanced_search" not in source
    assert "rank_answers" in source


def test_search_suggestions_limit_is_clamped():
    from backend.server import app

    client = TestClient(app)
    response = client.get("/api/search/suggestions", params={"query": "ध्यान", "limit": 999})
    assert response.status_code == 200
    assert len(response.json().get("suggestions") or []) <= 20
