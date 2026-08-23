"""Query-scoped Q&A loading and YouTube paste-URL classification.

Ask/search used to dump 2000 documents into RAM. We now load a capped,
token-filtered candidate set and rank in process. Clip titles follow
YouTube's timestamp + short label pattern, not invented questions.
"""

from __future__ import annotations

import re
from typing import Any, Dict, Optional
from urllib.parse import parse_qs, urlparse

from backend.services.query_safety import escape_regex

CANDIDATE_CAP = 400
_TOKEN_SPLIT = re.compile(r"[^\w]+", re.UNICODE)
_YOUTUBE_HOSTS = {"youtube.com", "m.youtube.com", "youtu.be", "music.youtube.com"}
_VIDEO_ID = re.compile(r"^[A-Za-z0-9_-]{11}$")


def summarize_qa_counts(*, curated: int, ingested: int) -> Dict[str, Any]:
    curated_n = max(0, int(curated or 0))
    ingested_n = max(0, int(ingested or 0))
    return {
        "curated_qa": curated_n,
        "ingested_qa": ingested_n,
        "seed_only": ingested_n == 0,
        "total_qa_pairs": curated_n + ingested_n,
    }


def query_tokens(query: str) -> list[str]:
    parts = _TOKEN_SPLIT.split((query or "").strip().lower())
    return [part for part in parts if len(part) >= 2][:8]


def qa_load_plan(query: Optional[str]) -> Dict[str, Any]:
    if (query or "").strip():
        return {"mode": "query", "cap": CANDIDATE_CAP}
    return {"mode": "recent", "cap": CANDIDATE_CAP}


def qa_candidate_filter(query: Optional[str], channel_id: Optional[str] = None) -> Dict[str, Any]:
    clauses: list[Dict[str, Any]] = []
    tokens = query_tokens(query or "")
    if tokens:
        or_clause = []
        for token in tokens:
            rx = {"$regex": escape_regex(token), "$options": "i"}
            or_clause.extend(
                [
                    {"question": rx},
                    {"answer": rx},
                    {"video_title": rx},
                ]
            )
        clauses.append({"$or": or_clause})
    if channel_id and channel_id not in ("", "all"):
        clauses.append({"channel_id": channel_id})
    if not clauses:
        return {}
    if len(clauses) == 1:
        return clauses[0]
    return {"$and": clauses}


def classify_youtube_target(url: str) -> Dict[str, str]:
    raw = (url or "").strip()
    empty = {"kind": "invalid", "video_id": "", "channel": ""}
    if not raw:
        return empty
    parsed = urlparse(raw if "://" in raw else f"https://{raw}")
    host = (parsed.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    if host not in _YOUTUBE_HOSTS:
        return empty
    path = parsed.path or ""
    query = parse_qs(parsed.query or "")
    if host == "youtu.be":
        video_id = path.strip("/").split("/")[0]
        if _VIDEO_ID.fullmatch(video_id or ""):
            return {"kind": "video", "video_id": video_id, "channel": ""}
        return empty
    video_id = (query.get("v") or [""])[0]
    if _VIDEO_ID.fullmatch(video_id or ""):
        return {"kind": "video", "video_id": video_id, "channel": ""}
    for prefix in ("/shorts/", "/embed/", "/live/"):
        if prefix in path:
            candidate = path.split(prefix, 1)[-1].split("/")[0]
            if _VIDEO_ID.fullmatch(candidate or ""):
                return {"kind": "video", "video_id": candidate, "channel": ""}
    handle = re.search(r"/@([^/?]+)", path)
    if handle:
        return {"kind": "channel", "video_id": "", "channel": handle.group(1)}
    for prefix in ("/c/", "/user/", "/channel/"):
        if prefix in path:
            name = path.split(prefix, 1)[-1].split("/")[0]
            if name:
                return {"kind": "channel", "video_id": "", "channel": name}
    return empty
