# Security findings

Audit trail. New inspection 2026-08-23. Earlier notes in `SECURITY_MODEL.md` remain valid.

## CRITICAL

### SEC-01 — Unauthenticated cloud restore can overwrite the corpus
**AREA:** Security / API  
**WHAT IS WRONG:** `POST /api/cloud/restore` and `POST /api/cloud/backup` have no `require_control`. Anyone who can reach the API can restore Firestore over Mongo when cloud is enabled.  
**EVIDENCE:** `backend/server.py:945-997` — no `Depends(require_control)`.  
**USER IMPACT:** Corpus and Q&A replaced or wiped.  
**REAL-WORLD SCENARIO:** Operator enables Firestore; a stranger POSTs restore.  
**ROOT CAUSE:** Cloud routes added without the later CONTROL_TOKEN gate.  
**SEVERITY:** CRITICAL (if Firestore configured); otherwise HIGH (open destructive API).  
**CONFIDENCE:** CONFIRMED (code). Live Firestore: NEEDS VERIFICATION.  
**EXPECTED BEHAVIOR:** Same token (or better, real auth) as keys/ingest. Disable restore without confirmation + backup.  
**AFFECTED LAYERS:** API, Backend, Database, Infrastructure  
**REPRODUCTION:** `curl -X POST $API/cloud/restore`  
**TEST THAT SHOULD EXIST:** 401 when `CONTROL_TOKEN` set and header missing; also fail closed when token unset in a “production” flag.

### SEC-02 — Write/admin routes are demo-open when CONTROL_TOKEN is unset
**AREA:** Security  
**WHAT IS WRONG:** `authorize_control` returns True if env empty. `PUT /control/keys` stores secrets.  
**EVIDENCE:** `backend/services/control_auth.py:19-23`; `.env.example` documents this.  
**USER IMPACT:** Internet-exposed demo = anyone pastes their keys into your Mongo, or replaces yours.  
**SEVERITY:** CRITICAL (exposed deploy) / MEDIUM (localhost-only).  
**CONFIDENCE:** CONFIRMED  
**EXPECTED BEHAVIOR:** Production profile requires token or refuses to boot writes.  
**TEST:** Production-mode 401 without token.

## HIGH

### SEC-03 — BYOK secrets stored cleartext in Mongo
**EVIDENCE:** `backend/services/byok.py` `secrets_document`; `control_secrets` collection. GET masks; disk does not.  
**SEVERITY:** HIGH  
**CONFIDENCE:** CONFIRMED  
**EXPECTED:** Secret manager or envelope encryption.

### SEC-04 — CORS `allow_origins=["*"]` + `allow_credentials=True`
**EVIDENCE:** `backend/server.py:1151-1157`  
**SEVERITY:** HIGH  
**CONFIDENCE:** CONFIRMED  
**EXPECTED:** Explicit origins; never `*` with credentials.

### SEC-05 — `$regex` unsanitized on search suggestions
**EVIDENCE:** `backend/server.py:894-897`  
**SEVERITY:** HIGH (ReDoS / injection)  
**CONFIDENCE:** CONFIRMED  
**REPRODUCTION:** `GET /api/search/suggestions?query=(a+)+`  
**TEST:** Escape or literal substring match.

### SEC-06 — Unauthenticated feedback accepts arbitrary dict
**EVIDENCE:** `backend/server.py:919-934` — no size cap.  
**SEVERITY:** HIGH (storage abuse)  
**CONFIDENCE:** CONFIRMED  

## MEDIUM

### SEC-07 — Mala `device_id` IDOR
**EVIDENCE:** `GET /mala/day`, `POST /mala/sync` — client-chosen id.  
**SEVERITY:** MEDIUM  
**CONFIDENCE:** CONFIRMED  

### SEC-08 — Conversation history steers lexical rank
**EVIDENCE:** `relevance_search.expand_query` concatenates history.  
**SEVERITY:** MEDIUM  
**CONFIDENCE:** HIGH  

### SEC-09 — Scrapling scrape path not proven redirect-safe
**EVIDENCE:** `public_enrichment.py` Scrapling branch vs httpx `follow_redirects=False`.  
**SEVERITY:** MEDIUM  
**CONFIDENCE:** POSSIBLE  

### SEC-10 — Health leaks `keys_configured`
**EVIDENCE:** `GET /api/health`  
**SEVERITY:** LOW  
**CONFIDENCE:** CONFIRMED  

## Previously noted, still true
Cleartext env copy of keys; no user auth; no rate limit; no CSRF story beyond CORS.
