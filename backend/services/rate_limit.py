"""In-process sliding window. Enough for a single-operator API."""

from __future__ import annotations

import time
from collections import defaultdict, deque


class RateLimiter:
    def __init__(self) -> None:
        self._hits: dict[str, deque[float]] = defaultdict(deque)

    def allow(self, key: str, limit: int = 60, window_s: int = 60) -> bool:
        now = time.monotonic()
        bucket = self._hits[key]
        cutoff = now - max(1, int(window_s))
        while bucket and bucket[0] < cutoff:
            bucket.popleft()
        if len(bucket) >= max(1, int(limit)):
            return False
        bucket.append(now)
        return True


LIMITER = RateLimiter()
