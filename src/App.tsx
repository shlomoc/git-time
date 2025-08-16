
import React, { useState } from 'react';
import './App.css';
import RepoForm from './components/RepoForm';
import LoadingState from './components/LoadingState';
import Timeline from './components/Timeline';
import Summary from './components/Summary';
import { AnalysisResult } from './types';

interface AppState {
  loading: boolean;
  error: string | null;
  result: AnalysisResult | null;
}

export default function App() {
  const [state, setState] = useState<AppState>({
    loading: false,
    error: null,
    result: null
  });

  const handleAnalyze = async (repoUrl: string, topic: string) => {
    setState({ loading: true, error: null, result: null });

    try {
      const response = await fetch('http://localhost:5000/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          repo_url: repoUrl,
          topic: topic
        })
      });

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const result = await response.json();
      setState({ loading: false, error: null, result });

    } catch (error) {
      setState({
        loading: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
        result: null
      });
    }
  };

  const handleReset = () => {
    setState({ loading: false, error: null, result: null });
  };

  return (
    <div className="app">
      <header className="app-header">
        <h1>🕰️ Codebase Time Machine</h1>
        <p>Explore how features evolved in any GitHub repository</p>
      </header>

      <main className="app-main">
        {!state.result && !state.loading && (
          <RepoForm onAnalyze={handleAnalyze} />
        )}

        {state.loading && <LoadingState />}

        {state.error && (
          <div className="error-container">
            <div className="error-message">
              <h3>❌ Analysis Failed</h3>
              <p>{state.error}</p>
              <button onClick={handleReset} className="retry-button">
                Try Again
              </button>
            </div>
          </div>
        )}

        {state.result && (
          <div className="results-container">
            <div className="results-header">
              <button onClick={handleReset} className="new-analysis-button">
                ← New Analysis
              </button>
            </div>
            
            <Summary 
              summary={state.result.summary}
              commitCount={state.result.commits.length}
            />
            
            <Timeline 
              timeline={state.result.timeline}
              commits={state.result.commits}
            />
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Built for hackathon demo • Powered by GPT-4 & GitPython</p>
      </footer>
    </div>
  );
}
