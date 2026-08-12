from backend.services.relevance_search import expand_query, is_follow_up


def test_short_hindi_follow_up_uses_prior_question():
    expanded = expand_query("और कैसे?", ["ध्यान कैसे करें?"])
    assert "ध्यान" in expanded
    assert "कैसे" in expanded


def test_english_tell_me_more_is_a_follow_up():
    assert is_follow_up("tell me more")
    expanded = expand_query("why?", ["What is karma?"])
    assert "karma" in expanded.lower()


def test_standalone_question_is_not_rewritten():
    query = "मोक्ष कैसे प्राप्त करें?"
    assert expand_query(query, ["ध्यान कैसे करें?"]) == query


def test_empty_history_returns_original():
    assert expand_query("और कैसे?", []) == "और कैसे?"
