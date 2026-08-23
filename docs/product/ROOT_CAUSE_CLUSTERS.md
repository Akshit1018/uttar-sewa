# Root-cause clusters

Do not file forty tickets. Fix these trunks.

## C1 — Two products, one binary

**Defect:** Flutter and PWA implement different contracts for save, mala, companions, BYOK, API setup.  
**Causes:** pin≠heart, mala unsynced, companions missing on PWA, API URL not editable on PWA, voice-only-PWA, Control-vs-Admin.  
**User:** “It worked on the website.”  
**Business:** support load, no single funnel.  
**Fix direction:** pick a primary client; make the other a subset with a written matrix.

## C2 — Activation requires an operator

**Defect:** The aha (cited clip) is behind ingest + reachable API.  
**Causes:** loopback default; PWA host; `/process/start` ignores `channel_url`; no paste-URL path; seed library masquerades as success.  
**User:** 30-second bounce or false “it works” on curated rows.  
**Business:** NotebookLM wins time-to-value.  
**Fix direction:** paste URL → extractive clips; first-run wizard; honor channel body.

## C3 — Evidence model is caption slices in RAM

**Defect:** `_load_qa_database` pulls 2000 docs; “questions” are `text[:80]`; retrieve is lexical.  
**Causes:** weak ask, search≠ask, 2001st row invisible, confidence % theater, recommendations recycle slices.  
**User:** “That’s not what I asked” / missing later videos.  
**Business:** cannot scale a real channel.  
**Fix direction:** retrieve from `transcript_segments` with timestamps; cap in the database (indexes already exist); hybrid later.

## C4 — Operator surface mixed into seeker surface

**Defect:** Control/Admin/Processing/BYOK/scrape live in the same nav as Chat.  
**Causes:** accidental key paste, accidental process start, cognitive load, demo-open writes.  
**User:** fear and mis-taps.  
**Business:** looks unfinished / dangerous.  
**Fix direction:** hide operator behind a lock; fail-closed when networked.

## C5 — Dead sophistication

**Defect:** ultra search, Gemini extract, unused embeddings, unused `/mala/tap`, unused `BackgroundTasks`, UI-less cloud, `console.log` analytics.  
**Causes:** maintenance cost, BYOK implying Gemini answers, engineer distrust.  
**User:** settings that do not change ask.  
**Business:** “AI theater.”  
**Fix direction:** delete or quarantine; stop selling unused models.

## C6 — Native / japa half is a counter, not a practice app

**Defect:** No reminders; Flutter orb undo missing; overlay/Live/Watch unproven; volume hijack.  
**Causes:** mala apps outcompete the daily habit.  
**User:** uses Mantrum for japa, NotebookLM for talks.  
**Business:** join never happens.  
**Fix direction:** reminder + haptic + consistent undo; prove overlay or remove the buttons.

## Negative graph

```
C2 Activation / operator-only ingest
    → empty or curated first answer
    → seeker distrusts “from the discourses”
    → no daily ask habit
    → mala apps win the daily slot
    → product is unused

C3 RAM bag + 80-char questions
    → refuse/search disagreement
    → support: “Chat said no, Search said yes”
    → operator adds more videos that never enter the 2000 window
    → more distrust

C1 Dual clients
    → lost pins / lost mala
    → “your app deleted my sadhana”
    → uninstall
```

## We have this — why? (KEEP / SIMPLIFY / MERGE / HIDE / REMOVE)

| Feature | Verdict | Why |
|---|---|---|
| Extractive `/ask` | KEEP | Only defensible answer contract |
| Timestamp button | KEEP | Job-to-be-done |
| Local mala math | KEEP | Offline beads |
| Public companions | KEEP but HIDE default | Labeled; easy to confuse |
| Flutter Control | HIDE | Operator only |
| PWA Admin analytics | REMOVE or replace | Mocked |
| ultra_* modules | REMOVE | Dead |
| Cloud restore API | HIDE + document | Nuclear |
| Search without refuse | SIMPLIFY | Same contract as ask or label “clips only” |
| Live/Watch buttons | SIMPLIFY | Hide until device-proven |
| Seed library | REDESIGN | Label “demo teachings, not your channel” |
