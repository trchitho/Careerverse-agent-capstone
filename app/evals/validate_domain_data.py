"""Compatibility entrypoint for production domain dataset validation."""

from typing import Any

from scripts.validate_domain_dataset import load_json, validate_dataset


def validate_domain_data() -> list[str]:
    """Return production dataset validation errors."""
    errors, _payloads = validate_dataset()
    return errors


def load_domain_json(filename: str) -> Any:
    """Load one domain JSON file for application-level tests."""
    return load_json(filename)


def main() -> int:
    """Print a concise compatibility validation result."""
    errors = validate_domain_data()
    if errors:
        print("DOMAIN DATA VALIDATION: FAIL")
        for error in errors:
            print(f"- {error}")
        return 1
    print("DOMAIN DATA VALIDATION: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
