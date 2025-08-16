
export interface Commit {
  hash: string;
  author: string;
  email: string;
  date: string;
  message: string;
  files_changed: string[];
  diff: string;
  stats: {
    insertions: number;
    deletions: number;
    files: number;
  };
}

export interface TimelineItem {
  date: string;
  hash: string;
  message: string;
  author: string;
  changes: number;
}

export interface AnalysisResult {
  summary: string;
  commits: Commit[];
  timeline: TimelineItem[];
}
