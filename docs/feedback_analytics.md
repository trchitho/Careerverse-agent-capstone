# Feedback Analytics

## Overview
CareerVerse provides a local mechanism to solicit, store, and analyze user feedback on career guidance recommendations. It helps measure agent recommendation alignment, UI helpfulness, and user satisfaction while strictly adhering to privacy safeguards.

## Feedback Endpoint
- **Solicitation Route**: `POST /api/v1/feedback/recommendation`
- **Retrieval Route**: `GET /api/v1/feedback/summary`

### Schema Fields Stored
For each feedback submission, the ephemeral process storage records:
- `id`: Unique feedback uuid.
- `created_at`: Date-time of submission.
- `session_id` (Optional): ID tracking the user session context.
- `career_id` (Optional): Target career suggestion identifier.
- `career_title` (Optional): Target career suggestion name.
- `rating`: Numeric evaluation between `1` and `5`.
- `helpful`: Boolean indicating if the roadmap was helpful.
- `comment`: Sanitized, safe comment string (max 300 characters).
- `source`: Originator identifier (defaults to `web`).

## Fields Not Stored
To protect user anonymity, the feedback collector strictly avoids soliciting or logging:
- User email addresses.
- Phone numbers or contact details.
- Real names, student IDs, or IP logs.
- Raw career profiles containing detailed personal histories.

## Safety Filtering
The `app/services/feedback_service.py` evaluates all feedback comments prior to storage:
- **Redaction Logic**: If comments match patterns indicating email addresses, system paths, API tokens, or prompt injection payloads, they are automatically replaced with a safety tag: `[Redacted due to input safety warning]`.
- **Length Constraint**: All comments are truncated to 300 characters to prevent buffer issues or database flooding attempts.

## Metrics Summary
- **Route**: `GET /api/v1/metrics/summary`
- **Output Data**: Returns aggregated numbers including:
  - `total_feedback_count`
  - `average_rating`
  - `helpful_count`
  - `not_helpful_count`
  - `app_mode` (e.g. `development`/`production` indicator)
  - `llm_fallback_enabled` (indicating if explanation generation is running offline or via API models)

## In-Memory Storage Limitation
This is a local, process-ephemeral memory database (`InMemoryFeedbackRepository`) suitable for demo operations. All records reside in process RAM and will clear when the API container or dev server restarts. It is not an enterprise analytics warehouse.
