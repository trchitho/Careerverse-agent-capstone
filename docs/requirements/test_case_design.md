# Test Case Design

This document details the conventions, schemas, and design guidelines for FR and NFR test cases.

## 1. Case ID Convention
- **Functional Requirements (FR)**:
  - `FR-{REQ_NUMBER}-TC-{CASE_NUMBER}`
  - Example: `FR-02-TC-001` (First test case for Profile Validation FR-02).
- **Non-Functional Requirements (NFR)**:
  - `NFR-{REQ_NUMBER}-TC-{CASE_NUMBER}`
  - Example: `NFR-01-TC-001` (First test case for Security Hygiene NFR-01).

## 2. Test Case Schema Structure
Every test case in the `fr_cases.json` and `nfr_cases.json` datasets adheres to the following fields:
- `case_id`: String, unique identifier matching ID conventions.
- `requirement_id`: String, parent requirement (e.g. `FR-03`, `NFR-01`).
- `requirement_type`: String, either `FR` or `NFR`.
- `title`: String, concise test intent.
- `description`: String, descriptive test details.
- `category`: String, category tag (`positive`, `negative`, `boundary`, `edge`, `regression`, `compliance`, `abuse`, etc.).
- `priority`: String, priority rank (`P0`, `P1`, `P2`).
- `preconditions`: List of Strings, setup preconditions.
- `input_data`: Dictionary, sample request arguments or verification variables.
- `steps`: List of Strings, logical test runner operations.
- `expected`: Dictionary/String, expected result structure or target messages.
- `negative`: Boolean, indicates if this case asserts error handling/validation rejection.
- `automation_level`: String, indicates if check is executable or document scan (`automated`, `semi-automated`, `manual`).
- `verification_method`: String, check execution technique (`api_call`, `unit_test`, `file_scan`, `text_matching`).
- `target_files`: List of Strings, project files containing verified implementation.
- `target_endpoints`: List of Strings, endpoint URLs verified.
- `tags`: List of Strings, extra tag details.

## 3. Test Design Categories
- **Positive Testing**: Asserts that correct arguments produce expected HTTP 200 outputs.
- **Negative Testing**: Asserts that malformed payloads return specific schema error contracts.
- **Boundary Testing**: Validates system performance at extremes (e.g., maximum field length, maximum list size).
- **Abuse/Security Testing**: Passes prompt injection strings or private email credentials to test protection levels.
- **Compliance / File Testing**: Asserts that file directories contain necessary deployment, launch, or workflow scripts.
