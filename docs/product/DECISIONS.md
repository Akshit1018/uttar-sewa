# Decision log

## D1 — Extractive corpus, not Gemini Q&A

**Decision:** Persist `segments_to_qa` as the grounded video corpus. Do not write Gemini paraphrases into `question_answers`.

**Alternatives:** LLM extract then cite; hybrid store both.

**Why:** The product contract is “no invented teaching.” LLM extractive Q&A can paraphrase or invent. Grounded `/api/ask` already copies corpus text verbatim. Garbage in the corpus becomes a “cited” hallucination.

**Tradeoffs:** Questions are often the first 80 characters of the segment, not a polished seeker question. Search quality depends on lexical overlap.

**Reversal:** Only if an evaluation set shows LLM Q&A is strictly extractive (answer ⊆ transcript) and users cannot distinguish invented claims.

## D2 — Local-first japa

**Decision:** Flutter `applyTap` / `applyUndo` run on device. Persist + sync after. Do not call `/api/mala/tap` after a local increment (that would double-count if both ran).

**Why:** A mala that requires the API is not a mala. Offline sadhana is the core loop.

**Tradeoffs:** Server `/mala/tap` still exists for other clients; two clients on one device_id can diverge until sync.

**Reversal:** If a shared household counter becomes a real requirement, introduce a single sync-authoritative device.

## D3 — PWA chat uses `/ask`

**Decision:** Main PWA chat posts `/api/ask`, same contract as Flutter and the orb.

**Why:** `/search` never refuses. Seekers were shown ranked hits as if they were answers.

**Tradeoffs:** Search tab (Flutter) still uses `/search` for browse. That is intentional.

## D4 — Optional CONTROL_TOKEN

**Decision:** If `CONTROL_TOKEN` is unset, write routes stay demo-open. If set, require `X-Control-Token` on keys, ingest, process, pin, scrape, settings writes.

**Why:** Unauthenticated `PUT /control/keys` stores secrets. A required always-on auth system would break local demo and tests.

**Tradeoffs:** Demo deployments without the env var remain open. Keys are still cleartext in Mongo.

**Reversal:** When a real multi-user auth exists, replace this header with session/role checks.

## D5 — Scrape does not follow redirects

**Decision:** `PublicHttp` uses `follow_redirects=False` after the allowlist check.

**Why:** Allowlist-then-follow is a classic SSRF. A 302 to `169.254.169.254` bypasses host checks.

**Tradeoffs:** Some public pages that 301 to `www.` will fail. Prefer official APIs.

## D6 — Do not rewrite into recruiting software

**Decision:** Ignore generic “candidate profile / resume / interview” templates. This repository is Uttar Sewa.

**Why:** Filenames and prior agent briefs must not redefine the product.
