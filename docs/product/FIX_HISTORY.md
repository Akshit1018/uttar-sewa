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

## Phone/PWA API bootstrap (UX-01, UX-02)

**Symptom:** Flutter talked only to `127.0.0.1`; PWA became `undefined/api`.

**Fix:** Editable Flutter API URL (persisted). PWA `resolveBackendUrl` falls back to page origin, then localhost. `.env.example` has a real origin.

**Regression:** `tests/test_hardening.py` + `mobile/test/api_client_test.dart`.

## Cloud backup/restore ungated (SEC-01)

**Symptom:** `POST /api/cloud/restore` open when token unset.

**Fix:** `authorize_cloud` fail-closed. Token must be set and match.

**Regression:** `test_cloud_routes_require_token_even_when_unset`.

## Ingest delete-then-insert hole (DB-03)

**Symptom:** Crash after delete emptied a video.

**Fix:** Upsert extractive rows first, then drop stale keys.

**Regression:** `test_reingest_replaces_existing_segments_and_qa`.

## Search LLM / ultra path (AI-01)

**Symptom:** `/search` could rank via LLM.

**Fix:** Lexical `rank_answers` only.

## Empty-corpus / 900+ copy / fake settings

**Symptom:** Chat hid empty corpus; About claimed 900+ AI answers; Dark Mode / Auto Download did nothing; clear had no confirm.

**Fix:** Chat/Flutter empty-corpus banners; honest copy; removed fake toggles; confirm on Settings/Favorites clear.

## Ask channel + offline + Live/Watch off

**Symptom:** Flutter Chat / PWA orb omitted `channel_id`; offline Chat reused search cache; Live/Watch start-only; undo skipped native count.

**Fix:** Channel on all ask clients; offline throws; stop Live/Watch methods; undo calls `updateCount`.

## Green Team activation + corpus honesty (2026-08-23)

**Symptom:** Custom channel URL discarded; seed library hid empty-corpus; questions were caption `[:80]`; ask loaded 2000 docs.

**Root cause:** HTTP handler dropped `channel_url`; banners used total count; slicer treated slices as questions; uncapped RAM dump.

**Fix:** `ProcessStartRequest` + `/process/from-url`; `curated_qa`/`ingested_qa`/`seed_only`; timestamped clip titles; query-scoped load (cap 400); Chat paste-URL; PWA persisted API URL; Flutter orb double-tap undo; Gemini marked unused.

**Regression:** `tests/test_green_team_corpus.py` (116 pytest total).

## Green Team closeout (2026-08-23)

**Symptom:** leftovers — cleartext keys, pin/heart split, unique indexes swallowed, no rate limit, ingest died with the worker, PWA no BYOK/mala sync.

**Fix:** sealed `enc_v1` secrets; pin as seeker API + PWA sync; unique index failures stay unique; `$text` then regex; sliding-window rate limits; persist `channel_url` and resume pending jobs; PWA Settings keys + mala sync; control writes fail-closed off loopback when token unset.

**Regression:** `tests/test_green_team_closeout.py`.
