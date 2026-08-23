# Logic failures

INPUT → STATE → ACTION → SIDE EFFECT → NEXT STATE.

## LOG-01 — Ask vs search vs orb (HIGH, CONFIRMED)
Same query, three contracts. See `API_FINDINGS.md`.

## LOG-02 — Offline ask uses search cache (HIGH, CONFIRMED)
`ChatInterface.jsx` offline: `getCachedResults` then treats array as ask payload; `answer`/`refused` may be missing.  
**Sequence:** Search online → go offline → Chat “ask” → wrong semantics.

## LOG-03 — Ingest crash leaves hole (HIGH, CONFIRMED)
Delete evidence → insert → crash → video marked processed or not depending on path; corpus empty. `_ingest_and_persist` deletes then inserts then sets `transcript_processed`.

## LOG-04 — Silent success on failed persist (HIGH, CONFIRMED)
Settings/pin/sync return 200; Mongo never wrote. UI believes saved.

## LOG-05 — Mala two writers (MEDIUM, CONFIRMED)
Local applyTap + `/mala/sync` replace_one. Two devices, same `device_id` (copied prefs) or different ids that never merge. PWA never syncs.

## LOG-06 — Undo does not update native count (MEDIUM, CONFIRMED)
`tapBead` updates overlay; `undoBead` does not.

## LOG-07 — Double-tap undo promised on PWA Sadhana copy, absent on Flutter orb
`SadhanaDashboard.jsx` vs `widgets.dart` GestureDetector.

## LOG-08 — Health ready vs database (MEDIUM)
Orchestrators think the service is ready.

## LOG-09 — Curated fallback masquerades as video answers
Mongo empty → `spiritual_qa_content` (~30 pairs, often no `video_id`). Ask can cite “curated” without the user understanding it is not a timestamped clip. Flutter/PWA do label curated in some clip cards — not everywhere.

## LOG-10 — Control token typed but not persisted (MEDIUM)
`onChanged` mutates memory; kill app → token gone; subsequent BYOK 401.

## LOG-11 — `channelId=all` ingest → hardcoded `bhajanmarg`
Operator thinks “all”.  
**EVIDENCE:** `screens.dart` ingest branch.

## LOG-12 — Refresh / two tabs
PWA mala: localStorage last write. Chat messages: memory only (lost on refresh). Flutter chat: single `_result` (lost on tab switch). No draft recovery.

## LOG-13 — Pin without token
401 swallowed or uncaught on Flutter Control switches / pin.

## Impossible / missing states
- No “ingest running” lock in UI for two Start clicks (`create_task` twice).  
- No “corpus stale” after evidence replace (clients cache search results).  
- No “day rolled over” mala reset UX (prefs persist beads_today across calendar days until sync key changes — Flutter persist uses today's date only on sync, local prefs keep old counts overnight). **NEEDS VERIFICATION** of day rollover in `boot()`.
