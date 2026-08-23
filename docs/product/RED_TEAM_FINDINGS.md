# Red-team findings (master)

**Date:** 2026-08-23  
**Product:** Uttar Sewa — spiritual Q&A + japa. Not recruiting.  
**Method:** Code inspection + cited web research. Flutter/PWA **not** executed on a device.  
**If I wanted this product to fail first:** ship the Flutter binary as-is (talks to `127.0.0.1`) **or** expose the API without `CONTROL_TOKEN` and `POST /api/cloud/restore` / `PUT /api/control/keys`.

Related files: `RED_TEAM_SCORECARD.md`, `PRODUCT_FLAWS.md`, `UX_FAILURES.md`, `LOGIC_FAILURES.md`, `FRONTEND_FINDINGS.md`, `BACKEND_FINDINGS.md`, `DATABASE_FINDINGS.md`, `API_FINDINGS.md`, `ARCHITECTURE_FINDINGS.md`, `AI_FINDINGS.md`, `SECURITY_FINDINGS.md`, `COMPETITOR_GAPS.md`, `MISSING_FEATURES.md`, `BAD_FEATURES.md`, `UNVERIFIED_ASSUMPTIONS.md`.

## Executive verdict

| Dimension | /10 |
|---|---|
| PRODUCT QUALITY | 4 |
| USER EXPERIENCE | 3 |
| UI QUALITY | 4 |
| PRODUCT LOGIC | 4 |
| FRONTEND | 4 |
| BACKEND | 5 |
| DATABASE | 3 |
| API DESIGN | 3 |
| ARCHITECTURE | 3 |
| AI QUALITY | 5 |
| SECURITY | 2 |
| PERFORMANCE | 4 |
| RELIABILITY | 3 |
| MARKET COMPETITIVENESS | 3 |
| PRODUCTION READINESS | 2 |

## Top 10 reasons this product could fail

1. **Does not work on a phone or a default PWA** (`127.0.0.1`, `undefined/api`).  
2. **Open admin surface** — keys, ingest, cloud restore — when token unset or restore ungated.  
3. **Empty / fake corpus vs “900+ AI answers”** — first question dies; trust dies.  
4. **NotebookLM + a mala app already cover the two jobs** with less setup.  
5. **Chat / Search / orb disagree** (refuse, channel, LLM, cache).  
6. **Ingest delete-then-insert** — one crash empties a video’s evidence.  
7. **Mala is a weaker, split implementation** vs Mantrum/JapGuru (no reminders, no off-toggle, PWA unsynced).  
8. **No unique indexes / last-write mala / silent 200s** — data you cannot trust.  
9. **Accessibility: no Flutter Semantics; icon-only PWA actions.**  
10. **Analytics is `console.log`** — cannot tell if anyone got a cited answer.

## CRITICAL

| ID | Title | Confidence |
|---|---|---|
| UX-01 | Flutter default API loopback | CONFIRMED |
| UX-02 | PWA `undefined/api` | CONFIRMED |
| SEC-01 | Unauthenticated cloud restore/backup | CONFIRMED (code); live Firestore NV |
| SEC-02 | Demo-open writes without CONTROL_TOKEN | CONFIRMED |

## HIGH (selected)

UX-03 onboarding, UX-04 empty Chat, UX-05 900+/AI copy, UX-06 fake toggles, UX-07 clear data, UX-08 channel split, UX-10 Live/Watch no off, UX-14 pin≠heart, UX-15 Semantics, SEC-03 cleartext keys, SEC-04 CORS, SEC-05 regex, SEC-06 feedback blob, API-02 2000 cap, API-04 silent persist, API-06 no rate limit, DB-01/02/03 indexes+ingest, AI-01 search LLM, AI-02 no evals, AI-03 80-char questions, AI-08 marketing, FE-22 offline cache, BE-03 RAM corpus.

Full lists in satellite files.

## User pain map

| User | Journey | Pain | Cause | Sev | Alternative |
|---|---|---|---|---|---|
| First-time seeker | Install Flutter | Dead app | 127.0.0.1 | CRITICAL | YouTube search |
| First-time seeker | Open PWA | Dead fetches | empty env | CRITICAL | NotebookLM |
| First-time seeker | Chat | No answers, no why | Empty corpus, no CTA | HIGH | YouTube chapters |
| Returning seeker | Ask vs search | Different answers | Split contracts | HIGH | One YouTube tab |
| Seeker | Save clip | Lost on other client | pin vs heart | HIGH | Browser bookmarks |
| Seeker | Japa | Overlay/Watch stuck/silent | start-only APIs | HIGH | Mantrum / JapGuru |
| Operator | Settings PWA | Cannot lock API | no token UI | HIGH | SSH + curl |
| Operator | Ingest | Duplicates / hole | no unique + no txn | HIGH | Manual captions |
| Attacker | Internet API | Steal/replace keys, wipe DB | open routes | CRITICAL | n/a |
| Screen-reader user | Any Flutter tab | Unlabeled controls | no Semantics | HIGH | Physical mala |

