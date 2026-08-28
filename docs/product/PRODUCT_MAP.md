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
| POST `/api/process/from-url` | Paste a watch or channel URL (Chat activation) |
| POST `/api/process/start` | Incremental processing; optional JSON `channel_url` |
| GET/PUT `/api/control/keys` | BYOK; masked GET |
| POST `/api/enrich/companions` | Labeled public cards |
| POST `/api/control/scrape` | Allowlisted page; no redirects |

## Data

Mongo `uttar_sewa`: videos, transcript_segments, question_answers, processing_status, control_settings, control_secrets, pinned_qa, mala_days.

Fallback: `backend/spiritual_qa_content.py` when Q&A collection is empty or Mongo is down.

Ask/search load a **query-scoped** candidate set (cap 400) via `qa_corpus.qa_candidate_filter`, then rank in process. Ingest clip titles are YouTube-style `M:SS — snippet` (`clip_title_from_segment`), not invented questions. `POST /process/start` forwards `channel_url` when provided. Stats expose `curated_qa` / `ingested_qa` / `seed_only`.
