import React from 'react';

interface SafetyNoticeProps {
  notice?: string;
}

export const SafetyNotice: React.FC<SafetyNoticeProps> = ({ notice }) => {
  const defaultNotice =
    "This system provides educational career guidance only. It does not guarantee employment outcomes or replace professional counseling.";
  const displayNotice = notice || defaultNotice;

  return (
    <div className="safety-notice-alert" role="alert">
      <strong>Safety Notice:</strong> {displayNotice}
    </div>
  );
};
