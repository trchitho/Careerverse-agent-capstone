import React from 'react';
import { RoadmapResult, CareerRecommendation } from '../types/api';

interface RoadmapPreviewProps {
  roadmap?: RoadmapResult;
  selectedCareer?: CareerRecommendation;
}

export const RoadmapPreview: React.FC<RoadmapPreviewProps> = ({ roadmap, selectedCareer }) => {
  if (!selectedCareer) {
    return null;
  }

  const isTargetMatch = roadmap && roadmap.career_id === selectedCareer.career_id;
  const tasks = isTargetMatch ? roadmap.weekly_tasks : [];
  const duration = isTargetMatch ? roadmap.duration_days : 30;

  return (
    <div className="card" style={{ marginBottom: '1.5rem' }}>
      <h3 style={{ borderBottom: '1px solid rgba(255,255,255,0.08)', paddingBottom: '0.5rem' }}>
        📅 Learning Roadmap ({duration} Days)
      </h3>

      {!isTargetMatch ? (
        <p style={{ marginTop: '1rem', color: 'var(--text-muted)' }}>
          Detailed roadmap is loading or was not retrieved for this specific path.
        </p>
      ) : (
        <div style={{ marginTop: '1rem' }}>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {tasks.map(task => (
              <div
                key={task.week}
                style={{
                  borderLeft: '2px solid var(--color-cyan)',
                  paddingLeft: '1rem',
                  marginLeft: '0.5rem',
                }}
              >
                <div style={{ fontWeight: 600, color: 'var(--color-cyan)', fontSize: '0.95rem' }}>
                  Week {task.week}: {task.topic}
                </div>
                <p style={{ fontSize: '0.9rem', color: 'var(--text-secondary)', marginTop: '0.25rem', marginBottom: 0 }}>
                  {task.description}
                </p>
              </div>
            ))}

            {tasks.length === 0 && (
              <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>
                No task checkpoints configured for this career roadmap.
              </p>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
