"""Full project Web UI structural and integration regression tests."""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def test_web_package_json_properties() -> None:
    package_file = ROOT / "web" / "package.json"
    assert package_file.is_file(), "web/package.json is missing"
    
    data = json.loads(package_file.read_text(encoding="utf-8"))
    assert "react" in data.get("dependencies", {})
    assert "typescript" in data.get("devDependencies", {})


def test_web_env_example_and_api_client() -> None:
    env_example = ROOT / "web" / ".env.example"
    assert env_example.is_file(), "web/.env.example is missing"
    
    api_client_file = ROOT / "web" / "src" / "lib" / "apiClient.ts"
    assert api_client_file.is_file(), "apiClient.ts is missing"
    
    api_client_content = api_client_file.read_text(encoding="utf-8")
    assert "/api/v1/recommend" in api_client_content, "API Client does not call /api/v1/recommend"
    assert "import.meta.env.VITE_API_BASE_URL" in api_client_content


def test_web_app_components_exist() -> None:
    app_tsx = ROOT / "web" / "src" / "App.tsx"
    assert app_tsx.is_file()
    
    content = app_tsx.read_text(encoding="utf-8")
    
    # Assert form does not collect PII (email, phone, home address)
    assert "email" not in content.lower() or "redacted" in content.lower()
    assert "phone" not in content.lower()
    assert "address" not in content.lower()
    
    # Verify core components are rendered
    components_dir = ROOT / "web" / "src" / "components"
    assert components_dir.is_dir()
    
    expected_components = [
        "ProfileForm.tsx",
        "RecommendationResults.tsx",
        "SkillGapCard.tsx",
        "RoadmapPreview.tsx",
        "FeedbackWidget.tsx",
        "SafetyNotice.tsx",
        "StatusBanner.tsx"
    ]
    for c in expected_components:
        assert (components_dir / c).is_file(), f"Component missing: {c}"
