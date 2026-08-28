# Database findings

Mongo `uttar_sewa`. Schema: `backend/db_schema.py`.

## HIGH / MEDIUM

### DB-01 — `videos.video_id` is not unique
**EVIDENCE:** INDEXES has `[("video_id", 1)]` not unique. Ingest upserts one path; concurrent insert can duplicate.  
**SEVERITY:** HIGH  
**CONFIDENCE:** CONFIRMED (schema). Race: HIGH CONFIDENCE.  

### DB-02 — No unique Q&A identity
**EVIDENCE:** `question_answers` indexes video_id/channel/language/pinned only.  
**SEVERITY:** HIGH  
**EXPECTED:** Unique `(video_id, start_time, answer)` or content hash.

### DB-03 — Ingest is delete-then-insert, no transaction
**EVIDENCE:** `processing_service._replace_video_evidence` then sequential inserts.  
**USER IMPACT:** Crash mid-ingest → empty or partial video evidence; ask refuses.  
**SEVERITY:** HIGH  
**CONFIDENCE:** CONFIRMED  

### DB-04 — `feedback` not in COLLECTIONS/INDEXES
**EVIDENCE:** `server.py:934` vs `db_schema.py:6-15`.  
**SEVERITY:** MEDIUM  

### DB-05 — `pinned_qa` insert_one, no upsert
Repeat pin → duplicate docs. Index is non-unique.  
**SEVERITY:** MEDIUM  

### DB-06 — No referential integrity
Delete video → orphan segments/Q&A. Mongo has no FKs; no cascade job.  
**SEVERITY:** MEDIUM  

### DB-07 — `embedding` field never written
**EVIDENCE:** `backend/models.py` QuestionAnswer.embedding.  
**SEVERITY:** LOW (dead schema).  

### DB-08 — `mala_days` last-write-wins
**EVIDENCE:** `replace_one` on device+day+mantra. No version.  
**SEVERITY:** MEDIUM  

### DB-09 — Secrets in `control_secrets` cleartext
See SECURITY SEC-03.

### DB-10 — `processing_status` unindexed
Queried for active jobs.  
**SEVERITY:** LOW until volume.
