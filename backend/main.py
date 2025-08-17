
import os
import logging
import hashlib
import time
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any
import asyncio

from git_utils import GitAnalyzer
from gpt_summarizer import GPTSummarizer

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Repository cache to avoid re-cloning
repo_cache: Dict[str, Dict[str, Any]] = {}
CACHE_EXPIRY_SECONDS = 1800  # 30 minutes

app = FastAPI(title="Codebase Time Machine API")

# CORS middleware for React frontend
# Allow both development and production origins
# CORS configuration - simplified for Render deployment
allowed_origins = [
    "http://localhost:5173",  # Local dev
    "http://localhost:3000",  # Alternative local dev
    "https://git-time-frontend.onrender.com",  # Production frontend
]

# Add environment-based origins
if os.environ.get("FRONTEND_URL"):
    allowed_origins.append(os.environ.get("FRONTEND_URL"))

# Temporarily allow all origins in production for debugging
is_production = os.environ.get("RENDER")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"] if is_production else allowed_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

class AnalyzeRequest(BaseModel):
    repo_url: str
    topic: str = "auth"

class QARequest(BaseModel):
    question: str
    repo_url: str
    topic: str = None

class AnalyzeResponse(BaseModel):
    summary: str
    commits: list
    timeline: list
    qa_data: dict = None
    visualizations: dict = None

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
        
        # Generate visualization data
        visualizations = git_analyzer.generate_visualization_data(commits)
        
        # Process default Q&A
        default_question = f"How did {request.topic} evolve in this codebase?"
        qa_data = await gpt_summarizer.process_qa(default_question, commits, request.topic, visualizations)
        
        logger.info(f"Analysis complete. Found {len(commits)} commits.")
        
        return AnalyzeResponse(
            summary=summary,
            commits=commits,
            timeline=timeline,
            qa_data=qa_data,
            visualizations=visualizations
        )
        
    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/qa")
async def ask_question(request: QARequest):
    """Answer questions about repository evolution"""
    try:
        logger.info(f"Processing Q&A: {request.question}")
        
        # Initialize analyzers
        git_analyzer = GitAnalyzer()
        gpt_summarizer = GPTSummarizer()
        
        # Clone and analyze repository
        topic = request.topic or "general"
        commits = await git_analyzer.analyze_repo(request.repo_url, topic)
        
        if not commits:
            raise HTTPException(status_code=404, detail="No commits found for the specified topic")
        
        # Generate visualization data
        visualizations = git_analyzer.generate_visualization_data(commits)
        
        # Process Q&A
        qa_response = await gpt_summarizer.process_qa(request.question, commits, topic, visualizations)
        
        logger.info("Q&A processing completed")
        
        return qa_response
        
    except Exception as e:
        logger.error(f"Q&A failed: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    cache_size = len(repo_cache)
    return {
        "status": "healthy",
        "cache_size": cache_size,
        "cached_repos": list(repo_cache.keys()) if cache_size < 10 else f"{cache_size} entries"
    }

@app.post("/clear-cache")
async def clear_cache():
    """Clear repository cache"""
    global repo_cache
    cache_size = len(repo_cache)
    repo_cache.clear()
    logger.info(f"Cleared cache with {cache_size} entries")
    return {"status": "cache cleared", "entries_removed": cache_size}

# Cleanup old cache entries periodically
async def cleanup_cache():
    """Remove expired cache entries"""
    while True:
        await asyncio.sleep(900)  # Check every 15 minutes
        current_time = time.time()
        expired_keys = [
            key for key, value in repo_cache.items()
            if current_time - value.get('timestamp', 0) > CACHE_EXPIRY_SECONDS
        ]
        
        for key in expired_keys:
            del repo_cache[key]
        
        if expired_keys:
            logger.info(f"Cleaned up {len(expired_keys)} expired cache entries")

@app.on_event("startup")
async def startup_event():
    """Start background tasks"""
    asyncio.create_task(cleanup_cache())

if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 5002))
    uvicorn.run(app, host="0.0.0.0", port=port)
