import React from 'react';
import { SkillGapResult, CareerRecommendation } from '../types/api';

interface SkillGapCardProps {
  skillGap?: SkillGapResult;
  selectedCareer?: CareerRecommendation;
}

export const SkillGapCard: React.FC<SkillGapCardProps> = ({ skillGap, selectedCareer }) => {
  if (!selectedCareer) {
    return <p>Select a career recommendation on the left to inspect skill gap details.</p>;
  }

  const isTargetMatch = skillGap && skillGap.career_id === selectedCareer.career_id;
  const readinessPct = isTargetMatch ? skillGap.readiness_percentage : Math.round((selectedCareer.breakdown?.skill_match || 0) * 100);
  const missingSkills = isTargetMatch ? skillGap.missing_skills : selectedCareer.missing_skills;

  return (
    <div className="card" style={{ marginBottom: '1.5rem' }}>
      <h3 style={{ borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '0.5rem' }}>
        📊 Skill Gap: {selectedCareer.title}
      </h3>

      <div style={{ marginTop: '1rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontWeight: 600, fontSize: '0.95rem' }}>
          <span>Skill Readiness</span>
          <span style={{ color: 'var(--color-cyan)' }}>{readinessPct}%</span>
        </div>
        <div className="progress-container">
          <div className="progress-bar" style={{ width: `${readinessPct}%` }}></div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '1rem', marginTop: '0.5rem' }}>
        <div>
          <strong style={{ fontSize: '0.85rem', color: 'var(--color-success)' }}>🟢 Possessed Required Skills:</strong>
          <div className="skill-tags" style={{ marginTop: '0.4rem' }}>
            {selectedCareer.matched_skills.map(skill => (
              <span key={skill} className="skill-tag">
                {skill}
              </span>
            ))}
            {selectedCareer.matched_skills.length === 0 && (
              <span style={{ color: 'var(--text-muted)', fontSize: '0.85rem' }}>None</span>
            )}
          </div>
        </div>

        <div>
          <strong style={{ fontSize: '0.85rem', color: 'var(--color-danger)' }}>🔴 Missing Required Skills:</strong>
          <div className="skill-tags" style={{ marginTop: '0.4rem' }}>
            {missingSkills.map(skill => (
              <span key={skill} className="skill-tag missing">
                {skill}
              </span>
            ))}
            {missingSkills.length === 0 && (
              <span style={{ color: 'var(--color-success)', fontSize: '0.85rem' }}>No missing skills! You are 100% ready.</span>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
