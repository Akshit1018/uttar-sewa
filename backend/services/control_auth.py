"""Optional CONTROL_TOKEN gate for write/admin routes.

When CONTROL_TOKEN is unset the API stays demo-open (local/dev).
When it is set, clients must send the same value as X-Control-Token.
"""

import os
from typing import Optional


def expected_control_token() -> str:
    return (os.environ.get("CONTROL_TOKEN") or "").strip()


def control_token_required() -> bool:
    return bool(expected_control_token())


def authorize_control(provided: Optional[str]) -> bool:
    expected = expected_control_token()
    if not expected:
        return True
    return (provided or "").strip() == expected


def authorize_cloud(provided: Optional[str]) -> bool:
    """Cloud backup/restore always fail closed. Token must be set and match."""
    expected = expected_control_token()
    if not expected:
        return False
    return (provided or "").strip() == expected
