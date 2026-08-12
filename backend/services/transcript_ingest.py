"""Caption-first transcript ingest. Whisper only when captions are missing.

Never invents speech. Empty captions + no audio → empty segments.
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any, Callable, Dict, List, Optional

try:
    import whisper as whisper_lib
except ImportError:
    whisper_lib = None


TranscribeFn = Callable[..., List[Dict[str, Any]]]
AUDIO_EXTENSIONS = (".wav", ".mp3", ".m4a")


def normalize_segments(raw: Optional[List[Dict[str, Any]]]) -> List[Dict[str, Any]]:
    segments = []
    for item in raw or []:
        text = str(item.get("text") or "").strip()
        if not text:
            continue
        start = float(item.get("start") or item.get("start_time") or 0)
        end = float(item.get("end") or item.get("end_time") or start)
        if end < start:
            end = start
        segments.append({"start": start, "end": end, "text": text})
    return segments


def ingest_transcript(
    captions: Optional[List[Dict[str, Any]]] = None,
    transcribe: Optional[TranscribeFn] = None,
    audio_path: Optional[str] = None,
    language: str = "hi",
) -> Dict[str, Any]:
    caption_segments = normalize_segments(captions)
    if caption_segments:
        return {"source": "captions", "segments": caption_segments, "invented": False}
    if audio_path and transcribe is not None:
        whispered = normalize_segments(transcribe(audio_path, language=language))
        if whispered:
            return {"source": "whisper", "segments": whispered, "invented": False}
    return {"source": "none", "segments": [], "invented": False}


def segments_to_qa(
    segments: List[Dict[str, Any]],
    video_id: str,
    video_title: str,
) -> List[Dict[str, Any]]:
    rows = []
    for item in normalize_segments(segments):
        rows.append(
            {
                "video_id": video_id,
                "video_title": video_title,
                "question": item["text"][:80],
                "answer": item["text"],
                "start_time": item["start"],
                "end_time": item["end"],
                "source": "transcript",
                "language": "hi",
                "confidence_score": 0.7,
                "tags": ["transcript"],
            }
        )
    return rows


def audio_path_for(video_id: str, directory: Optional[str] = None) -> Optional[str]:
    """Return a local audio file for Whisper when captions are missing."""
    root = Path(directory or os.getenv("WHISPER_AUDIO_DIR") or "")
    if not video_id or not root.is_dir():
        return None
    for ext in AUDIO_EXTENSIONS:
        candidate = root / f"{video_id}{ext}"
        if candidate.is_file():
            return str(candidate)
    return None


def resolve_video_transcript(
    video_id: str,
    captions: Optional[List[Dict[str, Any]]] = None,
    transcribe: Optional[TranscribeFn] = None,
    audio_directory: Optional[str] = None,
    language: str = "hi",
) -> Dict[str, Any]:
    """Captions first; Whisper only if a local audio file exists."""
    return ingest_transcript(
        captions=captions,
        transcribe=transcribe,
        audio_path=audio_path_for(video_id, directory=audio_directory),
        language=language,
    )


def to_caption_segments(
    segments: Optional[List[Dict[str, Any]]],
    language: str = "hi",
) -> List[Dict[str, Any]]:
    """Map ingest segments to TranscriptSegment / LLM chunk fields."""
    rows = []
    for item in normalize_segments(segments):
        rows.append(
            {
                "start_time": item["start"],
                "end_time": item["end"],
                "text": item["text"],
                "language": language,
            }
        )
    return rows


def transcribe_with_whisper(audio_path: str, language: str = "hi") -> List[Dict[str, Any]]:
    """Optional OpenAI Whisper. Tests inject a fake transcribe function instead."""
    if whisper_lib is None:
        raise RuntimeError("openai-whisper is not installed")
    model = whisper_lib.load_model("base")
    result = model.transcribe(audio_path, language=language if language in ("hi", "en") else None)
    segments = []
    for item in result.get("segments") or []:
        segments.append(
            {
                "start": float(item.get("start") or 0),
                "end": float(item.get("end") or 0),
                "text": str(item.get("text") or "").strip(),
            }
        )
    return normalize_segments(segments)
