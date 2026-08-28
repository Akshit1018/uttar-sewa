"""Known spiritual channels and topic groupings for cross-channel search."""

from typing import Dict, List, Optional

DEFAULT_CHANNELS: List[Dict[str, str]] = [
    {
        "id": "bhajanmarg",
        "name": "Bhajan Marg",
        "name_hi": "भजन मार्ग",
        "topic": "bhakti",
        "handle": "bhajanmarg",
        "description": "Primary bhakti discourses and kirtan",
    },
    {
        "id": "meditation",
        "name": "Meditation",
        "name_hi": "ध्यान",
        "topic": "meditation",
        "handle": "meditation",
        "description": "Meditation, sadhana, and mind training",
    },
    {
        "id": "philosophy",
        "name": "Philosophy",
        "name_hi": "दर्शन",
        "topic": "philosophy",
        "handle": "philosophy",
        "description": "Vedanta, karma, moksha, and life purpose",
    },
    {
        "id": "peace",
        "name": "Peace & Healing",
        "name_hi": "शांति",
        "topic": "peace",
        "handle": "peace",
        "description": "Mental peace, anger, stress, and daily life",
    },
]

_TOPIC_TAGS = {
    "bhakti": {"bhakti", "guru", "devotion", "love", "seva", "service", "satsang", "worship", "diksha"},
    "meditation": {"meditation", "mind", "sadhana", "mantra", "japa", "concentration", "practice", "dhyan"},
    "philosophy": {"karma", "moksha", "liberation", "purpose", "life", "death", "meaning", "truth"},
    "peace": {"peace", "anger", "stress", "anxiety", "happiness", "contentment", "family", "calmness"},
}


def list_channels() -> List[Dict[str, str]]:
    all_entry = {
        "id": "all",
        "name": "All channels",
        "name_hi": "सभी चैनल",
        "topic": "all",
        "handle": "",
        "description": "Search across every processed channel",
    }
    return [all_entry, *[dict(channel) for channel in DEFAULT_CHANNELS]]


def get_channel(channel_id: Optional[str]) -> Optional[Dict[str, str]]:
    if not channel_id:
        return None
    for channel in DEFAULT_CHANNELS:
        if channel["id"] == channel_id or channel["topic"] == channel_id:
            return dict(channel)
    return None


def topic_for_tags(tags: Optional[List[str]]) -> str:
    lowered = {str(tag).lower() for tag in (tags or [])}
    best_topic = "philosophy"
    best_hits = 0
    for topic, topic_tags in _TOPIC_TAGS.items():
        hits = len(lowered & topic_tags)
        if hits > best_hits:
            best_topic = topic
            best_hits = hits
    return best_topic
