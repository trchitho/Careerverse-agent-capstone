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


def _normalize_text(text: str | None) -> str:
    """Normalize text for deterministic phrase detection."""
    return re.sub(r"\s+", " ", text or "").strip().casefold()


def detect_prompt_injection(text: str | None) -> dict[str, Any]:
    """Detect explicit attempts to override instructions or extract secrets."""
    normalized = _normalize_text(text)
    matches = [
        (pattern, category, risk)
        for pattern, category, risk in PROMPT_INJECTION_RULES
        if pattern in normalized
    ]
    if not matches:
        return {
            "is_suspicious": False,
            "risk_level": "none",
            "matched_patterns": [],
            "categories": [],
            "safe_message": "",
        }

    risk_level = max((item[2] for item in matches), key=RISK_ORDER.__getitem__)
    return {
        "is_suspicious": True,
        "risk_level": risk_level,
        "matched_patterns": list(dict.fromkeys(item[0] for item in matches)),
        "categories": list(dict.fromkeys(item[1] for item in matches)),
        "safe_message": SAFE_REQUEST_MESSAGE,
    }


def redact_sensitive_text(text: str | None) -> str:
    """Redact supported sensitive-data patterns without logging source values."""
    redacted = text or ""
    redacted = PRIVATE_KEY_PATTERN.sub("[REDACTED_PRIVATE_KEY]", redacted)
    redacted = EMAIL_PATTERN.sub("[REDACTED_EMAIL]", redacted)
    redacted = GOOGLE_KEY_PATTERN.sub("[REDACTED_SECRET]", redacted)
    redacted = GITHUB_TOKEN_PATTERN.sub("[REDACTED_TOKEN]", redacted)
    redacted = OPENAI_TOKEN_PATTERN.sub("[REDACTED_TOKEN]", redacted)
    redacted = ASSIGNED_PASSWORD_PATTERN.sub(
        lambda match: f"{match.group(1)}=[REDACTED_PASSWORD]",
        redacted,
    )
    redacted = ASSIGNED_TOKEN_PATTERN.sub(
        lambda match: f"{match.group(1)}=[REDACTED_SECRET]",
        redacted,
    )
    return LONG_ID_PATTERN.sub("[REDACTED_ID]", redacted)


def _has_sensitive_text(text: str) -> bool:
    """Return whether redaction would alter the supplied text."""
    return redact_sensitive_text(text) != text


def _profile_mapping(profile: object) -> dict[str, Any]:
    """Return a defensive profile copy from a mapping or Pydantic model."""
    if hasattr(profile, "model_dump"):
        payload = profile.model_dump()
    elif isinstance(profile, dict):
        payload = deepcopy(profile)
    else:
        raise ValueError("Profile must be a dictionary or Pydantic model.")
    return payload


def _scan_values(value: object) -> list[str]:
    """Flatten supported scalar and list profile values into strings."""
    if isinstance(value, str):
        return [value]
    if isinstance(value, list):
        return [item for item in value if isinstance(item, str)]
    return []


def _redact_value(value: object) -> object:
    """Return a redacted copy of a supported profile field value."""
    if isinstance(value, str):
        return redact_sensitive_text(value)
    if isinstance(value, list):
        return [redact_sensitive_text(item) if isinstance(item, str) else item for item in value]
    return value


def _sensitive_risk(text: str) -> str:
    """Classify sensitive content as blocking high risk or redaction-only low risk."""
    severe_patterns = (
        PRIVATE_KEY_PATTERN,
        GOOGLE_KEY_PATTERN,
        GITHUB_TOKEN_PATTERN,
        OPENAI_TOKEN_PATTERN,
        ASSIGNED_PASSWORD_PATTERN,
        ASSIGNED_TOKEN_PATTERN,
    )
    if any(pattern.search(text) for pattern in severe_patterns):
        return "high"
    if EMAIL_PATTERN.search(text) or LONG_ID_PATTERN.search(text):
        return "low"
    return "none"


def _issue(field: str, category: str, message: str) -> dict[str, str]:
    """Build a public issue object without including source text."""
    return {"field": field, "category": category, "message": message}


def validate_profile_safety(profile: object) -> dict[str, Any]:
    """Validate profile text and return a redacted, non-mutating safety result."""
    payload = _profile_mapping(profile)
    redacted_profile = deepcopy(payload)
    issues: list[dict[str, str]] = []
    highest_risk = "none"
    scan_fields = (
        "name",
        "education",
        "interests",
        "skills",
        "career_goal",
        "preferred_learning_style",
        "language",
        "experience_level",
    )

    for field in scan_fields:
        value = payload.get(field)
        redacted_profile[field] = _redact_value(value)
        for text in _scan_values(value):
            injection = detect_prompt_injection(text)
            if injection["is_suspicious"]:
                highest_risk = max(
                    (highest_risk, injection["risk_level"]),
                    key=RISK_ORDER.__getitem__,
                )
                for category in injection["categories"]:
                    issues.append(
                        _issue(
                            field,
                            category,
                            "Unsafe instruction-override content detected.",
                        )
                    )

            sensitive_risk = _sensitive_risk(text)
            if sensitive_risk != "none":
                highest_risk = max(
                    (highest_risk, sensitive_risk),
                    key=RISK_ORDER.__getitem__,
                )
                issues.append(
                    _issue(
                        field,
                        "sensitive_data",
                        "Sensitive data was removed from this field.",
                    )
                )

    blocking = highest_risk in {"medium", "high"} and any(
        issue["category"] != "sensitive_data" or highest_risk == "high"
        for issue in issues
    )
