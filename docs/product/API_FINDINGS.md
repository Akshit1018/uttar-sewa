# API findings

## Contract contradictions

| Topic | `/api/ask` | `/api/search` |
|---|---|---|
| Refuse | Yes (`grounded_ask` threshold 0.42) | No |
| LLM | Not for the answer sentence | `enhanced_search_coordinator` can call LLM |
| Channel | Optional `channel_id` | Optional `channel_id` |
| Flutter Chat | Uses ask, **drops channel** | Uses search **with channel** |
| PWA Chat | Uses ask **with channel** | Search page separate |
| PWA orb | Ask **without channel** | n/a |

**LOG-01** HIGH CONFIRMED: same seeker question, three different result sets.

## HIGH / MEDIUM

### API-01 — Unbounded `limit`
**EVIDENCE:** `backend/models.py` SearchQuery/AskQuery — no `le=`.  
**SEVERITY:** MEDIUM  
**TEST:** Reject `limit > 50`.

### API-02 — Corpus silently truncated at 2000
**EVIDENCE:** `server.py` `_load_qa_database` `to_list(2000)`.  
**SEVERITY:** HIGH if library grows; MEDIUM now.  
**EXPECTED:** Pagination or index search, not load-all.

### API-03 — Health lies about readiness
**EVIDENCE:** `"ready": True` always; `database` can be false.  
**SEVERITY:** MEDIUM  
**CONFIDENCE:** CONFIRMED  

### API-04 — Persist failures return 200
**EVIDENCE:** `_save_control_settings`, pin, mala sync — except log, return payload.  
**SEVERITY:** HIGH  
**CONFIDENCE:** CONFIRMED  

### API-05 — `process/clear` failure is HTTP 200 `ok: false`
**EVIDENCE:** `server.py:797-813`  
**SEVERITY:** LOW  

### API-06 — No rate limiting
**EVIDENCE:** No SlowAPI/middleware. Public `/ask`, `/search`, `/enrich/*`, `/feedback`.  
**SEVERITY:** HIGH for an exposed host.  

### API-07 — No API versioning
All routes are `/api/...` v0 forever.

### API-08 — Admin reads unauthenticated
Dashboard, stats, analytics, gaps, videos, system/status — no token.  
**SEVERITY:** MEDIUM  

### API-09 — Cloud/sync/backup unauthenticated
See SECURITY SEC-01.

## Naming
`success` vs `ok` vs HTTP status mixed. Feedback uses `success`; process uses `ok`.
