from backend.services.mala_counter import apply_tap, empty_state, summarize_day
from backend.services.grounded_ask import grounded_ask
from backend.services.relevance_search import library_as_qa
from backend.models import AskQuery, MalaState


def test_ask_query_model_accepts_history():
    body = AskQuery(query="ध्यान", conversation_history=["गुरु"], language="hi")
    assert body.limit == 3


def test_mala_state_roundtrip_summary():
    state = empty_state()
    for _ in range(10):
        state = apply_tap(state)
    dumped = MalaState(**state).model_dump()
    summary = summarize_day(dumped)
    assert summary["beads_today"] == 10
    assert summary["progress_label"] == "10/108"


def test_grounded_ask_empty_question_still_safe():
    result = grounded_ask("   ", library_as_qa(), language="en")
    assert result["refused"] is True
