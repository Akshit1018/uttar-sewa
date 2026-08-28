# Forensic critic passes

## Second pass — “the last team was incompetent”

Unique findings the prior red-team file set under-weighted or missed after the repair commit:

| ID | Finding | Why it was missed | Confidence |
|---|---|---|---|
| F-NEW-01 | `POST /process/start` **ignores** PWA `{channel_url}` | Repair pass fixed copy/cloud, not this contract | **PROVEN** |
| F-NEW-02 | Seed library hides the empty-corpus banner (`total_qa_pairs` ≥ 30) | Banner checks count, not `source=curated` | **PROVEN** |
| F-NEW-03 | `segments_to_qa` questions are `text[:80]` | Treated as “extractive Q&A” without reading the slicer | **PROVEN** |
| F-NEW-04 | `_load_qa_database` hard-cap 2000 | Listed as API-02 before; still present after “resolve all” | **PROVEN** |
| F-NEW-05 | Two `useChannels()` instances (App + Chat) | Channel on orb vs Chat looked “fixed” | **STRONG** |
| F-NEW-06 | Flutter `/mala/tap` client methods unused | Local-first fix hid the dead API | **PROVEN** |
| F-NEW-07 | BYOK configures models that ask/search never call | Keys UI shipped; contract not re-read | **PROVEN** |
| F-NEW-08 | README “daily counts synced” is false for PWA | Docs lag | **PROVEN** |
| F-NEW-09 | Android volume keys always consumed in `MainActivity` | Native “feature” not walked as a11y | **PROVEN** |
| F-NEW-10 | `include_companions` on `/ask` unused by PWA | Flutter has a side call; looked done | **PROVEN** |
| F-NEW-11 | Unique index creation swallows errors and creates non-unique | `database.py` except | **STRONG** |
| F-NEW-12 | In-process ingest dies with the worker | No queue — not in P0 list as “job reliability” | **STRONG** |
| F-NEW-13 | `test_result.md` / FEATURE_BRAINSTORM still claim 900+ / ultra search | Docs not in repair scope | **PROVEN** |
| F-NEW-14 | ChatInterface still imports offline cache helpers it does not use | Partial repair | **PROVEN** |

None of these require praising the repair pass. They are leftover trunks (C2, C3, C5).

## Third pass — “the audit exaggerated”

| Claim to downgrade | Why |
|---|---|
| “The product does not work at all” | Japa works offline. Ask works against seed/curated. API tests pass (102). Overstatement if we ignore the mala half. |
| “Cloud restore will wipe production tomorrow” | Fail-closed without token; no UI; Firestore often unconfigured. **SUSPECTED** risk, not a live incident. |
| “Live Activity is a lie” | Code paths exist; we did not run a device. Class is PARTIAL/UNVERIFIED, not BROKEN. |
| “Must build user accounts” | Single-operator product. Accounts are not MUST HAVE until a second seeker exists. |
| “Must add vector search now” | Extractive lexical + refuse is a coherent v1. Vector without evals repeats the ultra-search mistake. |
| “PWA is useless” | Chat `/ask`, voice, favorites, drag orb, SW — real for browser users on the same origin. |
| “Security 2/10 still” | Cloud is locked; CORS tightened; regex escaped. Demo-open **control** writes remain. Score should move to ~3–4 for a LAN demo, not “production.” |
| “NotebookLM makes this pointless” | True for *setup speed*. False for *refuse + mala + channel ingest* if those three work. |

## Agent disagreement (not forced consensus)

| Agent | Position | Evidence |
|---|---|---|
| UX | Hide Control from the seeker nav immediately | Zero-patience + chaotic personas |
| Operator / power | Keep Control one tap away; ingest is the product | Channel-scale job |
| Product | Lock Control behind token + 5-tap or Settings | Both are right; nav is the bug, not the feature |
| AI | Delete Gemini BYOK until ingest uses it | Skeptical persona + unused call sites |
| Ingest engineer | Keep BYOK YouTube key; drop Gemini/Mistral fields | YouTube key is used; others are theater |
| Mala traditionalist | Never add streaks | Vision file |
| Growth | Add streaks or die | Rejected by product rule — do not “resolve” this with a league |

**Resolution used:** hide operator chrome; keep YouTube key; do not add leaderboards; do not add vectors before evals.

## 5-minute test (simulated)

| Question | Answer |
|---|---|
| Understand the value? | Only if they tap a suggestion and get a clip. Default Hindi + API error → no. |
| Achieve anything useful? | Bead tap: yes. Cited guru talk: usually no. |
| Friction? | API URL, Control, curated vs real. |
| Trust? | Down if the answer is generic seed. Up if refuse is honest. |
| Return? | Mala users might. Ask users will open YouTube. |

## 30-day test (simulated)

| Question | Answer |
|---|---|
| More useful? | Only if ingest happened and the 2000 cap is not hit. |
| Remember context? | No server threads. Local history on PWA only. |
| Less repeated work? | Pins/hearts do not cross clients. |
| Accumulated data? | `mala_days` and `question_answers` can accumulate; no seeker-facing history of malas. |
| Lock-in? | Inconvenience (two apps), not value, unless the corpus is unique. |

## Delete-the-docs test

Without README: Flutter still requires knowing that Settings holds the LAN API. PWA custom channel looks real. Hold-2.5s is not discoverable except tiny orb aria text. **Core ask+japa is not self-explanatory.**

## Industry-standard gaps (EXPECTED vs ACTUAL)

| Subsystem | Expected | Actual | Consequence |
|---|---|---|---|
| Auth | Fail-closed writes on a network | Demo-open control; fail-closed cloud | LAN demo is a key dump |
| Search | Retrieve then optional generate | RAM scan 2000 rows | Scale cliff |
| Onboarding | Empty state with one CTA | Banner or curated lie | Activation fail |
| Jobs | Queue + retry | `create_task` | Lost ingest |
| RAG | Chunk + cite + eval | Caption slice + lexical | Weak questions |
| Observability | Cited-answer rate | console.log | Cannot operate |
| A11y | Labeled controls | Partial | TalkBack **UNVERIFIED** |
| Mobile | Hosted or first-run URL | Loopback default | Dead install |

## Skill / tool discipline

See [SKILL_TOOL_LOG.md](SKILL_TOOL_LOG.md). This pass did not pretend Parallel or Firecrawl ran.
