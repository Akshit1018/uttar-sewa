# Architecture decisions

## Corpus load is query-scoped, not a full dump

Ask/search rank in process. Loading every document (previously 2000) hid later talks and hid the real retrieval problem. Candidates are token-filtered and capped at 400. This is still lexical, not semantic.

## Seed library is not the seeker’s corpus

`source=curated_library` is counted separately. Chat activation is paste-URL ingest. Curated text may still answer when Mongo is empty, but the UI must say so.

## Clip rows stay extractive

Titles are timestamps + snippets. Gemini is not allowed to invent questions that become canonical corpus rows.

## Paste URL is a first-class activation API

`POST /process/from-url` classifies watch vs channel. Clients do not reimplement YouTube URL parsing.

## Gemini/Mistral keys are optional leftovers

YouTube is the ingest credential. Chat/Search do not call Gemini/Mistral. Required-key theater blocked “ready” without changing answers.

## Same-origin PWA for a Cloudflare tunnel

A public demo needs one URL. When `frontend/build/index.html` exists, FastAPI mounts that folder at `/` after `/api`. The PWA then calls `window.location.origin/api`. Two tunnels (CRA :3000 + API :8000) would break CORS and bake localhost. The quick tunnel (`trycloudflare.com`) is ephemeral and is not a production hostname.
