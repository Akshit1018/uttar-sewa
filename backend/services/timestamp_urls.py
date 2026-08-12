"""Canonical YouTube timestamp URLs.

YouTube accepts ``t=125`` (seconds) on watch and youtu.be links.
A trailing ``s`` is ignored by some clients and breaks others, so we never emit it.
"""

from typing import Optional


def normalize_start_seconds(start_time: Optional[float]) -> int:
    try:
        seconds = int(float(start_time or 0))
    except (TypeError, ValueError):
        return 0
    return max(0, seconds)


def build_watch_url(video_id: str, start_time: Optional[float] = 0) -> str:
    video_id = (video_id or "").strip()
    if not video_id:
        return ""
    seconds = normalize_start_seconds(start_time)
    return f"https://www.youtube.com/watch?v={video_id}&t={seconds}"


def build_youtu_be_url(video_id: str, start_time: Optional[float] = 0) -> str:
    video_id = (video_id or "").strip()
    if not video_id:
        return ""
    seconds = normalize_start_seconds(start_time)
    return f"https://youtu.be/{video_id}?t={seconds}"


def build_embed_url(video_id: str, start_time: Optional[float] = 0) -> str:
    video_id = (video_id or "").strip()
    if not video_id:
        return ""
    seconds = normalize_start_seconds(start_time)
    return f"https://www.youtube.com/embed/{video_id}?start={seconds}"


def format_timestamp_display(seconds: Optional[float]) -> str:
    total = normalize_start_seconds(seconds)
    hours = total // 3600
    minutes = (total % 3600) // 60
    secs = total % 60
    if hours > 0:
        return f"{hours}:{minutes:02d}:{secs:02d}"
    return f"{minutes}:{secs:02d}"
