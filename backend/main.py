
import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import asyncio

from git_utils import GitAnalyzer
from gpt_summarizer import GPTSummarizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Codebase Time Machine API")

# CORS middleware for React frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    repo_url: str
    topic: str = "auth"

class AnalyzeResponse(BaseModel):
    summary: str
    commits: list
    timeline: list

@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_repo(request: AnalyzeRequest):
    """Analyze a GitHub repository for feature evolution"""
    try:
        logger.info(f"Analyzing repo: {request.repo_url} for topic: {request.topic}")
        
        # Initialize analyzers
        git_analyzer = GitAnalyzer()
        gpt_summarizer = GPTSummarizer()
        
        # Clone and analyze repository
        commits = await git_analyzer.analyze_repo(request.repo_url, request.topic)
        
        if not commits:
            raise HTTPException(status_code=404, detail="No commits found for the specified topic")
        
        # Generate GPT summary
        summary = await gpt_summarizer.summarize_commits(commits, request.topic)
        
        # Create timeline data
        timeline = git_analyzer.create_timeline(commits)
        
        logger.info(f"Analysis complete. Found {len(commits)} commits.")
        
        return AnalyzeResponse(
            summary=summary,
            commits=commits,
            timeline=timeline
        )
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5000)
