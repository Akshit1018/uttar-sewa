from backend.services.relevance_search import library_as_qa, recommend_from_history


def test_library_fallback_has_channel_metadata():
    items = library_as_qa()
    assert len(items) > 10
    assert all(item["question"] and item["answer"] for item in items)
    assert any(item["channel_id"] for item in items)


def test_recommendations_follow_recent_meditation_queries():
    corpus = library_as_qa()
    results = recommend_from_history(["ध्यान", "meditation"], corpus, limit=4)
    assert results
    blob = " ".join(item["question"].lower() + item["answer"].lower() for item in results)
    assert "ध्यान" in blob or "meditat" in blob
