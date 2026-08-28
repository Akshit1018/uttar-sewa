"""Close remaining Green Team leftovers: secrets, pins, jobs, indexes, rate limits."""

from pathlib import Path

from backend.db_schema import INDEXES
from backend.services.control_auth import authorize_control
from backend.services.job_resume import jobs_to_resume
from backend.services.rate_limit import RateLimiter
from backend.services.secret_seal import seal_secret, unseal_secret


ROOT = Path(__file__).resolve().parents[1]


def test_secrets_are_sealed_not_stored_cleartext():
    token = "AIzaSySuperSecretKey99"
    sealed = seal_secret(token, key="operator-secret")
    assert token not in sealed
    assert sealed.startswith("enc_v1:")
    assert unseal_secret(sealed, key="operator-secret") == token
    assert unseal_secret(token, key="operator-secret") == token


def test_secrets_document_does_not_embed_raw_youtube_key():
    from backend.services.byok import secrets_document, secrets_from_document

    doc = secrets_document({"youtube": "AIzaSySuperSecretKey99"}, key="k")
    blob = str(doc)
    assert "SuperSecret" not in blob
    assert secrets_from_document(doc, key="k")["youtube"] == "AIzaSySuperSecretKey99"


def test_unique_index_failure_is_not_downgraded(monkeypatch):
    from backend.services import database as database_mod

    class FakeColl:
        def __init__(self):
            self.calls = []

        async def create_index(self, keys, name=None, unique=False, background=True):
            self.calls.append({"name": name, "unique": unique})
            if unique:
                raise RuntimeError("existing non-unique index")

    coll = FakeColl()

    class FakeDb:
        def __getitem__(self, _name):
            return coll

    import asyncio

    asyncio.get_event_loop().run_until_complete(database_mod.ensure_indexes(FakeDb()))
    unique_calls = [item for item in coll.calls if item["unique"]]
    nonunique_after_fail = [item for item in coll.calls if item["unique"] is False and "video_id" in (item["name"] or "")]
    assert unique_calls
    assert not any(item["name"] == unique_calls[0]["name"] and item["unique"] is False for item in coll.calls)


def test_control_writes_fail_closed_off_loopback_when_token_unset(monkeypatch):
    monkeypatch.delenv("CONTROL_TOKEN", raising=False)
    assert authorize_control(None) is True
    assert authorize_control(None, peer="127.0.0.1") is True
    assert authorize_control(None, peer="testclient") is True
    assert authorize_control(None, peer="203.0.113.9") is False


def test_rate_limiter_blocks_after_window_budget():
    limiter = RateLimiter()
    for _ in range(3):
        assert limiter.allow("ask:1.1.1.1", limit=3, window_s=60) is True
    assert limiter.allow("ask:1.1.1.1", limit=3, window_s=60) is False
    assert limiter.allow("ask:2.2.2.2", limit=3, window_s=60) is True


def test_interrupted_processing_jobs_are_resumable():
    rows = [
        {"id": "live", "status": "processing", "channel_url": "https://youtube.com/@x"},
        {"id": "queued", "status": "pending", "channel_url": None},
        {"id": "done", "status": "completed", "channel_url": "https://youtube.com/@y"},
        {"id": "dead", "status": "failed"},
    ]
    resume = jobs_to_resume(rows)
    assert [item["id"] for item in resume] == ["live", "queued"]
    assert resume[0]["channel_url"] == "https://youtube.com/@x"


def test_schema_has_text_index_and_feedback():
    found_text = False
    for spec in INDEXES["question_answers"]:
        keys = spec.get("keys") if isinstance(spec, dict) else spec
        if any(direction == "text" for _field, direction in keys):
            found_text = True
    assert found_text
    assert "feedback" in INDEXES


def test_pin_is_seeker_action_when_control_token_set(monkeypatch):
    from fastapi.testclient import TestClient
    from backend.server import app

    monkeypatch.setenv("CONTROL_TOKEN", "lock")
    client = TestClient(app)
    pinned = client.post(
        "/api/control/qa/pin",
        json={"question": "ध्यान", "answer": "अभ्यास", "video_id": "abc", "start_time": 12},
    )
    assert pinned.status_code == 200
    denied = client.put("/api/control/keys", json={"youtube": "AIzaSyBlocked"})
    assert denied.status_code == 401
    removed = client.post("/api/control/qa/unpin", json={"video_id": "abc", "question": "ध्यान"})
    assert removed.status_code == 200


def test_pwa_favorites_and_mala_sync_and_byok_are_wired():
    favorites = (ROOT / "frontend/src/hooks/useFavorites.js").read_text()
    mala = (ROOT / "frontend/src/hooks/useMala.js").read_text()
    settings = (ROOT / "frontend/src/components/Pages/SettingsPage.jsx").read_text()
    assert "/control/qa/pin" in favorites
    assert "/control/qa/unpin" in favorites or "/control/qa/pinned" in favorites
    assert "/mala/sync" in mala
    assert "/control/keys" in settings


def test_dead_ultra_search_is_not_imported_by_server():
    source = (ROOT / "backend/server.py").read_text()
    assert "ultra_search_engine" not in source
    assert "enhanced_search_coordinator" not in source
    assert "ultra_video_service" not in source
