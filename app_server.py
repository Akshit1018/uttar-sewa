#!/usr/bin/env python3
"""Compatibility entrypoint — the FastAPI app lives in backend.server."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from backend.server import app  # noqa: E402

__all__ = ["app"]
