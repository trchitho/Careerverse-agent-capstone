import React, { useState } from 'react';
import { UserProfileRequest } from '../types/api';

interface ProfileFormProps {
  onSubmit: (profile: UserProfileRequest, topK: number) => void;
  loading: boolean;
}

export const ProfileForm: React.FC<ProfileFormProps> = ({ onSubmit, loading }) => {
  const [name, setName] = useState('Demo Student');
  const [education, setEducation] = useState('Final-year IT Student');
  const [interestsInput, setInterestsInput] = useState('AI, web development, product building');
  const [skillsInput, setSkillsInput] = useState('Python, React, SQL');
  const [careerGoal, setCareerGoal] = useState('Become an AI full-stack developer');
  const [learningStyle, setLearningStyle] = useState<'project_based' | 'theory_first' | 'mixed'>('project_based');
  const [language, setLanguage] = useState('en');
  const [experienceLevel, setExperienceLevel] = useState<'beginner' | 'university' | 'career_changer'>('university');
  const [timeBudget, setTimeBudget] = useState(8);
  const [topK, setTopK] = useState(3);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    const interests = interestsInput.split(',').map(s => s.trim()).filter(Boolean);
    const skills = skillsInput.split(',').map(s => s.trim()).filter(Boolean);

    onSubmit(
      {
        name,
        education,
        interests,
        skills,
        career_goal: careerGoal,
        preferred_learning_style: learningStyle,
        language,
        experience_level: experienceLevel,
        time_budget_hours_per_week: timeBudget,
      },
      topK
    );
  };

  return (
    <form className="card" onSubmit={handleSubmit} aria-label="Student Profile Assessment Form">
      <h3 style={{ marginBottom: '1.25rem' }}>🎯 Profile Assessment Form</h3>
      
      <div className="form-group">
        <label htmlFor="student-name">Full Name *</label>
        <input
          id="student-name"
          className="input-field"
          type="text"
          required
          value={name}
          onChange={e => setName(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label htmlFor="student-education">Education / Background *</label>
        <input
          id="student-education"
          className="input-field"
          type="text"
          required
          value={education}
          onChange={e => setEducation(e.target.value)}
        />
      </div>

      <div className="form-group">
        <label htmlFor="student-interests">Interests (comma separated) *</label>
        <input
          id="student-interests"
          className="input-field"
          type="text"
          required
          value={interestsInput}
          onChange={e => setInterestsInput(e.target.value)}
          placeholder="e.g. AI, Cloud, UX Design"
        />
      </div>

      <div className="form-group">
        <label htmlFor="student-skills">Skills You Already Have (comma separated)</label>
        <input
          id="student-skills"
          className="input-field"
          type="text"
          value={skillsInput}
          onChange={e => setSkillsInput(e.target.value)}
          placeholder="e.g. Python, SQL, JS"
        />
      </div>

      <div className="form-group">
        <label htmlFor="student-goal">Career Goal / Objective *</label>
        <input
          id="student-goal"
          className="input-field"
          type="text"
          required
          value={careerGoal}
          onChange={e => setCareerGoal(e.target.value)}
          placeholder="e.g. Become a data engineer"
        />
      </div>

      <div className="form-group">
        <label htmlFor="student-style">Preferred Learning Style *</label>
        <select
          id="student-style"
          className="select-field"
          value={learningStyle}
          onChange={e => setLearningStyle(e.target.value as any)}
        >
          <option value="project_based">Project Based</option>
          <option value="theory_first">Theory First</option>
          <option value="mixed">Mixed</option>
        </select>
      </div>

      <div className="form-group">
        <label htmlFor="student-level">Experience Level *</label>
        <select
          id="student-level"
          className="select-field"
          value={experienceLevel}
          onChange={e => setExperienceLevel(e.target.value as any)}
        >
          <option value="beginner">Beginner / High School</option>
          <option value="university">University Student</option>
          <option value="career_changer">Career Changer</option>
        </select>
      </div>

      <div className="form-group" style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem' }}>
        <div>
          <label htmlFor="student-budget">Hours / Week *</label>
          <input
            id="student-budget"
            className="input-field"
            type="number"
            min={1}
            max={100}
            required
            value={timeBudget}
            onChange={e => setTimeBudget(Number(e.target.value))}
          />
        </div>
        <div>
          <label htmlFor="student-topk">Max Results *</label>
          <input
            id="student-topk"
            className="input-field"
            type="number"
            min={1}
            max={10}
            required
            value={topK}
            onChange={e => setTopK(Number(e.target.value))}
          />
        </div>
      </div>

      <div className="form-group">
        <label htmlFor="student-lang">Preferred Language *</label>
        <input
          id="student-lang"
          className="input-field"
          type="text"
          required
          value={language}
          onChange={e => setLanguage(e.target.value)}
        />
      </div>

      <div style={{ display: 'flex', gap: '1rem', marginTop: '1.5rem' }}>
        <button className="btn btn-primary" type="submit" disabled={loading} style={{ flex: 1 }}>
          {loading ? 'Processing...' : 'Get Recommendations'}
        </button>
        <button
          className="btn btn-secondary"
          type="button"
          disabled={loading}
          onClick={() => {
            setName('');
            setEducation('');
            setInterestsInput('');
            setSkillsInput('');
            setCareerGoal('');
            setLearningStyle('project_based');
            setLanguage('en');
            setExperienceLevel('university');
            setTimeBudget(8);
            setTopK(3);
          }}
        >
          Reset
        </button>
      </div>
    </form>
  );
};
