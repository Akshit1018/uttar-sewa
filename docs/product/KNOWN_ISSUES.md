# Known issues

## EXTERNAL_DEPENDENCY_REQUIRED

- Live YouTube Data API / Gemini / Mistral keys (paste in Settings or `.env`)
- MongoDB for persist (API falls back to curated Q&A + default control settings)
- `openai-whisper` package and `WHISPER_AUDIO_DIR` audio files for caption-less videos
- Android SDK / iOS toolchain — this Linux agent cannot `flutter build apk` or prove overlay/Watch
- `CONTROL_TOKEN` must be set by the operator for any internet-exposed API

## Product gaps still open

- Flutter Search empty-results / error recovery is still thin
- Default Flutter API base is wrong on a physical device until Settings is saved
- Two admin UIs (Flutter Control vs React Admin) can drift
- `ultra_video_service` remains unused (not imported)
- Ingest is still in-process (startup resumes pending jobs; no Redis/queue)
- Secret seal uses stdlib PBKDF2+HMAC, not a hardware keystore
- Flutter/PWA on a real device: UNVERIFIED in this environment

## Do not “fix” by rewriting

Do not replace the extractive ask pipeline with an unconstrained chat model.
Do not add recruiting / resume features from generic agent templates.
