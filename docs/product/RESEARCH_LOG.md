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

## Job-search / recruiting templates

**REJECT:** This repository is a spiritual Q&A + mala product. Candidate-profile graphs do not apply.

## Sadhana apps

Common mala apps count locally and sync later. Network-first tap is a frequent complaint (lost beads).

**ADOPT:** Flutter local `applyTap` / `applyUndo`.
