import os

from backend.services.transcript_ingest import (
    audio_path_for,
    ingest_transcript,
    normalize_segments,
    resolve_video_transcript,
    segments_to_qa,
    to_caption_segments,
    transcribe_with_whisper,
    whisper_lib,
)


def test_captions_win_and_whisper_is_not_called():
    called = {"n": 0}

    def transcribe(_path, language="hi"):
        called["n"] += 1
        return [{"start": 0, "end": 1, "text": "should not run"}]

    result = ingest_transcript(
        captions=[{"start": 12, "end": 18, "text": "ध्यान करो"}],
        transcribe=transcribe,
        audio_path="/tmp/fake.wav",
    )
    assert result["source"] == "captions"
    assert result["invented"] is False
    assert result["segments"][0]["text"] == "ध्यान करो"
    assert called["n"] == 0


def test_missing_captions_uses_whisper_segments():
    def transcribe(_path, language="hi"):
        return [{"start": 0.0, "end": 4.5, "text": "राम राम जपें"}]

    result = ingest_transcript(captions=None, transcribe=transcribe, audio_path="talk.wav")
    assert result["source"] == "whisper"
    assert result["invented"] is False
    assert result["segments"][0]["end"] == 4.5
    assert "जपें" in result["segments"][0]["text"]


def test_no_captions_and_no_audio_returns_empty_not_invented():
    result = ingest_transcript(captions=[], transcribe=None, audio_path=None)
    assert result["source"] == "none"
    assert result["segments"] == []
    assert result["invented"] is False


def test_empty_whisper_text_is_dropped():
    segs = normalize_segments([{"start": 0, "end": 1, "text": "  "}, {"start": 1, "end": 2, "text": "गुरु"}])
    assert len(segs) == 1
    assert segs[0]["text"] == "गुरु"


def test_segments_become_citable_qa_with_timestamps():
    qa = segments_to_qa(
        [{"start": 90, "end": 120, "text": "कर्म करो, फल मत सोचो"}],
        video_id="abc",
        video_title="Satsang",
    )
    assert qa[0]["video_id"] == "abc"
    assert qa[0]["start_time"] == 90
    assert qa[0]["answer"] == "कर्म करो, फल मत सोचो"
    assert qa[0]["source"] == "transcript"
    assert qa[0]["confidence_score"] == 0.7


def test_audio_path_for_finds_wav_in_directory(tmp_path):
    wav = tmp_path / "abc123.wav"
    wav.write_bytes(b"RIFF")
    assert audio_path_for("abc123", directory=str(tmp_path)).endswith("abc123.wav")
    assert audio_path_for("missing", directory=str(tmp_path)) is None


def test_audio_path_for_reads_whisper_audio_dir_env(tmp_path, monkeypatch):
    mp3 = tmp_path / "vid9.mp3"
    mp3.write_bytes(b"ID3")
    monkeypatch.setenv("WHISPER_AUDIO_DIR", str(tmp_path))
    assert audio_path_for("vid9").endswith("vid9.mp3")
    monkeypatch.delenv("WHISPER_AUDIO_DIR")
    assert audio_path_for("vid9") is None


def test_resolve_video_transcript_uses_whisper_only_when_audio_exists(tmp_path):
    called = {"n": 0}

    def transcribe(path, language="hi"):
        called["n"] += 1
        assert path.endswith("v1.wav")
        return [{"start": 1, "end": 2, "text": "सतसंग"}]

    (tmp_path / "v1.wav").write_bytes(b"RIFF")
    whispered = resolve_video_transcript(
        "v1",
        captions=None,
        transcribe=transcribe,
        audio_directory=str(tmp_path),
    )
    assert whispered["source"] == "whisper"
    assert called["n"] == 1

    captions = resolve_video_transcript(
        "v1",
        captions=[{"start_time": 0, "end_time": 3, "text": "कैप्शन"}],
        transcribe=transcribe,
        audio_directory=str(tmp_path),
    )
    assert captions["source"] == "captions"
    assert called["n"] == 1

    empty = resolve_video_transcript("missing", captions=[], transcribe=transcribe, audio_directory=str(tmp_path))
    assert empty["source"] == "none"
    assert empty["invented"] is False
    assert called["n"] == 1


def test_to_caption_segments_uses_start_time_fields():
    rows = to_caption_segments([{"start": 5, "end": 9, "text": "जप"}])
    assert rows == [{"start_time": 5.0, "end_time": 9.0, "text": "जप", "language": "hi"}]


def test_transcribe_with_whisper_fails_clearly_without_optional_package():
    if whisper_lib is not None:
        return
    try:
        transcribe_with_whisper("missing.wav")
    except RuntimeError as error:
        assert "whisper" in str(error).lower()
        return
    raise AssertionError("expected RuntimeError when openai-whisper is missing")
