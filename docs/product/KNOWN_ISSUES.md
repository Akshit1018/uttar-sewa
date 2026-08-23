# Known issues

## EXTERNAL_DEPENDENCY_REQUIRED

- Live YouTube Data API / Gemini / Mistral keys (paste in Settings or `.env`)
- MongoDB for persist (API falls back to curated Q&A + default control settings)
- `openai-whisper` package and `WHISPER_AUDIO_DIR` audio files for caption-less videos
- Android SDK / iOS toolchain — this Linux agent cannot `flutter build apk` or prove overlay/Watch
- `CONTROL_TOKEN` must be set by the operator for any internet-exposed API

## Product gaps still open

- PWA Settings has no BYOK or control-token field
- Flutter Search empty-results / error recovery is thin
- Default API base `http://127.0.0.1:8000/api` is wrong on a physical device (emulator: `10.0.2.2`)
- Two admin UIs (Flutter Control vs React Admin) can drift
- `ultra_video_service` appears unused
- `feedback` collection is not in `db_schema`
- CORS `*` + credentials
- Keys stored cleartext in Mongo

## Do not “fix” by rewriting

Do not replace the extractive ask pipeline with an unconstrained chat model.
Do not add recruiting / resume features from generic agent templates.
