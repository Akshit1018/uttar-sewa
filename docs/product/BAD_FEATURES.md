# Bad / extra features

Remove, hide, or redesign. More features made the first session worse.

| Feature | Verdict | Why |
|---|---|---|
| Control tab in Flutter primary nav | Hide | Seekers hit ingest/scrape/BYOK |
| React Admin + Processing **and** Flutter Control | Consolidate | Two operator surfaces, token only on Flutter |
| PWA Dark Mode toggle | Remove or implement | Fake |
| PWA Auto Download toggle | Remove or implement | Fake |
| `/search` LLM hybrid | Disable by default | Contradicts grounded ask |
| `enhanced_search_coordinator` + ultra/intelligent | Delete or quarantine | Complexity without evals |
| `ultra_video_service` | Delete | Unused |
| `/mala/tap` + `/mala/undo` HTTP | Deprecate | Flutter does not call them; two sources of truth |
| Cloud backup/restore (unauth) | Lock or remove | Restore is a weapon |
| Unbounded `/feedback` | Constrain or remove | Abuse |
| About “900+” and “AI understands” | Rewrite | False if corpus empty / ask is extractive |
| Wikipedia scrape box defaulting to Karma | Empty placeholder | Demo smell |
| Confidence NaN badge | Hide if missing | Looks broken |
| Four search strategies | One lexical path | Architecture astronautics |
| Public companions on every ask (when enabled) | Opt-in | Latency + distraction next to refuse |
| `system/status` Gemini cost estimate | Remove | Stale after extractive ingest |

**Keep (they have a job):** extractive `/ask`, timestamp URLs, local mala math, caption→Whisper ingest, labeled companions, optional CONTROL_TOKEN (but fail closed in prod).
