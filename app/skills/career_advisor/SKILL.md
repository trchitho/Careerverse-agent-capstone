---
name: career-advisor
description: Provide structured educational career recommendations, skill gap analysis, learning roadmaps, and portfolio project guidance for students, early-career learners, and career changers. Use when a user supplies education, interests, skills, career goals, learning preferences, or asks to run the CareerVerse multi-agent workflow and MCP-style career tools.
---

# Career Advisor Skill

## 1. Purpose

Use this skill to provide educational career guidance through the implemented CareerVerse
system. Recommend career options, explain deterministic scores, analyze skill gaps, and return
a practical learning roadmap.

Use the local `UserProfileRequest`, scoring engine, multi-agent workflow, domain dataset, and
MCP-style tools. Do not replace professional career counseling or guarantee employment.

## 2. When to Use

Use this skill when the user provides or requests:

- education background, interests, current skills, or a career goal;
- a preferred learning style, experience level, language, or weekly time budget;
- ranked career recommendations or career exploration;
- skill gap analysis or priority skills;
- a 30-day or 8-week learning roadmap;
- portfolio project suggestions based on a target career.

## 3. When Not to Use

Do not use this skill to:

- diagnose psychological, psychiatric, or clinical conditions;
- guarantee that a major, role, salary, or career decision is correct;
- provide legal, financial, or medical advice;
- request unnecessary sensitive or private personal data;
- process a real CV containing private data without informed user consent;
- replace a mentor, teacher, counselor, or qualified career advisor.

## 4. Required Inputs

Require these fields before running the complete recommendation workflow:

```json
{
  "name": "Demo User",
  "education": "Final-year IT student",
  "interests": ["AI", "web development"],
  "skills": ["Python", "React", "SQL"],
  "career_goal": "Become an AI full-stack developer"
}
```

Use synthetic demo users in public examples. Ask only for missing, non-sensitive information.
