"""
Simple Policy Engine

Evaluates authorization requests using external JSON configuration.

The application delegates authorization decisions to this module.
"""

from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).parent


def load_json(filename: str) -> dict:
    """Load a JSON document from the src directory."""
    path = BASE_DIR / filename

    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


def authorize(principal: str, action: str, resource: str) -> bool:
    """
    Evaluate whether a principal is allowed to perform an action.

    The resource is accepted for API consistency with future policy engines,
    although it is not evaluated in this MVP.
    """
    del resource  # Reserved for future policy evaluation.

    principals = load_json("principals.json")["principals"]
    policy = load_json("policy.json")["roles"]

    role = None

    for user in principals:
        if user["id"] == principal:
            role = user["role"]
            break

    if role is None:
        return False

    allowed_actions = policy.get(role, [])

    return action in allowed_actions
