# Feature truth map

**Rule:** classify the *shipped behavior*, not the filename.  
**Date:** 2026-08-23. Runtime of Flutter/PWA on a device: **UNVERIFIED**.

Legend: REAL | PARTIAL | COSMETIC | MOCKED | BROKEN | HIDDEN | DEAD | DUPLICATE | MISLEADING | UNVERIFIED

| Feature (as claimed) | Class | Evidence | User consequence |
|---|---|---|---|
| Grounded `/api/ask` (copy or refuse) | **REAL** (API + tests) | `grounded_ask.py`; `tests/test_ask_eval.py`, `test_grounded_ask.py` | Seeker gets corpus text or a refuse sentence. **UNVERIFIED** that a live corpus feels useful. |
| Timestamp YouTube links | **REAL** (URL builder) | `timestamp_urls.py`; clip cards in both clients | Click opens `watch?v=&t=` if `video_id` exists. Curated rows have empty video_id → no clip. |
| Lexical `/api/search` | **REAL** | `search_questions` uses `rank_answers` only; `test_search_handler_is_lexical_only` | Hits without refuse. Weak matches still look like answers. |
| “AI understands your question” | **MISLEADING** | About/translations rewritten; leftover dead `llm_service` still in tree | Seeker who reads old Admin/test_result.md still thinks Gemini ranks search. |
| Channel ingest of a guru library | **PARTIAL** | `ingest_video_list` + YouTube captions/Whisper | Works if captions or local audio exist. Caption-less videos stay unprocessed. |
| PWA “custom channel URL” on Start | **COSMETIC / BROKEN** | `ProcessingStatus.jsx` POSTs `{channel_url}`; `start_processing()` takes **no body** (`server.py`) | Operator believes they ingested a different channel. Default `bhajanmarg` still runs. |
| Flutter YouTube library ingest | **PARTIAL** | Control → `POST /process/ingest` | Hidden from PWA. Needs token when locked. |
| Unique indexes + upsert ingest | **REAL** (code + tests) | `db_schema.py`, `_persist_extractive` | Crash after upsert no longer empties the video. Unique index create may silently fall back non-unique (`database.py` except). |
| Curated library fallback | **REAL** and **MISLEADING** | `_load_qa_database` → `library_as_qa()` | App “works” with 30 generic pairs that are not the seeker’s guru. Citations look like answers. |
| Empty-corpus Chat honesty | **PARTIAL** | Banners when `total_qa_pairs == 0` | If seed ran, count is 30, banner hidden, answers are curated — seeker thinks the library is theirs. |
| Japa mala (count beads) | **REAL** locally | `mala_counter.py` / `lib/mala.js` / `MalaState.applyTap` | Beads increment offline. |
| Japa synced across devices | **PARTIAL** | Flutter `/mala/sync`; PWA never calls it | Two clients, two malas. README still says daily counts sync. |
| Hold orb to ask | **REAL** (wired) | Flutter focus Chat; PWA `JapaChatSheet` | **UNVERIFIED** hold timing on real phones. |
| Live Activity / Watch | **PARTIAL** | Start/stop methods exist; Android returns `false`; iOS stubs | Buttons toggle state in Dart. Device proof **UNVERIFIED**. Overlay permission flow **UNVERIFIED**. |
| Volume-key bead | **PARTIAL** | Android `onKeyDown` → `volumeTap` | Eats volume keys while the Activity is focused. iOS: no equivalent. |
| BYOK | **PARTIAL** | Flutter UI + Mongo `control_secrets` cleartext | Keys reconfigure YouTube/Gemini/Mistral. Ask/search still do not use those models. |
| Control token | **PARTIAL** | Optional; demo-open writes | Cloud routes fail-closed. Keys/ingest open on a LAN demo. |
| Cloud backup/restore | **HIDDEN** | API + Firestore service; no client UI | Operator can wipe Mongo via curl if token+creds exist. Seeker never sees it. |
| Public companions (Gita/Wiki) | **PARTIAL** | Flutter only; PWA copy-only | Split product. Companions never enter the video answer string. |
| Favorites ♥ | **REAL** (local) | PWA `useFavorites` | Lost on clear / new browser. Not on Flutter. |
| Server pins | **REAL** (API) | Flutter pin | Not on PWA. Requires control auth when token set. |
| Recommendations | **PARTIAL** | `recommend_from_history` over same 2000-row bag | Recycles corpus questions. Not personalized beyond recent query strings. |
| Voice search | **PARTIAL** | PWA Web Speech | Flutter: none. iOS Safari **UNVERIFIED**. |
| Offline search | **PARTIAL** | PWA Search cache | Chat offline is honest (throws). Cache can be stale. |
| Health / ready | **REAL** | `ready == database` | Orchestrators can distinguish API-up / Mongo-down. |
| Analytics dashboard | **MOCKED** | `analyticsService` → localStorage + `console.log`; Admin export is that blob | Operator cannot tell if anyone got a cited answer. |
| Admin “real_data_only” | **PARTIAL** | Regex on sample video_id prefixes | Cosmetic health theater if ingest used real ids. |
| Dark Mode / Auto Download | **DEAD** (removed from UI) | Settings copy admits they were fake | — |
| 900+ videos | **DEAD** (copy removed) | About/translations | Old `test_result.md` / FEATURE_BRAINSTORM still claim enterprise scale. |
| Semantic / embedding search | **DEAD** | `embedding` field unused | Marketing leftover in brainstorm docs. |
| Ultra / intelligent / enhanced search | **DEAD** | Orphan modules, not imported | Complexity tax; tests forbid re-wiring to `/search`. |
| Conversation memory | **PARTIAL** | Last N user strings sent as `conversation_history` | Not a stored thread. Refresh loses it. |
| Multi-user accounts | **MISSING** → treat as **DEAD** for SaaS claims | No users table | One Mongo, one operator. |
| Rate limiting | **MISSING** | Open `/ask` `/search` `/feedback` | Abuse surface. |
| Pagination | **MISSING** | `to_list(2000)` | Q&A 2001+ invisible to ask/search. |
| Question quality | **MISLEADING** | `segments_to_qa` question = `text[:80]` | “Q&A” is caption slices, not real questions. |
| PWA API bootstrap | **PARTIAL** | `resolveBackendUrl`; `.env.example` has origin | Empty CRA env no longer becomes `undefined/api`. Phone PWA still needs same-origin or a filled env. |
| Flutter API bootstrap | **PARTIAL** | Settings field + persist | Default remains `127.0.0.1`. First-run still dead until the seeker types a LAN URL. |
| Accessibility | **PARTIAL** | Orb Semantics / aria-labels | Most cards unlabeled. **UNVERIFIED** with TalkBack. |
| Notifications / sandhya | **PARTIAL** | PWA `notificationService` if permission; Flutter native none for sandhya | Easy to miss. |
| Service worker | **UNVERIFIED** | Registered in `App.js` | May cache stale JS; not tested here. |

## Scores (implementation quality, not morale)

A feature can exist and still score low.

| Area | Completeness | Reliability | Mobile | Security | Competitive |
|---|---|---|---|---|---|
| Ask | 7 | 6 | 5 | 4 | 4 |
| Search | 5 | 5 | 5 | 4 | 3 |
| Ingest | 5 | 4 | n/a | 3 | 5 vs NotebookLM time-to-value |
| Japa | 5 | 6 local | 5 | n/a | 3 vs Mantrum/JapGuru |
| Operator control | 6 Flutter / 3 PWA | 5 | 4 | 3 | n/a |
| Companions | 4 | 4 | 3 | 5 (labeled) | 3 |
| Analytics | 1 | 1 | 1 | 2 | 1 |

Confidence: scores are **STRONG** from code; not production-measured.
