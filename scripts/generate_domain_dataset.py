"""Generate deterministic production-minded CareerVerse domain datasets."""

import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = ROOT / "app" / "data"
SAFETY_NOTE = (
    "This recommendation is educational guidance only and does not guarantee "
    "employment outcomes."
)
ROADMAP_SAFETY_NOTE = (
    "This roadmap is educational guidance only and should be adapted to the "
    "learner's context."
)


def slugify(value: str) -> str:
    """Convert a human-readable value to a stable snake_case identifier."""
    normalized = re.sub(r"[^a-z0-9]+", "_", value.lower())
    return normalized.strip("_")


def write_json(filename: str, payload: Any) -> None:
    """Write deterministic UTF-8 JSON using the required formatting."""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    with (DATA_DIR / filename).open("w", encoding="utf-8", newline="\n") as file:
        json.dump(payload, file, ensure_ascii=False, indent=2)
        file.write("\n")


SKILL_GROUPS = {
    "frontend": [
        "HTML", "CSS", "JavaScript", "TypeScript", "React", "Next.js",
        "Tailwind CSS", "Accessibility", "Responsive Design", "API Integration",
        "State Management", "Form Validation", "Component Design", "UI Testing",
        "Frontend Performance", "Web Components", "Design Systems",
        "Browser DevTools", "Progressive Web Apps", "Internationalization",
    ],
    "backend": [
        "Python", "FastAPI", "Node.js", "REST API Design", "GraphQL Basics",
        "Authentication Basics", "JWT", "OAuth2 Basics", "Background Jobs",
        "Error Handling", "API Documentation", "Caching", "Rate Limiting",
        "Webhooks", "Message Queues", "Server-side Validation", "API Versioning",
        "Concurrency Basics", "Dependency Injection", "Service Integration",
    ],
    "ai": [
        "LLM API Integration", "Prompt Engineering", "Tool Calling",
        "Agent Orchestration", "MCP", "Agent Evaluation", "Embeddings",
        "Vector Search", "RAG", "Prompt Injection Defense", "AI Safety",
        "Model Evaluation", "Function Calling", "Context Engineering",
        "Agent Memory", "Machine Learning Fundamentals", "Feature Engineering",
        "NLP Fundamentals", "Computer Vision Fundamentals", "Model Serving",
    ],
    "data": [
        "Data Cleaning", "Data Visualization", "Statistics Basics", "Pandas",
        "NumPy", "SQL Analysis", "Dashboard Design", "ETL Basics",
        "Data Modeling", "BI Reporting", "A/B Testing Basics", "Data Quality",
        "Exploratory Data Analysis", "Metric Design", "Data Storytelling",
        "Spreadsheet Analysis", "Time Series Basics", "Data Governance Basics",
        "Experiment Analysis", "Data Pipeline Testing",
    ],
