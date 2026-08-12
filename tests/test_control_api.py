from backend.db_schema import COLLECTIONS, INDEXES
from backend.services.control_store import (
    default_settings,
    merge_settings,
    pin_document,
    dashboard_payload,
)


def test_schema_has_core_collections():
    names = set(COLLECTIONS.values())
    assert "videos" in names
    assert "question_answers" in names
    assert "control_settings" in names
    assert "pinned_qa" in names
    assert "mala_days" in names
    assert INDEXES["question_answers"]
    assert INDEXES["videos"]


def test_default_settings_are_controllable():
    settings = default_settings()
    assert settings["language"] == "hi"
    assert settings["beads_per_cycle"] == 108
    assert settings["processing_enabled"] is True
    assert settings["public_companions"] is True
    assert settings["sandhya"] is True


def test_merge_settings_clamps_cycle_length():
    merged = merge_settings(default_settings(), {"beads_per_cycle": 27, "language": "en"})
    assert merged["beads_per_cycle"] == 27
    assert merged["language"] == "en"
    bad = merge_settings(default_settings(), {"beads_per_cycle": 99})
    assert bad["beads_per_cycle"] == 108


def test_pin_document_marks_verified_clip():
    doc = pin_document(
        {
            "question": "ध्यान",
            "answer": "नियमित अभ्यास",
            "video_id": "abc",
            "start_time": 12,
        }
    )
    assert doc["pinned"] is True
    assert doc["video_id"] == "abc"
    assert doc["question"] == "ध्यान"


def test_dashboard_payload_shape():
    payload = dashboard_payload(
        stats={"total_videos": 2, "processed_videos": 1, "total_qa_pairs": 9, "unprocessed_videos": 1},
        settings=default_settings(),
        pinned_count=3,
        api_ok=True,
    )
    assert payload["ready"] is True
    assert payload["stats"]["total_qa_pairs"] == 9
    assert payload["controls"]["language"] == "hi"
    assert "named_malas" in payload["controls"]
    assert payload["database"] == "uttar_sewa"
    assert payload["enrichment"]["listed_in"].endswith("public-apis")


def test_control_http_endpoints_work_without_mongo():
    from fastapi.testclient import TestClient

    from backend.server import app

    client = TestClient(app)
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["ok"] is True
    assert health.json()["api"] is True

    root = client.get("/api/")
    assert root.status_code == 200
    assert root.json()["flutter"] is True

    dash = client.get("/api/control/dashboard")
    assert dash.status_code == 200
    body = dash.json()
    assert "stats" in body
    assert "controls" in body
    assert body["controls"]["beads_per_cycle"] in (11, 27, 54, 108)

    settings = client.put("/api/control/settings", json={"beads_per_cycle": 27, "language": "en"})
    assert settings.status_code == 200
    assert settings.json()["beads_per_cycle"] == 27
    assert settings.json()["language"] == "en"

    pin = client.post(
        "/api/control/qa/pin",
        json={"question": "ध्यान", "answer": "अभ्यास", "video_id": "abc", "start_time": 12},
    )
    assert pin.status_code == 200
    assert pin.json()["pinned"] is True

    pinned = client.get("/api/control/qa/pinned")
    assert pinned.status_code == 200
    assert "items" in pinned.json()

    gaps = client.get("/api/control/library/gaps")
    assert gaps.status_code == 200
    assert "items" in gaps.json()

    catalog = client.get("/api/enrich/catalog")
    assert catalog.status_code == 200
    ids = {item["id"] for item in catalog.json()["items"]}
    assert "gita" in ids
    assert catalog.json()["public_apis"].endswith("public-apis")

    blocked = client.post("/api/control/scrape", json={"url": "http://127.0.0.1/secret"})
    assert blocked.status_code == 400

    search = client.post("/api/search", json={"query": "ध्यान", "language": "hi", "limit": 2})
    assert search.status_code == 200
    assert isinstance(search.json(), list)
    assert search.json()

    cleared = client.post("/api/process/clear")
    assert cleared.status_code == 200
