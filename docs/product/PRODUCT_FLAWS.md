# Product flaws

Identity: a seeker wants (1) timestamped answers from a guru’s videos and (2) a mala that works in the hand.

## Positioning failure

The product is **weaker than the pair of alternatives people already use**:

- Q&A on a YouTube corpus: [Gemini Notebook / NotebookLM](https://notebooklm.google/) imports a YouTube URL, answers from the transcript, and shows citations ([Tom’s Guide, 27 Jun 2026](https://www.tomsguide.com/ai/i-turned-youtube-into-an-ai-bootcamp-with-notebooklm-heres-my-workflow); [XDA](https://www.xda-developers.com/i-dont-watch-youtube-videos-anymore-i-consume-them-using-notebooklm/)).
- Japa: [Mantrum](https://mantrum.app/) (4.8, iOS+Android, haptic Rudraksha, 27/54/108), [JapGuru](https://play.google.com/store/apps/details?hl=en_US&id=com.mantra.japguru) (offline, streaks, Feb 2026 update), [Naam Jap](https://karmalive.org/mantra-jap-counter-app) (free, no ads, sankalp), [Japa Counter](https://apps.apple.com/in/app/japa-counter-mantra-tracker/id6757606346) (offline, reminders, graphs).

Uttar Sewa’s differentiator *should* be: **one corpus, refuse if not in the videos, jump to the exact second, mala in the same hand.** That differentiator is not delivered on first launch (empty/wrong API, Chat/Search split, mala weaker than dedicated apps).

## Trust defects (claims vs code)

| Claim | Reality |
|---|---|
| 900+ videos | Copy in About + translations; DB may be 0 |
| AI understands the question | `/ask` copies a row or refuses |
| Overlay / Watch | Channels exist; no device proof; cannot toggle off |
| Dark mode / auto-download | Fake toggles |
| Processing 900+ videos CTA | Start ignores channel; ingest is extractive captions |

## Activation failure

Time-to-value requires: running API, Mongo or curated fallback, correct `API_BASE` / `REACT_APP_BACKEND_URL`, optionally keys + ingest. A first-time user following the store icon never gets a cited clip.

## Retention failure

No reminders (competitors have them). No history graph. PWA mala not synced. Flutter chat forgets previous answers. No reason to open tomorrow except leftover bead count in prefs.

## Support tickets we will get

- “App won’t load / no answers” (127.0.0.1 / undefined/api)  
- “It said 900 videos”  
- “I saved a favorite on the website”  
- “Overlay does nothing”  
- “I asked the same thing in Search and Chat, different answers”  
- “Clear data deleted my mala”  
- “Dark mode doesn’t work”
