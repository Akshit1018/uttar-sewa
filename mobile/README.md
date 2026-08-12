# Uttar Sewa — Flutter

Mobile client for the FastAPI backend. Android, iOS, and web shells are generated.

```bash
cd mobile
flutter pub get
flutter test
flutter analyze
flutter run --dart-define=API_BASE=http://127.0.0.1:8000/api
```

Android emulator: `http://10.0.2.2:8000/api`.


## Tabs

1. **Chat** — grounded `/api/ask` (hold the japa orb 2.5s to jump here)
2. **Search** — `/api/search` with channel filter
3. **Sadhana** — mala counts + named mantra
4. **Control** — dashboard against Mongo `uttar_sewa`
5. **Settings** — language + API/database status
