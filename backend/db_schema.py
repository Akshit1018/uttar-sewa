"""Mongo collections and indexes for Uttar Sewa.

The Flutter app and control dashboard talk to these collections through /api.
"""

COLLECTIONS = {
    "videos": "videos",
    "transcripts": "transcript_segments",
    "qa": "question_answers",
    "processing": "processing_status",
    "settings": "control_settings",
    "secrets": "control_secrets",
    "pins": "pinned_qa",
    "mala": "mala_days",
    "feedback": "feedback",
}

INDEXES = {
    "videos": [
        {"keys": [("video_id", 1)], "unique": True},
        {"keys": [("transcript_processed", 1)]},
        {"keys": [("channel_id", 1)]},
    ],
    "transcript_segments": [
        {"keys": [("video_id", 1), ("start_time", 1), ("text", 1)], "unique": True},
    ],
    "question_answers": [
        {"keys": [("video_id", 1), ("start_time", 1), ("answer", 1)], "unique": True},
        {"keys": [("channel_id", 1)]},
        {"keys": [("language", 1)]},
        {"keys": [("pinned", 1)]},
        {
            "keys": [("question", "text"), ("answer", "text"), ("video_title", "text")],
            "name": "qa_text",
        },
    ],
    "pinned_qa": [
        {"keys": [("video_id", 1), ("question", 1)], "unique": True},
    ],
    "mala_days": [
        {"keys": [("device_id", 1), ("day", 1), ("mantra_id", 1)], "unique": True},
    ],
    "feedback": [
        {"keys": [("timestamp", 1)]},
    ],
    "processing_status": [
        {"keys": [("status", 1), ("started_at", 1)]},
    ],
}

SETTINGS_DOC_ID = "app"
SECRETS_DOC_ID = "byok"