## Architecture failure map

Phone/PWA misconfig → no API. API up, Mongo down → curated 30 pairs presented as product. API up, Mongo up, 2001st Q&A → invisible. Ingest crash → empty video. Search LLM on → invented rank. Restore POST → corpus gone. Two malas → last write wins.

## What to fix first (do not implement in this audit)

**P0:** Phone/PWA API bootstrap; fail-closed admin (token + cloud routes); empty-corpus Chat honesty; kill fake 900+/AI copy; unique indexes + atomic ingest; confirm destructive clear.  
**P1:** Unify ask contract + channel; disable search LLM; offline honesty; pin/favorite model; Semantics + icon labels; Live/Watch off; regex/rate limit/CORS; eval fixtures; persist 503.  
**P2:** Reminders (not leaderboards); haptics; real analytics; PWA BYOK or remove Admin; delete dead ultra_* ; semantic search after evals.  
**P3:** Desktop polish, scrape placeholder, conversation export.

## Repair status (2026-08-23 green pass)

| Finding | Status |
|---|---|
| UX-01 Flutter loopback | RESOLVED — editable persisted API URL + always-visible error |
| UX-02 PWA `undefined/api` | RESOLVED — origin fallback; `.env.example` set |
| SEC-01 cloud restore/backup | RESOLVED — fail-closed even if token unset |
| SEC-02 demo-open writes | PARTIALLY RESOLVED — control writes still demo-open; cloud locked |
| UX-04 empty Chat | RESOLVED — PWA + Flutter banners |
| UX-05 900+/AI copy | RESOLVED — About + translations rewritten |
| UX-06 fake toggles | RESOLVED — removed |
| UX-07 clear confirm | RESOLVED — Settings + Favorites |
| UX-08 channel split | RESOLVED — Flutter ask + PWA orb send `channel_id` |
| UX-09 hold orb focus | RESOLVED — switches to Chat and focuses field |
| UX-10 Live/Watch off | RESOLVED — stop methods + toggle labels |
| UX-12 Flutter empty search | RESOLVED |
| UX-13 orb network as refuse | RESOLVED — networkError copy |
| UX-15 Semantics | PARTIALLY RESOLVED — orb + nav |
| SEC-04 CORS | RESOLVED — localhost list; `*` only if listed, no credentials |
| SEC-05 regex | RESOLVED — `escape_regex` |
| SEC-06 feedback blob | RESOLVED — 4000 char cap |
| API-02 limit cap | RESOLVED — clamp 1–50 |
| DB-01/02/03 indexes+ingest | RESOLVED — unique indexes + upsert-then-drop |
| AI-01 search LLM | RESOLVED — lexical only |
| FE-22 offline cache as ask | RESOLVED — offline throws |
| LOG-08 health ready | RESOLVED — `ready == database` |
| UX-14 pin≠heart | OPEN — pin upserts; hearts still local |
| SEC-03 cleartext keys | OPEN |
| API-06 rate limit | OPEN |

## Prior backlog status (do not delete)

| Earlier item | This audit |
|---|---|
| Local Flutter japa | PARTIALLY RESOLVED — still no day-rollover proof, PWA unsynced, undo≠native |
| PWA `/ask` | PARTIALLY RESOLVED — Chat uses ask; Search/LLM/offline cache still broken |
| Scrape no-redirect | PARTIALLY RESOLVED — httpx only; Scrapling NV |
| Extractive ingest | RESOLVED for persist path; Gemini leftover in tree |
| CONTROL_TOKEN | PARTIALLY RESOLVED — optional; cloud/feedback still open |

## Audit self-critique

- **Tested vs speculated:** Code CONFIRMED. UI/runtime UNVERIFIED. Market cited, apps not installed.  
- **Over-focused on code?** Also scored activation and competitors.  
- **Manufactured issues?** Fake toggles, loopback, restore, 900+ copy are not invented.  
- **Missed because it looked polished?** Dark PWA chrome hides empty corpus and fake settings.  
- **Another pass:** Did not run axe/Lighthouse; did not fuzz `/ask` with 10k unicode; did not prove Scrapling SSRF.
