from backend.services.relevance_search import rank_answers, related_questions
from backend.spiritual_qa_content import SPIRITUAL_QA_LIBRARY


def _corpus():
    items = []
    for i, qa in enumerate(SPIRITUAL_QA_LIBRARY):
        items.append({
            **qa,
            "video_id": f"vid{i}",
            "start_time": float(i * 30),
            "end_time": float(i * 30 + 45),
            "video_title": f"Discourse {i}",
            "channel_id": "bhakti" if "bhakti" in qa.get("tags", []) or "guru" in qa.get("tags", []) else "meditation",
        })
    return items


def test_exact_hindi_question_ranks_first():
    results = rank_answers("जीवन का अर्थ क्या है?", _corpus(), limit=3)
    assert results
    assert "जीवन" in results[0]["question"]
    assert results[0]["confidence_score"] >= 0.7


def test_english_meditation_query_prefers_meditation_answers():
    results = rank_answers("How to meditate when the mind wanders?", _corpus(), limit=5)
    assert results
    joined = " ".join(r["question"].lower() + r["answer"].lower() for r in results[:2])
    assert "meditat" in joined or "ध्यान" in joined or "mind" in joined


def test_synonym_match_guru_and_teacher():
    results = rank_answers("How to find a spiritual teacher?", _corpus(), limit=5)
    assert results
    tags = " ".join(" ".join(r.get("tags", [])) for r in results[:3])
    text = " ".join(r["question"].lower() for r in results[:3])
    assert "guru" in tags or "guru" in text or "teacher" in text


def test_empty_query_returns_no_results():
    assert rank_answers("   ", _corpus()) == []


def test_channel_filter_limits_results():
    results = rank_answers("meditation", _corpus(), limit=10, channel_id="meditation")
    assert results
    assert all(r.get("channel_id") == "meditation" for r in results)


def test_related_questions_come_from_same_topic():
    corpus = _corpus()
    top = rank_answers("भक्ति का सच्चा अर्थ क्या है?", corpus, limit=1)[0]
    related = related_questions(top, corpus, limit=3)
    assert related
    assert top["question"] not in related
