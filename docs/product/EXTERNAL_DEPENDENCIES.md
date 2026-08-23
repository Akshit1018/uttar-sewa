# External dependencies

| Dependency | Used by | Status if missing |
|---|---|---|
| MongoDB | Persist videos / Q&A / settings | API falls back to curated library + default settings |
| YouTube Data API key | Channel listing / captions (when fetcher needs it) | `from-url` / start processing fail at runtime — **EXTERNAL_DEPENDENCY_REQUIRED** |
| Gemini / Mistral | Unused by Chat/Search | Optional; not required for ready |
| `openai-whisper` + local audio | Caption-less videos | Those videos stay unprocessed |
| `CONTROL_TOKEN` | Lock ingest/keys on a shared network | Demo-open control writes if unset |
| Flutter / Android / iOS toolchains | Device proof | **UNVERIFIED** here |

Do not claim live YouTube ingest was validated in this Green Team run.
