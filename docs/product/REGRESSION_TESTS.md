# Regression tests

Fresh command used: `python3 -m pytest tests/ -q`

Closeout: `tests/test_green_team_closeout.py` (secrets, unique indexes, remote control lock, rate limit, job resume, pin/unpin, PWA wiring).

| Area | Test |
|---|---|
| Channel URL on start | `test_process_start_forwards_channel_url` |
| Paste URL ingest routing | `test_process_from_url_routes_watch_to_ingest` |
| Seed vs ingested stats | `test_summarize_qa_counts_*`, `test_stats_payload_*` |
| Clip titles | `test_clip_title_*`, `test_segments_to_qa_question_*` |
| Query-scoped load | `test_query_scoped_load_plan_*`, `test_load_qa_database_is_query_scoped` |
| Curated labels | `test_curated_library_clips_are_labeled_*`, `test_curated_clips_are_labeled_*` |
| BYOK honesty | `test_gemini_is_optional_because_ask_does_not_call_it` |
| Client contracts | `test_pwa_*`, `test_flutter_chat_and_orb_*` |
| Prior P0/P1 | `test_hardening.py`, ingest re-replace, cloud fail-closed |
| Same-origin PWA mount | `tests/test_pwa_static.py` |

Flutter widget tests and browser journeys were **not** run (SDK / browser harness absent).
