# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a "Codebase Time Machine" - a full-stack application that analyzes GitHub repositories to show how specific features (like authentication, APIs, etc.) evolved over time. It uses GPT-4 to generate intelligent summaries of commit histories.

**Architecture:**
- **Frontend**: React + TypeScript with Vite bundler
- **Backend**: FastAPI (Python) with async endpoints
- **Key Libraries**: GitPython for repository analysis, OpenAI API for summaries
- **Deployment**: Originally built for Replit hosting
| Visualization | Chart.js, react-flow, visx |

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
python -m pip install -r requirements.txt  # Install dependencies
python main.py                              # Start FastAPI server on port 5000
```

### Full Stack Development
The frontend expects the backend to run on port 5000. The hardcoded backend URL in App.tsx may need updating for local development.

## Architecture Details

### Frontend Structure
- `src/App.tsx` - Main application state and API integration
- `src/components/` - Reusable UI components (RepoForm, Timeline, Summary, LoadingState)
- `src/types.ts` - TypeScript interfaces for API responses

### Backend Structure
- `backend/main.py` - FastAPI application with CORS middleware
- `backend/git_utils.py` - GitAnalyzer class for repository cloning and commit filtering
- `backend/gpt_summarizer.py` - GPTSummarizer class for OpenAI API integration

### Key Data Flow
1. User submits GitHub repo URL + topic (auth, api, database, ui)
2. Backend clones repo, filters commits by topic keywords
3. GPT-4 analyzes filtered commits to generate summary
4. Frontend displays timeline and summary

### API Endpoints
- `POST /analyze` - Main analysis endpoint (repo_url, topic)
- `GET /health` - Health check

### Environment Requirements
- Backend requires OpenAI API key (likely via environment variable)
- CORS configured for cross-origin requests from frontend
- Git must be available for repository cloning

## Important Notes

- The app has a hardcoded Replit backend URL in App.tsx that needs updating for local development
- Topic filtering uses predefined keywords in GitAnalyzer.TOPIC_KEYWORDS
- Commit analysis is limited to 20 most recent matching commits
- Temporary directories are used for git clones and cleaned up after analysis

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

- [ ] GitHub repo input works?
- [ ] Auth evolution demo is polished?
- [ ] Timeline renders and looks clean?
- [ ] GPT summaries are insightful?
- [ ] React UI has loading, error, happy states?
- [ ] Project can be explained in 60 seconds?

Let’s ship this fast, clean, and awesome.

🧠✌️ Team GitTime