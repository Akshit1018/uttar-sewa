# Hostile persona swarm

Each persona walks Ask, Search, Japa, Ingest, Settings.  
Hesitation / confusion / failure / missing / extra step / trust.  
Confidence: **STRONG** from code; device behavior **UNVERIFIED**.

## ZERO-PATIENCE (10–30s)

- Flutter: black app, API error banner, Hindi default. No satsang clip in 30s. **Failure.**  
- PWA: Chat welcome + suggestions. If seed exists, a tap may return a curated row that is not their guru. **Trust drop.**  
- Japa orb works immediately — they may think the product *is* a counter and leave.  
- Missing: paste-URL aha.

## NON-TECHNICAL

- “API URL”, “CONTROL_TOKEN”, “BYOK”, “ingest”, “corpus”, “database offline mode”.  
- PWA Settings shows a raw `http://…/api` string.  
- Processing “custom channel” looks like Hindi/English help and **does nothing**.  
- Confusion: Chat vs Search vs Admin vs Control.

## POWER USER

- No `/` to focus ask, no `j` for bead, no saved views, no bulk pin, no URL state for search.  
- Two ask surfaces (page + sheet) with slightly different error copy.  
- Flutter `api.tap` unused — they curl `/mala/tap` and wonder why the orb disagrees.  
- Ceiling: they stay as fast as a beginner.

## MOBILE-ONLY

- Flutter default `127.0.0.1` is the phone. **Failure** until Settings.  
- PWA cannot edit API host.  
- Flutter: no voice. PWA: voice **UNVERIFIED** on iOS.  
- Hold 2.5s is long on a moving bus; accidental taps increment beads.  
- Overlay / Live / Watch: labels exist; **UNVERIFIED** they work.

## SKEPTICAL (does not trust AI)

- Extractive refuse is aligned — **this persona can stay** if the UI keeps saying “copied from the talk.”  
- Confidence `%` on clips (PWA) looks like model certainty; it is a lexical score. **Trust issue.**  
- BYOK Gemini field implies Gemini answers questions. It does not. **Misleading.**  
- Curated fallback without a loud “not your channel” label. **Trust issue.**

## CHAOTIC

- Clears data without wanting to — now confirmed, good.  
- Switches language; suggestions mix Hindi defaults + API.  
- Changes channel mid-chat; orb uses `preferredChannel` independently of Chat’s hook instance (two `useChannels()` in App + Chat — **same localStorage key**, last write wins).  
- Double-taps Flutter orb: no undo (PWA would undo). **Failure.**

## LARGE-DATA (2000+ Q&A)

- `_load_qa_database` `to_list(2000)` — later talks vanish. **PROVEN** in code.  
- Ingest in-process can run a long time; restart orphans `processing_status`.  
- Admin top-videos aggregate has no pagination.  
- Search limit clamped to 50; still no cursor.

## RETURNING (weeks later)

- PWA: favorites and mala still on that browser profile. New phone: empty.  
- Flutter mala: day rollover resets local counts (**REAL**). Server `mala_days` may still have old days — no history UI.  
- Recommendations: last 6 local history strings. Empty history → generic sample.  
- Control token forgotten → 401 on ingest with no recovery copy beyond SnackBar.

## ACCESSIBILITY

- Flutter: one Semantics on the orb; form fields unlabeled beyond hints.  
- PWA: better aria on nav/chat; result cards still icon-only share/heart in places.  
- 2.5s hold is hostile for motor impairment.  
- Volume-key capture (Android) breaks accessibility volume.

## BAD-NETWORK

- Japa still works (both). **This is the one journey that holds.**  
- Flutter ask: SnackBar. PWA Chat: honest offline sentence. Search: may show stale cache (looks live).  
- Ingest: no resume.  
- Companions: extra HTTP; Flutter ask “succeeds” then companions silently empty.

## Cross-persona ticket cluster (predicted support)

1. “Nothing loads on my phone.” (loopback / PWA host)  
2. “Answers are not from my Guruji.” (seed / 80-char captions / 2000 cap)  
3. “I set the channel URL and it processed the old one.” (ignored body)  
4. “My mala on the website is not on the app.” (no PWA sync)  
5. “I saved a clip and it vanished on the other device.” (heart vs pin)  
6. “I turned on Gemini and answers did not change.” (BYOK unused by ask)  
7. “Search found something Chat refused.” (split contract)  
8. “Live Activity does nothing.” (stub / permission)  
9. “Volume buttons stopped working.” (Android hijack)  
10. “I cannot turn off the overlay.” (permission / plugin miss — overlay *can* toggle in Dart)

Repeated tickets 1–5 are **design** failures, not missing FAQs.
