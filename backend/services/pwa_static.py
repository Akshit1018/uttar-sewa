"""Serve the built React PWA from the same origin as /api.

One public URL (LAN or Cloudflare tunnel) then works without a second
host or a baked-in REACT_APP_BACKEND_URL. The PWA falls back to
window.location.origin when that env is empty.
"""

from pathlib import Path

from fastapi import FastAPI
from starlette.exceptions import HTTPException as StarletteHTTPException
from starlette.staticfiles import StaticFiles
from starlette.types import Scope


def default_pwa_build_dir() -> Path:
    return Path(__file__).resolve().parents[2] / "frontend" / "build"


class SpaStaticFiles(StaticFiles):
    """Unknown paths return index.html so the PWA shell can load."""

    async def get_response(self, path: str, scope: Scope):
        try:
            return await super().get_response(path, scope)
        except StarletteHTTPException as exc:
            if exc.status_code != 404:
                raise
            return await super().get_response("index.html", scope)


def mount_built_pwa(app: FastAPI, build_dir: Path | None = None) -> bool:
    root = Path(build_dir) if build_dir is not None else default_pwa_build_dir()
    if not (root / "index.html").is_file():
        return False
    app.mount("/", SpaStaticFiles(directory=str(root), html=True), name="pwa")
    return True
