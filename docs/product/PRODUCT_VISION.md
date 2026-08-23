# Product vision — Uttar Sewa

**What this is:** a Hindi/English spiritual Q&A companion plus a japa mala. Answers come from discourse transcripts (YouTube captions or local Whisper). Public texts (Gita, Wikipedia, dictionary, sandhya, Open Library) are labeled companions only.

**What this is not:** a recruiting copilot, resume builder, interview coach, job board, or general chatbot that invents teaching.

## Who it is for

Seekers who already listen to long satsang videos and want:

1. A question answered **only** from those discourses, with a clickable timestamp.
2. A mala in the same hand — tap a bead, complete 11 / 27 / 54 / 108, then hold to ask.

## Core principle

The **canonical evidence layer** is the transcript corpus (`transcript_segments` + extractive `question_answers`). Every downstream surface reuses it:

Seeker → Chat / Search / Orb → `/api/ask` or `/api/search` → corpus → extractive answer + citation → optional public companions → follow-up.

If the corpus does not contain the teaching, the product **refuses**. It does not invent a remedy.

## Current product direction

Keep the grounded-sadhana companion. Make the corpus trustworthy (extractive ingest, no Gemini paraphrases as video answers). Make japa work without a network hop. Align PWA chat with Flutter `/ask`. Protect write/admin routes when `CONTROL_TOKEN` is set. Distinguish user facts, transcript evidence, AI inference, and public companions.

## Non-goals (do not add)

- Leaderboards, streak freeze, ads after 108
- Recruiter / candidate / resume / job-search features
- Mixing public-web text into the video answer
- Trusting scraped pages as canonical teaching
