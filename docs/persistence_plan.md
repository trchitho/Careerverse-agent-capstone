# Persistence Plan

## Overview
This document outlines the data access layer design, current file-based storage architecture, and the roadmap toward a future relational database persistence layer for the CareerVerse Agent system. The architecture separates business logic from data access via repository interfaces, enabling flexible storage engine swaps.

## Current JSON Data Source
Currently, all reference data for careers, skills, and study roadmaps resides in local static JSON datasets within the `app/data/` folder:
- `careers.json`
- `skills.json`
- `roadmaps.json`

These datasets are loaded and parsed through the standard data access layer. LRU caching is applied at the module level to avoid repeated file IO during execution.

## Repository Interfaces
To cleanly decouple data operations, we introduce repository interfaces using Python's structural subtyping (`typing.Protocol`):
1. `CareerRepository`: Defines methods to list all careers, search by keyword, and get career by ID.
2. `SkillRepository`: Defines methods to list all skills and retrieve skill metadata by name, ID, or alias.
3. `RoadmapRepository`: Defines methods to list roadmaps and retrieve roadmaps matching a specific career ID.
4. `SavedRecommendationRepository`: Defines storage operations (save, list, retrieve, clear) for saved recommendation snapshots.

These interfaces are located at `app/repositories/interfaces.py`.

## JSON Repository Implementations
We provide JSON-backed implementations of the catalog repository protocols:
- `JsonCareerRepository`: Implements `CareerRepository` using `careers.json`.
- `JsonSkillRepository`: Implements `SkillRepository` using `skills.json`.
- `JsonRoadmapRepository`: Implements `RoadmapRepository` using `roadmaps.json`.

These repositories read deep copies of data loaded from JSON files to prevent tests or runtime tasks from mutating the cached data structures.

## Optional PostgreSQL Path
PostgreSQL is a future path, not required by the current MVP.
To facilitate the transition to PostgreSQL in the future, the following elements are prepared:
- Configuration placeholders in `.env.example`: `DATA_SOURCE=json` and `DATABASE_URL=`
- Decoupled interfaces that can easily be re-implemented using SQLAlchemy or SQLModel without altering route handlers or agent controllers.
- An in-memory/process-local demo session repository, allowing recommendations to be stored in an ephemeral format without database schema migrations.

## Session-Safe Saved Recommendations
The session-safe saved recommendations layer allows students to save recommendations using a temporary `session_id`. Stored records are handled by an `InMemorySavedRecommendationRepository` which acts as an ephemeral mock database.

## What Is Not Implemented
- A live PostgreSQL database engine or connection pool is not implemented.
- Database schemas, migrations (Alembic), and direct SQL execution are not included in the MVP.
- Production-grade multi-user persistent tables or distributed session storage.

## Migration Checklist
If PostgreSQL is adopted in the future, the migration will require:
1. Installing `SQLAlchemy` or `asyncpg` dependencies.
2. Implementing `SqlCareerRepository`, `SqlSkillRepository`, `SqlRoadmapRepository`, and `SqlSavedRecommendationRepository` satisfying the respective repository protocols.
3. Generating Alembic migration scripts from Pydantic/SQLAlchemy models.
4. Injecting SQL repository instances instead of JSON instances in router configurations.

## Safety and Privacy Notes
- The repository layer does not mutate reference JSON datasets.
- Sensitive user inputs or raw prompts are not recorded in persistence layers.
- Session IDs are validated to prevent resource exhaustion or directory traversal risks.
