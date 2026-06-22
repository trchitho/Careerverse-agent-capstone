# User Onboarding Guide

Welcome to the CareerVerse Agent! Follow these steps to navigate the platform, assess your tech career alignment, and preview study roadmaps.

## Who This Is For
- Computer Science students deciding on technical specs.
- Self-taught learners tracking missing capabilities.
- Tech enthusiasts seeking structured learning curriculums.

## What You Need Before Starting
- A web browser (Chrome, Firefox, Edge, Safari).
- A list of your current skills and interests.
- Your weekly study time budget in hours.

## Step 1: Open the Web UI
1. Verify the FastAPI backend API server is running on `http://127.0.0.1:8000`.
2. Start the local frontend dev server by running `npm run dev` in the `web` folder.
3. Open your browser and navigate to `http://localhost:5173` (or the port specified by Vite).

## Step 2: Fill in Your Learning Profile
Locate the **Profile Assessment Form** and complete the fields:
- **Name**: Enter your name (or a nickname).
- **Education**: Select/enter your educational background.
- **Interests**: Input comma-separated interest tags (e.g. `web development, AI, cloud`).
- **Skills**: Input comma-separated skills you already possess (e.g. `Python, CSS, Git`).
- **Career Goal**: State your target role (e.g. `Become a cloud devops engineer`).
- **Learning Style**: Choose between project-based or self-paced styles.
- **Time Budget**: Set weekly hour limits.

> [!CAUTION]
> **Data Privacy Alert**: Do not enter sensitive personal information such as passwords, address details, phone numbers, or upload raw CV files containing confidential text.

## Step 3: Review Career Recommendations
Click **Get Recommendations**. The Multi-Agent Coordinator validates input security, computes similarity scores, and outputs matches.
- Matches show percentage rankings based on Interest, Skill, and Goal alignment.
- Read the fit explanation text explaining why the path was suggested.

## Step 4: Review Skill Gaps
In the matched results, look at the **Skill Gap Card**:
- Mastered skills are highlighted in green.
- Missing skills are marked clearly to focus your study.
- A visual progress bar details your readiness score.

## Step 5: Review Roadmap
Review the week-by-week curriculum:
- Actions are scheduled according to your weekly hours budget.
- Focus on completing the suggested portfolio projects.

## Step 6: Submit Feedback
Use the **Feedback Widget** at the bottom of the card:
- Rate the suggestion (1 to 5 stars).
- Click the checkmark if the roadmap matches your expectations.
- Optionally add a brief comment (max 300 characters).

## Safety Notes
- The recommendations are designed for **educational guidance only**.
- It does not guarantee employment outcomes or replace professional counseling.
- The matcher is deterministic and relies on a local JSON dataset catalog.

## Troubleshooting
- **API Connection Error**: Check if the backend is running.
- **Form validation issues**: Ensure required fields are completed and commas separate multiple tags.
