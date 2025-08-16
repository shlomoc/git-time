import React, { useState } from 'react';
import { QAResponse, QAEvidence } from '../types';

interface QASectionProps {
  initialQA?: QAResponse;
  repoUrl?: string;
  topic?: string;
  onNewQuestion?: (question: string) => void;
}

export default function QASection({ initialQA, repoUrl, topic, onNewQuestion }: QASectionProps) {
  const [question, setQuestion] = useState('');
  const [currentQA, setCurrentQA] = useState<QAResponse | undefined>(initialQA);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!question.trim() || !repoUrl) return;

    setLoading(true);
    
    try {
      const response = await fetch('http://localhost:5002/qa', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          question: question.trim(),
          repo_url: repoUrl,
          topic: topic
        })
      });

      if (!response.ok) {
        throw new Error('Failed to get answer');
      }

      const qaResponse = await response.json();
      setCurrentQA(qaResponse);
      
      if (onNewQuestion) {
        onNewQuestion(question);
      }
      
      setQuestion('');
    } catch (error) {
      console.error('Q&A error:', error);
      // Could add error state handling here
    } finally {
      setLoading(false);
    }
  };

  const suggestedQuestions = [
    "Why was this pattern introduced?",
    `How did ${topic || 'this feature'} evolve over time?`,
    "What were the major architectural changes?",
    "Who were the key contributors to this feature?",
    "When did the most significant changes happen?"
  ];

  const handleSuggestedQuestion = (suggestedQuestion: string) => {
    setQuestion(suggestedQuestion);
  };

  return (
    <div className="qa-section">
      <h3>❓ Ask About This Codebase</h3>
      
      {/* Question Input Form */}
      <form onSubmit={handleSubmit} className="qa-form">
        <div className="question-input-group">
          <input
            type="text"
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Ask anything about how this feature evolved..."
            className="question-input"
            disabled={loading}
          />
          <button 
            type="submit" 
            disabled={!question.trim() || loading}
            className="ask-button"
          >
            {loading ? '🤔' : '🔍'} {loading ? 'Thinking...' : 'Ask'}
          </button>
        </div>
      </form>

      {/* Suggested Questions */}
      <div className="suggested-questions">
        <p>Try asking:</p>
        <div className="question-buttons">
          {suggestedQuestions.map((sq, index) => (
            <button
              key={index}
              onClick={() => handleSuggestedQuestion(sq)}
              className="suggested-question-btn"
              disabled={loading}
            >
              {sq}
            </button>
          ))}
        </div>
      </div>

      {/* Q&A Response */}
      {currentQA && (
        <div className="qa-response">
          <div className="qa-answer">
            <h4>Answer</h4>
            <p>{currentQA.answer}</p>
          </div>

          {currentQA.evidence && currentQA.evidence.length > 0 && (
            <div className="qa-evidence">
              <h4>Key Evidence</h4>
              <ul className="evidence-list">
                {currentQA.evidence.map((evidence: QAEvidence, index) => (
                  <li key={index} className="evidence-item">
                    <span className="commit-hash">{evidence.hash}</span>
                    <span className="evidence-description">— {evidence.description}</span>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      )}

      {/* Loading State */}
      {loading && (
        <div className="qa-loading">
          <div className="loading-spinner"></div>
          <p>Analyzing commits and generating answer...</p>
        </div>
      )}
    </div>
  );
}