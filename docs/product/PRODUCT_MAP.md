# Product map (execution paths, not filenames)

## Clients

- **Flutter** `mobile/lib/` — Chat (`/ask`), Search (`/search`), Sadhana (local mala + native channels), Control, Settings (BYOK + control token).
- **React PWA** `frontend/src/` — Chat (`/ask`), Search page, japa orb (`JapaChatSheet` → `/ask`), Admin/Processing screens. No BYOK UI.

## API (`backend/server.py`)

| Path | Contract |
|---|---|
| POST `/api/ask` | Extractive answer or refuse; clips with timestamps |
| POST `/api/search` | Ranked Q&A list; no refuse |
| POST `/api/mala/tap` \| `/undo` | Server-side math (Flutter no longer depends on this for the orb) |
| POST `/api/mala/sync` | Best-effort day persist |
| POST `/api/process/ingest` | YouTube videos → extractive corpus |
| POST `/api/process/start` | Incremental caption/Whisper processing |
| GET/PUT `/api/control/keys` | BYOK; masked GET |
| POST `/api/enrich/companions` | Labeled public cards |
| POST `/api/control/scrape` | Allowlisted page; no redirects |

## Data

Mongo `uttar_sewa`: videos, transcript_segments, question_answers, processing_status, control_settings, control_secrets, pinned_qa, mala_days.

Fallback: `backend/spiritual_qa_content.py` when Q&A collection is empty or Mongo is down.

Ask/search load at most **2000** Q&A documents into process memory (`_load_qa_database`). Extractive “questions” from ingest are the first 80 characters of a caption (`segments_to_qa`). `POST /process/start` does not read a JSON `channel_url` (PWA custom-channel field is discarded).
