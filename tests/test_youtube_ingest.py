import asyncio
from datetime import datetime, timezone

from backend.services.youtube_ingest import build_library, video_record_from_oembed
from backend.services.youtube_service import YouTubeService
from backend.services.processing_service import ProcessingService
from tests.test_processing_whisper import FakeDB, FakeLLM, VIDEO


class FakeYouTubeFetcher:
    def __init__(self, videos=None, captions=None):
        self.videos = videos or [
            {
                "video_id": "abc123",
                "title": "Satsang",
                "description": "live",
                "duration": "0:10:00",
                "upload_date": datetime.now(timezone.utc),
                "view_count": 9,
                "transcript_processed": False,
            }
        ]
        self.captions = captions if captions is not None else {
            "abc123": [{"start_time": 10, "end_time": 20, "text": "ध्यान करो", "language": "hi"}]
        }
        self.channel_calls = []

    def list_channel_videos(self, channel):
        self.channel_calls.append(channel)
        return list(self.videos)

    def get_captions(self, video_id):
        return self.captions.get(video_id)


def test_injected_fetcher_lists_videos_without_api_key(monkeypatch):
    monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)
    fetcher = FakeYouTubeFetcher()
    service = YouTubeService(fetcher=fetcher)
    videos = asyncio.run(service.get_channel_videos("bhajanmarg"))
    assert videos[0]["video_id"] == "abc123"
    assert fetcher.channel_calls == ["bhajanmarg"]
    captions = asyncio.run(service.get_video_captions("abc123"))
    assert captions[0]["text"] == "ध्यान करो"


def test_build_library_from_youtube_videos_not_curated():
    library = build_library(
        videos=[{"video_id": "abc123", "title": "Satsang"}],
        captions_for=lambda _vid: [{"start_time": 10, "end_time": 20, "text": "ध्यान करो"}],
    )
    assert library["source"] == "youtube"
    assert library["invented"] is False
    assert library["videos"][0]["video_id"] == "abc123"
    assert library["videos"][0]["transcript_processed"] is True
    assert library["segments"][0]["text"] == "ध्यान करो"
    assert library["qa"][0]["video_id"] == "abc123"
    assert library["qa"][0]["answer"] == "ध्यान करो"
    assert "curated" not in (library["qa"][0].get("source") or "")


def test_build_library_uses_whisper_when_captions_missing(tmp_path):
    (tmp_path / "abc123.wav").write_bytes(b"RIFF")
    library = build_library(
        videos=[{"video_id": "abc123", "title": "Satsang"}],
        captions_for=lambda _vid: None,
        transcribe=lambda _path, language="hi": [{"start": 0, "end": 3, "text": "राम राम"}],
        audio_directory=str(tmp_path),
    )
    assert library["qa"][0]["answer"] == "राम राम"
    assert library["videos"][0]["transcript_processed"] is True


def test_build_library_skips_empty_transcript_without_inventing():
    library = build_library(
        videos=[{"video_id": "empty1", "title": "No speech"}],
        captions_for=lambda _vid: None,
    )
    assert library["qa"] == []
    assert library["skipped"] == ["empty1"]
    assert library["videos"][0]["transcript_processed"] is False
    assert library["invented"] is False


def test_oembed_meta_becomes_ingest_video_record():
    record = video_record_from_oembed(
        {"title": "Live Satsang", "author_name": "Bhajan Marg"},
        video_id="xyz789",
    )
    assert record["video_id"] == "xyz789"
    assert record["title"] == "Live Satsang"
    assert record["transcript_processed"] is False
    assert record["source"] == "youtube_oembed"


def test_processing_ingest_video_list_stores_youtube_qa_not_curated():
    db = FakeDB()
    service = ProcessingService(
        db,
        youtube_service=YouTubeService(fetcher=FakeYouTubeFetcher()),
        llm_service=FakeLLM(pairs=[]),
    )
    result = asyncio.run(
        service.ingest_video_list(
            [
                {
                    **VIDEO,
                    "captions": [{"start_time": 4, "end_time": 9, "text": "गुरु चरण", "language": "hi"}],
                }
            ]
        )
    )
    assert result["ok"] is True
    assert result["source"] == "youtube"
    assert result["qa_count"] == 1
    assert db.question_answers.docs[0]["answer"] == "गुरु चरण"
    assert db.videos.docs[0]["transcript_processed"] is True


def test_ingest_from_channel_uses_fetcher_not_api_key(monkeypatch):
    monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)
    db = FakeDB()
    service = ProcessingService(
        db,
        youtube_service=YouTubeService(fetcher=FakeYouTubeFetcher()),
        llm_service=FakeLLM(pairs=[]),
    )
    result = asyncio.run(service.ingest_from_channel("bhajanmarg"))
    assert result["ok"] is True
    assert result["source"] == "youtube"
    assert result["qa_count"] == 1
    assert db.question_answers.docs[0]["video_id"] == "abc123"


def test_ingest_endpoint_requires_videos_or_channel():
    from fastapi.testclient import TestClient

    from backend.server import app

    client = TestClient(app)
    response = client.post("/api/process/ingest", json={})
    assert response.status_code == 400
    paths = {getattr(route, "path", None) for route in app.routes}
    assert "/api/process/ingest" in paths
