# Security model

## Trust boundaries

| Layer | Trust | Notes |
|---|---|---|
| Public `/api/ask`, `/api/search`, `/api/mala/*` | Unauthenticated | Intended for a single-operator / household deploy |
| Write/admin `/api/control/*` writes, `/api/process/*` | Optional `CONTROL_TOKEN` | Demo-open when unset |
| BYOK secrets | User-provided | Stored cleartext in Mongo `control_secrets` `_id: byok`; copied into `os.environ` |
| Public scrape | Allowlisted hosts | No redirect follow |
| Transcript / Whisper | Local or YouTube captions | Never treat as user identity |

## Known residual risks (honest)

- **No user auth / IDOR model.** Any client that can reach the API can ask, sync mala, and (if token unset) write keys.
- **CORS `allow_origins=["*"]`.** Fine for a personal PWA; not for a multi-tenant SaaS.
- **BYOK in Mongo is cleartext.** GET masks (`AIza••••ey99`). Disk/backups still hold full keys.
- **Prompt injection:** `/ask` is extractive (copy corpus). Companions are fetched from allowlisted public APIs, not from user URLs except `/control/scrape`.
- **SSRF:** scrape allowlist + no redirects. DNS rebinding is not fully mitigated.
- **Uploads:** none. Whisper reads `WHISPER_AUDIO_DIR/{video_id}.wav|.mp3|.m4a` only.

## Required production settings

1. Set `CONTROL_TOKEN` and paste it in Settings → Control token.
2. Do not expose Mongo or the API without TLS.
3. Treat BYOK as EXTERNAL_DEPENDENCY / operator secret, not multi-tenant isolation.
4. Keep `public_companions` labeled; never splice companion text into `answer`.

## Status

`IMPLEMENTED` for optional token + scrape no-redirect.  
**Not** `PRODUCTION_VALIDATED` as a multi-user security model.
