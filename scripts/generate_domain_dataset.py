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
    "cloud": [
        "Cloud Run", "AWS Basics", "Azure Basics", "Google Cloud Basics",
        "Cloud Deployment", "Serverless Basics", "Cloud Storage",
        "Cloud Networking Basics", "Identity and Access Management",
        "Cloud Cost Awareness", "Managed Databases", "Cloud Functions",
        "Container Registry", "Load Balancing Basics", "Auto Scaling Basics",
        "Cloud Architecture", "Infrastructure Monitoring", "Cloud Migration",
        "Disaster Recovery Basics", "Multi-region Concepts",
    ],
    "security": [
        "Input Validation", "Secret Management", "Security Review",
        "OWASP Basics", "Dependency Scanning", "Error Sanitization",
        "Access Control Basics", "Threat Modeling", "Secure Coding",
        "Vulnerability Management", "Security Logging", "Network Security Basics",
        "Application Security Testing", "Cloud Security Basics",
        "Incident Response Basics", "Data Privacy Basics", "API Security",
        "Identity Security", "Security Risk Assessment", "Phishing Awareness",
    ],
    "testing": [
        "Unit Testing", "API Testing", "Integration Testing", "End-to-end Testing",
        "Test Design", "Test Automation", "Regression Testing", "Performance Testing",
        "Load Testing Basics", "Contract Testing", "Mocking", "Test Data Management",
        "Browser Testing", "Mobile Testing", "Accessibility Testing",
        "Exploratory Testing", "Quality Risk Analysis", "Bug Reporting",
        "Acceptance Testing", "Continuous Testing",
    ],
    "devops": [
        "Docker", "Git", "GitHub", "GitHub Actions", "CI/CD", "Linux Basics",
        "Logging", "Monitoring", "Observability", "Deployment",
        "Environment Variables", "Reverse Proxy Basics", "Kubernetes Basics",
        "Infrastructure as Code Basics", "Release Management", "Shell Scripting",
        "Configuration Management", "Build Automation", "Incident Management",
        "Service Health Checks",
    ],
    "product": [
        "Product Thinking", "Problem Framing", "User Empathy", "User Research",
        "Prioritization", "Product Analytics", "Roadmap Planning",
        "Requirements Discovery", "Rapid Prototyping", "Feature Scoping",
        "Outcome Metrics", "Customer Journey Mapping", "Market Research Basics",
        "Product Experimentation", "Backlog Management", "Product Strategy Basics",
        "Usability Evaluation", "Feedback Synthesis", "Value Proposition Design",
        "Product Discovery",
    ],
    "soft-skill": [
        "Communication", "Learning Planning", "Stakeholder Communication",
        "Demo Presentation", "Collaboration", "Critical Thinking",
        "Time Management", "Problem Solving", "Feedback Skills", "Facilitation",
        "Mentoring Basics", "Cross-functional Collaboration", "Active Listening",
        "Decision Documentation", "Conflict Resolution Basics", "Adaptability",
        "Self-directed Learning", "Professional Communication",
        "Remote Collaboration", "Technical Interview Communication",
    ],
    "database": [
        "SQL", "PostgreSQL", "MySQL Basics", "Relational Modeling",
        "Indexing Basics", "Transaction Basics", "Query Optimization Basics",
        "Database Migration", "Schema Design", "Database Backup Basics",
        "NoSQL Basics", "Redis Basics", "Data Integrity", "Database Security",
        "Connection Pooling", "ORM Basics", "Stored Procedure Basics",
        "Database Monitoring", "Replication Basics", "Data Warehousing Basics",
    ],
    "architecture": [
        "Clean Architecture", "Modular Monolith", "Service Boundaries",
        "Event-driven Basics", "System Design Basics", "Design Patterns",
        "Scalability Basics", "Reliability Patterns", "API Gateway Basics",
        "Domain Modeling", "Architecture Decision Records", "Message-driven Design",
        "Distributed Systems Basics", "Fault Tolerance Basics", "Data Flow Design",
        "Integration Patterns", "Technical Tradeoff Analysis", "Layered Architecture",
        "Hexagonal Architecture Basics", "Capacity Planning Basics",
    ],
    "documentation": [
        "Documentation", "Technical Writing", "OpenAPI", "README Authoring",
        "API Reference Writing", "Architecture Diagrams", "Tutorial Writing",
        "Release Notes", "Runbook Writing", "Knowledge Base Design",
        "Code Comments", "Documentation Testing", "Information Architecture",
        "Content Review", "Developer Documentation", "User Guide Writing",
        "Change Communication", "Diagramming", "Example Design",
        "Documentation Maintenance",
    ],
}

SKILL_LEVELS = {
    "frontend": "intermediate", "backend": "intermediate", "ai": "advanced",
    "data": "intermediate", "cloud": "intermediate", "security": "intermediate",
    "testing": "intermediate", "devops": "intermediate", "product": "beginner",
    "soft-skill": "beginner", "database": "intermediate",
    "architecture": "advanced", "documentation": "beginner",
}
