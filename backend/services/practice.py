"""Sadhana helpers that stay independent of Mongo: share cards and sandhya times."""

from datetime import datetime, timedelta
from typing import Dict


def format_share_card(question: str, answer: str, timestamp_url: str = "") -> str:
    parts = [str(question or "").strip(), str(answer or "").strip()[:220]]
    link = str(timestamp_url or "").strip()
    if link:
        parts.append(link)
    return "\n\n".join(part for part in parts if part)


def next_sandhya(now: datetime) -> Dict:
    """Local sandhya as 6:00 and 18:00 until a native location API exists."""
    morning = now.replace(hour=6, minute=0, second=0, microsecond=0)
    evening = now.replace(hour=18, minute=0, second=0, microsecond=0)
    if now < morning:
        return {"kind": "morning", "at": morning}
    if now < evening:
        return {"kind": "evening", "at": evening}
    return {"kind": "morning", "at": morning + timedelta(days=1)}
