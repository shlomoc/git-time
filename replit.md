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
- Keep components < 150 lines
- Split logic-heavy UI (e.g. timeline) into smaller components
- Store API URL in a `config.js` file
- Don’t overuse global state — use `useState` locally

---

## 🛠️ Tech Stack

| Layer | Tool |
|-------|------|
| Backend | Python + FastAPI |
| Git Parsing | GitPython or PyDriller |
| GPT | OpenAI GPT-4 API |
| Frontend | React (Vite or CRA) |
| Visualization | Chart.js, react-flow, visx |
| Hosting | Replit (or Netlify for frontend) |

---

## 💡 Core Development Rules

1. **End-to-end working > building more**
2. **Every commit must support the demo**
3. **Backend is the brain, frontend is the face**
4. **Logs > print for debugging**
5. **Write reusable functions — don’t hardcode auth logic**

---

## 🧪 Team Workflow Rules

- **Branch only if you're 2+ devs**. Otherwise commit fast and fix forward.
- **Commit messages:**
[feat] Add GPT summary call
[fix] Handle missing repo URL
[ui] Add loading state to timeline

yaml
Copy
Edit
- Pair on hard problems. Solo on polish.

---

## 📦 LLM Usage Guidelines

- Use consistent `prompt.md`
- GPT temp = 0.3 for reliability
- Chunk commits into logical topic blocks
- Strip large diffs — only send what matters
- Keep max token request under 2000 total

---

## 🧠 Hackathon Best Practices

| Rule | Why |
|------|-----|
| 🎯 Build the demo first | The rest is optional |
| 🔁 Test full loop early | Avoid late-stage surprises |
| 📺 Have a demo video | Replit lag is real |
| 💡 Pitch the pain | The story sells it, not just the tech |

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