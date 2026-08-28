import os

from backend.services.byok import (
    CLEAR_TOKEN,
    apply_env,
    mask_secret,
    merge_secrets,
    public_keys_payload,
    reset_memory_secrets,
    resolve_key,
    set_memory_secrets,
)


def test_mask_secret_hides_the_middle():
    assert mask_secret("") == ""
    assert mask_secret("short") == "••••"
    assert mask_secret("AIzaSySuperSecretKey99") == "AIza••••ey99"
    assert "SuperSecret" not in mask_secret("AIzaSySuperSecretKey99")


def test_user_key_wins_over_env():
    assert resolve_key("youtube", {"youtube": "user-yt"}, {"YOUTUBE_API_KEY": "env-yt"}) == "user-yt"
    assert resolve_key("youtube", {}, {"YOUTUBE_API_KEY": "env-yt"}) == "env-yt"
    assert resolve_key("youtube", {}, {}) is None


def test_empty_patch_does_not_wipe_existing_key():
    merged = merge_secrets({"youtube": "keep-me"}, {"youtube": "  ", "gemini": "new-gem"})
    assert merged["youtube"] == "keep-me"
    assert merged["gemini"] == "new-gem"


def test_clear_token_removes_user_key():
    merged = merge_secrets({"youtube": "gone", "gemini": "stay"}, {"youtube": CLEAR_TOKEN})
    assert "youtube" not in merged
    assert merged["gemini"] == "stay"


def test_public_payload_never_leaks_full_key():
    payload = public_keys_payload(
        {"youtube": "AIzaSySuperSecretKey99"},
        {"GEMINI_API_KEY": "gem-env-secret-value"},
    )
    blob = str(payload)
    assert "SuperSecret" not in blob
    assert "gem-env-secret-value" not in blob
    by_id = {item["id"]: item for item in payload["providers"]}
    assert by_id["youtube"]["configured"] is True
    assert by_id["youtube"]["source"] == "user"
    assert "••••" in by_id["youtube"]["hint"]
    assert by_id["gemini"]["configured"] is True
    assert by_id["gemini"]["source"] == "env"
    assert by_id["mistral"]["configured"] is False
    assert by_id["mistral"]["source"] == "missing"
    assert payload["byok"] is True
    assert "docs" in by_id["youtube"]


def test_apply_env_configures_process_without_restart(monkeypatch):
    monkeypatch.delenv("YOUTUBE_API_KEY", raising=False)
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    apply_env({"youtube": "yt-live", "gemini": "gm-live"})
    assert os.environ["YOUTUBE_API_KEY"] == "yt-live"
    assert os.environ["GEMINI_API_KEY"] == "gm-live"


def test_keys_http_save_masks_and_configures():
    reset_memory_secrets()
    from fastapi.testclient import TestClient

    from backend.server import app

    client = TestClient(app)
    listed = client.get("/api/control/keys")
    assert listed.status_code == 200
    assert listed.json()["byok"] is True
    assert {item["id"] for item in listed.json()["providers"]} >= {"youtube", "gemini", "mistral"}

    saved = client.put(
        "/api/control/keys",
        json={"youtube": "AIzaSyTestKeyValueXX", "gemini": "AIzaSyGeminiKeyYY12"},
    )
    assert saved.status_code == 200
    blob = str(saved.json())
    assert "AIzaSyTestKeyValueXX" not in blob
    assert "AIzaSyGeminiKeyYY12" not in blob
    youtube = next(item for item in saved.json()["providers"] if item["id"] == "youtube")
    assert youtube["configured"] is True
    assert youtube["source"] == "user"

    again = client.get("/api/control/keys")
    assert again.json()["providers"]
    health = client.get("/api/health")
    assert health.status_code == 200
    assert health.json()["byok"] is True
    assert "youtube" in health.json()["keys_configured"]
    reset_memory_secrets()
