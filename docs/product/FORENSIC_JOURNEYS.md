# Forensic journeys (reconstruction)

This file does not argue quality. It records what the repository implements.

## What exists in the tree

Three runnable surfaces share one FastAPI process:

| Surface | Entrypoint | Navigation |
|---|---|---|
| API | `backend/server.py` via `app_server.py` / `run_backend.py` | `/api/*` |
| Flutter | `mobile/lib/main.dart` → `HomeShell` | 5 tabs, no named routes |
| PWA | `frontend/src/App.js` | `currentView` string; React Router only redirects `*` → `/` |

There are **no** queues, workers, Redis, Celery, feature flags, OpenTelemetry, or Sentry. Channel processing is `asyncio.create_task` inside the API process. Client analytics write `localStorage` and `console.log`. Flutter has no analytics module.

Mongo database name: `uttar_sewa`. Collections: `videos`, `transcript_segments`, `question_answers`, `processing_status`, `control_settings`, `control_secrets`, `pinned_qa`, `mala_days`, `feedback`. Startup `bootstrap_database` creates indexes and seeds `SPIRITUAL_QA_LIBRARY` when Q&A count is 0.

When Mongo is down, ask/search fall back to that curated in-memory library. Health `ready` equals the database ping.

## Canonical data path

```
Seeker types a question
  → Chat / Search / Orb
  → POST /api/ask  or  POST /api/search
  → _load_qa_database()   # find().to_list(2000) or curated fallback
  → expand_query + rank_answers (lexical)
  → /ask: grounded_ask copies corpus text or refuses (threshold 0.42)
  → /search: ranked list, no refuse
  → UI shows answer/clips + YouTube watch?v=&t=
```

Gemini / Mistral are **configured** by BYOK and **not called** by `/ask` or `/search`. Ingest persists `segments_to_qa` (caption slice as question, full caption as answer). Whisper runs only when captions are empty and a local audio file exists.

## Journey A — First ask (PWA)

```
USER opens /
SCREEN ChatInterface (default currentView)
ACTION types / taps a suggestion / voice
STATE messages[], channelId (localStorage preferredChannel)
API POST /api/ask {query, language, conversation_history, channel_id}
    no include_companions
DOMAIN grounded_ask on up to 2000 Q&A docs
DB question_answers or library_as_qa()
RESULT {answer, refused, clips[]}
UI bot bubble + clip cards + heart (localStorage)
NEXT another question, Search, or hold-orb sheet
```

Evidence: `frontend/src/App.js`, `ChatInterface.jsx`, `backend/server.py` ask handler, `grounded_ask.py`.

## Journey B — First ask (Flutter)

```
USER opens app
SCREEN ChatScreen (tab 0)
ACTION types question
STATE AppState.language, channelId, history in the screen
API POST /ask then, if public_companions, POST /enrich/companions
DOMAIN same grounded_ask
RESULT AskResult + CompanionCard list
UI answer text + ClipCard + public cards
NEXT Search / Sadhana / Control
```

Hold 2.5s on the orb sets `askRequested`, switches to tab 0, increments `askFocusTick`, focuses the field.

## Journey C — Search

Same lexical corpus as ask. Search never refuses. PWA can replay `spiritual_qa_offline_cache` when offline. Flutter Chat/Search errors are SnackBars. Flutter empty search shows amber copy after a performed search.

## Journey D — Japa

| Client | Tap | Hold | Undo | Persist |
|---|---|---|---|---|
| Flutter | `MalaState.applyTap` local | switch to Chat + focus | Sadhana button; updates native count | SharedPreferences + best-effort `/mala/sync` |
| PWA | `useMala.tap` local | `JapaChatSheet` `/ask` | double-tap orb | `localStorage` only — **never** `/mala/sync` |

Server `/mala/tap` and `/mala/undo` exist. Flutter `ApiClient` defines them and **does not use them** for the orb.

## Journey E — Ingest / process

Two APIs:

1. `POST /process/start` — `require_control`, **no request body**. Always `start_channel_processing()` with default channel unless the unused `channel_url` argument is passed from Python. PWA still POSTs `{channel_url}` JSON. FastAPI discards it.
2. `POST /process/ingest` — structured videos / ids / channel. Flutter Control button uses this.

Persist: upsert extractive rows, then drop stale keys for that `video_id`.

Background: in-process `asyncio.create_task`. Process restart loses the job handle except `processing_status` rows.

## Journey F — Operator keys / token

Flutter Settings: editable API URL, control token, BYOK PUT `/control/keys`.  
PWA Settings: token only; API URL displayed, not edited.

`authorize_control`: demo-open when `CONTROL_TOKEN` unset.  
`authorize_cloud`: fail-closed always.

## Journey G — Pin vs heart

Flutter pin → Mongo `pinned_qa`.  
PWA heart → `spiritual_qa_favorites` localStorage.  
These never meet.

## Journey H — Cloud restore

`POST /api/cloud/restore` overwrites Mongo from Firestore if configured and token matches. **No Flutter or PWA screen** calls it. Operator must curl.

## Journey I — Public companions

Flutter: `/enrich/companions` after ask; `/enrich/today` at boot.  
PWA: no companion fetch. About copy mentions labeled public texts.  
Server `include_companions` on `/ask` is unused by both shipped ask UIs except Flutter's separate call.

## What is not a journey (dead / unused)

| Artifact | Why it is not a journey |
|---|---|
| `enhanced_search_coordinator`, `ultra_search_engine`, `intelligent_search_service`, `ultra_video_service` | Not imported by `server.py` |
| `LLMService.extract_qa_from_transcript` / `understand_user_query` | Not called from ingest or search |
| `ProcessingService._process_channel_videos` | Defined, never referenced |
| FastAPI `BackgroundTasks` import | Unused |
| Flutter `api.tap` / `api.undo` | Defined, unused |
| PWA `getCachedResults` in Chat | Imported; offline path throws instead |

## Client capability split (fact)

| Capability | Flutter | PWA |
|---|---|---|
| `/ask` + `/search` | yes | yes |
| Editable API URL | yes | no |
| BYOK UI | yes | no |
| Server pin | yes | no |
| Local hearts | no | yes |
| Mala API sync | yes | no |
| Companions | yes | no |
| Voice input | no | yes |
| Double-tap undo / drag orb | no | yes |
| Native overlay / Live / Watch | yes (channels) | no |
| Cloud UI | no | no |
