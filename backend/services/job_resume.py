"""Resume in-process ingest jobs after a worker restart."""

from __future__ import annotations

from typing import Any, Dict, Iterable, List


def jobs_to_resume(rows: Iterable[Dict[str, Any]] | None) -> List[Dict[str, Any]]:
    out: List[Dict[str, Any]] = []
    for row in rows or []:
        if row.get("status") in ("pending", "processing") and row.get("id"):
            out.append({"id": row.get("id"), "channel_url": row.get("channel_url")})
    return out
