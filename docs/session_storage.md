# Session-Safe Saved Recommendations

## Overview
The Saved Recommendations framework provides an ephemeral persistence storage capability for session snapshots. This enables storing and listing recommendations generated for a given session.

## Demo Session IDs
Users provide an arbitrary `session_id` string when saving recommendations.
- Recommended format: alphanumeric slugs or generated UUIDs (e.g. `demo-session-001`, `session-12345`).
- Blank or whitespace-only session IDs are rejected with an HTTP 400 Bad Request status code.

## Stored Fields
To protect user privacy, only static recommendation metadata is stored:
- `id`: Unique snapshot identifier.
- `session_id`: Provided session reference.
- `created_at`: ISO timestamp of generation.
- `title`: Display title of recommendation.
- `career_id`: Reference code of career path.
- `career_title`: Name of target career.
- `score`: Relevance evaluation score.
- `summary`: Short summary of matching reason.
- `safety_notice`: Standard system disclaimer.

## Fields Not Stored
To prevent leakage:
- Raw user profile structures, emails, personal information, passwords, and API credentials are not stored.
- Malicious prompt inputs or injection strings are entirely excluded.

## In-Memory Storage Limitation
The default demo session store, `InMemorySavedRecommendationRepository`, is completely process-local.
- All stored recommendation snapshots are lost when the FastAPI process terminates or restarts.
- This is not production authentication and must not be used for long-term production persistence.

## Privacy Notes
- No personally identifiable information (PII) is written to disk or logged.
- The storage system contains no access controls beyond checking the matching `session_id`.

## Future Authentication Path
This is not production authentication.
A future path to production authentication will include:
1. Swapping `InMemorySavedRecommendationRepository` for a SQL database storage.
2. Integrating OAuth2 or password-based JWT authentication layers.
3. Restricting saved recommendation retrieval to the authenticated user ID.
