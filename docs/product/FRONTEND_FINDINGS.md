# Frontend findings

## Flutter

| ID | Title | Evidence | Sev |
|---|---|---|---|
| FE-01 | Default loopback API | `api_client.dart:24-27` | CRITICAL |
| FE-02 | `screens.dart` ~713-line god file | line count | MEDIUM |
| FE-03 | Chat is single `_result` | `screens.dart` | MEDIUM |
| FE-04 | Search no empty state | `screens.dart` list of hits | MEDIUM |
| FE-05 | No Semantics | grep empty | HIGH |
| FE-06 | `loading` never set | `app_state.dart` | LOW |
| FE-07 | Unused `api.tap`/`undo` | `api_client.dart` | LOW |
| FE-08 | Live Activity / Watch no stop | `app_state.dart` | HIGH |
| FE-09 | Pin no loading/error | `ClipCard` | MEDIUM |
| FE-10 | Control in primary IA | `main.dart` tabs | MEDIUM |

## PWA

| ID | Title | Evidence | Sev |
|---|---|---|---|
| FE-11 | `undefined/api` | `.env.example` empty | CRITICAL |
| FE-12 | ChatInterface ~600 lines; SearchInterface ~560 duplicate | files | MEDIUM |
| FE-13 | Ask payload hung on Array | `data.refused` on array | LOW |
| FE-14 | NaN% confidence | `Math.round(score * 100)` | MEDIUM |
| FE-15 | Fake darkMode / autoDownload | SettingsPage | HIGH |
| FE-16 | Destructive clear, no confirm | Settings, Favorites | HIGH |
| FE-17 | No BYOK / control token | SettingsPage | HIGH |
| FE-18 | Admin fetches without token | ProcessingStatus, AdminDashboard | HIGH |
| FE-19 | Icon buttons without aria-label | ChatInterface hearts | MEDIUM |
| FE-20 | JapaChatSheet no focus trap / Esc | `role=dialog` only | MEDIUM |
| FE-21 | Analytics is console + localStorage | `analyticsService.js` | HIGH (cannot know if product works) |
| FE-22 | Offline cache type mismatch | Chat + useOfflineStorage | HIGH |

## Button honesty
See UX button table in the inspection notes: Overlay/Watch/Live Activity/Pin/Clear/Share fail closed or silently.

## Styling
Dark glass cards, gradients (`from-blue-500/20`), generic “AI dashboard” look. Not measured for contrast (POSSIBLE WCAG fail on `text-gray-400`).
