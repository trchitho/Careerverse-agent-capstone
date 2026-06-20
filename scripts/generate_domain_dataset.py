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

ROLE_GROUPS = {
    "Software Engineering": [
        ("Frontend Developer", "entry_to_mid", "accessible web interfaces"),
        ("Backend Developer", "entry_to_mid", "reliable server-side services"),
        ("Full-stack Developer", "entry_to_mid", "end-to-end web products"),
        ("Mobile Developer", "entry_to_mid", "mobile application experiences"),
        ("Software Engineer", "entry_to_mid", "maintainable software systems"),
        ("QA Automation Engineer", "entry_to_mid", "automated quality checks"),
        ("API Engineer", "mid", "stable service contracts"),
        ("Platform Engineer", "mid", "internal developer platforms"),
        ("Integration Engineer", "mid", "connected business systems"),
        ("Junior Frontend Developer", "entry", "entry-level web interfaces"),
    ],
    "AI / ML / Agent": [
        ("AI Full-stack Developer", "entry_to_mid", "AI-enabled web products"),
        ("AI Agent Engineer", "mid", "tool-using agent workflows"),
        ("LLM Application Developer", "entry_to_mid", "language-model applications"),
        ("Prompt Engineer", "entry_to_mid", "structured model instructions"),
        ("Machine Learning Engineer", "mid", "production machine learning"),
        ("MLOps Engineer", "mid", "model delivery and operations"),
        ("NLP Engineer", "mid", "language processing systems"),
        ("Computer Vision Engineer", "mid", "visual recognition systems"),
        ("AI Product Engineer", "mid", "user-centered AI features"),
        ("AI Evaluation Engineer", "mid", "AI quality and safety evaluation"),
    ],
    "Data": [
        ("Data Analyst", "entry_to_mid", "decision-ready data analysis"),
        ("Business Intelligence Analyst", "entry_to_mid", "business dashboards"),
        ("Data Engineer", "mid", "reliable data pipelines"),
        ("Analytics Engineer", "mid", "modeled analytics datasets"),
        ("Data Scientist", "mid", "statistical product insights"),
        ("Product Data Analyst", "entry_to_mid", "product behavior analysis"),
        ("Marketing Data Analyst", "entry_to_mid", "marketing performance analysis"),
        ("Financial Data Analyst", "entry_to_mid", "financial reporting analysis"),
        ("Education Data Analyst", "entry_to_mid", "learning outcome analysis"),
        ("Fresher Data Analyst", "entry", "entry-level reporting and analysis"),
    ],
    "Cloud / DevOps": [
        ("DevOps Engineer", "entry_to_mid", "automated software delivery"),
        ("Cloud Engineer", "entry_to_mid", "managed cloud services"),
        ("Site Reliability Engineer", "mid", "service reliability"),
        ("Infrastructure Engineer", "mid", "computing infrastructure"),
        ("Observability Engineer", "mid", "operational telemetry"),
        ("Release Engineer", "mid", "repeatable release workflows"),
        ("Cloud Support Engineer", "entry_to_mid", "cloud issue resolution"),
        ("Platform Operations Engineer", "mid", "platform operations"),
        ("Junior DevOps Engineer", "entry", "entry-level delivery automation"),
        ("FinOps Analyst", "entry_to_mid", "cloud cost visibility"),
    ],
    "Security": [
        ("Security Analyst", "entry_to_mid", "security monitoring and response"),
        ("Application Security Engineer", "mid", "secure application delivery"),
        ("Cloud Security Engineer", "mid", "cloud security controls"),
        ("Security Operations Analyst", "entry_to_mid", "security event triage"),
        ("Identity and Access Analyst", "entry_to_mid", "identity governance"),
        ("Vulnerability Analyst", "entry_to_mid", "vulnerability prioritization"),
        ("API Security Engineer", "mid", "secure API boundaries"),
        ("DevSecOps Engineer", "mid", "security in delivery pipelines"),
        ("Junior Cybersecurity Analyst", "entry", "entry-level security operations"),
        ("Security Awareness Specialist", "entry_to_mid", "practical security education"),
    ],
    "Product / Business": [
        ("Product-oriented Software Engineer", "entry_to_mid", "user-centered delivery"),
        ("Product Manager", "mid", "product outcomes and prioritization"),
        ("Technical Product Manager", "mid", "technical product strategy"),
        ("Business Analyst", "entry_to_mid", "business process requirements"),
        ("Solution Consultant", "mid", "technical solution discovery"),
        ("Technical Writer", "entry_to_mid", "clear technical documentation"),
        ("Developer Advocate", "mid", "developer education and feedback"),
        ("Customer Success Engineer", "entry_to_mid", "technical customer outcomes"),
        ("Product Operations Analyst", "entry_to_mid", "product process coordination"),
        ("Junior Business Analyst", "entry", "entry-level requirements analysis"),
    ],
    "Education / Social Good": [
        ("EdTech Developer", "entry_to_mid", "learning technology products"),
        ("Learning Experience Designer", "entry_to_mid", "digital learning experiences"),
        ("Career Guidance Technology Specialist", "entry_to_mid", "career support tools"),
        ("Digital Skills Trainer", "entry_to_mid", "practical technology education"),
        ("Accessibility Engineer", "mid", "inclusive digital systems"),
        ("Learning Analytics Specialist", "entry_to_mid", "learning data insights"),
        ("Education Platform Engineer", "mid", "reliable education platforms"),
        ("Civic Technology Developer", "entry_to_mid", "public-interest software"),
        ("Nonprofit Data Specialist", "entry_to_mid", "social-impact data use"),
        ("Digital Inclusion Specialist", "entry_to_mid", "equitable technology access"),
    ],
    "Tech Support / Operations": [
        ("IT Support Engineer", "entry", "technical user support"),
        ("ERP Developer", "entry_to_mid", "enterprise workflow systems"),
        ("Low-code Automation Developer", "entry_to_mid", "low-code business automation"),
        ("RPA Developer", "entry_to_mid", "robotic process automation"),
        ("Fresher QA Engineer", "entry", "entry-level software quality"),
        ("Systems Support Specialist", "entry_to_mid", "business system support"),
        ("Technical Operations Analyst", "entry_to_mid", "operational technology workflows"),
        ("Application Support Engineer", "entry_to_mid", "application issue resolution"),
        ("Service Desk Analyst", "entry", "frontline technical assistance"),
        ("Junior ERP Consultant", "entry", "entry-level enterprise solutions"),
    ],
}

