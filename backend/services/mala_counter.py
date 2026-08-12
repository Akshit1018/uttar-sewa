"""108-bead mala counter. Pure functions so the orb and dashboard stay in sync."""

from typing import Dict

BEADS_PER_CYCLE = 108
HOLD_MS = 2500


def empty_state() -> Dict:
    return {
        "beads_today": 0,
        "cycles_today": 0,
        "current_in_cycle": 0,
        "completed_cycle": False,
        "questions_today": 0,
        "streak_days": 0,
    }


def apply_tap(state: Dict) -> Dict:
    next_state = dict(state or empty_state())
    next_state["beads_today"] = int(next_state.get("beads_today") or 0) + 1
    next_state["current_in_cycle"] = int(next_state.get("current_in_cycle") or 0) + 1
    next_state["completed_cycle"] = False
    if next_state["current_in_cycle"] >= BEADS_PER_CYCLE:
        next_state["cycles_today"] = int(next_state.get("cycles_today") or 0) + 1
        next_state["current_in_cycle"] = 0
        next_state["completed_cycle"] = True
    return next_state


def apply_undo(state: Dict) -> Dict:
    next_state = dict(state or empty_state())
    beads = int(next_state.get("beads_today") or 0)
    current = int(next_state.get("current_in_cycle") or 0)
    cycles = int(next_state.get("cycles_today") or 0)
    if beads <= 0:
        return next_state
    if current == 0 and cycles > 0:
        next_state["cycles_today"] = cycles - 1
        next_state["current_in_cycle"] = BEADS_PER_CYCLE - 1
    else:
        next_state["current_in_cycle"] = max(0, current - 1)
    next_state["beads_today"] = beads - 1
    next_state["completed_cycle"] = False
    return next_state


def summarize_day(state: Dict) -> Dict:
    current = int((state or {}).get("current_in_cycle") or 0)
    cycles = int((state or {}).get("cycles_today") or 0)
    beads = int((state or {}).get("beads_today") or 0)
    return {
        "beads_today": beads,
        "malas_today": cycles,
        "current_in_cycle": current,
        "beads_per_cycle": BEADS_PER_CYCLE,
        "progress_label": f"{current}/{BEADS_PER_CYCLE}",
        "questions_today": int((state or {}).get("questions_today") or 0),
        "hold_ms": HOLD_MS,
    }
