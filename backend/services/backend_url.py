def resolve_backend_url(configured: str = "", origin: str = "") -> str:
    """Never return undefined/api. Env wins; else page origin; else local API host."""
    raw = (configured or "").strip().rstrip("/")
    if raw.endswith("/api"):
        raw = raw[:-4].rstrip("/")
    if raw.lower() in {"", "undefined", "null"}:
        origin = (origin or "").strip().rstrip("/")
        if origin and origin.lower() not in {"null", "undefined", "file://"}:
            return origin
        return "http://127.0.0.1:8000"
    return raw
