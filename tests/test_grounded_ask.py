from backend.services.grounded_ask import grounded_ask
from backend.services.relevance_search import library_as_qa


def test_known_hindi_question_is_answered_from_corpus_only():
    result = grounded_ask("जीवन का अर्थ क्या है?", library_as_qa(), language="hi")
    assert result["refused"] is False
    assert result["answer"]
    assert "परमात्मा" in result["answer"] or "मोक्ष" in result["answer"] or "जीवन" in result["answer"]
    assert result["clips"]
    assert result["clips"][0]["source_question"]


def test_unrelated_query_is_refused():
    result = grounded_ask("How do I bake a chocolate cake with ganache?", library_as_qa(), language="en")
    assert result["refused"] is True
    assert "chocolate" not in result["answer"].lower()
    assert "ganache" not in result["answer"].lower()


def test_follow_up_uses_history():
    result = grounded_ask("और कैसे?", library_as_qa(), conversation_history=["ध्यान में मन भटकता है क्या करें?"], language="hi")
    assert result["refused"] is False
    blob = result["answer"] + " ".join(clip.get("source_question", "") for clip in result["clips"])
    assert "ध्यान" in blob or "मन" in blob


def test_curated_clips_are_labeled_when_no_video_id():
    result = grounded_ask("भक्ति का सच्चा अर्थ क्या है?", library_as_qa(), language="hi")
    assert result["clips"]
    assert result["clips"][0]["citation_kind"] in {"curated", "video"}
