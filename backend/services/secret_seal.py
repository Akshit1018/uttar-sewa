"""Stdlib sealed envelope for BYOK values at rest.

Not FIPS AES-GCM. Authenticated PBKDF2 stream + HMAC. Prefer SECRETS_KEY
or CONTROL_TOKEN; the baked fallback is local-dev only.
"""

from __future__ import annotations

import base64
import hashlib
import hmac
import os

PREFIX = "enc_v1:"
_DEV_KEY = "uttar-sewa-dev-local"


def secrets_key(environ: dict | None = None) -> str:
    env = environ if environ is not None else os.environ
    return (env.get("SECRETS_KEY") or env.get("CONTROL_TOKEN") or _DEV_KEY).strip()


def _derive(key: str, salt: bytes, length: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", (key or "").encode("utf-8"), salt, 120_000, dklen=length)


def seal_secret(plaintext: str, key: str) -> str:
    raw = (plaintext or "").encode("utf-8")
    if not raw:
        return ""
    salt = os.urandom(16)
    stream = _derive(key, salt, len(raw) + 32)
    cipher = bytes(left ^ right for left, right in zip(raw, stream))
    mac = hmac.new(stream[len(raw) :], salt + cipher, hashlib.sha256).digest()
    packed = salt + mac + cipher
    return PREFIX + base64.urlsafe_b64encode(packed).decode("ascii")


def unseal_secret(value: str, key: str) -> str:
    text = value or ""
    if not text.startswith(PREFIX):
        return text
    packed = base64.urlsafe_b64decode(text[len(PREFIX) :].encode("ascii"))
    salt, mac, cipher = packed[:16], packed[16:48], packed[48:]
    stream = _derive(key, salt, len(cipher) + 32)
    expected = hmac.new(stream[len(cipher) :], salt + cipher, hashlib.sha256).digest()
    if not hmac.compare_digest(mac, expected):
        raise ValueError("sealed secret mac mismatch")
    return bytes(left ^ right for left, right in zip(cipher, stream)).decode("utf-8")
