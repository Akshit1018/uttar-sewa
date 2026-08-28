"""Turn YouTube video payloads into a citable library.

Does not invent teaching. Captions or Whisper only. Never the curated fallback.
"""

from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Callable, Dict, List, Optional

from .public_enrichment import parse_youtube_oembed
from .transcript_ingest import resolve_video_transcript, segments_to_qa, to_caption_segments

CaptionsFn = Callable[[str], Optional[List[Dict[str, Any]]]]
TranscribeFn = Callable[..., List[Dict[str, Any]]]


def _parse_upload_date(value: Any) -> datetime:
    if isinstance(value, datetime):
        return value
    if isinstance(value, str) and value:
        try:
            return datetime.fromisoformat(value.replace("Z", "+00:00"))
        except ValueError:
            pass
    return datetime.now(timezone.utc)


def normalize_video_record(raw: Dict[str, Any]) -> Dict[str, Any]:
    video_id = str(raw.get("video_id") or "").strip()
    return {
        "video_id": video_id,
        "title": str(raw.get("title") or video_id),
        "description": str(raw.get("description") or ""),
        "duration": str(raw.get("duration") or "0:00:00"),
        "upload_date": _parse_upload_date(raw.get("upload_date")),
        "view_count": int(raw.get("view_count") or 0),
        "transcript_processed": bool(raw.get("transcript_processed")),
        "channel_id": raw.get("channel_id"),
        "source": raw.get("source") or "youtube",
    }


def video_record_from_oembed(data: Dict[str, Any], video_id: str) -> Dict[str, Any]:
    meta = parse_youtube_oembed(data, video_id=video_id)
    return normalize_video_record(
        {
            "video_id": video_id,
            "title": meta.get("title") or video_id,
            "description": meta.get("author") or "",
            "source": "youtube_oembed",
            "transcript_processed": False,
        }
    )


def build_library(
    videos: List[Dict[str, Any]],
    captions_for: CaptionsFn,
    transcribe: Optional[TranscribeFn] = None,
    audio_directory: Optional[str] = None,
) -> Dict[str, Any]:
    out_videos: List[Dict[str, Any]] = []
    out_segments: List[Dict[str, Any]] = []
    out_qa: List[Dict[str, Any]] = []
    skipped: List[str] = []

    for raw in videos:
        record = normalize_video_record(raw)
        video_id = record["video_id"]
        if not video_id:
            continue
        ingested = resolve_video_transcript(
            video_id,
            captions=captions_for(video_id),
            transcribe=transcribe,
            audio_directory=audio_directory,
        )
        storage = to_caption_segments(ingested["segments"])
        if not storage:
            record["transcript_processed"] = False
            out_videos.append(record)
            skipped.append(video_id)
            continue
        record["transcript_processed"] = True
        out_videos.append(record)
        for segment in storage:
            out_segments.append({"video_id": video_id, **segment})
        out_qa.extend(segments_to_qa(ingested["segments"], video_id, record["title"]))

    return {
        "source": "youtube",
        "invented": False,
        "videos": out_videos,
        "segments": out_segments,
        "qa": out_qa,
        "skipped": skipped,
    }
