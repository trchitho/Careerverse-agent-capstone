# Explanation Service

## Overview
The `ExplanationService` generates educational explanations detailing why a specific career is recommended based on the user's profile interests, skills, and goals. It supports both static local logic and an optional advanced LLM engine.

## Offline Fallback
By default, the explanation service operates offline using local rules. The local fallback builder:
- Inspects matched and missing skills between the user and recommended role.
- Highlights common interests and aligns the guidance to the user's career path.
- Appends general disclaimers to clearly separate guidance from a guarantee of employment.

## Optional LLM Mode
External LLM explanations are disabled by default.
If LLM explanations are enabled, the service leverages the Google Gemini API to dynamically expand the fit details. To utilize this mode:
- The system must have `ENABLE_LLM_EXPLANATIONS` set to true.
- A valid `GOOGLE_API_KEY` must be configured in environment variables.

If LLM Mode is enabled but the API key is missing or calls fail, the system falls back gracefully to the offline explanation.

## Environment Variables
The explanation service behaviour is controlled by:
- `ENABLE_LLM_EXPLANATIONS`: Boolean setting (default: false)
- `MODEL_NAME`: The Gemini model identifier (default: gemini-2.5-flash)
- `GOOGLE_API_KEY`: API credential (default: empty)

## Safety Rules
- Under no circumstances does the explanation service output raw model responses or internal prompts to the user.
- If a security warning or prompt injection signature is detected in the user profile (e.g. "ignore previous instructions"), the explanation is redacted to a standard validation notice: "Fit analysis unavailable due to profile input validation warning."

## Data Minimization
To uphold privacy rules, only non-identifying profile fields (interests, skills, career_goal) are evaluated for matching. Private metadata (such as full names or emails) is excluded from external calls.

## Testing
- Tests execute offline without requiring network calls or active Gemini keys.
- Mock assertions in the test suite ensure that the local fallback mechanism is called when `ENABLE_LLM_EXPLANATIONS` is set to false.

## Limitations
- Local fallback explanations are template-driven and may appear repetitive.
- Optional Gemini models are subject to external service latency, API limits, and potential network interruptions.
