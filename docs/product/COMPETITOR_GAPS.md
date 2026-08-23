# Competitor gaps

Research date: 2026-08-23. `parallel-cli` **not installed**; facts from web search only. Do not invent ratings beyond sources.

## Capability matrix

States: MISSING / WEAK / PARTIAL / COMPARABLE / BETTER.

| Capability | Uttar Sewa | NotebookLM / Gemini Notebook | Dedicated mala apps | GitaGPT-class OSS | Gap matters? |
|---|---|---|---|---|---|
| Ask a YouTube transcript with citations | PARTIAL (own ingest; extractive; refuse) | BETTER — paste URL, citations, audio overview ([official](https://notebooklm.google/), [Tom’s Guide 27 Jun 2026](https://www.tomsguide.com/ai/i-turned-youtube-into-an-ai-bootcamp-with-notebooklm-heres-my-workflow)) | MISSING | WEAK (scripture, not your guru’s channel) | Yes — core job |
| Jump to exact YouTube timestamp | PARTIAL (we build `watch?v=&t=`) | PARTIAL (transcript cite; not always a watch URL) | MISSING | MISSING | Yes — our real edge if it works |
| Refuse when not in corpus | COMPARABLE/BETTER if `/ask` used | WEAK (model can still talk) | n/a | WEAK | Yes — trust |
| Semantic retrieval | MISSING (`embedding` unused) | BETTER | n/a | BETTER ([aprameyak/GitaGPT](https://github.com/aprameyak/GitaGPT) Chroma) | Yes after corpus exists |
| Works on a phone out of the box | WEAK (loopback default) | BETTER (hosted) | BETTER | WEAK | Yes |
| Offline japa | PARTIAL (Flutter local; PWA localStorage) | n/a | BETTER — designed offline ([Japa Counter](https://apps.apple.com/in/app/japa-counter-mantra-tracker/id6757606346), [JapGuru](https://play.google.com/store/apps/details?hl=en_US&id=com.mantra.japguru)) | n/a | Yes for mala half |
| Haptics / bead feel | WEAK | n/a | BETTER ([Mantrum](https://mantrum.app/) Rudraksha + haptics) | n/a | Yes for mala users |
| Reminders / streaks / graphs | MISSING (and we rejected leaderboards on purpose) | n/a | BETTER — streaks/graphs/reminders (Japa Counter, JapGuru Feb 2026) | n/a | Reminders: yes. Leaderboards: no (product rule) |
| Empty-corpus honesty | WEAK (Chat silent) | BETTER (no source → user adds one) | n/a | COMPARABLE | Yes |
| Operator ingest of a whole channel | PARTIAL | WEAK (manual URLs/playlists) | n/a | MISSING | Yes — our other edge |
| Auth / multi-user | MISSING | BETTER (Google account) | BETTER (optional login) | VARIES | Yes if ever shared |
| Eval / quality reports | MISSING | Unknown | n/a | PARTIAL (My Kanha claims coverage reports) | Yes for AI trust |

## How a competitor would beat this

1. **NotebookLM pitch:** “Paste the satsang URL. Don’t run Mongo or Whisper.” Time-to-value minutes, not an operator dashboard.  
2. **Mala app pitch:** “Offline, reminders, haptics. We don’t make you configure FastAPI.”  
3. **Exploit our bugs:** dead phone install, 900+ lie, Chat vs Search, fake settings, open admin API.

## Open-source we rebuilt worse

- Vector RAG over a closed text: GitaGPT/Chroma — we have an unused `embedding` field and lexical-only ask.  
- FastAPI + React spiritual chat: several GitaGPT repos. We added mala + YouTube timestamps (good idea) then failed first-run and security.

**ADOPT later (not this audit):** hybrid search after evals; phone-first API setup; reminders without gamification.

Sources:
- [Gemini Notebook](https://notebooklm.google/) (Jul 2026 rename note in search snippet)
- [Tom’s Guide NotebookLM YouTube workflow](https://www.tomsguide.com/ai/i-turned-youtube-into-an-ai-bootcamp-with-notebooklm-heres-my-workflow) (27 Jun 2026)
- [XDA — consume YouTube via NotebookLM](https://www.xda-developers.com/i-dont-watch-youtube-videos-anymore-i-consume-them-using-notebooklm/)
- [Mantrum](https://mantrum.app/)
- [JapGuru Play Store](https://play.google.com/store/apps/details?hl=en_US&id=com.mantra.japguru) (update cited Feb 6, 2026)
- [Naam Jap](https://karmalive.org/mantra-jap-counter-app)
- [Japa Counter App Store](https://apps.apple.com/in/app/japa-counter-mantra-tracker/id6757606346)
- [aprameyak/GitaGPT](https://github.com/aprameyak/GitaGPT)
