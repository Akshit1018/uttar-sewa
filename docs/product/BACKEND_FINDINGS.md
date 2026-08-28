# Backend findings

`backend/server.py` is the application. ~1170 lines. Routes, Mongo, BYOK reconfigure, search, ask, cloud, feedback.

## HIGH

### BE-01 — Silent write success
Settings, secrets (except apply_env), pin, mala sync: except → log → 200.

### BE-02 — Ingest not atomic
`_replace_video_evidence` + inserts. No transaction.

### BE-03 — Full corpus in memory
`_load_qa_database` `to_list(2000)` every ask/search.

### BE-04 — Search coordinator complexity
Four strategies; LLM optional; user query logged at INFO.

### BE-05 — Unauth cloud + feedback + analytics reads

### BE-06 — Regex suggestions

### BE-07 — No rate limit / no request size limits on feedback

## MEDIUM

### BE-08 — Dead `_process_channel_videos` and `ultra_video_service`

### BE-09 — `/process/start` ignores channel body

### BE-10 — Gemini extract still callable

### BE-11 — Blocking-style httpx in companion path (sync Client inside async app)
`PublicHttp` uses sync `httpx.Client` — blocks the event loop per companion fetch.

### BE-12 — `asyncio.sleep(3)` per video in incremental processing
Slow, still on the API process.

## LOW

Hardcoded `bhajanmarg`, Varanasi sandhya, overlay “later” note in `/mala/config` (stale vs shipped native channels).
