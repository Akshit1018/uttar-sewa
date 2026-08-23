# Absent capabilities

What a reasonable seeker or operator would look for after using the screens we have.  
Classification: MUST HAVE | EXPECTED | DIFFERENTIATOR | POWER FEATURE | NICE TO HAVE | IRRELEVANT  
Decision: BUILD NOW | FOUNDATION NOW | BACKLOG | REJECT (conflicts with product rules)

| Absent thing | Who | Frequency | Class | Our substitute | Decision |
|---|---|---|---|---|---|
| Paste a YouTube URL and ask in one step | Seeker | First session | MUST HAVE | Operator ingest + hope | FOUNDATION NOW |
| First-run: “this is your API / this is empty / ingest or refuse” wizard | Seeker | Once | MUST HAVE | Amber banners after load | BUILD NOW |
| Calm daily japa reminder (not a streak league) | Seeker | Daily | EXPECTED | Optional PWA notification if they toggle it | BUILD NOW |
| Bead haptic + optional tap sound | Seeker | Every tap | EXPECTED | Light haptic on Flutter tap; PWA `vibrate` | BACKLOG |
| Undo on the Flutter orb (PWA has double-tap) | Seeker | Often | EXPECTED | Sadhana screen button | BUILD NOW |
| One favorites model (pin = heart) | Seeker | Weekly | EXPECTED | Split | FOUNDATION NOW |
| Mala sync on PWA | Returning | Daily | EXPECTED | localStorage | BACKLOG or HIDE PWA mala as device-local |
| Editable PWA API URL | Mobile PWA | First session | MUST HAVE | Display only | BUILD NOW |
| Channel URL honored by `/process/start` | Operator | When adding a guru | MUST HAVE | JSON body ignored | BUILD NOW |
| Ingest progress that survives API restart | Operator | Long jobs | EXPECTED | in-process task | FOUNDATION NOW |
| Pagination / no 2000 cap | Operator | After ~hundreds of talks | MUST HAVE | Silent truncate | FOUNDATION NOW |
| Real questions (not `text[:80]`) | Seeker | Every ask | MUST HAVE | Caption slices | FOUNDATION NOW — extractive spans are fine if UI does not call them “questions” |
| Hybrid / semantic retrieve after evals | Seeker | Hard paraphrases | DIFFERENTIATOR | Lexical only | BACKLOG |
| Eval set beyond one fixture | Operator | Every ingest | EXPECTED | `test_ask_eval.py` one pair | BUILD NOW |
| Rate limit + abuse cap on `/ask` | Operator | Always | EXPECTED | None | BUILD NOW if API is networked |
| Encrypt BYOK at rest | Operator | Always | EXPECTED | Cleartext Mongo | BACKLOG |
| User accounts | Multi-seeker | Rare today | NICE TO HAVE | Single tenant | REJECT until there is a second user |
| NotebookLM-style audio overview | Seeker | Sometimes | NICE TO HAVE | TTS on PWA orb only | BACKLOG |
| Playlist ingest | Operator | Setup | EXPECTED | Channel fetch / video_ids | BACKLOG |
| History that survives refresh (server thread) | Seeker | Session | NICE TO HAVE | In-memory last N strings | BACKLOG |
| Export a cited card to image / WhatsApp | Seeker | Share | EXPECTED | PWA `shareCard`; Flutter weak | BACKLOG |
| Keyboard shortcuts (j/k, `/` to ask) | Power | Daily | POWER FEATURE | None | BACKLOG |
| TalkBack-complete Flutter | A11y | Always | MUST HAVE | Orb + tooltips | BUILD NOW incrementally |
| Crash/error reporting | Operator | 3am | EXPECTED | Python logs | BACKLOG |
| Product analytics (cited-answer rate) | Founder | Weekly | MUST HAVE | `console.log` | BUILD NOW (privacy-minimal) |
| Cloud restore UI with typed confirm | Operator | Rare | EXPECTED | Hidden curl | HIDE or add confirm — do not leave nuclear API undocumented |
| Overlay that works over other apps without eating volume | Mobile | Daily japa | DIFFERENTIATOR | Overlay + volume hijack | BACKLOG |
| Sandhya that actually fires on Flutter | Seeker | Daily | EXPECTED | Control toggle + PWA timeout | BACKLOG |
| Leaderboards / punya points / ads after 108 | Market mala apps | Daily | IRRELEVANT | — | **REJECT** (vision) |
| Recruiting / resume | Template pressure | — | IRRELEVANT | — | **REJECT** |

## Next-obvious-action gaps (per screen)

| Screen | Next obvious action | Present? |
|---|---|---|
| Chat empty corpus | “Ingest this channel” / “Paste a video” | No — banner only |
| Chat refuse | “Open nearest clip anyway” | Clips may still show; not explained |
| Search empty | Change channel to All | Flutter copy only |
| Sadhana | Reminder time | No |
| Control | “You are about to spend YouTube quota” | No |
| Settings PWA | Change API host | Display only |
| Favorites | Sync to another phone | No |
| Processing custom URL | Actually ingest that URL | **No** (broken contract) |

## Friction count (core journeys)

Estimated extra events a first-time seeker hits before the aha. **HYPOTHESIS** (not timed on a device).

| Journey | Friction events | Examples |
|---|---|---|
| Flutter first ask | 6–9 | Install → dead API → Settings → type LAN URL → save → Chat → empty/curated answers → find Control → ingest |
| PWA first ask | 4–7 | Open → maybe wrong API host → Chat → curated 30 → no companions → no pin |
| Japa only | 1–2 | Find orb → tap (works) |
| Operator custom channel (PWA) | 3 + **false success** | Type URL → Start → watch wrong channel process |

Japa-only users can get value in seconds. Ask users cannot without an operator step. That is the activation cliff.
