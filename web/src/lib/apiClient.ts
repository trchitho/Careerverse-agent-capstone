import {
  UserProfileRequest,
  AgentRecommendationResponse,
  FeedbackRequest,
  FeedbackResponse,
  MetricsSummary,
  McpTool,
  McpSearchCareerResponse,
} from '../types/api';

const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000').replace(/\/$/, '');

async function safeFetch<T>(path: string, options?: RequestInit): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options?.headers || {}),
    },
  });

  if (!response.ok) {
    let errMessage = `HTTP error! Status: ${response.status}`;
    try {
      const errBody = await response.json();
      // Handle standard ErrorResponse layout or detail layout
      errMessage = errBody.message || errBody.detail || errMessage;
      if (typeof errMessage === 'object') {
        errMessage = JSON.stringify(errMessage);
      }
    } catch {
      // Ignore parse failure on error body
    }
    throw new Error(errMessage);
  }

  return response.json() as Promise<T>;
}

export const apiClient = {
  getHealth: () => safeFetch<{ status: string; message: string }>('/api/v1/health'),
  getHealthLive: () => safeFetch<{ status: string; message: string }>('/api/v1/health/live'),
  getHealthReady: () => safeFetch<{ status: string; message: string }>('/api/v1/health/ready'),

  getMetadata: () => safeFetch<Record<string, any>>('/api/v1/metadata'),

  validateProfile: (profile: UserProfileRequest) =>
    safeFetch<{ status: string; normalized_profile: Record<string, any> }>('/api/v1/profiles/validate', {
      method: 'POST',
      body: JSON.stringify(profile),
    }),

  recommendCareer: async (profile: UserProfileRequest, topK: number = 3): Promise<AgentRecommendationResponse> => {
    const raw = await safeFetch<any>(`/api/v1/recommend?top_k=${topK}`, {
      method: 'POST',
      body: JSON.stringify(profile),
    });

    const topRecommendations = (raw.top_recommendations || []).map((rec: any) => ({
      career_id: rec.career_id,
      title: rec.title,
      score: (rec.score || 0) / 100,
      breakdown: {
        interest_match: (rec.score_breakdown?.interest_score || 0) / 100,
        skill_match: (rec.score_breakdown?.skill_score || 0) / 100,
        goal_match: (rec.score_breakdown?.goal_score || 0) / 100,
      },
      matched_skills: rec.matched_skills || [],
      missing_skills: rec.missing_skills_preview || [],
      fit_explanation: rec.explanation,
    }));

    const topCareerId = topRecommendations[0]?.career_id || '';

    return {
      user_summary: raw.user_summary,
      top_recommendations: topRecommendations,
      skill_gap: {
        career_id: topCareerId,
        missing_skills: raw.skill_gap?.missing_skills || [],
        readiness_percentage: Math.round(raw.skill_gap?.readiness_score || 0),
      },
      personalized_roadmap: {
        career_id: raw.personalized_roadmap?.career_id || topCareerId,
        duration_days: 30,
        weekly_tasks: (raw.personalized_roadmap?.thirty_day_plan || []).map((w: any) => ({
          week: w.week,
          topic: w.focus || w.topic || '',
          description: w.checkpoint || w.description || '',
        })),
      },
      safety_notice: raw.safety_notice || '',
      course_concepts_demonstrated: raw.course_concepts_demonstrated || [],
    };
  },

  getTools: () => safeFetch<McpTool[]>('/api/v1/tools'),

  searchCareers: async (query: string): Promise<McpSearchCareerResponse[]> => {
    const raw = await safeFetch<any>(`/api/v1/mcp/search/careers?q=${encodeURIComponent(query)}`);
    const items = raw.items || [];
    return items.map((c: any) => ({
      career_id: c.career_id || c.id,
      title: c.title,
      required_skills: c.required_skills || [],
    }));
  },

  sendRecommendationFeedback: (feedback: FeedbackRequest) =>
    safeFetch<FeedbackResponse>('/api/v1/feedback/recommendation', {
      method: 'POST',
      body: JSON.stringify(feedback),
    }),

  getMetricsSummary: () => safeFetch<MetricsSummary>('/api/v1/metrics/summary'),
};
