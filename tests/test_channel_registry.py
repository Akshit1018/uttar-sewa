from backend.services.channel_registry import (
    DEFAULT_CHANNELS,
    get_channel,
    list_channels,
    topic_for_tags,
)


def test_default_channels_cover_core_topics():
    topics = {c["topic"] for c in DEFAULT_CHANNELS}
    assert {"bhakti", "meditation", "philosophy"}.issubset(topics)
    assert all(c["id"] and c["name"] for c in DEFAULT_CHANNELS)


def test_get_channel_and_list():
    assert get_channel("bhajanmarg")["topic"] == "bhakti"
    assert get_channel("bhakti")["id"] == "bhajanmarg"
    assert get_channel("missing") is None
    listed = list_channels()
    assert listed[0]["id"] == "all"
    assert len(listed) == len(DEFAULT_CHANNELS) + 1


def test_topic_for_tags():
    assert topic_for_tags(["guru", "bhakti"]) == "bhakti"
    assert topic_for_tags(["meditation", "mind"]) == "meditation"
    assert topic_for_tags(["unknown"]) == "philosophy"
