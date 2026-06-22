# Privacy Note

This document describes how user data is processed by the CareerVerse Agent app and details the privacy controls.

### Data Minimization Design
The application is built on zero-knowledge and data minimization principles:
- **No Personal Identifiers**: Users do not need to register accounts, provide email addresses, input phone numbers, or upload files containing contact information.
- **No Document Parsing**: The MVP does not parse resumes, CV files, or official school transcripts.

### Feedback Submission Safeguards
When submitting ratings or comments using the Feedback Widget:
- **No Personal Fields**: The feedback collection schema lacks contact fields.
- **Redaction Middleware**: Comments undergo sanitization. Email addresses, tokens, and system paths are automatically redacted to `[Redacted due to input safety warning]` before writing to RAM.
- **Do Not Include Private Info**: Users are warned not to include names, passwords, or personal histories in the comment box.

### Storage Limitations
All feedback, session tokens, and saved snapshots are processed **in-memory** and stored within process RAM. There is no database storage, and all data is lost when the server restarts.

### Production Disclaimer
- This configuration is designed for local demonstration.
- It has not been audited or certified for GDPR, CCPA, or HIPAA compliance.
- A comprehensive third-party privacy review is required prior to public cloud hosting.
