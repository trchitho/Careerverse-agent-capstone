import React from 'react';
import { CareerRecommendation } from '../types/api';

interface RecommendationResultsProps {
  recommendations: CareerRecommendation[];
  concepts?: string[];
  onSelectCareer: (career: CareerRecommendation) => void;
  selectedCareerId?: string;
}

export const RecommendationResults: React.FC<RecommendationResultsProps> = ({
  recommendations,
  concepts,
  onSelectCareer,
  selectedCareerId,
}) => {
  if (!recommendations || recommendations.length === 0) {
    return <p>No recommendations available. Please fill out the form above.</p>;
  }

  return (
    <div className="recommendations-list">
      {recommendations.map((rec, index) => {
        const isSelected = selectedCareerId === rec.career_id;
        const totalScorePct = Math.round(rec.score * 100);

        return (
          <div
            key={rec.career_id}
            className="recommendation-item"
            style={{
              cursor: 'pointer',
              borderColor: isSelected ? 'var(--color-cyan)' : 'var(--color-accent)',
              backgroundColor: isSelected ? 'rgba(6, 182, 212, 0.04)' : undefined,
            }}
            onClick={() => onSelectCareer(rec)}
            role="button"
            aria-pressed={isSelected}
            tabIndex={0}
            onKeyDown={e => {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                onSelectCareer(rec);
              }
            }}
          >
            <div className="recommendation-header">
              <span className="recommendation-title">
                {index + 1}. {rec.title}
              </span>
              <span className="recommendation-score">Match: {totalScorePct}%</span>
            </div>

            <div className="score-breakdown-badges">
              <span className="score-badge">Interest: {Math.round((rec.breakdown?.interest_match || 0) * 100)}%</span>
              <span className="score-badge">Skill: {Math.round((rec.breakdown?.skill_match || 0) * 100)}%</span>
              <span className="score-badge">Goal: {Math.round((rec.breakdown?.goal_match || 0) * 100)}%</span>
            </div>

            {rec.fit_explanation && (
              <p style={{ fontStyle: 'italic', fontSize: '0.9rem', color: 'var(--text-secondary)', marginBottom: '0.75rem' }}>
                💡 {rec.fit_explanation}
              </p>
            )}

            <div style={{ marginTop: '0.5rem' }}>
              <strong style={{ fontSize: '0.85rem' }}>Possessed skills:</strong>
              <div className="skill-tags">
                {rec.matched_skills.slice(0, 8).map(skill => (
                  <span key={skill} className="skill-tag">
                    {skill}
                  </span>
                ))}
                {rec.matched_skills.length === 0 && <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>None</span>}
              </div>
            </div>

            <div style={{ marginTop: '0.75rem' }}>
              <strong style={{ fontSize: '0.85rem' }}>Missing skills preview:</strong>
              <div className="skill-tags">
                {rec.missing_skills.slice(0, 8).map(skill => (
                  <span key={skill} className="skill-tag missing">
                    {skill}
                  </span>
                ))}
                {rec.missing_skills.length === 0 && <span style={{ color: 'var(--text-success)', fontSize: '0.85rem' }}>None</span>}
              </div>
            </div>
            
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '0.75rem', textAlign: 'right' }}>
              Click to view detailed skill gap and daily learning roadmap.
            </p>
          </div>
        );
      })}

      {concepts && concepts.length > 0 && (
        <div style={{ marginTop: '1rem', padding: '1rem', backgroundColor: 'rgba(255,255,255,0.02)', borderRadius: '8px' }}>
          <strong style={{ fontSize: '0.85rem', display: 'block', marginBottom: '0.5rem' }}>📚 Capstone Concepts Demonstrated:</strong>
          <div className="skill-tags">
            {concepts.map(concept => (
              <span key={concept} style={{ fontSize: '0.75rem', padding: '0.15rem 0.4rem', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '4px', color: 'var(--text-secondary)' }}>
                {concept}
              </span>
            ))}
          </div>
        </div>
      )}
    </div>
  );
};
