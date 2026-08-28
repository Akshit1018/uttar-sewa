"""Green Team: activation honesty, clip titles, query-scoped corpus load."""

import inspect
from pathlib import Path
from fastapi.testclient import TestClient

from backend.services.qa_corpus import (
    CANDIDATE_CAP,
    classify_youtube_target,
    qa_candidate_filter,
    qa_load_plan,
    summarize_qa_counts,
)
from backend.services.transcript_ingest import clip_title_from_segment, segments_to_qa
from backend.services.grounded_ask import _clip_from


ROOT = Path(__file__).resolve().parents[1]


def test_summarize_qa_counts_flags_seed_only_library():
    seed = summarize_qa_counts(curated=30, ingested=0)
    assert seed["curated_qa"] == 30
    assert seed["ingested_qa"] == 0
    assert seed["seed_only"] is True
    assert seed["total_qa_pairs"] == 30

    live = summarize_qa_counts(curated=30, ingested=12)
    assert live["seed_only"] is False
    assert live["ingested_qa"] == 12
    assert live["total_qa_pairs"] == 42


def test_clip_title_is_timestamped_snippet_not_fake_question():
    title = clip_title_from_segment("कर्म करो फल मत सोचो और मन को शांत रखो", 90)
    assert title.startswith("1:30")
    assert "कर्म" in title
    assert len(title) <= 80


def test_segments_to_qa_question_is_clip_title_not_raw_slice():
    long = "कर्म " * 40
    qa = segments_to_qa([{"start": 125, "end": 140, "text": long.strip()}], "vid", "Satsang")
    assert qa[0]["answer"] == long.strip()
    assert qa[0]["question"] != long.strip()[:80]
    assert qa[0]["question"].startswith("2:05")
    assert qa[0]["kind"] == "clip"


def test_query_scoped_load_plan_never_dumps_uncapped_corpus():
    plan = qa_load_plan("ध्यान कैसे करें")
    assert plan["mode"] == "query"
    assert plan["cap"] <= CANDIDATE_CAP
    filt = qa_candidate_filter("ध्यान कैसे करें")
    assert "$or" in filt
    empty = qa_load_plan("   ")
    assert empty["mode"] == "recent"
    assert empty["cap"] <= CANDIDATE_CAP


def test_load_qa_database_is_query_scoped():
    from backend.server import _load_qa_database

    source = inspect.getsource(_load_qa_database)
    assert "to_list(2000)" not in source
    assert "qa_load_plan" in source or "qa_candidate_filter" in source


def test_classify_youtube_watch_versus_channel():
    watch = classify_youtube_target("https://www.youtube.com/watch?v=dQw4w9wgGcQ")
    assert watch["kind"] == "video"
    assert watch["video_id"] == "dQw4w9wgGcQ"
    short = classify_youtube_target("https://youtu.be/abcdefghijk")
    assert short["kind"] == "video"
    assert short["video_id"] == "abcdefghijk"
    channel = classify_youtube_target("https://www.youtube.com/@satsang")
    assert channel["kind"] == "channel"
    assert "satsang" in channel["channel"]
    bad = classify_youtube_target("https://example.com/not-youtube")
    assert bad["kind"] == "invalid"


def test_curated_library_clips_are_labeled_even_with_video_id():
    clip = _clip_from(
        {
            "video_id": "abc123",
            "source": "curated_library",
            "question": "ध्यान?",
            "answer": "नियमित अभ्यास",
            "start_time": 0,
            "video_title": "Curated teaching",
        }
    )
    assert clip["citation_kind"] == "curated"


def test_stats_payload_exposes_curated_versus_ingested():
    from backend.server import app

    client = TestClient(app)
    body = client.get("/api/stats").json()
    assert "curated_qa" in body
    assert "ingested_qa" in body
    assert "seed_only" in body


def test_process_start_forwards_channel_url(monkeypatch):
    from backend import server

    captured = {}

    async def fake_start(channel_url=None):
        captured["url"] = channel_url
        return "job-channel"

    async def fake_settings():
        return {"processing_enabled": True}

    monkeypatch.setattr(server.processing_service, "start_channel_processing", fake_start)
    monkeypatch.setattr(server, "_load_control_settings", fake_settings)

    client = TestClient(server.app)
    response = client.post(
        "/api/process/start",
        json={"channel_url": "https://www.youtube.com/@demo-channel"},
    )
    assert response.status_code == 200
    assert captured["url"] == "https://www.youtube.com/@demo-channel"
    assert response.json()["status_id"] == "job-channel"


def test_process_from_url_routes_watch_to_ingest(monkeypatch):
    from backend import server

    captured = {}

    async def fake_settings():
        return {"processing_enabled": True}

    async def fake_list(videos):
        captured["videos"] = videos
        return {"ok": True, "ingested": 1}

    monkeypatch.setattr(server, "_load_control_settings", fake_settings)
    monkeypatch.setattr(server.processing_service, "ingest_video_list", fake_list)

    client = TestClient(server.app)
    response = client.post(
        "/api/process/from-url",
        json={"url": "https://www.youtube.com/watch?v=dQw4w9wgGcQ"},
    )
    assert response.status_code == 200
    assert captured["videos"][0]["video_id"] == "dQw4w9wgGcQ"


def test_gemini_is_optional_because_ask_does_not_call_it():
    from backend.services.byok import PROVIDERS

    by_id = {item["id"]: item for item in PROVIDERS}
    assert by_id["youtube"]["required"] is True
    assert by_id["gemini"]["required"] is False
    assert "not used" in by_id["gemini"]["help"].lower() or "unused" in by_id["gemini"]["help"].lower()


def test_pwa_chat_uses_ingested_count_and_paste_url():
    text = (ROOT / "frontend/src/components/ChatInterface.jsx").read_text()
    assert "ingested_qa" in text
    assert "from-url" in text


def test_pwa_settings_can_persist_backend_url():
    settings = (ROOT / "frontend/src/components/Pages/SettingsPage.jsx").read_text()
    backend = (ROOT / "frontend/src/lib/backend.js").read_text()
    assert "writeStoredBackendUrl" in settings
    assert "uttar_sewa_backend_url" in backend


def test_flutter_chat_and_orb_support_activation_and_undo():
    screens = (ROOT / "mobile/lib/screens.dart").read_text()
    orb = (ROOT / "mobile/lib/widgets.dart").read_text()
    api = (ROOT / "mobile/lib/api_client.dart").read_text()
    assert "ingestFromUrl" in api
    assert "ingestFromUrl" in screens
    assert "ingested_qa" in screens
    assert "undoBead" in orb
