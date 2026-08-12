from backend.services.mala_counter import (
    BEADS_PER_CYCLE,
    HOLD_MS,
    apply_tap,
    apply_undo,
    summarize_day,
    empty_state,
)


def test_mala_cycle_is_108():
    assert BEADS_PER_CYCLE == 108
    assert HOLD_MS == 2500


def test_one_tap_increments_bead_not_cycle():
    state = apply_tap(empty_state())
    assert state["beads_today"] == 1
    assert state["current_in_cycle"] == 1
    assert state["cycles_today"] == 0
    assert state["completed_cycle"] is False


def test_108th_tap_completes_a_cycle():
    state = empty_state()
    for _ in range(107):
        state = apply_tap(state)
    assert state["cycles_today"] == 0
    state = apply_tap(state)
    assert state["beads_today"] == 108
    assert state["cycles_today"] == 1
    assert state["current_in_cycle"] == 0
    assert state["completed_cycle"] is True


def test_undo_reverses_last_bead():
    state = apply_tap(apply_tap(empty_state()))
    state = apply_undo(state)
    assert state["beads_today"] == 1
    assert state["current_in_cycle"] == 1


def test_undo_after_cycle_restores_107():
    state = empty_state()
    for _ in range(108):
        state = apply_tap(state)
    state = apply_undo(state)
    assert state["cycles_today"] == 0
    assert state["current_in_cycle"] == 107
    assert state["beads_today"] == 107


def test_summarize_day_includes_progress():
    state = empty_state()
    for _ in range(47):
        state = apply_tap(state)
    summary = summarize_day(state)
    assert summary["progress_label"] == "47/108"
    assert summary["malas_today"] == 0
    assert summary["beads_today"] == 47
