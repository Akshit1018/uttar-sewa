# UX failures

Hostile first-time user + UX researcher. Evidence from code; browser not run (UNVERIFIED visually).

## CRITICAL / HIGH

### UX-01 — App is dead on a real phone
Flutter default API `http://127.0.0.1:8000/api` (`api_client.dart:24-27`). No first-run URL screen.  
**Pain:** “I installed it. Nothing works.”  
**SEVERITY:** CRITICAL  
**CONFIDENCE:** CONFIRMED  

### UX-02 — PWA fetches `undefined/api`
`REACT_APP_BACKEND_URL=` empty (`frontend/.env.example`).  
**SEVERITY:** CRITICAL  
**CONFIDENCE:** CONFIRMED  

### UX-03 — No onboarding
Grep onboarding/firstLaunch: none. Seeker lands on Chat. Control tab sits in Flutter bottom nav (operator ingest/BYOK).  
**SEVERITY:** HIGH  
**CONFIDENCE:** CONFIRMED  

### UX-04 — Chat does not warn empty corpus; Search does
`SearchInterface.jsx` “Processing Required”; Chat does not. `App.js:115-118` empty if-block.  
**SEVERITY:** HIGH  

### UX-05 — About/marketing: 900+ videos + “AI understands”
`AboutPage.jsx`, `translations.js`. Stats may be 0. Ask is extractive copy.  
**SEVERITY:** HIGH (trust)  

### UX-06 — Fake Settings: Dark Mode, Auto Download
Persisted; never consumed (`SettingsPage.jsx` vs grep).  
**SEVERITY:** HIGH (angry customer: “I paid/toggled and nothing happened”)  
**Note:** There is no payment. Still a broken control.

### UX-07 — Clear All Data: no confirm, no undo
`SettingsPage.jsx:35-39` `localStorage.clear()` + `alert`.  
**SEVERITY:** HIGH  

### UX-08 — Channel filter does not apply to Flutter Chat or PWA orb
`app_state.ask` omits channel; `JapaChatSheet` omits `channel_id`.  
**SEVERITY:** HIGH  
**CONFIDENCE:** CONFIRMED  

### UX-09 — Hold orb on Flutter does not open ask UI
`openAsk` → switch tab only (`main.dart`). Empty field. PWA opens sheet.  
**SEVERITY:** MEDIUM  

### UX-10 — Live Activity / Watch cannot turn off
`toggleLiveActivity` / `toggleWatch` only start.  
**SEVERITY:** HIGH  

### UX-11 — Overlay fail-closed with no snackbar
MissingPlugin → silent.  
**SEVERITY:** MEDIUM  

### UX-12 — Flutter Search: blank empty results
`screens.dart` maps hits only.  
**SEVERITY:** MEDIUM  

### UX-13 — Network error shown as “refused” in orb
`JapaChatSheet.jsx` catch → `refused: true`.  
**SEVERITY:** MEDIUM  

### UX-14 — Pin vs heart
Flutter server pin vs PWA localStorage favorites. User thinks they saved a clip.  
**SEVERITY:** HIGH  

### UX-15 — Zero Flutter Semantics
TalkBack: unlabeled orb/nav.  
**SEVERITY:** HIGH  

### UX-16 — Flutter boot: no loading, errors hidden if dashboard exists
`loading` unused; error banner only when `dashboard == null`.  
**SEVERITY:** MEDIUM  

## Hesitation map (first session)

1. What language? (flash Hindi)  
2. Why is Control next to Chat?  
3. I typed a question — is the library empty?  
4. I tapped Overlay — nothing.  
5. I favorited on web, opened phone — gone.  
6. I held the bead — why am I on Chat with no keyboard?
