# Competitor attack script

Truthful lines a salesperson could say to our user. If the line is true, we have a gap.  
Research date: 2026-08-23. Apps not installed. `parallel-cli` / Firecrawl **not used**.

## NotebookLM / Gemini Notebook (Q&A-from-YouTube)

**Their actual workflow (reconstructed from published use):** paste a YouTube URL as a source; the tool reads the **transcript**, not the pixels; the user asks questions and gets cited passages; extras include summaries, study guides, and Audio Overview. Videos without captions fail until the user pastes a transcript. Sources: [Android Police — NotebookLM + YouTube](https://www.androidpolice.com/im-using-notebooklm-to-watch-youtube-for-me-and-im-learning-twice-as-much/), [VidNotes — captions required](https://vidnotes.app/blog/199-How-to-Use-YouTube-Videos-in-NotebookLM), [XDA — consume YouTube via NotebookLM](https://www.xda-developers.com/i-dont-watch-youtube-videos-anymore-i-consume-them-using-notebooklm/).

| Line they can say | True? | Our counter |
|---|---|---|
| “Paste the satsang URL. Don’t run Mongo.” | **Yes** | We require API + ingest job |
| “I can add a playlist / Watch Later dump.” | **Mostly** (extensions + notebooks) | We have channel ingest **if** the operator uses the Flutter ingest path, not the PWA custom URL |
| “Answers cite the transcript.” | **Yes** (numbered citations) | We cite too, but only after ingest; we **refuse** more often |
| “I get an Audio Overview for commute.” | **Yes** | We have PWA TTS on the orb only |
| “It works in the browser on a phone without a LAN IP.” | **Yes** (hosted) | Flutter defaults to loopback |
| “I don’t need a Control tab.” | **Yes** | Our nav exposes operator chrome |

**Where we are not worse:** we can refuse instead of chatting; we can jump to `watch?v=&t=` as a first-class button; we attach a mala. Those only matter after the corpus exists.

**Best-in-class pattern to steal:** time-to-first-citation = paste URL. Not “start processing 900 videos.”

## Mantrum (japa)

Site claims: virtual mala, 27/54/108/custom, haptics, reminders, streaks, points, 100K+ devotees marketing. Source: [mantrum.app](https://mantrum.app/), [App Store listing](https://apps.apple.com/cl/app/mantrum-daily-japa-mala/id6752685948).

| Line | True? |
|---|---|
| “We remind you to sit. They don’t.” | **Yes** (we have no first-class reminder product) |
| “Eyes-closed haptics, bead sound, bead skins.” | **Yes** vs our numeric orb |
| “Offline is the default story.” | **Yes** (their marketing; ours works offline for tap but first-run is API-shaped) |
| “We have a satsang timestamp.” | **No** — we win this sentence |

Product rule: do **not** copy streaks/leaderboards. Copy **reminders + haptic**, not gamification.

## JapGuru

Play Store / site: offline counter, bead types, streaks, live “devotees chanting,” AI guru nudges, leaderboards. Sources: [Play Store](https://play.google.com/store/apps/details?hl=en_US&id=com.mantra.japguru), [japguru.in](https://japguru.in/). Update snippet dated Feb 6, 2026 on Play.

| Line | True? |
|---|---|
| “Fully offline chanting.” | **Yes** as their store promise |
| “Social / live count.” | **Yes** for them; **REJECT** for us |
| “AI mantra coach.” | They claim it; we must not imitate invented teaching |

## Open-source YouTube RAG (engineer dismissal)

Mature pattern: chunk with `start_sec`, hybrid retrieve, generate **only** from chunks, parse `[video_id:t]` citations, evaluate faithfulness. Examples: [justinduplain/youtube-transcript-rag](https://github.com/justinduplain/youtube-transcript-rag) (hybrid + timestamp citations), [shreyas-kapse/youtube_bot](https://github.com/shreyas-kapse/youtube_bot) (hybrid + RAGAS), [VidNavigator — RAG for video transcripts](https://vidnavigator.com/en/blog/rag-for-video-transcripts) (grounding primitive = `video_id` + `start_sec`).

| Line from an engineer | True? |
|---|---|
| “You reinvented lexical bag-of-words and called it Q&A.” | **Yes** — `rank_answers` + `text[:80]` questions |
| “You load 2000 documents into RAM per request.” | **Yes** — `_load_qa_database` |
| “You left ultra-search files in the tree.” | **Yes** |
| “You did get extractive refuse right.” | **Yes** — keep it |

**ADOPT later:** timestamp-preserving chunks (we already store segments) + hybrid retrieve **after** evals.  
**DO NOT ADOPT:** unconstrained LLM answers as the video sentence.

## THEM vs US vs BEST

| Job | Them | Us | Best-in-class |
|---|---|---|---|
| First citation | NotebookLM: minutes | Operator + Mongo | Paste URL → cite |
| Faithful answer | NotebookLM: cited but generative | Extractive refuse | Extractive **or** generate-only-from-chunks with eval |
| Daily japa | Mantrum/JapGuru | Local orb | Offline + reminder + haptic, no league |
| Combined cite+bead | Nobody serious | **Only us** | Us, if activation works |

## Investor dismissal (product weakness, not fundraising)

- Why isn’t this a NotebookLM notebook + a $0 mala app?  
- Differentiation is the **join**, not either half.  
- Retention: mala is daily; ask is sporadic. If the corpus is seed data, ask dies.  
- Proprietary data: only if a channel is ingested and unique Q&A accumulates. Seed library is not proprietary.  
- Distribution: none in code (no store listing, no analytics).

## Designer dismissal (remove / change / missing)

**Remove from seeker chrome:** Control, Admin, Processing, scrape box, sample-data alerts, ultra-search leftovers.  
**Change:** orb is a number in a circle; mala apps show beads. 2.5s hold is an unteachable gesture without onboarding.  
**Missing:** first citation in one action; reminder; single save model.

## Founder dismissal (six months of runway)

Wasted if kept as-is: Firestore cloud UI-less API, Admin `console.log` analytics, dead ultra/LLM modules, PWA/Flutter feature fork, Live Activity theater.  
Keep: extractive ask, timestamp button, local mala, ingest upsert.

Sources:
- [I'm using NotebookLM to watch YouTube](https://www.androidpolice.com/im-using-notebooklm-to-watch-youtube-for-me-and-im-learning-twice-as-much/)
- [How to Use YouTube Videos in NotebookLM](https://vidnotes.app/blog/199-How-to-Use-YouTube-Videos-in-NotebookLM)
- [I don't watch YouTube videos anymore, I consume them using NotebookLM](https://www.xda-developers.com/i-dont-watch-youtube-videos-anymore-i-consume-them-using-notebooklm/)
- [Mantrum](https://mantrum.app/)
- [Mantrum App Store](https://apps.apple.com/cl/app/mantrum-daily-japa-mala/id6752685948)
- [JapGuru Play Store](https://play.google.com/store/apps/details?hl=en_US&id=com.mantra.japguru)
- [JapGuru site](https://japguru.in/)
- [justinduplain/youtube-transcript-rag](https://github.com/justinduplain/youtube-transcript-rag)
- [VidNavigator RAG for video transcripts](https://vidnavigator.com/en/blog/rag-for-video-transcripts)
