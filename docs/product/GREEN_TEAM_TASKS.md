# Green Team tasks

Statuses: IMPLEMENTED | TESTED | PRODUCTION-VALIDATED | PARTIAL | MOCKED | BLOCKED | RESEARCHED | REJECTED

Classification of Red Team claims used: VERIFIED / PARTIALLY VERIFIED / FALSE POSITIVE / OUTDATED / NEEDS RESEARCH / NEEDS USER VALIDATION.

## TASK-G001 — Honor `channel_url` on process start

| Field | Content |
|---|---|
| Problem | PWA custom channel POST body was discarded |
| Red Team | F-NEW-01 **VERIFIED** |
| Root cause | `start_processing()` took no body; service already accepted `channel_url` |
| Research | YouTube handle/`@` URL patterns used by the existing extractor |
| Solution | `ProcessStartRequest` forwarded to `start_channel_processing` |
| Tests | `test_process_start_forwards_channel_url` |
| Status | **IMPLEMENTED** / **TESTED**. Live channel fetch **EXTERNAL_DEPENDENCY_REQUIRED** |

## TASK-G002 — Stats honesty (curated vs ingested)

| Field | Content |
|---|---|
| Problem | Seed ~30 pairs hid the empty-corpus banner |
| Red Team | F-NEW-02 **VERIFIED** |
| Root cause | Banner used `total_qa_pairs`, not `source` |
| Solution | `summarize_qa_counts`; `/stats`, dashboard, system status expose `curated_qa` / `ingested_qa` / `seed_only` |
| Tests | `test_summarize_qa_counts_flags_seed_only_library`, `test_stats_payload_exposes_curated_versus_ingested` |
| Status | **IMPLEMENTED** / **TESTED**. Device UI **UNVERIFIED** |

## TASK-G003 — Query-scoped corpus load

| Field | Content |
|---|---|
| Problem | Every ask/search dumped 2000 docs into RAM |
| Red Team | F-NEW-04 **VERIFIED** |
| Research | Keep lexical ranking (vector search **REJECTED** until evals). Cap + token `$or` filter |
| Solution | `qa_load_plan` / `qa_candidate_filter`, cap 400, recent fallback |
| Tests | `test_query_scoped_load_plan_never_dumps_uncapped_corpus`, `test_load_qa_database_is_query_scoped` |
| Status | **IMPLEMENTED** / **TESTED**. Synonym miss is a known limitation |

## TASK-G004 — Clip titles, not fake questions

| Field | Content |
|---|---|
| Problem | `question = text[:80]` looked like Q&A |
| Red Team | F-NEW-03 **VERIFIED** |
| Research | YouTube chapter format `M:SS` + short label ([YouTube Help](https://support.google.com/youtube/answer/9884579)) |
| Solution | `clip_title_from_segment`; `kind=clip`; no Gemini-invented questions |
| Tests | `test_clip_title_is_timestamped_snippet_not_fake_question` |
| Status | **IMPLEMENTED** / **TESTED** |

## TASK-G005 — Paste YouTube URL from Chat

| Field | Content |
|---|---|
| Problem | First cited clip needed hidden Control |
| Red Team | Activation / NotebookLM time-to-value **VERIFIED** as product gap |
| Solution | `POST /process/from-url` + Chat paste field (PWA + Flutter) |
| Tests | `test_process_from_url_routes_watch_to_ingest`, source contracts |
| Status | **IMPLEMENTED** / **TESTED**. Live ingest **EXTERNAL_DEPENDENCY_REQUIRED** (YouTube key) |

## TASK-G006 — Flutter orb undo + PWA API URL persist

| Field | Content |
|---|---|
| Problem | PWA had double-tap undo; Flutter orb did not. PWA API URL was env-only |
| Classification | **VERIFIED** (code) |
| Solution | Flutter double-tap → `undoBead`; Settings persist `uttar_sewa_backend_url` |
| Status | **IMPLEMENTED**. Flutter/PWA device **UNVERIFIED** |

## TASK-G007 — Curated evidence labels + unused BYOK honesty

| Field | Content |
|---|---|
| Problem | Seed clips looked like guru video; Gemini marked required |
| Red Team | F-NEW-07 **VERIFIED**; curated mislabel **VERIFIED** |
| Solution | `citation_kind` from `source`; Gemini `required=False` + unused help; PWA `include_companions` |
| Status | **IMPLEMENTED** / **TESTED** |

## Rejected / backlog

| Item | Decision |
|---|---|
| User accounts | **REJECTED** — single-operator product |
| Vector/hybrid search | **BACKLOG** — repeats ultra-search without evals |
| Leaderboards / punya / ads | **REJECTED** |
| Encrypt keys at rest | **IMPLEMENTED** — sealed envelope (`enc_v1`) keyed by `SECRETS_KEY`/`CONTROL_TOKEN` |
| Unify pin vs heart | **IMPLEMENTED** — PWA hearts call `/control/qa/pin` + `/unpin`; local cache offline |
| Durable ingest queue | **PARTIAL** — persist `channel_url` and resume pending/processing on startup. Still in-process. |

## Closeout (this session)

| ID | Status |
|---|---|
| TASK-G008 secrets at rest | **IMPLEMENTED** / **TESTED** — not AES-GCM; stdlib sealed envelope |
| TASK-G009 pin/heart unify | **IMPLEMENTED** / **TESTED** — pin is a seeker action |
| TASK-G010 unique indexes | **IMPLEMENTED** / **TESTED** — unique failure is not downgraded |
| TASK-G011 text index | **IMPLEMENTED** — schema + `$text` then regex fallback |
| TASK-G012 rate limits | **IMPLEMENTED** / **TESTED** — in-process sliding window |
| TASK-G013 job resume | **IMPLEMENTED** / **TESTED** — startup replay |
| TASK-G014 PWA BYOK + mala sync | **IMPLEMENTED** — Settings `/control/keys`; `useMala` posts `/mala/sync` |
| TASK-G015 remote control lock | **IMPLEMENTED** / **TESTED** — token unset only loopback is demo-open |

## Still blocked (cannot claim 100%)

- Flutter/PWA on a real device: **UNVERIFIED**
- Live YouTube ingest: **EXTERNAL_DEPENDENCY_REQUIRED**
- Overlay / Watch / Live Activity hardware: **UNVERIFIED**
- Vector search / accounts / ads: **REJECTED**
