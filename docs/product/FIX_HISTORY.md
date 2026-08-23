# Fix history

## Flutter japa required the API

**Symptom:** No network → tap failed or hung; beads did not increment.

**Root cause:** `tapBead` awaited `/api/mala/tap` before updating UI.

**Fix:** `MalaState.applyTap` / `applyUndo` (same math as `mala_counter.py`); persist/sync after.

**Regression:** `mobile/test/models_test.dart` cycle 11 tap/undo.

## PWA chat treated search hits as answers

**Symptom:** Weak matches still presented as “Found N results” with no refuse.

**Root cause:** `ChatInterface` posted `/api/search`.

**Fix:** Post `/api/ask`; render `answer` / `refused` / clips. Orb requires `response.ok`.

## Scrape redirect SSRF

**Symptom:** Allowlisted URL could 302 to an internal host.

**Root cause:** `httpx.Client(follow_redirects=True)` after host check.

**Fix:** `follow_redirects=False`.

**Regression:** `tests/test_scrape_ssrf.py`.

## Re-ingest duplicated evidence

**Symptom:** Same `video_id` ingested twice → two Q&A rows, stale + new.

**Root cause:** Always `insert_one` segments/Q&A.

**Fix:** `delete_many` for that `video_id` before insert.

**Regression:** `test_reingest_replaces_existing_segments_and_qa`.

## Gemini paraphrases in the grounded corpus

**Symptom:** `/api/ask` could cite invented teaching with a timestamp.

**Root cause:** `_ingest_and_persist` preferred `extract_qa_from_transcript`.

**Fix:** Persist only `segments_to_qa`.

**Regression:** `test_gemini_paraphrase_is_not_stored_as_grounded_corpus`.

## Open write of API keys

**Symptom:** Anyone who could hit the API could `PUT /control/keys`.

**Root cause:** No auth on control writes.

**Fix:** Optional `CONTROL_TOKEN` / `X-Control-Token`; Flutter Settings field.

**Regression:** `tests/test_control_token.py`.
