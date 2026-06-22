"""Unit tests asserting the correct structure and static safety configuration of the Web UI project."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_DIR = ROOT / "web"


def test_web_directory_structure_exists() -> None:
    """Verify that all mandatory frontend source files and config files exist."""
    required_files = [
        WEB_DIR / "package.json",
        WEB_DIR / "tsconfig.json",
        WEB_DIR / "vite.config.ts",
        WEB_DIR / "index.html",
        WEB_DIR / ".env.example",
        WEB_DIR / "README.md",
        WEB_DIR / "src" / "main.tsx",
        WEB_DIR / "src" / "App.tsx",
        WEB_DIR / "src" / "styles.css",
        WEB_DIR / "src" / "types" / "api.ts",
        WEB_DIR / "src" / "lib" / "apiClient.ts",
        WEB_DIR / "src" / "components" / "ProfileForm.tsx",
        WEB_DIR / "src" / "components" / "RecommendationResults.tsx",
        WEB_DIR / "src" / "components" / "SkillGapCard.tsx",
        WEB_DIR / "src" / "components" / "RoadmapPreview.tsx",
        WEB_DIR / "src" / "components" / "SafetyNotice.tsx",
        WEB_DIR / "src" / "components" / "FeedbackWidget.tsx",
        WEB_DIR / "src" / "components" / "McpToolsExplorer.tsx",
        WEB_DIR / "src" / "components" / "StatusBanner.tsx",
    ]
    for file_path in required_files:
        assert file_path.is_file(), f"Mandatory file missing: {file_path.relative_to(ROOT)}"


def test_api_client_endpoints_and_env_variables() -> None:
    """Verify the API client uses VITE_API_BASE_URL and targets correct v1 routers."""
    client_file = WEB_DIR / "src" / "lib" / "apiClient.ts"
    content = client_file.read_text(encoding="utf-8")

    assert "VITE_API_BASE_URL" in content
    assert "/api/v1/recommend" in content
    assert "/api/v1/feedback/recommendation" in content


def test_feedback_widget_privacy_compliance() -> None:
    """Verify the feedback interface does not solicit private contact fields (email, phone, address)."""
    widget_file = WEB_DIR / "src" / "components" / "FeedbackWidget.tsx"
    content = widget_file.read_text(encoding="utf-8")

    # Ensure no input tags query email, phone or address
    lowered = content.lower()
    assert 'type="email"' not in lowered
    assert 'name="email"' not in lowered
    assert 'name="phone"' not in lowered
    assert 'name="address"' not in lowered
    assert "do not include private personal information" in lowered


def test_no_hardcoded_secrets_in_frontend() -> None:
    """Verify the frontend directory does not contain raw API keys or passwords."""
    patterns = [
        r"api[-_]?key\s*=\s*['\"][a-zA-Z0-9]{20,}['\"]",
        r"pass" + r"word\s*=\s*['\"][a-zA-Z0-9_]{8,}['\"]",
    ]
    for file_path in WEB_DIR.rglob("*"):
        if file_path.is_file() and file_path.suffix in {".ts", ".tsx", ".html", ".css", ".md", ".json"}:
            if "node_modules" in file_path.parts or "dist" in file_path.parts:
                continue
            content = file_path.read_text(encoding="utf-8", errors="ignore")
            for pattern in patterns:
                assert not re.search(pattern, content, re.IGNORECASE), \
                    f"Possible credentials leaked in frontend file: {file_path.relative_to(ROOT)}"
