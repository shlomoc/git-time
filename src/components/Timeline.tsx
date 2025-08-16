
import React, { useState } from 'react';
import { TimelineItem, Commit } from '../types';

interface TimelineProps {
  timeline: TimelineItem[];
  commits: Commit[];
}

export default function Timeline({ timeline, commits }: TimelineProps) {
  const [selectedCommit, setSelectedCommit] = useState<Commit | null>(null);

  const handleCommitClick = (hash: string) => {
    const commit = commits.find(c => c.hash === hash);
    setSelectedCommit(commit || null);
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric'
    });
  };

  return (
    <div className="timeline-container">
      <h2>📈 Feature Timeline</h2>
      
      <div className="timeline-content">
        <div className="timeline-list">
          {timeline.map((item, index) => (
            <div 
              key={item.hash}
              className="timeline-item"
              onClick={() => handleCommitClick(item.hash)}
            >
              <div className="timeline-marker">
                <div className="timeline-dot"></div>
                {index < timeline.length - 1 && <div className="timeline-line"></div>}
              </div>
              
              <div className="timeline-content-item">
                <div className="timeline-header">
                  <span className="commit-hash">#{item.hash}</span>
                  <span className="commit-date">{formatDate(item.date)}</span>
                </div>
                
                <h4 className="commit-message">{item.message}</h4>
                
                <div className="commit-meta">
                  <span className="commit-author">👤 {item.author}</span>
                  <span className="commit-changes">📝 {item.changes} files</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {selectedCommit && (
          <div className="commit-details">
            <div className="commit-details-header">
              <h3>Commit Details</h3>
              <button 
                onClick={() => setSelectedCommit(null)}
                className="close-button"
              >
                ✕
              </button>
            </div>
            
            <div className="commit-details-content">
              <div className="detail-row">
                <strong>Hash:</strong> {selectedCommit.hash}
              </div>
              <div className="detail-row">
                <strong>Author:</strong> {selectedCommit.author} ({selectedCommit.email})
              </div>
              <div className="detail-row">
                <strong>Date:</strong> {formatDate(selectedCommit.date)}
              </div>
              <div className="detail-row">
                <strong>Message:</strong> {selectedCommit.message}
              </div>
              <div className="detail-row">
                <strong>Files Changed:</strong>
                <ul className="files-list">
                  {selectedCommit.files_changed.slice(0, 10).map(file => (
                    <li key={file}>{file}</li>
                  ))}
                  {selectedCommit.files_changed.length > 10 && (
                    <li>... and {selectedCommit.files_changed.length - 10} more</li>
                  )}
                </ul>
              </div>
              <div className="detail-row">
                <strong>Changes:</strong> 
                <span className="stats">
                  +{selectedCommit.stats.insertions} -{selectedCommit.stats.deletions}
                </span>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
