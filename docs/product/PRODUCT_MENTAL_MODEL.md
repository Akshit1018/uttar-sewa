# Product mental model

## What this is trying to become

A **grounded sadhana companion**: the seeker asks a question that already lives in long satsang videos, gets the **same words** the video said, jumps to that second, and can count a mala in the same hand.

Stated in `docs/product/PRODUCT_VISION.md` and enforced in `grounded_ask.py` (answer ⊆ corpus or refuse).

## Who it is for

1. **Seeker** — already watches a specific Hindi (or bilingual) discourse channel. Job: “where did Guruji say this?”  
2. **Operator** (often the same person) — pastes keys, starts ingest, sets `CONTROL_TOKEN`. Job: “fill the corpus.”

It is **not** for: people who want a general spiritual chatbot, a social japa league, or a hosted Notebook.

## Primary job-to-be-done

**Find the moment in a talk, then return to japa.**

Secondary jobs the architecture also tries to serve: daily Gita verse, Wikipedia companions, operator scrape, Firestore backup.

## Expected aha

A refuse-or-cite answer with a working `watch?v=&t=` link, followed by a bead tap that does not need the network.

That aha **cannot happen** until: API reachable from the device + at least one ingested (or seeded) Q&A row that matches the question.

## Recurring value

- Ask again tomorrow (same corpus).  
- Count mala daily (local).  

Value compounds **only** if the corpus is *their* talks. The seed library is generic spiritual Q&A. After 30 days of using only the seed, the product is a 30-item FAQ + a counter.

## Where time should be spent

Most minutes: **orb + chat**.  
Operator time: ingest once, then rarely.

The Flutter bottom nav puts **Control** next to Chat. The PWA puts Admin/Processing behind More. Architecture says the operator is a first-class user of the mobile app.

## Intended moat

1. Extractive refuse (NotebookLM will still *talk*).  
2. Channel-scale ingest (NotebookLM wants URLs/playlists one at a time).  
3. Japa in the same surface (NotebookLM has none; mala apps have no satsang cite).

None of these are moats if first-run is dead or the corpus is 30 curated rows.

## What the architecture wanted

A single FastAPI + Mongo “uttar_sewa” with Flutter as the real client and the PWA as a leftover CRA app. BYOK and control dashboard are operator tooling bolted onto the seeker app. Public enrichment was added as corrective-RAG *beside* the answer, not inside it.

Dead `ultra_*` / `enhanced_search_*` / Gemini extract modules show an earlier ambition: **AI search engine over 900+ videos**. The current contract walked that back to lexical extractive copy. The files were not deleted.

## Where implementation drifted

| Intent | Drift |
|---|---|
| One product | Two clients with different save models, companions, BYOK, mala sync |
| Guru’s corpus | Seed library + 80-character caption “questions” |
| Seeker-first | Control/Admin/Processing in primary nav |
| Grounded AI | Dead LLM stack still configured by BYOK as if it mattered for ask |
| Daily sadhana | PWA mala never syncs; no reminders (rejected leaderboards, but also skipped calm reminders) |
| Phone-first | Default API loopback; PWA API not editable |

## Glued-on parts

- Firestore cloud backup with no UI  
- Admin analytics that only export `console.log` events  
- Public scrape box on Flutter Control  
- Profile / Terms / sample-data alerts on PWA  
- Live Activity / Watch stubs that cannot be proven here  

These do not serve the aha. They increase the surface an attacker or a confused seeker can hit.

## Attack the model (inconsistencies)

If the job is “cite the talk,” then:

- Search without refuse is a second, weaker product.  
- Caption-`[:80]` “questions” are not questions. Retrieval quality is an accident of substring overlap.  
- `to_list(2000)` means the product silently drops evidence at modest library size.  
- A seeker who never opens Control will never ingest. Activation depends on an operator persona the first-time user is not.

If the job is “count a mala,” then Mantrum/JapGuru already do it with haptics, reminders, and offline as the default story. Our orb is a counter plus a hold-to-ask gesture. That gesture is the only reason japa belongs in this repo.

**KEEP** the join (cite + bead).  
**HIDE** operator surfaces from the seeker nav.  
**REMOVE or quarantine** dead ultra/LLM search.  
**SIMPLIFY** two clients or accept PWA as kiosk-only.
