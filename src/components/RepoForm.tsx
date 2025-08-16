
import React, { useState } from 'react';

interface RepoFormProps {
  onAnalyze: (repoUrl: string, topic: string) => void;
}

const DEMO_REPOS = [
  'https://github.com/supabase/supabase',
  'https://github.com/nextauthjs/next-auth', 
  'https://github.com/strapi/strapi'
];

const TOPICS = [
  { value: 'auth', label: 'Authentication' },
  { value: 'api', label: 'API' },
  { value: 'database', label: 'Database' },
  { value: 'ui', label: 'User Interface' }
];

export default function RepoForm({ onAnalyze }: RepoFormProps) {
  const [repoUrl, setRepoUrl] = useState('');
  const [topic, setTopic] = useState('auth');

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (repoUrl.trim()) {
      onAnalyze(repoUrl.trim(), topic);
    }
  };

  const handleDemoRepo = (url: string) => {
    setRepoUrl(url);
  };

  return (
    <div className="repo-form-container">
      <div className="form-card">
        <h2>🔍 Analyze Repository</h2>
        <p>Enter a GitHub repository URL to explore how a feature evolved over time.</p>

        <form onSubmit={handleSubmit} className="repo-form">
          <div className="form-group">
            <label htmlFor="repoUrl">GitHub Repository URL</label>
            <input
              id="repoUrl"
              type="url"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/owner/repository"
              required
              className="repo-input"
            />
          </div>

          <div className="form-group">
            <label htmlFor="topic">Feature to Analyze</label>
            <select
              id="topic"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              className="topic-select"
            >
              {TOPICS.map(t => (
                <option key={t.value} value={t.value}>
                  {t.label}
                </option>
              ))}
            </select>
          </div>

          <button type="submit" className="analyze-button">
            🚀 Analyze Feature Evolution
          </button>
        </form>

        <div className="demo-section">
          <h3>📚 Try Demo Repositories</h3>
          <div className="demo-buttons">
            {DEMO_REPOS.map(url => (
              <button
                key={url}
                onClick={() => handleDemoRepo(url)}
                className="demo-button"
              >
                {url.split('/').slice(-2).join('/')}
              </button>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
