# Architecture

```
Flutter / PWA
    │  HTTP
    ▼
FastAPI (backend/server.py)
    ├─ grounded_ask          extractive refuse/cite
    ├─ relevance_search      lexical rank
    ├─ processing_service    ingest + replace evidence
    │     ├─ youtube_ingest / youtube_service
    │     └─ transcript_ingest (captions → Whisper → none)
    ├─ public_enrichment     companions + scrape (no redirects)
    ├─ byok + control_auth   user keys; optional CONTROL_TOKEN
    └─ mala_counter          tap/undo math
         ▼
    MongoDB (optional at runtime)
```

## Boundaries that must stay

- Video answer path never calls public scrape or Gemini for the sentence shown as the teaching.
- Companions are a parallel card list with attribution.
- Ingest writes transcript-derived rows only.
- Control writes are demo-open unless `CONTROL_TOKEN` is set.

## Dead / leftover (do not build on)

- `ultra_video_service` unused
- unused `embedding` field
- `feedback` collection mentioned in code paths but not in `db_schema`
- React Admin vs Flutter Control duplication
