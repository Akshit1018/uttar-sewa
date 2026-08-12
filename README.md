# Uttar Sewa

**Spiritual Q&A from video discourses — ask in Hindi or English, jump to the exact timestamp.**

Uttar Sewa ("Northern Service") is a Flutter + FastAPI app. Answers come only from processed YouTube transcripts. Each answer cites the source video and opens at the matching moment.

The **control dashboard** in the Flutter app talks to `/api/control/*` and the MongoDB database `uttar_sewa`.

## What it does

- **Chat and search** — conversational Q&A with follow-ups, or a classic search page
- **Grounded ask** — answers only from the video corpus, with timestamp citations
- **Japa mala orb** — tap a bead; 11 / 27 / 54 / 108 completes a mala; hold 2.5s to ask
- **Sadhana** — named malas (Ram Ram, Hare Krishna, Om), daily counts synced to the API
- **Control dashboard** — library stats, mala settings, pin clips, start/clear processing, public scrape
- **Public companions** — Gita verse, Wikipedia, dictionary, Open Library, sandhya times (labeled, never mixed into the video answer)
- **Timestamp links** — real YouTube watch URLs (`watch?v=…&t=seconds`)
- **Channel groups** — filter by topic (bhakti, meditation, philosophy, peace)
- **Web PWA** — the React client in `frontend/` still works for browsers

## Architecture

```
mobile/                          Flutter client (chat, search, sadhana, control)
frontend/                        React PWA (optional web client)
app_server.py / run_backend.py   FastAPI entry (imports backend.server)
backend/server.py                API routes
backend/db_schema.py             Mongo collections + indexes
backend/services/database.py     bootstrap indexes + seed curated Q&A
backend/services/control_store.py control dashboard payload / settings
backend/services/public_enrichment.py  Gita/Wikipedia/dictionary/sandhya/Open Library + Scrapling fetch
backend/spiritual_qa_content.py  curated Q&A fallback when the DB is empty
tests/                           unit + API tests (Mongo optional)
```

## Database

MongoDB database name: **`uttar_sewa`**.

On API startup, `bootstrap_database` creates indexes and seeds curated Q&A if `question_answers` is empty.

| Collection | Purpose |
|---|---|
| `videos` | YouTube metadata + `transcript_processed` |
| `transcript_segments` | timed captions |
| `question_answers` | searchable Q&A with citations |
| `processing_status` | ingest jobs |
| `control_settings` | dashboard toggles (one doc, `_id: app`) |
| `pinned_qa` | clips pinned from the app |
| `mala_days` | per-device daily japa sync |

Set `MONGO_URL` (default `mongodb://localhost:27017`) and `DB_NAME` (default `uttar_sewa`). If Mongo is down, the API still serves search from the curated library and returns default control settings.

You can also paste YouTube, Gemini, and Mistral keys in the app (**Settings → Bring your keys**). User keys override `.env` and take effect without a restart. GET `/api/control/keys` never returns the full secret.

## Control API

| Method | Path | What it does |
|---|---|---|
| GET | `/api/health` | API + database ping |
| GET | `/api/control/dashboard` | stats + current controls |
| GET/PUT | `/api/control/settings` | language, mala cycle, sandhya, processing |
| GET/PUT | `/api/control/keys` | bring-your-own API keys (masked on read; live reconfigure) |
| POST | `/api/process/ingest` | fill library from videos / video_ids / channel |
| POST | `/api/control/qa/pin` | pin a cited clip |
| GET | `/api/control/qa/pinned` | list pinned clips |
| GET | `/api/control/library/gaps` | unprocessed videos |
| POST | `/api/mala/sync` | persist today's mala |
| GET | `/api/mala/day` | load today's mala |
| POST | `/api/process/start` | start ingest (disabled if processing is off) |
| POST | `/api/process/clear` | clear ingest status |
| GET | `/api/enrich/catalog` | public-apis sources used by the app |
| GET | `/api/enrich/today` | daily Gita verse + Varanasi sunrise/sunset |
| POST | `/api/enrich/companions` | corrective-RAG public cards for a question |
| POST | `/api/control/scrape` | Scrapling/httpx fetch of an allowlisted public page |
| POST | `/api/control/enrich/video` | YouTube oEmbed metadata |

Public companions come from [public-apis](https://github.com/public-apis/public-apis). HTML fetch uses [Scrapling](https://github.com/D4Vinci/Scrapling) when that package and its extras are installed; otherwise httpx. The companion cards follow the corrective-RAG pattern from [awesome-llm-apps](https://github.com/Shubhamsaboo/awesome-llm-apps): extra sources are graded and labeled, and they **never** replace a video citation.

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env                 # optional fallback keys; or paste them in Settings
uvicorn backend.server:app --reload --port 8000
```

### Flutter app

```bash
cd mobile
flutter create . --project-name uttar_sewa --org sewa.uttar
flutter pub get
flutter run --dart-define=API_BASE=http://127.0.0.1:8000/api
```

Android emulator: use `http://10.0.2.2:8000/api` as `API_BASE`.

### Web PWA (optional)

```bash
cd frontend
cp .env.example .env                                 # set REACT_APP_BACKEND_URL
yarn install
yarn start
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

Flutter client + control API + Mongo bootstrap are in this release. Search ranking, timestamp URLs, chat memory, grounded `/api/ask`, and the in-app japa orb are included. YouTube processing still needs captions (or transcription) for a full 900+ video index; the curated library is used when the database is empty. Native overlay / Watch / Whisper STT remain later.

## License

MIT
