"""In-memory-safe control-plane helpers. Mongo is optional at test time."""

from datetime import datetime, timezone
from typing import Any, Dict, List, Optional
from uuid import uuid4

from backend.services.mala_counter import ALLOWED_CYCLE_LENGTHS, BEADS_PER_CYCLE, named_malas


def default_settings() -> Dict[str, Any]:
    return {
        "_id": "app",
        "language": "hi",
        "beads_per_cycle": BEADS_PER_CYCLE,
        "mantra_id": "ram",
        "sandhya": True,
        "japa_focus": False,
        "notifications": True,
        "processing_enabled": True,
        "public_companions": True,
        "default_channel_id": "all",
        "updated_at": datetime.now(timezone.utc).isoformat(),
    }


def merge_settings(current: Optional[Dict[str, Any]], patch: Optional[Dict[str, Any]]) -> Dict[str, Any]:
    merged = {**default_settings(), **(current or {}), **(patch or {})}
    cycle = int(merged.get("beads_per_cycle") or BEADS_PER_CYCLE)
    if cycle not in ALLOWED_CYCLE_LENGTHS:
        cycle = BEADS_PER_CYCLE
    merged["beads_per_cycle"] = cycle
    language = merged.get("language") or "hi"
    merged["language"] = "hi" if language not in ("hi", "en") else language
    merged["updated_at"] = datetime.now(timezone.utc).isoformat()
    merged["_id"] = "app"
    return merged


def pin_document(body: Dict[str, Any]) -> Dict[str, Any]:
    return {
        "id": str(uuid4()),
        "question": (body.get("question") or "").strip(),
        "answer": (body.get("answer") or "").strip(),
        "video_id": body.get("video_id") or "",
        "video_title": body.get("video_title") or "",
        "start_time": float(body.get("start_time") or 0),
        "timestamp_url": body.get("timestamp_url") or "",
        "channel_id": body.get("channel_id"),
        "pinned": True,
        "pinned_at": datetime.now(timezone.utc).isoformat(),
    }


def dashboard_payload(
    stats: Dict[str, Any],
    settings: Dict[str, Any],
    pinned_count: int,
    api_ok: bool,
) -> Dict[str, Any]:
    videos = int(stats.get("total_videos") or 0)
    qa = int(stats.get("total_qa_pairs") or 0)
    return {
        "ready": bool(api_ok),
        "database": "uttar_sewa",
        "stats": {
            "total_videos": videos,
            "processed_videos": int(stats.get("processed_videos") or 0),
            "unprocessed_videos": int(stats.get("unprocessed_videos") or 0),
            "total_qa_pairs": qa,
            "pinned_qa": int(pinned_count or 0),
        },
        "controls": {
            "language": settings.get("language"),
            "beads_per_cycle": settings.get("beads_per_cycle"),
            "mantra_id": settings.get("mantra_id"),
            "sandhya": bool(settings.get("sandhya")),
            "japa_focus": bool(settings.get("japa_focus")),
            "processing_enabled": bool(settings.get("processing_enabled")),
            "public_companions": bool(settings.get("public_companions", True)),
            "default_channel_id": settings.get("default_channel_id"),
            "named_malas": named_malas(),
            "allowed_cycle_lengths": list(ALLOWED_CYCLE_LENGTHS),
        },
        "library": {
            "has_citations": qa > 0 or videos > 0,
            "needs_captions": int(stats.get("unprocessed_videos") or 0),
        },
        "enrichment": {
            "listed_in": "https://github.com/public-apis/public-apis",
            "scraper": "https://github.com/D4Vinci/Scrapling",
            "rag_pattern": "https://github.com/Shubhamsaboo/awesome-llm-apps",
        },
    }


def mala_day_key(device_id: str, day: str, mantra_id: str) -> Dict[str, str]:
    return {
        "device_id": device_id or "anonymous",
        "day": day,
        "mantra_id": mantra_id or "ram",
    }
