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

  recommendCareer: (profile: UserProfileRequest, topK: number = 3) =>
    safeFetch<AgentRecommendationResponse>(`/api/v1/recommend?top_k=${topK}`, {
      method: 'POST',
      body: JSON.stringify(profile),
    }),

  getTools: () => safeFetch<McpTool[]>('/api/v1/tools'),

  searchCareers: (query: string) =>
    safeFetch<McpSearchCareerResponse[]>(`/api/v1/mcp/search/careers?q=${encodeURIComponent(query)}`),

  sendRecommendationFeedback: (feedback: FeedbackRequest) =>
    safeFetch<FeedbackResponse>('/api/v1/feedback/recommendation', {
      method: 'POST',
      body: JSON.stringify(feedback),
    }),

  getMetricsSummary: () => safeFetch<MetricsSummary>('/api/v1/metrics/summary'),
};
