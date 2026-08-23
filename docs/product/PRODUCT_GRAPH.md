# Product graph — Uttar Sewa

Nodes and invalidation. This is the real domain, not a recruiting ontology.

```
Seeker
  → asks Question
      → grounded Ask (/api/ask)
          → Evidence (Q&A row copied from transcript)
              → Citation (video_id + start_time + watch URL)
              → Answer (verbatim corpus text, or refuse)
      → Search (/api/search) — ranked list, no refuse contract
      → Companions (Gita / Wikipedia / dictionary / sandhya / books)
          → labeled public; never mixed into Answer

Seeker
  → taps Bead
      → MalaState (local applyTap / applyUndo)
          → persist prefs
          → optional /api/mala/sync
          → native overlay / Live Activity / Watch count

Video
  → captions OR Whisper audio
      → TranscriptSegment (source=captions|whisper)
      → extractive QuestionAnswer (source=transcript)
          → replaces prior segments/Q&A for that video_id

Control
  → settings, pin, ingest, scrape, BYOK keys
      → gated by optional CONTROL_TOKEN
```

## Source of truth

| Data | Source of truth | Stale if |
|---|---|---|
| Video answer | `question_answers` from extractive ingest | Re-ingest or new transcript |
| Transcript | `transcript_segments` | New captions/Whisper |
| Curated fallback | `spiritual_qa_content.py` | Only when Mongo Q&A is empty |
| Mala today | Device prefs first; `mala_days` is a sync copy | Sync fails (local still wins) |
| Public companions | Live public APIs | Network/allowlist failure → empty cards |
| API keys | User BYOK in `control_secrets` overrides `.env` | PUT keys / process env |

## Invalidation

- New transcript for `video_id` → delete prior segments + Q&A → write extractive rows → search/ask see new evidence.
- Gemini/Mistral output is **not** stored as video Q&A. Do not invalidate the corpus from an LLM paraphrase.
- Companion fetch failure does not change the video answer.
- Mala tap does not wait on `/api/mala/tap`. Sync is best-effort after the local increment.
