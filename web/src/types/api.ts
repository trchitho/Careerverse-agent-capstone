export interface UserProfileRequest {
  name: string;
  education: string;
  interests: string[];
  skills: string[];
  career_goal: string;
  preferred_learning_style: 'project_based' | 'theory_first' | 'mixed';
  language: string;
  experience_level: 'beginner' | 'university' | 'career_changer';
  time_budget_hours_per_week: number;
}

export interface ScoreBreakdown {
  interest_match: number;
  skill_match: number;
  goal_match: number;
}

export interface CareerRecommendation {
  career_id: string;
  title: string;
  score: number;
  breakdown: ScoreBreakdown;
  matched_skills: string[];
  missing_skills: string[];
  fit_explanation?: string;
}

export interface SkillGapResult {
  career_id: string;
  missing_skills: string[];
  readiness_percentage: number;
}

export interface WeeklyTask {
  week: number;
  topic: string;
  description: string;
}

export interface RoadmapResult {
  career_id: string;
  duration_days: number;
  weekly_tasks: WeeklyTask[];
}

export interface UserSummary {
  name: string;
  experience_level: string;
  skills_count: number;
}

export interface AgentRecommendationResponse {
  user_summary: UserSummary;
  top_recommendations: CareerRecommendation[];
  skill_gap: SkillGapResult;
  personalized_roadmap: RoadmapResult;
  safety_notice: string;
  course_concepts_demonstrated?: string[];
}

export interface FeedbackRequest {
  session_id?: string;
  career_id?: string;
  career_title?: string;
  rating: number;
  helpful: boolean;
  comment?: string;
  source?: string;
}

export interface FeedbackResponse {
  id: string;
  created_at: string;
  status: string;
}

export interface MetricsSummary {
  total_feedback_count: number;
  average_rating: number;
  helpful_count: number;
  not_helpful_count: number;
  data_source: string;
  external_llm_enabled: boolean;
  app_version: string;
  environment: string;
}

export interface McpTool {
  name: string;
  description: string;
  input_schema?: Record<string, any>;
}

export interface McpSearchCareerResponse {
  career_id: string;
  title: string;
  required_skills: string[];
}

export interface ApiError {
  error: string;
  message: string;
  status_code: number;
  details?: Record<string, any> | null;
}
