import re
from typing import Optional


def escape_regex(query: str) -> str:
    return re.escape((query or "")[:80])


def clamp_limit(value: Optional[int], low: int = 1, high: int = 50) -> int:
    try:
        number = int(value)
    except (TypeError, ValueError):
        return low
    return max(low, min(high, number))
