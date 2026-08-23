"""Bring-your-own-keys: paste in Control/Settings, mask on read, override .env."""

from __future__ import annotations

import os
from typing import Any, Dict, List, Mapping, MutableMapping, Optional

from backend.services.secret_seal import seal_secret, secrets_key, unseal_secret

CLEAR_TOKEN = "__clear__"

PROVIDERS: List[Dict[str, Any]] = [
    {
        "id": "youtube",
        "label": "YouTube Data API",
        "label_hi": "यूट्यूब API कुंजी",
        "env": "YOUTUBE_API_KEY",
        "docs": "https://console.cloud.google.com/apis/credentials",
        "help": "Google Cloud → APIs & Services → Credentials → API key. Enable YouTube Data API v3.",
        "required": True,
    },
    {
        "id": "gemini",
        "label": "Google Gemini",
        "label_hi": "जेमिनी API कुंजी",
        "env": "GEMINI_API_KEY",
        "docs": "https://aistudio.google.com/apikey",
        "help": "Unused by Chat/Search. Optional leftover for transcript extract experiments — answers stay extractive.",
        "required": False,
    },
    {
        "id": "mistral",
        "label": "Mistral",
        "label_hi": "मिस्ट्रल API कुंजी",
        "env": "MISTRAL_API_KEY",
        "docs": "https://console.mistral.ai/api-keys",
        "help": "Unused by Chat/Search. Optional leftover; ranking is lexical.",
        "required": False,
    },
    {
        "id": "google_translate",
        "label": "Google Translate",
        "label_hi": "अनुवाद API कुंजी",
        "env": "GOOGLE_TRANSLATE_API_KEY",
        "docs": "https://console.cloud.google.com/apis/credentials",
        "help": "Optional. Cloud Translation API key.",
        "required": False,
    },
]

PROVIDER_IDS = {item["id"] for item in PROVIDERS}
ENV_BY_ID = {item["id"]: item["env"] for item in PROVIDERS}

_memory_secrets: Dict[str, str] = {}


def memory_secrets() -> Dict[str, str]:
    return dict(_memory_secrets)


def set_memory_secrets(values: Optional[Mapping[str, str]]) -> Dict[str, str]:
    global _memory_secrets
    _memory_secrets = {
        key: str(value)
        for key, value in (values or {}).items()
        if key in PROVIDER_IDS and str(value or "").strip()
    }
    return memory_secrets()


def reset_memory_secrets() -> None:
    set_memory_secrets({})


def mask_secret(value: Optional[str]) -> str:
    text = str(value or "")
    if not text:
        return ""
    if len(text) <= 8:
        return "••••"
    return f"{text[:4]}••••{text[-4:]}"


def merge_secrets(
    current: Optional[Mapping[str, str]],
    patch: Optional[Mapping[str, Any]],
) -> Dict[str, str]:
    merged = {
        key: str(value)
        for key, value in (current or {}).items()
        if key in PROVIDER_IDS and str(value or "").strip()
    }
    for key, value in (patch or {}).items():
        if key not in PROVIDER_IDS or value is None:
            continue
        text = str(value).strip()
        if text == CLEAR_TOKEN:
            merged.pop(key, None)
        elif text:
            merged[key] = text
    return merged


def resolve_key(
    provider_id: str,
    stored: Optional[Mapping[str, str]] = None,
    environ: Optional[Mapping[str, str]] = None,
) -> Optional[str]:
    user = str((stored or {}).get(provider_id) or "").strip()
    if user:
        return user
    env_name = ENV_BY_ID.get(provider_id)
    if not env_name:
        return None
    env_val = str((environ if environ is not None else os.environ).get(env_name) or "").strip()
    return env_val or None


def resolve_all(
    stored: Optional[Mapping[str, str]] = None,
    environ: Optional[Mapping[str, str]] = None,
) -> Dict[str, str]:
    out: Dict[str, str] = {}
    for spec in PROVIDERS:
        value = resolve_key(spec["id"], stored, environ)
        if value:
            out[spec["id"]] = value
    return out


def apply_env(resolved: Mapping[str, str], environ: Optional[MutableMapping[str, str]] = None) -> None:
    target = environ if environ is not None else os.environ
    for provider_id, value in resolved.items():
        env_name = ENV_BY_ID.get(provider_id)
        if env_name and value:
            target[env_name] = value


def public_keys_payload(
    stored: Optional[Mapping[str, str]] = None,
    environ: Optional[Mapping[str, str]] = None,
) -> Dict[str, Any]:
    env = environ if environ is not None else os.environ
    providers = []
    for spec in PROVIDERS:
        user = str((stored or {}).get(spec["id"]) or "").strip()
        env_val = str(env.get(spec["env"]) or "").strip()
        if user:
            source = "user"
            raw = user
        elif env_val:
            source = "env"
            raw = env_val
        else:
            source = "missing"
            raw = ""
        providers.append(
            {
                "id": spec["id"],
                "label": spec["label"],
                "label_hi": spec["label_hi"],
                "env": spec["env"],
                "docs": spec["docs"],
                "help": spec["help"],
                "required": bool(spec.get("required")),
                "configured": bool(raw),
                "source": source,
                "hint": mask_secret(raw),
            }
        )
    ready = all(item["configured"] for item in providers if item["required"])
    return {
        "byok": True,
        "ready": ready,
        "providers": providers,
        "keys_configured": [item["id"] for item in providers if item["configured"]],
    }


def secrets_document(values: Mapping[str, str], key: Optional[str] = None) -> Dict[str, Any]:
    material = key if key is not None else secrets_key()
    doc: Dict[str, Any] = {"_id": "byok", "sealed": True}
    for provider_id, value in values.items():
        if provider_id in PROVIDER_IDS and str(value or "").strip():
            doc[provider_id] = seal_secret(str(value), material)
    return doc


def secrets_from_document(doc: Optional[Mapping[str, Any]], key: Optional[str] = None) -> Dict[str, str]:
    if not doc:
        return {}
    material = key if key is not None else secrets_key()
    out: Dict[str, str] = {}
    for provider_id, value in doc.items():
        if provider_id not in PROVIDER_IDS:
            continue
        text = str(value or "").strip()
        if not text:
            continue
        try:
            out[provider_id] = unseal_secret(text, material)
        except Exception:
            out[provider_id] = text
    return out
