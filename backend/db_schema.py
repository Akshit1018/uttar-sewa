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
}

INDEXES = {
    "videos": [
        [("video_id", 1)],
        [("transcript_processed", 1)],
        [("channel_id", 1)],
    ],
    "transcript_segments": [
        [("video_id", 1), ("start_time", 1)],
    ],
    "question_answers": [
        [("video_id", 1)],
        [("channel_id", 1)],
        [("language", 1)],
        [("pinned", 1)],
    ],
    "pinned_qa": [
        [("video_id", 1), ("start_time", 1)],
    ],
    "mala_days": [
        [("device_id", 1), ("day", 1), ("mantra_id", 1)],
    ],
}

SETTINGS_DOC_ID = "app"
SECRETS_DOC_ID = "byok"
