"""Deterministic profile safety and sensitive-text redaction tools."""

from __future__ import annotations

import re
from copy import deepcopy
from typing import Any

SAFETY_NOTICE = (
    "This system provides educational career guidance only. "
    "It does not guarantee employment outcomes or replace professional counseling."
)

SAFE_REQUEST_MESSAGE = (
    "The request contains unsafe instruction-override content and cannot be processed."
)
SAFE_PROFILE_MESSAGE = "The profile contains unsafe content and cannot be processed."

PROMPT_INJECTION_RULES = (
    ("ignore previous instructions", "instruction_override", "high"),
    ("override developer instructions", "instruction_override", "high"),
    ("ignore safety rules", "security_bypass", "high"),
    ("reveal system prompt", "system_prompt_extraction", "high"),
    ("hidden instructions", "system_prompt_extraction", "high"),
    ("system message", "system_prompt_extraction", "medium"),
    ("developer message", "system_prompt_extraction", "medium"),
    ("show api key", "secret_extraction", "high"),
    ("print secrets", "secret_extraction", "high"),
    ("bypass security", "security_bypass", "high"),
    ("disable guardrails", "security_bypass", "high"),
    ("jailbreak", "jailbreak", "high"),
)
