import React, { useState, useEffect } from 'react';
import { apiClient } from './lib/apiClient';
import { StatusBanner } from './components/StatusBanner';
import { ProfileForm } from './components/ProfileForm';
import { RecommendationResults } from './components/RecommendationResults';
import { SkillGapCard } from './components/SkillGapCard';
import { RoadmapPreview } from './components/RoadmapPreview';
import { FeedbackWidget } from './components/FeedbackWidget';
import { McpToolsExplorer } from './components/McpToolsExplorer';
import { SafetyNotice } from './components/SafetyNotice';
import { UserProfileRequest, AgentRecommendationResponse, CareerRecommendation, MetricsSummary } from './types/api';

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://127.0.0.1:8000';

export const App: React.FC = () => {
  const [healthy, setHealthy] = useState<boolean | null>(null);
  const [metrics, setMetrics] = useState<MetricsSummary | null>(null);
  const [loading, setLoading] = useState(false);
  const [errorMsg, setErrorMsg] = useState<string | null>(null);
  const [response, setResponse] = useState<AgentRecommendationResponse | null>(null);
  const [selectedCareer, setSelectedCareer] = useState<CareerRecommendation | undefined>(undefined);
  const [sessionId] = useState(() => `session-${Math.random().toString(36).substring(2, 11)}`);

  useEffect(() => {
    apiClient.getHealthReady()
      .then(res => setHealthy(res.status === 'ok'))
      .catch(() => setHealthy(false));
      
    fetchMetrics();
  }, []);

  useEffect(() => {
    if (selectedCareer) {
      setTimeout(() => {
        const element = document.getElementById('details-section');
        if (element) {
          element.scrollIntoView({ behavior: 'smooth', block: 'start' });
        }
      }, 80);
    }
  }, [selectedCareer]);

  const fetchMetrics = async () => {
    try {
      const data = await apiClient.getMetricsSummary();
      setMetrics(data);
    } catch {
      // Ignore background fetch failure
    }
  };

  const handleProfileSubmit = async (profile: UserProfileRequest, topK: number) => {
    setLoading(true);
    setErrorMsg(null);
    setResponse(null);
    setSelectedCareer(undefined);

    try {
      const data = await apiClient.recommendCareer(profile, topK);
      setResponse(data);
      if (data.top_recommendations && data.top_recommendations.length > 0) {
        setSelectedCareer(data.top_recommendations[0]);
      }
    } catch (err: any) {
      setErrorMsg(err.message || 'Failed to generate recommendations. Verify backend is running.');
    } finally {
      setLoading(false);
    }
  };

  const handleFeedbackSubmitted = () => {
    fetchMetrics();
  };

  return (
    <div className="container">
      <header>
        <StatusBanner healthy={healthy} apiUrl={API_BASE_URL} />
        <h1>CareerVerse Agent Dashboard</h1>
        <p style={{ textAlign: 'center', maxWidth: '800px', margin: '0 auto 2rem auto', color: 'var(--text-secondary)' }}>
          A deterministic multi-agent backend demonstrator for the Kaggle Capstone. Input your skills, interests, and budget to compute job fits, trace missing skill competencies, and map day-by-day learning checks.
        </p>
      </header>

      <main className="dashboard-grid">
        <section aria-label="Input Assessment Profile">
          <ProfileForm onSubmit={handleProfileSubmit} loading={loading} />
          
          {metrics && (
            <div className="card" style={{ marginTop: '1.5rem' }}>
              <h4>📊 System Feedback Quality Metrics</h4>
              <ul style={{ listStyle: 'none', marginTop: '0.5rem', fontSize: '0.85rem', color: 'var(--text-secondary)' }}>
                <li>Total Feedbacks Submitted: <strong style={{ color: 'var(--text-primary)' }}>{metrics.total_feedback_count}</strong></li>
                <li>Average Recommendation Rating: <strong style={{ color: 'var(--color-cyan)' }}>{metrics.average_rating}/5.00</strong></li>
                <li>Helpful matches: <strong style={{ color: 'var(--color-success)' }}>{metrics.helpful_count}</strong> | Unhelpful: {metrics.not_helpful_count}</li>
                <li style={{ marginTop: '0.5rem', fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                  App Version: {metrics.app_version} | Mode: {metrics.environment} | Data: {metrics.data_source}
                </li>
              </ul>
            </div>
          )}
        </section>

        <section aria-label="Assessment Outcomes and Recommendations">
          {loading && (
            <div className="card" style={{ textAlign: 'center', padding: '3rem' }}>
              <div className="spinner"></div>
              <p>Analyzing profile constraints...</p>
              <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>SkillGapAgent and RoadmapAgent are coordinating...</p>
            </div>
          )}

          {errorMsg && (
            <div className="card" style={{ borderColor: 'var(--color-danger)', backgroundColor: 'rgba(239, 68, 68, 0.05)' }}>
              <h3 style={{ color: 'var(--color-danger)' }}>⚠️ Recommendation Failed</h3>
              <p style={{ color: 'var(--text-primary)', marginTop: '0.5rem' }}>{errorMsg}</p>
            </div>
          )}

          {response && (
            <div style={{ display: 'flex', gap: '1.5rem', flexDirection: 'column' }}>
              <SafetyNotice notice={response.safety_notice} />

              <div className="card">
                <h3>🏆 Career Matches Found ({response.top_recommendations.length})</h3>
                <p style={{ fontSize: '0.875rem', color: 'var(--text-muted)' }}>
                  Showing career recommendations for <strong>{response.user_summary.name}</strong> ({response.user_summary.experience_level}) with {response.user_summary.skills_count} skills.
                </p>
                <RecommendationResults
                  recommendations={response.top_recommendations}
                  concepts={response.course_concepts_demonstrated}
                  onSelectCareer={setSelectedCareer}
                  selectedCareerId={selectedCareer?.career_id}
                />
              </div>

              {selectedCareer && (
                <div id="details-section" style={{ display: 'flex', gap: '1.5rem', flexDirection: 'column' }}>
                  <SkillGapCard skillGap={response.skill_gap} selectedCareer={selectedCareer} />
                  <RoadmapPreview roadmap={response.personalized_roadmap} selectedCareer={selectedCareer} />
                  
                  <div className="card">
                    <FeedbackWidget
                      sessionId={sessionId}
                      careerId={selectedCareer.career_id}
                      careerTitle={selectedCareer.title}
                      onSubmitted={handleFeedbackSubmitted}
                    />
                  </div>
                </div>
              )}
            </div>
          )}

          {!loading && !errorMsg && !response && (
            <div className="card" style={{ textAlign: 'center', padding: '4rem 2rem', borderStyle: 'dashed' }}>
              <h3 style={{ color: 'var(--text-secondary)' }}>Welcome to CareerVerse</h3>
              <p>Please enter your profile details on the left and submit to view personalized tech career guidance results.</p>
            </div>
          )}
        </section>
      </main>

      <section aria-label="MCP Server Tools Explorer">
        <McpToolsExplorer />
      </section>

      <footer>
        <p>CareerVerse Agent — AI Career Guidance MVP. Built for the Kaggle Capstone Competitions.</p>
        <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
          This system is in development. No production login or DB is active in the current local showcase.
        </p>
      </footer>
    </div>
  );
};
export default App;
