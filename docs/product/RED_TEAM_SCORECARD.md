# Red-team scorecard

Date: 2026-08-23. Inspected commit: `d8e36e2` plus working tree. Product: **Uttar Sewa** (spiritual Q&A + japa), not recruiting.

Scoring: 10 = production-grade and market-competitive. Scores are against a seeker who would otherwise use YouTube + a dedicated mala app + [NotebookLM / Gemini Notebook](https://notebooklm.google/).

| Dimension | Score | Why this low |
|---|---|---|
| PRODUCT QUALITY | 4/10 | Two products glued together; empty-corpus first run; marketing claims 900+ videos |
| USER EXPERIENCE | 3/10 | No onboarding; Chat vs Search vs orb disagree; fake Settings toggles |
| UI QUALITY | 4/10 | Dark generic PWA; Flutter Control in primary nav; NaN% badges |
| PRODUCT LOGIC | 4/10 | `/ask` refuses, `/search` does not; pin ≠ heart; mala last-write-wins |
| FRONTEND | 4/10 | Giant files; `undefined/api`; 127.0.0.1 default; unused `loading` |
| BACKEND | 5/10 | Extractive ingest is real; `server.py` is a god file; silent Mongo writes |
| DATABASE | 3/10 | No unique `video_id`; no Q&A uniqueness; no FKs; feedback unindexed |
| API DESIGN | 3/10 | No pagination/rate limits; health `ready: true` when Mongo down |
| ARCHITECTURE | 3/10 | Dual clients; unused ultra_video; enhanced-search soup; cloud restore unauth |
| AI QUALITY | 5/10 | Extractive `/ask` is honest; `/search` can still call LLM; no eval set |
| SECURITY | 2/10 | Demo-open writes; cleartext keys; unauthenticated cloud restore |
| PERFORMANCE | 4/10 | Full corpus `to_list(2000)`; unbounded `limit`; no rate limit |
| RELIABILITY | 3/10 | Ingest delete-then-insert; persist failures return 200 |
| MARKET COMPETITIVENESS | 3/10 | Mala apps and NotebookLM already own the two halves |
| PRODUCTION READINESS | 2/10 | Cannot ship to a phone without dart-define; no auth; no observability |

**Exploit first (if you wanted this product to fail):** expose the API without `CONTROL_TOKEN`, then `PUT /api/control/keys` or `POST /api/cloud/restore`. Product-failure exploit: install the Flutter app on a phone — it talks to `127.0.0.1` and looks dead.
