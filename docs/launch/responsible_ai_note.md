# Responsible AI Note

This document describes the safety guidelines and AI guardrails of the CareerVerse Agent app.

### 1. Educational Guidance Only
All matching profiles, similarity rankings, and weekly study roadmaps are generated for **educational exploration purposes only**. They should be treated as guidance references, not as automated career placements or certified curricula.

### 2. No Employment Guarantees
The suggestions do not promise job matches, hiring conversions, interview invitations, or professional licensing. 

### 3. Not a Professional Counseling Service
The application does not replace professional academic advisors, career guidance counselors, or official university guidance centers.

### 4. No Clinical Assessments
The app does not perform clinical psychological evaluations, clinical aptitude tests, or mental/psychiatric diagnostics.

### 5. Transparency in Algorithmic Scoring
Rather than opaque generative models, CareerVerse uses **deterministic Jaccard similarity algorithms** to rank matches. This ensures that every recommendation is:
- **Auditable**: Inputs map directly to output rankings.
- **Repeatable**: Identical inputs yield identical outputs.
- **Explainable**: The fit scoring breakdowns (interests, skills, goals) are clearly presented.

### 6. Input Safety Layer
The orchestrator filters all inputs prior to processing:
- **Injection Blocker**: Flags override strings (e.g. *"ignore previous instructions"*).
- **Sanitizer**: Redacts credentials, tokens, or email fields automatically.

### 7. Human Review Encouraged
Users are strongly encouraged to verify suggested roadmaps and skills lists with human mentors, university staff, or industry specialists before making career decisions.
