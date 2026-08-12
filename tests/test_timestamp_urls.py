from backend.services.timestamp_urls import (
    build_watch_url,
    build_youtu_be_url,
    build_embed_url,
    format_timestamp_display,
    normalize_start_seconds,
)


def test_watch_url_uses_integer_seconds_without_trailing_s():
    assert build_watch_url("abc123XYZ_-", 125.9) == "https://www.youtube.com/watch?v=abc123XYZ_-&t=125"


def test_watch_url_floors_and_clamps_negative_time():
    assert build_watch_url("vid", -3) == "https://www.youtube.com/watch?v=vid&t=0"
    assert normalize_start_seconds(None) == 0


def test_youtu_be_and_embed_urls():
    assert build_youtu_be_url("vid", 90) == "https://youtu.be/vid?t=90"
    assert build_embed_url("vid", 90) == "https://www.youtube.com/embed/vid?start=90"


def test_format_timestamp_display():
    assert format_timestamp_display(75) == "1:15"
    assert format_timestamp_display(3661) == "1:01:01"
