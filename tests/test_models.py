from backend.models import SearchQuery, SearchResult
from backend.services.timestamp_urls import build_watch_url


def test_search_query_accepts_memory_and_channel():
    query = SearchQuery(
        query="और कैसे?",
        conversation_history=["ध्यान कैसे करें?"],
        channel_id="meditation",
        limit=3,
    )
    assert query.conversation_history == ["ध्यान कैसे करें?"]
    assert query.channel_id == "meditation"


def test_search_result_timestamp_url_shape():
    url = build_watch_url("abc", 90)
    result = SearchResult(
        question="q",
        answer="a",
        video_id="abc",
        video_title="title",
        start_time=90,
        end_time=120,
        confidence_score=0.8,
        youtube_url="https://www.youtube.com/watch?v=abc",
        timestamp_url=url,
        related_questions=["next?"],
    )
    assert result.timestamp_url == "https://www.youtube.com/watch?v=abc&t=90"
    assert result.related_questions == ["next?"]
