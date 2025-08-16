
import React from 'react';

interface SummaryProps {
  summary: string;
  commitCount: number;
}

export default function Summary({ summary, commitCount }: SummaryProps) {
  return (
    <div className="summary-container">
      <div className="summary-header">
        <h2>📋 Evolution Summary</h2>
        <div className="summary-stats">
          <span className="stat-badge">{commitCount} commits analyzed</span>
        </div>
      </div>
      
      <div className="summary-content">
        <pre className="summary-text">{summary}</pre>
      </div>
    </div>
  );
}
