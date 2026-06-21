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

PRIVATE_KEY_PATTERN = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
    re.IGNORECASE | re.DOTALL,
)
EMAIL_PATTERN = re.compile(r"(?<![\w.+-])[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}")
GOOGLE_KEY_PATTERN = re.compile(r"\bAIza[0-9A-Za-z_-]{20,}\b")
GITHUB_TOKEN_PATTERN = re.compile(r"\b(?:ghp_|github_pat_)[0-9A-Za-z_]{12,}\b")
OPENAI_TOKEN_PATTERN = re.compile(r"\bsk-[0-9A-Za-z_-]{12,}\b")
ASSIGNED_PASSWORD_PATTERN = re.compile(
    r"(?i)\b(password|passwd|pwd)\s*[:=]\s*([^\s,;]+)"
)
ASSIGNED_TOKEN_PATTERN = re.compile(
    r"(?i)\b(api[_ -]?key|access[_ -]?token|auth[_ -]?token|token|secret)"
    r"\s*[:=]\s*([^\s,;]+)"
)
LONG_ID_PATTERN = re.compile(r"(?<!\d)\d{12,}(?!\d)")

RISK_ORDER = {"none": 0, "low": 1, "medium": 2, "high": 3}


def get_safety_notice() -> str:
    """Return the canonical educational guidance disclaimer."""
    return SAFETY_NOTICE
