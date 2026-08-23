from backend.services.grounded_ask import grounded_ask

CORPUS = [
    {
        "question": "मन भटकता है तो क्या करें?",
        "answer": "नाम जप करते रहो",
        "video_id": "abc",
        "video_title": "Satsang",
        "start_time": 12,
        "end_time": 20,
        "confidence_score": 0.9,
        "channel_id": "bhajanmarg",
    }
]


def test_ask_copies_corpus_and_refuses_unrelated():
    hit = grounded_ask("मन भटकता है", corpus=CORPUS, language="hi")
    assert hit["refused"] is False
    assert hit["answer"] == "नाम जप करते रहो"
    miss = grounded_ask("how do I file taxes in Delaware", corpus=CORPUS, language="en")
    assert miss["refused"] is True
    assert "नाम जप करते रहो" not in miss["answer"]
    assert miss["answer"].startswith("The collected discourses")