FAMILY_SKILL_MIX = {
    "Software Engineering": ("frontend", "backend", "testing", "architecture"),
    "AI / ML / Agent": ("ai", "backend", "data", "testing"),
    "Data": ("data", "database", "product", "documentation"),
    "Cloud / DevOps": ("devops", "cloud", "architecture", "security"),
    "Security": ("security", "devops", "testing", "architecture"),
    "Product / Business": ("product", "soft-skill", "documentation", "data"),
    "Education / Social Good": ("product", "frontend", "data", "soft-skill"),
    "Tech Support / Operations": ("devops", "soft-skill", "backend", "documentation"),
}

FAMILY_TRAITS = {
    "Software Engineering": ("systematic", "patient with debugging"),
    "AI / ML / Agent": ("curious", "comfortable with experimentation"),
    "Data": ("analytical", "careful with evidence"),
    "Cloud / DevOps": ("reliability-minded", "calm during troubleshooting"),
    "Security": ("risk-aware", "attentive to detail"),
    "Product / Business": ("user-centered", "comfortable with ambiguity"),
    "Education / Social Good": ("empathetic", "motivated by social impact"),
    "Tech Support / Operations": ("service-oriented", "persistent with problems"),
}


def all_role_definitions() -> list[tuple[str, str, str, str]]:
    """Flatten curated role groups while preserving stable ordering."""
    return [
        (title, family, level, focus)
        for family, roles in ROLE_GROUPS.items()
        for title, level, focus in roles
    ]


def aliases_for(name: str) -> list[str]:
    """Create conservative search aliases without inventing terminology."""
    aliases = [name.lower()]
    acronym = "".join(word[0] for word in re.findall(r"[A-Za-z0-9]+", name))
    if 2 <= len(acronym) <= 6 and acronym.lower() != name.lower():
        aliases.append(acronym.lower())
    return aliases[:2]


