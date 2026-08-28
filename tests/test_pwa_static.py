from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient


def test_mount_skips_missing_build(tmp_path):
    from backend.services.pwa_static import mount_built_pwa

    app = FastAPI()

    @app.get("/api/health")
    def health():
        return {"ok": True}

    assert mount_built_pwa(app, tmp_path) is False
    client = TestClient(app)
    assert client.get("/api/health").json() == {"ok": True}
    assert client.get("/").status_code == 404


def test_mount_serves_index_and_keeps_api(tmp_path):
    from backend.services.pwa_static import mount_built_pwa

    (tmp_path / "index.html").write_text("<html>uttar-sewa</html>", encoding="utf-8")
    (tmp_path / "asset-manifest.json").write_text("{}", encoding="utf-8")
    app = FastAPI()

    @app.get("/api/health")
    def health():
        return {"ok": True}

    assert mount_built_pwa(app, tmp_path) is True
    client = TestClient(app)
    home = client.get("/")
    assert home.status_code == 200
    assert b"uttar-sewa" in home.content
    assert client.get("/api/health").json() == {"ok": True}
    assert client.get("/missing-route").status_code == 200
    assert b"uttar-sewa" in client.get("/missing-route").content
    assert client.get("/asset-manifest.json").status_code == 200


def test_default_build_dir_is_frontend_build():
    from backend.services.pwa_static import default_pwa_build_dir

    path = default_pwa_build_dir()
    assert path.name == "build"
    assert path.parent.name == "frontend"


def test_server_attaches_pwa_mount_helper():
    import inspect

    from backend import server

    source = inspect.getsource(server)
    assert "mount_built_pwa" in source


def test_live_app_health_still_works_without_build():
    from backend.server import app

    client = TestClient(app)
    body = client.get("/api/health").json()
    assert "ok" in body
    assert body["ready"] == body["database"]


def test_startup_does_not_hang_when_mongo_never_answers(monkeypatch):
    import asyncio
    import time

    from backend import server

    async def forever(*_args, **_kwargs):
        await asyncio.sleep(30)

    monkeypatch.setattr(server, "bootstrap_database", forever)
    started = time.monotonic()
    asyncio.run(server.startup_database())
    assert time.monotonic() - started < 5
