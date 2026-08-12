# Grounded Sadhana Companion — Product Brainstorm & Design

**Product:** Uttar Sewa (Spiritual Q&A)  
**Date:** 2026-08-12  
**Status:** Brainstorm / design. Not implementation.

## Problem

Search is not how a seeker actually uses this. They want two things in the same breath:

1. **Ask a living question** and hear an answer that comes only from the guru’s videos, with the exact clip as proof.
2. **Keep a mala in the hand** while the phone is in use — tap, complete 108, see the day’s count — and when a doubt arises, hold the same bead-orb and speak.

Today the app is a website with chat and search. It does not yet have a grounded “only-from-videos” AI, and it has no always-available mala.

## Non-negotiable rules

- The model may **not** invent spiritual teaching. If the corpus does not contain it, it says so and offers the closest video clips.
- Every answer must cite **video title + timestamp + watch URL**. No citation, no sentence.
- A mala cycle is **108** taps (the “1.8” in the request is treated as 108).
- Hold the orb **~2.5 seconds** to open chat. A short tap only counts a bead.
- Voice uses the **phone’s own microphone permission**, then the same grounded answer path as typed chat.

## Two products in one orb

| Gesture | Meaning |
|---|---|
| Tap | One japa / one bead. Haptic click. Count +1. |
| 108 taps | One mala cycle. Soft chime / stronger haptic. Cycle +1. |
| Hold 2–3s | Chat overlay. Text or voice. Answers only from videos. |
| Drag | Move the orb so it does not cover content. |
| Double-tap (optional) | Undo last bead (mis-tap). |

Dashboard shows: beads today, malas today, current cycle progress (e.g. 47/108), streak of days with at least one mala, questions asked, last video cited.

---

## Grounded AI: how it should work

This is **retrieval-augmented generation over the video corpus**, not a general chatbot and not a multi-agent “crew.”

### What to use

**Recommended: LangGraph + hybrid retrieval + citation verifier.**

LangGraph is a state machine: question → retrieve clips → grade “is this actually in the videos?” → write answer → check every claim has a clip → return. That matches “only from the videos.”

**Not recommended as the core: CrewAI.** Crews are for several personas debating. Here there is one job: quote the discourses faithfully. Extra agents add cost, latency, and more chances to hallucinate. A second “citation critic” node *inside* LangGraph is enough.

**Storage is not LangGraph.** LangGraph orchestrates. Data lives in:

- **Transcript chunks** (10–30s windows): `video_id`, `start`, `end`, `text`, `language`, `channel_id`, embedding
- **Existing Q&A pairs** (already in Mongo): same metadata + embedding
- **Vector index** for meaning (Hindi + English)
- **Keyword index** for exact shlokas, names, mantras

MongoDB Atlas Vector Search can sit on the current Mongo. Qdrant or pgvector are fine if Atlas is not available. Do not store “the AI’s memory of videos” as a black-box prompt. Store **chunks with timestamps**.

### Answer contract

User: “मन भटकता है तो क्या करें?”

Assistant:

1. Two or three sentences **in the user’s language**, paraphrasing only what the clips say.
2. Source cards: video title, `12:34–13:10`, “Watch this moment.”
3. If nothing is close enough: “इस विषय पर संकलित प्रवचनों में स्पष्ट उत्तर नहीं मिला” + 3 nearest clips, **no invented remedy**.

Follow-ups (“और कैसे?”) reuse the last question + last cited videos as context (already started in the current search API).

### Ingestion (the hard part)

The old blocker remains: many videos have **no captions**. Grounded AI is only as good as transcripts.

Path:

1. YouTube captions when they exist.
2. Otherwise **audio → speech-to-text** (Whisper / Google STT) in Hindi, then chunk + embed.
3. Optional human “pin this as a canonical Q&A” in admin.

Until transcripts exist, the curated library can answer, but it must be labeled **“curated teaching, not a timestamped clip”** so we do not fake a video reference.

---

## Floating orb: what is actually possible

A true “always on top of every app, like AssistiveTouch” is **not the same on iOS and Android**.

| Surface | Overlay on other apps? | What to ship |
|---|---|---|
| Current React PWA | No. Only while the site is open. | In-app floating orb (Phase 1). |
| Android native / Capacitor | Yes, with `SYSTEM_ALERT_WINDOW` (“Display over other apps”). | Chat-head / bubble + mala. |
| iOS | **No third-party app may draw over other apps.** | In-app orb + **Live Activity / Dynamic Island** for the running mala + **Apple Watch** as the real bead + Home Screen widget for today’s count. |
| Web on desktop | In-tab only. | Same in-app orb. |

So: do not promise an iPhone AssistiveTouch clone over WhatsApp. Promise a mala that is always in *this* app, a Live Activity while a mala is running, and a Watch tapper. On Android, a real overlay is allowed after an explicit permission screen.

Permissions to request, in plain language, only when needed:

- Microphone (voice questions)
- Notifications (mala complete, Live Activity)
- Android: draw over other apps
- Optional: speech recognition

Never ask for overlay + mic on first launch.

### Hold-to-chat overlay

A bottom sheet / glass card:

- Transcript of voice, or a text field
- Waveform while listening (system mic)
- Answer + video cards
- “Open full app” for history, dashboard, favorites

Voice path: OS speech-to-text → same `/ask` API as typed chat → grounded answer. Do not send raw audio to a third-party unless STT on-device fails.