def roles_using_category(category: str) -> list[str]:
    """Return representative career titles connected to a skill category."""
    titles = []
    for title, family, _level, _focus in all_role_definitions():
        if category in FAMILY_SKILL_MIX[family]:
            titles.append(title)
    return titles[:8]


def build_skills() -> list[dict[str, Any]]:
    """Build a 260-entry skill catalog from curated domain terms."""
    skills = []
    for category, names in SKILL_GROUPS.items():
        for index, name in enumerate(names):
            related = [
                names[(index + offset) % len(names)]
                for offset in (1, 2, 3)
            ]
            skills.append({
                "id": slugify(name),
                "name": name,
                "category": category,
                "level": SKILL_LEVELS[category],
                "aliases": aliases_for(name),
                "description": (
                    f"{name} supports practical {category} work through "
                    "repeatable, reviewable techniques."
                ),
                "used_in_roles": roles_using_category(category),
                "related_skills": related,
                "learning_resources_keywords": [
                    f"{name.lower()} fundamentals",
                    f"{name.lower()} practical project",
                ],
                "assessment_hint": (
                    f"Ask the learner to explain and demonstrate {name} "
                    "in a small, reviewable task."
                ),
            })
    return skills


def select_role_skills(family: str, role_index: int) -> tuple[list[str], list[str]]:
    """Select stable, varied skill sets from the role family mix."""
    categories = FAMILY_SKILL_MIX[family]
    required: list[str] = []
    nice: list[str] = []
    for category_index, category in enumerate(categories):
        names = SKILL_GROUPS[category]
        start = (role_index * 2 + category_index * 3) % len(names)
        required.extend([names[start], names[(start + 1) % len(names)]])
        nice.append(names[(start + 2) % len(names)])
    first_names = SKILL_GROUPS[categories[0]]
    second_names = SKILL_GROUPS[categories[1]]
    nice.extend([
        first_names[(role_index * 2 + 4) % len(first_names)],
        second_names[(role_index * 2 + 5) % len(second_names)],
    ])
    return list(dict.fromkeys(required)), list(dict.fromkeys(nice))


def market_level(level: str, family: str) -> str:
    """Choose a realistic qualitative market label."""
    if family == "AI / ML / Agent":
        return "emerging"
    if level == "advanced":
        return "medium"
    return "high"


def build_career(
    title: str, family: str, level: str, focus: str, role_index: int
) -> dict[str, Any]:
    """Build one detailed career profile from a curated role definition."""
    required, nice = select_role_skills(family, role_index)
    traits = FAMILY_TRAITS[family]
    return {
        "id": slugify(title),
        "title": title,
        "family": family,
        "level": level,
        "description": (
            f"A {title} works on {focus} by combining technical practice, "
            "team collaboration, and responsible delivery."
        ),
        "target_users": [
            f"Learners interested in {focus}",
            f"Early-career professionals building skills in {family.lower()}",
            f"Career changers who prefer practical projects related to {title.lower()}",
        ],
        "required_skills": required,
        "nice_to_have_skills": nice,
        "recommended_for": [
            focus, family.lower(), "project-based learning",
            "continuous improvement", traits[0],
        ],
        "avoid_if": [
            f"You strongly dislike the core work involved in {focus}",
            "You prefer roles with little ongoing learning or feedback",
            f"You are not willing to practice {required[0]} through hands-on work",
        ],
        "sample_projects": [
            f"Build a small {focus} solution for a student or community need",
            f"Create a documented {title.lower()} case study using public sample data",
            f"Improve an existing project by applying {required[0]} and {required[1]}",
        ],
        "daily_work": [
            f"Plan and implement tasks related to {focus}",
            f"Review work involving {required[0]} and {required[1]}",
            "Collaborate with teammates and clarify requirements",
            "Test outcomes, document decisions, and address defects",
        ],
        "growth_paths": [
            f"Senior {title}",
            f"{title} Team Lead",
            f"{family} Solutions Specialist",
        ],
        "market_relevance": {
            "level": market_level(level, family),
            "reason": (
                f"Organizations continue to need practical capability in {focus}; "
                "demand varies by region, industry, and experience."
            ),
        },
