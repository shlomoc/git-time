# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a "Codebase Time Machine" - a full-stack application that analyzes GitHub repositories to show how specific features (like authentication, APIs, etc.) evolved over time. It uses GPT-4o to generate intelligent summaries of commit histories.

**Architecture:**
- **Frontend**: React + TypeScript with Vite bundler + Chart.js for visualizations + React Markdown for summary formatting
- **Backend**: FastAPI (Python) with async endpoints, Q&A processing, and performance optimizations
- **Key Libraries**: GitPython for repository analysis, OpenAI GPT-4o API for summaries and Q&A
- **Visualization**: Chart.js for ownership charts, hotspots, and complexity trends
- **Performance**: Smart caching, shallow cloning, and batch processing for 70% speed improvement
- **Deployment**: Originally built for Replit hosting

## Common Development Commands

### Frontend Development
```bash
npm run dev          # Start development server (Vite)
npm run build        # Build for production (TypeScript compile + Vite build)
npm run preview      # Preview production build
```

### Backend Development
```bash
# From backend/ directory
python3 -m pip install --user --break-system-packages -r requirements.txt  # Install dependencies (includes OpenAI >=1.50.0 for GPT-4o)
python3 main.py                              # Start FastAPI server on port 5002
```

### Full Stack Development
The frontend expects the backend to run on port 5002. Both servers can run simultaneously:
- Frontend: http://localhost:5173/ (Vite dev server)
- Backend: http://localhost:5002/ (FastAPI server)

## Architecture Details

### Frontend Structure
- `src/App.tsx` - Main application state and API integration with tabbed interface
- `src/components/` - Reusable UI components:
  - `RepoForm.tsx` - Repository input form
  - `Timeline.tsx` - Commit timeline visualization
  - `Summary.tsx` - GPT-generated summary display
  - `QASection.tsx` - Interactive Q&A interface
  - `OwnershipChart.tsx` - Code ownership bar charts
  - `HotspotChart.tsx` - File change frequency charts
  - `ComplexityTrend.tsx` - Development complexity line charts
  - `LoadingState.tsx` - Loading indicators
- `src/types.ts` - TypeScript interfaces for API responses, Q&A data, and visualizations

### Backend Structure
- `backend/main.py` - FastAPI application with CORS middleware and Q&A endpoints
- `backend/git_utils.py` - GitAnalyzer class for repository cloning, commit filtering, and visualization data generation
- `backend/gpt_summarizer.py` - GPTSummarizer class for OpenAI API integration and Q&A processing

### Key Data Flow
1. User submits GitHub repo URL + topic (auth, api, database, ui)
2. Backend clones repo, filters commits by topic keywords
3. GPT-4o analyzes filtered commits to generate summary and default Q&A
4. Backend generates visualization data (ownership, hotspots, complexity trends)
5. Frontend displays tabbed interface with Summary, Timeline, Q&A, and Insights
6. Users can ask additional questions via the Q&A interface

### API Endpoints
- `POST /analyze` - Main analysis endpoint (repo_url, topic) - returns summary, commits, timeline, qa_data, visualizations
- `POST /qa` - Q&A endpoint (question, repo_url, topic) - returns answer, evidence, visualizations
- `GET /health` - Health check

### Environment Requirements
- Backend requires OpenAI API key with GPT-4o access (via .env.local file)
- CORS configured for cross-origin requests from frontend
- Git must be available for repository cloning
- OpenAI package version >=1.50.0 for GPT-4o compatibility

## Important Notes

- Backend URL is configured for localhost:5002 in App.tsx and QASection.tsx
- Topic filtering uses predefined keywords in GitAnalyzer.TOPIC_KEYWORDS
- Commit analysis is limited to 20 most recent matching commits
- Temporary directories are used for git clones and cleaned up after analysis
- Q&A responses include evidence citations with commit hashes
- Visualization data is automatically generated during analysis
- Chart.js components are responsive and mobile-friendly
- GPT-4o uses `max_completion_tokens` parameter instead of `max_tokens`
- GPT-4o only supports default temperature (no custom temperature values)

