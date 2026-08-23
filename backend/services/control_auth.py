"""Optional CONTROL_TOKEN gate for write/admin routes.

When CONTROL_TOKEN is set, clients must send the same value as X-Control-Token.
When it is unset, only loopback/testclient peers stay demo-open.
"""

import os
from typing import Optional

LOOPBACK_PEERS = {"127.0.0.1", "::1", "localhost", "testclient"}


def expected_control_token() -> str:
    return (os.environ.get("CONTROL_TOKEN") or "").strip()


def control_token_required() -> bool:
    return bool(expected_control_token())


def is_loopback_peer(peer: Optional[str]) -> bool:
    host = (peer or "").strip().lower().split("%")[0]
    return host in LOOPBACK_PEERS


def authorize_control(provided: Optional[str], peer: Optional[str] = None) -> bool:
    expected = expected_control_token()
    if expected:
        return (provided or "").strip() == expected
    if peer is None:
        return True
    return is_loopback_peer(peer)


def authorize_cloud(provided: Optional[str]) -> bool:
    """Cloud backup/restore always fail closed. Token must be set and match."""
    expected = expected_control_token()
    if not expected:
        return False
    return (provided or "").strip() == expected
