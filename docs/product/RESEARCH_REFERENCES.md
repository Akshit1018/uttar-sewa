# Research references

Do not invent citations. Parallel CLI and Firecrawl were **not available** in this environment.

## YouTube chapter / clip titles

| Field | Value |
|---|---|
| Reference | Video Chapters |
| Source | https://support.google.com/youtube/answer/9884579 |
| Date inspected | 2026-08-23 |
| What it solves | How humans label a moment in a talk |
| Why relevant | Ingest “questions” were raw caption slices |
| What we learned | Timestamp first, short descriptive label, colon separators, keep titles short |
| What we reused | `M:SS — snippet` clip titles |
| What we intentionally did NOT reuse | Invented search-keyword chapter titles (would become fake questions) |
| License | Google Help (reference only) |

## Supporting write-ups (same day)

| Source | URL | Used for |
|---|---|---|
| TubeAlfred chapter format | https://tubealfred.com/blog/youtube-chapters-format/ | Confirm `timestamp + space + title`, ~50 char titles |
| Gyre 2026 chapter guide | https://gyre.pro/blog/youtube-video-chapters-how-to-add-them-why-they-increase-views | MM:SS vs H:MM:SS |

## Query-scoped retrieval

| Field | Value |
|---|---|
| Reference | Existing `rank_answers` lexical pipeline in this repo |
| Source | `backend/services/relevance_search.py` |
| Date inspected | 2026-08-23 |
| What we reused | Token rank after a smaller candidate set |
| What we intentionally did NOT reuse | Dead `enhanced_search_coordinator` / embeddings |

## Not used

- Parallel web search CLI — not installed
- Firecrawl CLI — not installed
- NotebookLM as a dependency — researched as a competitor pattern (paste source first), not copied
