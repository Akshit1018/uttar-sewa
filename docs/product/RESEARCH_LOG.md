# Research log

Research performed for this run. Dates relative to 2026-08-23.

## Grounded answers

- [Grounded RAG pattern](https://aiarch.dev/patterns/grounded-rag): refuse when evidence is thin; citations are a contract, not decoration.
- [Edtek 2026 — hallucination-proof RAG](https://edtek.ai/kb/hallucination-proof-rag-architecture/): generation must be constrained to retrieved spans.
- [grounded-rag-spec](https://github.com/jonathan-kellerai/grounded-rag-spec): structured refuse + provenance.

**ADOPT:** keep extractive `/api/ask` (answer ⊆ corpus). Do not persist LLM paraphrases as video evidence.

## SSRF

- [Trail of Bits FastAPI SSRF notes](https://github.com/trailofbits/skills-curated/blob/main/plugins/openai-security-best-practices/skills/openai-security-best-practices/references/python-fastapi-web-server-security.md): revalidate every hop or disable redirects.
- [ApiPosture FastAPI SSRF](https://www.apiposture.com/remediation/fastapi/how-to-fix-ssrf-in-fastapi-cve-2024-42816/): `follow_redirects=False`.

**ADOPT:** `PublicHttp` no longer follows redirects.

## BYOK UX

- Open WebUI Connections and LibreChat `user_provided`: user keys override env; UI never echoes the full secret after save.
- Pleo-style masking after save.

**ADOPT (already shipped):** mask on GET; empty PUT does not wipe; `__clear__` removes.  
**BACKLOG:** encrypt `control_secrets` at rest.

## 2026-08-23 red-team market pass

`parallel-cli` was **not installed**. Used web search.

- [NotebookLM / Gemini Notebook](https://notebooklm.google/) + [Tom’s Guide 27 Jun 2026](https://www.tomsguide.com/ai/i-turned-youtube-into-an-ai-bootcamp-with-notebooklm-heres-my-workflow): YouTube URL → transcript Q&A + citations. **ADOPT later:** time-to-value (paste URL). **REJECT:** unconstrained generation as our answer contract.
- Mala: [Mantrum](https://mantrum.app/), [JapGuru](https://play.google.com/store/apps/details?hl=en_US&id=com.mantra.japguru) (Feb 2026 update), [Naam Jap](https://karmalive.org/mantra-jap-counter-app), [Japa Counter](https://apps.apple.com/in/app/japa-counter-mantra-tracker/id6757606346). **ADOPT:** reminders + offline-first. **REJECT:** leaderboards (product rule).
- [GitaGPT + Chroma](https://github.com/aprameyak/GitaGPT): semantic RAG on a closed text. **BACKLOG:** embeddings after evals, not as a rewrite.

## Job-search / recruiting templates

**REJECT:** This repository is a spiritual Q&A + mala product. Candidate-profile graphs do not apply.

## Sadhana apps

Common mala apps count locally and sync later. Network-first tap is a frequent complaint (lost beads).

**ADOPT:** Flutter local `applyTap` / `applyUndo`.
