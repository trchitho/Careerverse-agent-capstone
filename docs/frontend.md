# Frontend Web UI

## Overview
The frontend is a lightweight, responsive dashboard designed for students to assess their career profiles, view recommended paths, trace skill gaps, and explore educational roadmaps interactively.

## Tech Stack
- **React 18** (UI components)
- **TypeScript** (Static typing)
- **Vite** (Rapid development server and build tool)
- **Vanilla CSS** (Custom styles with dark/light themes and custom variables)

## Folder Structure
```text
web/
├── package.json
├── tsconfig.json
├── vite.config.ts
├── index.html
├── .env.example
├── README.md
└── src/
    ├── main.tsx
    ├── App.tsx
    ├── styles.css
    ├── types/
    │   └── api.ts
    ├── lib/
    │   └── apiClient.ts
    └── components/
        ├── ProfileForm.tsx
        ├── RecommendationResults.tsx
        ├── SkillGapCard.tsx
        ├── RoadmapPreview.tsx
        ├── SafetyNotice.tsx
        ├── FeedbackWidget.tsx
        ├── McpToolsExplorer.tsx
        └── StatusBanner.tsx
```

## Environment Variables
The build and runtime options are managed via Vite environment variables:
- `VITE_API_BASE_URL`: Sets the target URL for the FastAPI backend (defaults to `http://127.0.0.1:8000`).

## Running Locally
Navigate to the `web` folder and start the dev server:
```bash
cd web
npm install
npm run dev
```

## Backend API Integration
- The API client is located in `web/src/lib/apiClient.ts`.
- Calls are structured under the versioned namespace `/api/v1/`.

## Main Screens
1. **Profile Input Form**: Collects skills, interests, goals, and learning constraints.
2. **Career Matches Panel**: Displays top matching results with matching similarity scores.
3. **Skill Gap Details**: Highlights possessed and missing competencies with readiness indicators.
4. **Roadmap Curriculum**: Traces week-by-week checkpoints.

## Accessibility Notes
- All interactive forms include semantic labels (`htmlFor` matching input `id`).
- High-contrast keyboard focus indicators (`:focus-visible`) are configured across controls.
- Keyboard navigation is fully supported for selection triggers.

## Safety Notice Display
The `SafetyNotice.tsx` component is prominently shown above recommendations to verify learners understand outcomes are guidance-only.

## Feedback Widget
The `FeedbackWidget.tsx` lets users rate their recommendations without soliciting personal information.

## Build Command
Generate production-ready assets:
```bash
cd web
npm run build
```

## Limitations
The frontend does not implement login or production authentication. No personal information or secure user profiles are registered.
