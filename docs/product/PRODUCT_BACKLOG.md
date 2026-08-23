# Product backlog

Statuses: DISCOVERED | VALIDATING | PLANNED | IN_PROGRESS | TESTING | BLOCKED | DONE | REJECTED

| ID | Problem | Severity | Status | Validation |
|---|---|---|---|---|
| P0-JAPA | Flutter tap required API; offline beads lost | P0 | DONE | Dart `applyTap` tests; local increment then persist |
| P0-ASK | PWA Chat used `/search` (no refuse) | P0 | DONE | ChatInterface posts `/ask`; orb checks `response.ok` |
| P0-SSRF | Scrape followed redirects after allowlist | P0 | DONE | `tests/test_scrape_ssrf.py` |
| P0-DEDUP | Re-ingest duplicated segments/Q&A | P0 | DONE | `test_reingest_replaces_existing_segments_and_qa` |
| P0-CORPUS | Gemini Q&A could enter grounded corpus | P0 | DONE | `test_gemini_paraphrase_is_not_stored_as_grounded_corpus` |
| P0-TOKEN | Unauthenticated PUT keys | P0 | DONE | Optional `CONTROL_TOKEN`; Flutter Settings field |
| P1-PWA-BYOK | PWA has no BYOK / control-token UI | P1 | DONE | Settings token + API URL + `/control/keys` paste |
| P1-SEARCH-EMPTY | Flutter Search has no empty-results UI | P1 | DONE | Empty-state copy after a search |
| P1-API-BASE | Flutter default `127.0.0.1` fails on a phone | P1 | DONE | Settings API URL persisted; banner always visible |
| P1-KEYS-AT-REST | BYOK cleartext in Mongo | P1 | DONE | Sealed `enc_v1` envelope; default key is local-dev |
| P1-PIN-SPLIT | Server pin vs local heart favorites | P1 | DONE | PWA pin/unpin + local offline cache |
| P1-LIVE-TOGGLE | Live Activity / Watch buttons do not toggle off | P1 | DONE | Symmetric stop + native methods |
| P0-CLOUD | Cloud restore/backup ungated | P0 | DONE | `authorize_cloud` fail-closed |
| P0-COPY | 900+ / AI understands / empty Chat | P0 | DONE | Honest copy + Chat banner |
| P0-INGEST | Delete-then-insert hole | P0 | DONE | Upsert then drop stale |
| P2-SEMANTICS | Flutter: zero `Semantics` | P2 | PARTIAL | Orb + nav tooltips labeled |
| P2-EVAL | No regression set for refuse / faithfulness | P2 | PARTIAL | `tests/test_ask_eval.py` fixture |
| P2-PWA-MALA | PWA mala never calls `/mala/sync` | P2 | DONE | `useMala` best-effort sync; local remains source |
| P3-VECTOR | Unused `embedding` field | P3 | DISCOVERED | Hybrid search only after extractive eval |
| P4-ADS | Ads / streaks / leaderboards | P4 | REJECTED | Conflicts with sadhana product |

Adversarial inspection (2026-08-23): see [`RED_TEAM_FINDINGS.md`](RED_TEAM_FINDINGS.md). Forensic extension: [`FORENSIC_INDEX.md`](FORENSIC_INDEX.md). Do not treat this backlog as complete.

| ID | Problem | Severity | Status | Validation |
|---|---|---|---|---|
| F-NEW-01 | PWA custom channel URL ignored by `/process/start` | P0 | DONE | `test_process_start_forwards_channel_url` |
| F-NEW-02 | Seeded 30 pairs hide empty-corpus banner | P0 | DONE | `ingested_qa` / `seed_only` + Chat paste URL |
| F-NEW-03 | Q&A questions are caption `[:80]` | P1 | DONE | Timestamped clip titles, not invented Qs |
| F-NEW-04 | Ask/search RAM-load 2000 docs | P1 | DONE | Query-scoped cap 400 |
| F-NEW-07 | BYOK Gemini/Mistral unused by ask | P2 | DONE | Gemini optional; help says unused |

## Completeness (honest)

| Surface | State |
|---|---|
| Landing / PWA chat | FUNCTIONAL — now `/ask` |
| Flutter chat | FUNCTIONAL |
| Japa Flutter | FUNCTIONAL — local-first, sync best-effort |
| Japa PWA | FUNCTIONAL — local first, `/mala/sync` best-effort |
| Ingest | FUNCTIONAL — extractive + replace; startup resume |
| BYOK | FUNCTIONAL — Flutter + PWA Settings; sealed at rest |
| Overlay / Watch | PARTIAL — channels present; no device proof here |
| Auth | PARTIAL — optional control token only |
| Multi-tenant SaaS | NOT_STARTED — not the current product |
