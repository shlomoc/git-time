
import React from 'react';

export default function LoadingState() {
  return (
    <div className="loading-container">
      <div className="loading-card">
        <div className="loading-spinner"></div>
        <h2>🔄 Analyzing Repository</h2>
        <div className="loading-steps">
          <div className="loading-step">
            <span className="step-icon">📥</span>
            <span>Cloning repository...</span>
          </div>
          <div className="loading-step">
            <span className="step-icon">🔍</span>
            <span>Parsing git history...</span>
          </div>
          <div className="loading-step">
            <span className="step-icon">🧠</span>
            <span>Generating AI summary...</span>
          </div>
          <div className="loading-step">
            <span className="step-icon">📊</span>
            <span>Building timeline...</span>
          </div>
        </div>
        <p className="loading-note">This may take 30-60 seconds depending on repository size.</p>
      </div>
    </div>
  );
}
