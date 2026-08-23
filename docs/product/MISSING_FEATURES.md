# Missing features

Only items with a real user job. Not a recruiting wishlist.

| Feature | Who needs it | Evidence it is expected | Priority if we build |
|---|---|---|---|
| Working API URL on first launch | Everyone | Phone ≠ 127.0.0.1 | P0 |
| Empty-corpus CTA on Chat | First-time | Search already has it | P0 |
| Confirm + undo on destructive clear | Everyone | Settings/Favorites | P0 |
| Auth or fail-closed CONTROL_TOKEN in prod | Operator | Open keys/restore | P0 |
| Unique video/Q&A indexes + atomic ingest | Operator | Schema | P0 |
| Channel filter on all ask surfaces | Seeker | Flutter Chat / orb omit it | P1 |
| Semantic search over transcripts | Seeker | Lexical 80-char “questions” miss paraphrases; GitaGPT uses vectors | P1 |
| Ask/search one contract | Seeker | Trust | P1 |
| Offline ask honesty | Seeker | Cache mismatch | P1 |
| Flutter conversation history | Seeker | PWA has it | P1 |
| PWA BYOK + token or “use Flutter” copy | Operator | Settings gap | P1 |
| Native overlay/Watch **off** + error text | Seeker | Buttons start-only | P1 |
| Day rollover + optional reminder | Seeker | Japa Counter / JapGuru | P1 |
| Haptics on bead | Seeker | Mantrum | P2 |
| Screen-reader labels | Disabled users | Zero Semantics | P1 |
| Favorites = pins one model | Seeker | Two stores | P1 |
| Eval set (refuse, faithfulness) | Quality | None | P1 |
| Rate limit | Operator | None | P1 |
| Real analytics sink | Product | localStorage only | P2 |
| Export mala / Q&A | Power user | None | P2 |
| Keyboard / Esc on orb sheet | A11y | Missing | P2 |

**Do not build:** leaderboards, ads after 108, streak freeze (product rule). Reminders ≠ leaderboards.
