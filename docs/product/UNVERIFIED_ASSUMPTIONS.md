# Unverified assumptions

This audit **did not**:

- Run the Flutter app on a phone or emulator (no Flutter SDK on the audit machine).
- Run the PWA in a browser or take screenshots.
- Hit a live YouTube / Gemini / Firestore account.
- Measure real latency, bundle size, or Lighthouse/axe scores.
- Interview seekers or operators.
- Use `parallel-cli` (not installed). Market claims use [WebSearch] results only; see `COMPETITOR_GAPS.md` sources.

Mark these as **NEEDS VERIFICATION**, not CONFIRMED:

| Assumption | Status |
|---|---|
| Scrapling follows redirects to private IPs | POSSIBLE — httpx path is CONFIRMED `follow_redirects=False`; Scrapling path untested |
| DNS rebinding of allowlisted hosts | POSSIBLE |
| Firestore restore actually wipes Mongo when `cloud_db.enabled` | HIGH CONFIDENCE from code; not live-tested |
| NaN% badge appears in production responses | HIGH CONFIDENCE if `confidence_score` omitted |
| Orb overlaps send button on iPhone SE | POSSIBLE (layout math only) |
| Contrast of `text-gray-400` fails WCAG | POSSIBLE (not measured) |
| Users prefer dedicated mala apps over this orb | HYPOTHESIS from competitor feature lists |
| Seekers already use NotebookLM on satsang YouTube | OBSERVED in 2026 press; not proven for this audience |

**Research limitation:** `parallel-cli` was not available. Competitor facts are cited from search results, not from installing those apps.
