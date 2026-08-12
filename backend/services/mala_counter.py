"""Mala counter. Cycle length defaults to 108; 11 / 27 / 54 are allowed."""

from typing import Dict, List

BEADS_PER_CYCLE = 108
HOLD_MS = 2500
ALLOWED_CYCLE_LENGTHS = (11, 27, 54, 108)

NAMED_MALAS = (
    {"id": "ram", "name_hi": "राम राम", "name_en": "Ram Ram"},
    {"id": "hare_krishna", "name_hi": "हरे कृष्ण", "name_en": "Hare Krishna"},
    {"id": "om", "name_hi": "ॐ", "name_en": "Om"},
)


def named_malas() -> List[Dict]:
    return [dict(item) for item in NAMED_MALAS]


def resolve_beads_per_cycle(state: Dict = None) -> int:
    value = int((state or {}).get("beads_per_cycle") or BEADS_PER_CYCLE)
    if value not in ALLOWED_CYCLE_LENGTHS:
        return BEADS_PER_CYCLE
    return value


def empty_state() -> Dict:
    return {
        "beads_today": 0,
        "cycles_today": 0,
        "current_in_cycle": 0,
        "completed_cycle": False,
        "questions_today": 0,
        "beads_per_cycle": BEADS_PER_CYCLE,
        "mantra_id": "ram",
    }


def apply_tap(state: Dict) -> Dict:
    next_state = dict(state or empty_state())
    cycle = resolve_beads_per_cycle(next_state)
    next_state["beads_per_cycle"] = cycle
    next_state["beads_today"] = int(next_state.get("beads_today") or 0) + 1
    next_state["current_in_cycle"] = int(next_state.get("current_in_cycle") or 0) + 1
    next_state["completed_cycle"] = False
    if next_state["current_in_cycle"] >= cycle:
        next_state["cycles_today"] = int(next_state.get("cycles_today") or 0) + 1
        next_state["current_in_cycle"] = 0
        next_state["completed_cycle"] = True
    return next_state


def apply_undo(state: Dict) -> Dict:
    next_state = dict(state or empty_state())
    cycle = resolve_beads_per_cycle(next_state)
    next_state["beads_per_cycle"] = cycle
    beads = int(next_state.get("beads_today") or 0)
    current = int(next_state.get("current_in_cycle") or 0)
    cycles = int(next_state.get("cycles_today") or 0)
    if beads <= 0:
        return next_state
    if current == 0 and cycles > 0:
        next_state["cycles_today"] = cycles - 1
        next_state["current_in_cycle"] = cycle - 1
    else:
        next_state["current_in_cycle"] = max(0, current - 1)
    next_state["beads_today"] = beads - 1
    next_state["completed_cycle"] = False
    return next_state


def summarize_day(state: Dict) -> Dict:
    current = int((state or {}).get("current_in_cycle") or 0)
    cycles = int((state or {}).get("cycles_today") or 0)
    beads = int((state or {}).get("beads_today") or 0)
    cycle = resolve_beads_per_cycle(state)
    return {
        "beads_today": beads,
        "malas_today": cycles,
        "current_in_cycle": current,
        "beads_per_cycle": cycle,
        "progress_label": f"{current}/{cycle}",
        "questions_today": int((state or {}).get("questions_today") or 0),
        "hold_ms": HOLD_MS,
        "mantra_id": (state or {}).get("mantra_id") or "ram",
    }


def sankalpa_remaining(malas_today: int, vow_malas: int) -> int:
    return max(0, int(vow_malas or 0) - int(malas_today or 0))
