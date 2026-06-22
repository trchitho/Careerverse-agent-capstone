import React from 'react';

interface StatusBannerProps {
  healthy: boolean | null;
  apiUrl: string;
}

export const StatusBanner: React.FC<StatusBannerProps> = ({ healthy, apiUrl }) => {
  if (healthy === null) {
    return (
      <div className="status-banner" role="status">
        <span>Checking connection to Backend API...</span>
        <span>{apiUrl}</span>
      </div>
    );
  }

  if (!healthy) {
    return (
      <div className="status-banner error" role="alert">
        <span>⚠️ Backend API is offline. Some features will be disabled.</span>
        <span>{apiUrl}</span>
      </div>
    );
  }

  return (
    <div className="status-banner" role="status">
      <span>🟢 Connected to API v1</span>
      <span>{apiUrl}</span>
    </div>
  );
};