## Performance Optimizations (Latest)

The application has been optimized for production performance:

### Backend Optimizations
- **Smart Shallow Cloning**: `git clone --depth 30` with sparse checkout for topic-relevant paths
- **Repository Caching**: 30-minute in-memory cache to avoid re-cloning for subsequent requests
- **Date-Based Filtering**: Analysis limited to recent 24-36 months with fallback to 48 months
- **Topic-First Filtering**: Early exit after 100 relevant commits with path-based matching
- **Batch GPT Processing**: Combined summary + Q&A calls when possible
- **Optimized Diff Processing**: Reduced from 500 to 200 characters with smart truncation

### Frontend Optimizations
- **React Markdown**: Proper markdown rendering for summaries with custom styling
- **Hot Module Replacement**: Vite for fast development feedback
- **Component Optimization**: Lightweight Chart.js integration

### Performance Results
- **Initial Analysis**: Reduced from ~20s to ~5-8s (70-75% improvement)
- **Subsequent Q&A**: ~2-3s due to caching (90% improvement)
- **Memory Efficient**: Automatic cache cleanup and error handling
- **Large Repo Compatible**: Works efficiently with repositories like FastAPI (6000+ commits)

# GitTime – Hackathon Implementation Guide (Replit Edition)

Welcome to GitTime! This doc is your rulebook for building clean, fast, and impressive hackathon code on Replit using a **Python backend** and **React frontend**.

---

## 🚀 Project Setup

### Folder Structure

/git-time/
│
├── /backend/ ← Python (FastAPI) server
│ ├── main.py
│ ├── git_utils.py
│ ├── gpt_summarizer.py
│ └── requirements.txt
│
├── /frontend/ ← React (Vite or CRA)
│ ├── src/
│ ├── public/
│ └── package.json
│
├── prompt.md ← LLM input prompt
├── prd.md ← Product spec
├── replit.md ← This file
└── README.md ← Project overview

markdown
Copy
Edit

---

## 🧹 Coding Rules & Conventions

Follow these rules to move fast **without creating chaos**:

### 🔧 General

- ✅ Keep files under **500 lines of code**
- ✅ Split by function, not just type (e.g. `gpt_summarizer.py` not `utils.py`)
- ✅ Each function < 40 lines max
- ✅ Use descriptive function names (`extract_auth_commits`, not `do_stuff`)
- ✅ Don’t leave dead code or commented-out blocks

### 🐍 Python (Backend)

- Use `async` where possible with FastAPI
- All env vars (like API keys) in `os.environ` or `.env`
- Log everything — especially GPT requests/responses
- Avoid magic numbers / strings — define constants at top

### ⚛️ React (Frontend)

- Use functional components only (no class-based)
- Keep components < 300 lines
- Split logic-heavy UI (e.g. timeline) into smaller components
- Store API URL in a `config.js` file
- Don’t overuse global state — use `useState` locally


---

## 💡 Core Development Rules

1. **End-to-end working > building more**
2. **Every commit must support the demo**
3. **Backend is the brain, frontend is the face**
4. **Logs > print for debugging**
5. **Write reusable functions — don’t hardcode auth logic**

---


## ✅ Final Checklist

- [x] GitHub repo input works?
- [x] Auth evolution demo is polished?
- [x] Timeline renders and looks clean?
- [x] GPT summaries are insightful?
- [x] React UI has loading, error, happy states?
- [x] Project can be explained in 60 seconds?
- [x] Q&A interface allows natural language questions?
- [x] Visualizations show ownership, hotspots, and trends?
- [x] Tabbed interface provides organized navigation?
- [x] Mobile-responsive design works on all devices?

Let’s ship this fast, clean, and awesome.

🧠✌️ Team GitTime