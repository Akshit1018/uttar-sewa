import asyncio

from backend.services.processing_service import ProcessingService


class FakeCollection:
    def __init__(self):
        self.docs = []
        self.updates = []

    async def insert_one(self, doc):
        self.docs.append(dict(doc))

    async def update_one(self, filt, update):
        self.updates.append((dict(filt), dict(update)))
        for doc in self.docs:
            if all(doc.get(key) == value for key, value in filt.items()):
                doc.update(update.get("$set") or {})
                return
        self.docs.append({**filt, **(update.get("$set") or {})})

    async def find_one(self, filt):
        for doc in self.docs:
            if all(doc.get(key) == value for key, value in filt.items()):
                return dict(doc)
        return None

    async def delete_many(self, filt):
        remaining = []
        for doc in self.docs:
            if all(doc.get(key) == value for key, value in filt.items()):
                continue
            remaining.append(doc)
        self.docs = remaining


class FakeDB:
    def __init__(self):
        self.videos = FakeCollection()
        self.transcript_segments = FakeCollection()
        self.question_answers = FakeCollection()
        self.processing_status = FakeCollection()


class FakeYouTube:
    def __init__(self, captions=None):
        self.captions = captions
        self.calls = []

    async def get_video_captions(self, video_id):
        self.calls.append(video_id)
        return self.captions


class FakeLLM:
    def __init__(self, pairs=None):
        self.pairs = pairs or []
        self.calls = []

    async def extract_qa_from_transcript(self, segments, title):
        self.calls.append((segments, title))
        return list(self.pairs)


VIDEO = {
    "video_id": "abc123",
    "title": "Satsang",
    "description": "",
    "duration": "0:10:00",
    "upload_date": "2024-01-01T00:00:00",
    "view_count": 1,
    "transcript_processed": False,
}


def test_no_captions_and_no_audio_leaves_video_unprocessed(tmp_path):
    db = FakeDB()
    service = ProcessingService(
        db,
        youtube_service=FakeYouTube(captions=None),
        llm_service=FakeLLM(),
        transcribe=lambda *_args, **_kwargs: [{"start": 0, "end": 1, "text": "should not run"}],
        audio_directory=str(tmp_path),
    )
    asyncio.run(service._process_single_video_smart(VIDEO, "status"))
    assert db.transcript_segments.docs == []
    assert db.question_answers.docs == []
    processed_flags = [upd[1]["$set"].get("transcript_processed") for upd in db.videos.updates]
    assert True not in processed_flags


def test_whisper_fills_captionless_video_and_marks_processed(tmp_path):
    (tmp_path / "abc123.wav").write_bytes(b"RIFF")
    db = FakeDB()
    called = {"n": 0}

    def transcribe(path, language="hi"):
        called["n"] += 1
        assert path.endswith("abc123.wav")
        return [{"start": 10, "end": 20, "text": "राम नाम जपो"}]

    service = ProcessingService(
        db,
        youtube_service=FakeYouTube(captions=None),
        llm_service=FakeLLM(pairs=[]),
        transcribe=transcribe,
        audio_directory=str(tmp_path),
    )
    asyncio.run(service._process_single_video_smart(VIDEO, "status"))
    assert called["n"] == 1
    assert db.transcript_segments.docs[0]["text"] == "राम नाम जपो"
    assert db.transcript_segments.docs[0]["start_time"] == 10
    assert db.question_answers.docs[0]["answer"] == "राम नाम जपो"
    assert db.question_answers.docs[0]["source"] == "transcript"
    assert any(upd[1]["$set"].get("transcript_processed") is True for upd in db.videos.updates)


def test_captions_win_so_whisper_is_not_called(tmp_path):
    (tmp_path / "abc123.wav").write_bytes(b"RIFF")
    db = FakeDB()
    called = {"n": 0}

    def transcribe(_path, language="hi"):
        called["n"] += 1
        return [{"start": 0, "end": 1, "text": "whisper"}]

    service = ProcessingService(
        db,
        youtube_service=FakeYouTube(
            captions=[{"start_time": 3, "end_time": 8, "text": "कैप्शन पाठ", "language": "hi"}]
        ),
        llm_service=FakeLLM(
            pairs=[
                {
                    "question": "क्या कहा?",
                    "answer": "कैप्शन पाठ",
                    "start_time": 3,
                    "end_time": 8,
                    "confidence_score": 0.9,
                    "language": "hi",
                    "tags": [],
                }
            ]
        ),
        transcribe=transcribe,
        audio_directory=str(tmp_path),
    )
    asyncio.run(service._process_single_video_smart(VIDEO, "status"))
    assert called["n"] == 0
    assert db.transcript_segments.docs[0]["text"] == "कैप्शन पाठ"
    assert db.question_answers.docs[0]["answer"] == "कैप्शन पाठ"
    assert db.question_answers.docs[0]["source"] == "transcript"
    assert "Gemini invented this teaching" not in db.question_answers.docs[0]["answer"]
    assert any(upd[1]["$set"].get("transcript_processed") is True for upd in db.videos.updates)


def test_gemini_paraphrase_is_not_stored_as_grounded_corpus():
    db = FakeDB()
    service = ProcessingService(
        db,
        youtube_service=FakeYouTube(
            captions=[{"start_time": 1, "end_time": 4, "text": "राम नाम सत्य है", "language": "hi"}]
        ),
        llm_service=FakeLLM(
            pairs=[
                {
                    "question": "What should a seeker do?",
                    "answer": "Gemini invented this teaching",
                    "start_time": 1,
                    "end_time": 4,
                    "confidence_score": 0.99,
                    "language": "en",
                    "tags": ["llm"],
                }
            ]
        ),
    )
    asyncio.run(service._process_single_video_smart(VIDEO, "status"))
    answers = [doc["answer"] for doc in db.question_answers.docs]
    assert answers == ["राम नाम सत्य है"]
    assert all(doc.get("source") == "transcript" for doc in db.question_answers.docs)
