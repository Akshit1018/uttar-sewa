# Architecture findings

## Why this can fail at 100 users

```
Phone (127.0.0.1) ──X── API
PWA (undefined/api) ──X── API
         │
    FastAPI god file (server.py)
         ├─ load 2000 Q&A into RAM every ask/search
         ├─ enhanced_search_coordinator (4 strategies)
         ├─ optional LLM
         ├─ companions (5 public APIs)
         └─ Mongo (optional; silent fallback to ~30 curated pairs)
```

Single process. No queue for ingest except `asyncio.create_task`. No worker. No cache with TTL (PWA localStorage search cache can poison `/ask`). No metrics backend.

## Overengineering

- `ultra_search_engine`, `intelligent_search_service`, `enhanced_search_coordinator`, `ultra_video_service` (unused import).
- Cloud Firestore backup **and** Mongo **and** curated Python fallback — three sources of truth.
- Flutter Control + React Admin/Processing — two operator UIs.

## Underengineering

- No authn/authz model.
- No unique indexes.
- No ingest transaction.
- No evals.
- No real analytics sink (`analyticsService` is localStorage + `console.log`).

## Coupling

`server.py` owns HTTP, Mongo fallback, BYOK reconfigure, search, ask, mala, enrich, cloud, feedback, analytics.

## Duplicate domain rules

Mala math: Python `mala_counter` **and** Dart `MalaState.applyTap`. Drift risk. Server `/mala/tap` unused by Flutter.

## Dead / leftover

| Item | Evidence |
|---|---|
| `ultra_video_service` | No Python imports |
| `QuestionAnswer.embedding` | Model only |
| `AppState.loading` | Never set |
| Flutter `api.tap` / `api.undo` | Never called |
| `_process_channel_videos` | Not called; incremental path is |
| `gemini_api_calls_needed` in system/status | Stale after extractive ingest |
