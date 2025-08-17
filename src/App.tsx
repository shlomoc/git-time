
import React, { useState } from 'react';
import './App.css';
import RepoForm from './components/RepoForm';
import LoadingState from './components/LoadingState';
import Timeline from './components/Timeline';
import Summary from './components/Summary';
import QASection from './components/QASection';
import OwnershipChart from './components/OwnershipChart';
import HotspotChart from './components/HotspotChart';
import ComplexityTrend from './components/ComplexityTrend';
import { AnalysisResult } from './types';

interface AppState {
  loading: boolean;
  error: string | null;
  result: AnalysisResult | null;
  activeTab: string;
  repoUrl: string;
  topic: string;
}

export default function App() {
  const [state, setState] = useState<AppState>({
    loading: false,
    error: null,
    result: null,
    activeTab: 'summary',
    repoUrl: '',
    topic: ''
  });

  const handleAnalyze = async (repoUrl: string, topic: string) => {
    setState(prev => ({ 
      ...prev, 
      loading: true, 
      error: null, 
      result: null, 
      repoUrl, 
      topic 
    }));

    try {
      const apiUrl = import.meta.env.VITE_API_URL || 'http://localhost:5002';
      console.log('API URL:', apiUrl); // Debug log
      console.log('Analyzing repo:', repoUrl, 'topic:', topic); // Debug log
      
      const response = await fetch(`${apiUrl}/analyze`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          repo_url: repoUrl,
          topic: topic
        })
      });

      console.log('Response status:', response.status); // Debug log
      console.log('Response headers:', response.headers); // Debug log
      
      if (!response.ok) {
        const responseText = await response.text();
        console.log('Error response text:', responseText); // Debug log
        let errorData;
        try {
          errorData = JSON.parse(responseText);
        } catch {
          throw new Error(`HTTP ${response.status}: ${responseText || 'Analysis failed'}`);
        }
        throw new Error(errorData.detail || 'Analysis failed');
      }

      const responseText = await response.text();
      console.log('Success response text:', responseText); // Debug log
      
      if (!responseText) {
        throw new Error('Empty response from server');
      }
      
      const result = JSON.parse(responseText);
      setState(prev => ({ ...prev, loading: false, error: null, result }));

    } catch (error) {
      console.error('Analysis error:', error); // Debug log
      setState(prev => ({
        ...prev,
        loading: false,
        error: error instanceof Error ? error.message : 'Unknown error occurred',
        result: null
      }));
    }
  };

  const handleReset = () => {
    setState({ 
      loading: false, 
      error: null, 
      result: null,
      activeTab: 'summary',
      repoUrl: '',
      topic: ''
    });
  };

  const handleTabChange = (tab: string) => {
    setState(prev => ({ ...prev, activeTab: tab }));
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
            
            {/* Tab Navigation */}
            <div className="tab-navigation">
              <button 
                onClick={() => handleTabChange('summary')}
                className={`tab-button ${state.activeTab === 'summary' ? 'active' : ''}`}
              >
                📄 Summary
              </button>
              <button 
                onClick={() => handleTabChange('timeline')}
                className={`tab-button ${state.activeTab === 'timeline' ? 'active' : ''}`}
              >
                ⏱️ Timeline
              </button>
              <button 
                onClick={() => handleTabChange('qa')}
                className={`tab-button ${state.activeTab === 'qa' ? 'active' : ''}`}
              >
                ❓ Q&A
              </button>
              <button 
                onClick={() => handleTabChange('visualizations')}
                className={`tab-button ${state.activeTab === 'visualizations' ? 'active' : ''}`}
              >
                📊 Insights
              </button>
            </div>

            {/* Tab Content */}
            <div className="tab-content">
              {state.activeTab === 'summary' && (
                <Summary 
                  summary={state.result.summary}
                  commitCount={state.result.commits.length}
                />
              )}

              {state.activeTab === 'timeline' && (
                <Timeline 
                  timeline={state.result.timeline}
                  commits={state.result.commits}
                />
              )}

              {state.activeTab === 'qa' && (
                <QASection 
                  initialQA={state.result.qa_data}
                  repoUrl={state.repoUrl}
                  topic={state.topic}
                />
              )}

              {state.activeTab === 'visualizations' && state.result.visualizations && (
                <div className="visualizations-tab">
                  <OwnershipChart data={state.result.visualizations.ownership} />
                  <HotspotChart data={state.result.visualizations.hotspots} />
                  <ComplexityTrend data={state.result.visualizations.complexity_trend} />
                </div>
              )}
            </div>
          </div>
        )}
      </main>

      <footer className="app-footer">
        <p>Built for hackathon demo • Powered by GPT-4o & GitPython</p>
      </footer>
    </div>
  );
}
