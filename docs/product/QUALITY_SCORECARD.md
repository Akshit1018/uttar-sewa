# Quality scorecard

Scores are against current acceptance criteria, not “perfect software.”

| Dimension | Score | Evidence |
|---|---|---|
| Product value | 8 | Grounded Q&A + mala is a coherent seeker product |
| UX | 7 | Chat now refuses; japa works offline; PWA BYOK missing |
| Logic | 8 | Extractive corpus; ingest replace; local mala math matches server |
| Architecture | 7 | One corpus, two clients; leftover unused services |
| Security | 6 | Optional token + no-redirect scrape; no real auth; cleartext keys |
| Testing | 8 | Pytest for ingest/SSRF/token; Dart mala unit tests |
| Observability | 4 | Logs exist; no metrics/alerts/eval harness |
| Docs | 8 | README + `docs/product/*` match the real product |
| Production readiness | 5 | Single-operator demo; not multi-tenant PRODUCTION_VALIDATED |

## TASK-001 self-eval (this slice)

Against acceptance: local japa, PWA `/ask`, scrape SSRF, ingest dedup, extractive persist, optional control token, product memory.

**10/10 against those criteria only if tests pass on a fresh command.** Runtime on a phone is IMPLEMENTATION_UNVERIFIED for overlay/Watch.
