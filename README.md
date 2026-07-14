# Uttar Sewa

**AI service platform — AI intake, service diagnosis, and provider matching.**

Uttar Sewa ("Northern Service") is a Python/FastAPI service platform that takes a user's request, diagnoses what service they need, and matches them to the right provider. Built as a two-sided service layer (customer intake ↔ provider matching).

## Architecture

- **Backend** — Python, FastAPI (`app_server.py` + `backend/`)
- **Frontend** — frontend app (see `frontend/`)
- **Tests** — `tests/`, `backend_test.py`, `test_imports.py`

```
app_server.py        FastAPI entrypoint
backend/             core service logic (intake, diagnosis, matching)
frontend/            frontend app
tests/               test suite
run_backend.py       runner helper
```

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r backend/requirements.txt
cp backend/.env.example backend/.env                 # fill in your keys
python run_backend.py
```

> ⚠️ `.env` files are git-ignored and **must not** be committed. Use `.env.example` as the template.

## Why it exists

Service businesses (legal, accounting, notary, consulting) lose leads at the intake step — the customer can't articulate what they need, and the business can't triage fast enough. Uttar Sewa puts an AI layer in front of intake: diagnose the need, then route to the right provider. Same pattern I deployed for an accounting-firm two-sided marketplace.

## Status

Working backend + frontend. Configuration and client-specific data abstracted for open-source release.

## License

MIT