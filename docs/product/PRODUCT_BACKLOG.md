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
| P1-PWA-BYOK | PWA has no BYOK / control-token UI | P1 | DISCOVERED | Add Settings parity or document Flutter-only |
| P1-SEARCH-EMPTY | Flutter Search has no empty-results UI | P1 | DISCOVERED | Empty state + retry |
| P1-API-BASE | Flutter default `127.0.0.1` fails on a phone | P1 | DISCOVERED | Sensible LAN default or first-run Settings |
| P1-KEYS-AT-REST | BYOK cleartext in Mongo | P1 | DISCOVERED | Encrypt or OS keystore |
| P1-PIN-SPLIT | Server pin vs local heart favorites | P1 | DISCOVERED | One favorites model |
| P1-LIVE-TOGGLE | Live Activity / Watch buttons do not toggle off | P1 | DISCOVERED | Symmetric stop |
| P2-SEMANTICS | Flutter: zero `Semantics` | P2 | DISCOVERED | TalkBack/VoiceOver labels |
| P2-EVAL | No regression set for refuse / faithfulness | P2 | DISCOVERED | Fixture corpus + ask eval |
| P2-PWA-MALA | PWA mala never calls `/mala/sync` | P2 | DISCOVERED | Optional sync, local remains source |
| P3-VECTOR | Unused `embedding` field | P3 | DISCOVERED | Hybrid search only after extractive eval |
| P4-ADS | Ads / streaks / leaderboards | P4 | REJECTED | Conflicts with sadhana product |

Adversarial inspection (2026-08-23): see [`RED_TEAM_FINDINGS.md`](RED_TEAM_FINDINGS.md). Do not treat this backlog as complete.

## Completeness (honest)

| Surface | State |
|---|---|
| Landing / PWA chat | FUNCTIONAL — now `/ask` |
| Flutter chat | FUNCTIONAL |
| Japa Flutter | FUNCTIONAL — local-first, sync best-effort |
| Japa PWA | PARTIAL — localStorage only |
| Ingest | FUNCTIONAL — extractive + replace |
| BYOK | FUNCTIONAL — Flutter; PWA missing |
| Overlay / Watch | PARTIAL — channels present; no device proof here |
| Auth | PARTIAL — optional control token only |
| Multi-tenant SaaS | NOT_STARTED — not the current product |
