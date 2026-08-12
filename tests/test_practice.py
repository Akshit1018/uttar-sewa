from datetime import datetime

from backend.services.mala_counter import (
    ALLOWED_CYCLE_LENGTHS,
    apply_tap,
    apply_undo,
    empty_state,
    named_malas,
    resolve_beads_per_cycle,
    summarize_day,
)
from backend.services.practice import format_share_card, next_sandhya


def test_allowed_cycle_lengths_are_traditional():
    assert ALLOWED_CYCLE_LENGTHS == (11, 27, 54, 108)
    assert resolve_beads_per_cycle({"beads_per_cycle": 27}) == 27
    assert resolve_beads_per_cycle({"beads_per_cycle": 99}) == 108


def test_named_malas_are_distinct_practices():
    ids = [item["id"] for item in named_malas()]
    assert ids == ["ram", "hare_krishna", "om"]


def test_27_bead_cycle_completes_on_27th_tap():
    state = empty_state()
    state["beads_per_cycle"] = 27
    for _ in range(26):
        state = apply_tap(state)
    assert state["cycles_today"] == 0
    state = apply_tap(state)
    assert state["cycles_today"] == 1
    assert state["current_in_cycle"] == 0
    assert state["completed_cycle"] is True
    summary = summarize_day(state)
    assert summary["beads_per_cycle"] == 27
    assert summary["progress_label"] == "0/27"


def test_undo_after_short_cycle_restores_last_bead():
    state = empty_state()
    state["beads_per_cycle"] = 11
    for _ in range(11):
        state = apply_tap(state)
    state = apply_undo(state)
    assert state["cycles_today"] == 0
    assert state["current_in_cycle"] == 10
    assert state["beads_today"] == 10


def test_share_card_is_question_answer_and_link():
    text = format_share_card(
        question="मन भटकता है तो क्या करें?",
        answer="प्रवचन कहते हैं कि नाम जप से मन स्थिर होता है।",
        timestamp_url="https://www.youtube.com/watch?v=abc&t=90",
    )
    assert "मन भटकता है तो क्या करें?" in text
    assert "नाम जप" in text
    assert "watch?v=abc&t=90" in text
    assert "ChatGPT" not in text


def test_next_sandhya_is_morning_or_evening_local():
    morning = next_sandhya(datetime(2026, 8, 12, 5, 0, 0))
    assert morning["kind"] == "morning"
    assert morning["at"].hour == 6

    afternoon = next_sandhya(datetime(2026, 8, 12, 10, 0, 0))
    assert afternoon["kind"] == "evening"
    assert afternoon["at"].hour == 18

    night = next_sandhya(datetime(2026, 8, 12, 19, 0, 0))
    assert night["kind"] == "morning"
    assert night["at"].day == 13
