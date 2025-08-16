
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

export interface EvolutionPoint {
  when: string;
  hash: string;
  title: string;
  detail: string;
  files: string[];
}

export interface OwnershipData {
  author: string;
  commits: number;
  lines_changed: number;
  first_commit: string;
  last_commit: string;
}

export interface HotspotData {
  file: string;
  commits_touching: number;
  lines_changed: number;
}

export interface ComplexityData {
  period: string;
  lines_added: number;
  lines_deleted: number;
  files_touched: number;
}

export interface VisualizationData {
  evolution: EvolutionPoint[];
  ownership: OwnershipData[];
  hotspots: HotspotData[];
  complexity_trend: ComplexityData[];
}

export interface QAEvidence {
  hash: string;
  description: string;
}

export interface QAResponse {
  answer: string;
  evidence: QAEvidence[];
  visualizations: VisualizationData;
}

export interface AnalysisResult {
  summary: string;
  commits: Commit[];
  timeline: TimelineItem[];
  qa_data?: QAResponse;
  visualizations?: VisualizationData;
}
