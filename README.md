# Uttar Sewa

**Spiritual Q&A from video discourses — ask in Hindi or English, jump to the exact timestamp.**

Uttar Sewa ("Northern Service") is a React + FastAPI app that answers spiritual questions from processed YouTube transcripts. Each answer cites the source video and opens at the matching moment.

## What it does

- **Chat and search** — conversational Q&A with follow-ups, or a classic search page
- **Timestamp links** — real YouTube watch URLs (`watch?v=…&t=seconds`) that open in a new tab
- **Channel groups** — filter by topic (bhakti, meditation, philosophy, peace) or search all
- **Memory** — follow-up questions like "और कैसे?" use the previous turn
- **Recommendations** — suggested questions from recent search history
- **PWA extras** — favorites, voice input, offline cache, Hindi/English UI

## Architecture

```
app_server.py / run_backend.py   FastAPI entry (imports backend.server)
backend/server.py                API routes
backend/services/               search, YouTube, processing, timestamps
backend/spiritual_qa_content.py curated Q&A fallback when the DB is empty
frontend/                        React (CRA + Tailwind)
tests/                           unit tests (no Mongo required)
```

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env                 # fill in your keys
python -c "from backend.server import app; print('ok')"   # import check

cd frontend
cp .env.example .env                                 # set REACT_APP_BACKEND_URL
yarn install
yarn start
```

Start the API with uvicorn after `.env` is filled:

```bash
uvicorn backend.server:app --reload --port 8000
```

> `.env` files are git-ignored and **must not** be committed. Use `.env.example` as the template.

## Tests

```bash
pip install -r backend/requirements.txt
python -m pytest tests/ -q
```

## Why it exists

Seekers ask the same questions that already live in long discourse videos. Uttar Sewa turns those videos into searchable Q&A with a clickable timestamp, instead of making people scrub through hours of footage.

## Status

Working backend + frontend. Core search ranking, timestamp URLs, chat memory, and channel filters were updated in this release. YouTube processing still needs captions (or transcription) for a full 900+ video index; the curated library is used when the database is empty.

## License

MIT
