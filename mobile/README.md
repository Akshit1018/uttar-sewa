# Uttar Sewa — Flutter

Mobile client for the FastAPI backend. The **Control** tab is the operator dashboard: library stats, mala settings, pinned clips, and processing.

Talks to `/api`, including `/api/control/*` and `/api/mala/*`.

## Run

```bash
# API (from repo root)
pip install -r backend/requirements.txt
uvicorn backend.server:app --reload --port 8000

# App
cd mobile
flutter create . --project-name uttar_sewa --org sewa.uttar
flutter pub get
flutter run --dart-define=API_BASE=http://127.0.0.1:8000/api
```

Android emulator: use `http://10.0.2.2:8000/api` as `API_BASE`.

`flutter create .` generates `android/` and `ios/` once. Do not commit those until you have run it locally.

## Tabs

1. **Chat** — grounded `/api/ask` (hold the japa orb 2.5s to jump here)
2. **Search** — `/api/search` with channel filter
3. **Sadhana** — mala counts + named mantra
4. **Control** — dashboard against Mongo `uttar_sewa`
5. **Settings** — language + API/database status