---

## Out-of-the-box features that fit this product

These are not a dump of “AI ideas.” They sit on the same two rails: **faithful video answers** and **sadhana in the hand**.

### Practice

- **Named malas** — different mantras, each with its own 108 and daily total.
- **Haptic bead** — light tap per bead, distinct pulse at 108.
- **Undo bead** — double-tap, because thumbs miss.
- **PiP satsang** — play the cited clip in picture-in-picture while the mala keeps counting.
- **Sandhya reminder** — local sunrise/sunset, not a generic “don’t forget to meditate” spam.
- **Anushthana mode** — “I will complete 11 malas” with a quiet progress ring, no leaderboard.
- **Do Not Disturb / Focus** — one switch: “Japa” focus while a mala is active.

### Answers

- **Clip-first cards** — the video moment is the product; the paragraph is a caption.
- **Language lock** — answer in the language of the question; offer the original Hindi clip anyway.
- **“Not in the corpus”** as a first-class UI, not an error.
- **Share a card** — question, two-line answer, timestamp link, no extra commentary.
- **Continue this video** — from the cited moment, not from 0:00.

### Surfaces beyond the phone screen

- **Apple Watch / Wear OS** — the honest mala. Tap the watch, phone stores the count.
- **Lock Screen / Home Screen widget** — today’s beads and malas.
- **Dynamic Island** — `47/108` while a mala is running.
- **WhatsApp / Telegram bot** for parents who will never install a PWA — still grounded, still cites YouTube.
- **Car voice** (later) — “What did Maharajji say about anger?” Hands-free, citations read aloud, no video autoplay while driving.

### Trust and library

- **Admin “pin”** — mark a Q&A as verified against a clip.
- **Missing-caption queue** — which videos still cannot be cited.
- **Per-channel corpus** — only this guru’s channels, never the open web.

### Explicitly out of scope (for now)

- AR/VR temples, emotion-detecting cameras, social feeds, public leaderboards of japa, generic ChatGPT knowledge, selling mantras.

---

## Integrations (only if they serve the two rails)

| Integrate | Why |
|---|---|
| YouTube Data API + captions | Source of videos |
| Whisper / Google STT | Transcripts when captions are missing |
| Embeddings (multilingual) | Hindi/English meaning search |
| LangGraph | Grounded ask-retrieve-cite-refuse loop |
| Mongo (existing) + vector index | Chunks, Q&A, mala events, users |
| Web Speech / iOS Speech / Android SpeechRecognizer | Voice questions |
| Capacitor or React Native | Overlay permission, haptics, Live Activities, Watch |
| APNs / FCM | Mala complete, Live Activity |
| Optional: Health / Mindfulness minutes | Only if the user opts in; japa as mindful minutes |

Do not integrate calendar, Instagram, or random wellness APIs until the orb and grounded ask are real.

---

## Architecture (target)

```
[Orb / Chat / Voice]
        │
        ▼
   /api/ask  (LangGraph)
        │
        ├─ expand follow-up from chat memory
        ├─ hybrid retrieve (vector + keyword) over chunks + Q&A
        ├─ grade: enough evidence?
        ├─ generate answer in user language
        └─ verify citations → { text, clips[] }

[Ingestion]
  YouTube → captions or STT → chunks → embeddings → Mongo/vector

[Mala]
  tap events → local first (offline) → sync → dashboard
```

API sketch (not implemented in this brainstorm):

- `POST /api/ask` `{ question, history, language, channel_id }` → `{ answer, clips: [{video_id, title, start, end, url}], refused: bool }`
- `POST /api/mala/events` `{ ts, beads_delta, mala_id }`
- `GET /api/mala/summary?day=` → `{ beads, cycles, goal_108 }`

The existing `/api/search` can remain as “find clips.” `/api/ask` is “speak from those clips.”

---

## Three ways to build it

**A. PWA-only (fastest)**  
In-app orb, hold-to-chat, voice via Web Speech, mala counts in localStorage, grounded `/ask` on the current FastAPI backend. No overlay on other apps. No Watch. Good for proving the idea.

**B. PWA + LangGraph RAG now, native shell next (recommended)**  
Ship A plus real chunk embeddings and citation-checked answers. Then wrap with Capacitor: Android overlay, iOS Live Activity, haptics, Watch later. One codebase, permissions where the OS allows them.

**C. Full native rewrite first**  
Best mala feel, slowest path, throws away the working React app. Do not do this until A/B is loved.

**Recommendation: B.** The differentiator is **grounded answers + a mala you actually use**, not a new UI framework.

---

## Phased delivery

1. **Grounded `/ask`** — retrieve chunks/Q&A, refuse if weak, cite timestamps. No orb yet.
2. **In-app orb** — tap = bead, 108 = cycle, hold = chat sheet, voice, dashboard today.
3. **Ingestion** — STT for caption-less videos so citations are real.
4. **Native shell** — Android overlay permission, iOS Live Activity, haptics.
5. **Watch + widgets** — the mala leaves the app screen.

---

## Success

- 80%+ of answers that claim a clip actually open the right moment.
- When the corpus has no answer, the app **refuses** instead of preaching.
- A user can complete one mala of 108 without opening a menu.
- Hold-to-chat works one-handed, including Hindi voice.

## Open decision (product, not tech)

Treat **108** as the cycle length unless a later setting allows 11 / 27 / 54 / 108.
