# Quality scorecard

Scores are against current acceptance criteria, not “perfect software.”

| Dimension | Score | Evidence |
|---|---|---|
| Product value | 8 | Grounded Q&A + mala + paste-URL activation |
| UX | 7 | Honest seed banner + Chat paste URL; device journeys UNVERIFIED |
| Logic | 8 | Extractive corpus; query-scoped load; clip titles not fake Qs |
| Architecture | 7 | One corpus, two clients; leftover unused services remain |
| Security | 5 | Cloud fail-closed; control writes still demo-open; keys cleartext |
| Testing | 8 | 116 pytest including `test_green_team_corpus.py`; Flutter/browser not run |
| Observability | 5 | process_start / from-url / qa_load logs; no metrics/alerts |
| Docs | 8 | Green Team memory files + updated truth map |
| Production readiness | 5 | Single-operator demo; ingest still in-process |

## Green Team self-eval (this slice)

| Dimension | /10 | Evidence |
|---|---|---|
| Product Value | 8 | Time-to-first-clip no longer requires hunting Control |
| Root-Cause Fix | 8 | Handler, source counts, slicer, load cap |
| UX | 7 | Paste URL + labels; two-client split remains |
| UI | 6 | Same dark chrome; not a design-system rewrite |
| Architecture | 7 | `qa_corpus` boundary; no new god file |
| Frontend | 7 | PWA Chat/Settings/Search; channel lift for Chat/orb |
| Backend | 8 | Start/from-url/stats/load |
| API | 8 | Explicit contracts + tests |
| Database | 6 | Honest counts; regex still unindexed |
| AI | 7 | Did not invent questions; Gemini demoted |
| Security | 5 | from-url uses same control auth |
| Performance | 7 | 400-cap vs 2000 dump; no load benchmark |
| Reliability | 5 | In-process jobs unchanged |
| Accessibility | 5 | URL field labeled; orb copy updated |
| Tests | 8 | Fresh 116 passed |
| Observability | 5 | Info logs only |
| Maintainability | 7 | Helpers are unit-testable |
| Competitive Quality | 6 | Closer to “paste a source” than before; not NotebookLM |

## TASK-001 self-eval (this slice)

Against acceptance: local japa, PWA `/ask`, scrape SSRF, ingest dedup, extractive persist, optional control token, product memory.

**10/10 against those criteria only if tests pass on a fresh command.** Runtime on a phone is IMPLEMENTATION_UNVERIFIED for overlay/Watch.
