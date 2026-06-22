import React, { useState } from 'react';
import { apiClient } from '../lib/apiClient';

interface FeedbackWidgetProps {
  careerId?: string;
  careerTitle?: string;
  sessionId?: string;
  onSubmitted?: () => void;
}

export const FeedbackWidget: React.FC<FeedbackWidgetProps> = ({
  careerId,
  careerTitle,
  sessionId,
  onSubmitted,
}) => {
  const [rating, setRating] = useState<number>(5);
  const [helpful, setHelpful] = useState<boolean>(true);
  const [comment, setComment] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [statusMsg, setStatusMsg] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

  const handleRatingClick = (r: number) => {
    setRating(r);
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setSubmitting(true);
    setStatusMsg(null);

    try {
      await apiClient.sendRecommendationFeedback({
        session_id: sessionId || 'demo-session',
        career_id: careerId,
        career_title: careerTitle,
        rating,
        helpful,
        comment: comment.trim() || undefined,
      });
      setStatusMsg({ type: 'success', text: 'Thank you for your feedback!' });
      setComment('');
      if (onSubmitted) {
        onSubmitted();
      }
    } catch (err: any) {
      setStatusMsg({ type: 'error', text: err.message || 'Failed to submit feedback.' });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="feedback-widget">
      <h4 style={{ marginBottom: '0.5rem' }}>💬 Provide Recommendation Feedback</h4>
      <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
        Let us know if this career match aligns with your expectations.
      </p>

      {statusMsg && (
        <div
          style={{
            padding: '0.75rem',
            borderRadius: '6px',
            fontSize: '0.875rem',
            margin: '0.5rem 0',
            backgroundColor: statusMsg.type === 'success' ? 'rgba(16, 185, 129, 0.1)' : 'rgba(239, 68, 68, 0.1)',
            color: statusMsg.type === 'success' ? 'var(--color-success)' : 'var(--color-danger)',
          }}
          role="status"
        >
          {statusMsg.text}
        </div>
      )}

      <form onSubmit={handleSubmit} style={{ marginTop: '1rem' }}>
        <div className="form-group">
          <label style={{ fontSize: '0.85rem' }}>Rate this match (1-5) *</label>
          <div className="rating-buttons" role="group" aria-label="Select rating out of 5 stars">
            {[1, 2, 3, 4, 5].map(num => (
              <button
                key={num}
                type="button"
                className={`rating-btn ${rating === num ? 'selected' : ''}`}
                onClick={() => handleRatingClick(num)}
                aria-label={`Rate ${num} out of 5`}
              >
                {num}
              </button>
            ))}
          </div>
        </div>

        <div className="form-group" style={{ display: 'flex', gap: '1.5rem', alignItems: 'center' }}>
          <span style={{ fontSize: '0.85rem', fontWeight: 600 }}>Was this match helpful?</span>
          <label style={{ display: 'inline-flex', alignItems: 'center', cursor: 'pointer', margin: 0 }}>
            <input
              type="radio"
              name="helpful"
              checked={helpful === true}
              onChange={() => setHelpful(true)}
              style={{ marginRight: '0.5rem' }}
            />
            Yes
          </label>
          <label style={{ display: 'inline-flex', alignItems: 'center', cursor: 'pointer', margin: 0 }}>
            <input
              type="radio"
              name="helpful"
              checked={helpful === false}
              onChange={() => setHelpful(false)}
              style={{ marginRight: '0.5rem' }}
            />
            No
          </label>
        </div>

        <div className="form-group">
          <label htmlFor="feedback-comment" style={{ fontSize: '0.85rem' }}>
            Comments (Optional, max 300 chars)
          </label>
          <textarea
            id="feedback-comment"
            className="input-field"
            rows={3}
            maxLength={300}
            value={comment}
            onChange={e => setComment(e.target.value)}
            placeholder="Do not include private personal info like emails, passwords, or phone numbers."
          />
          <small style={{ display: 'block', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
            ⚠️ Do not include private personal information in feedback.
          </small>
        </div>

        <button className="btn btn-primary" type="submit" disabled={submitting}>
          {submitting ? 'Submitting...' : 'Submit Feedback'}
        </button>
      </form>
    </div>
  );
};
