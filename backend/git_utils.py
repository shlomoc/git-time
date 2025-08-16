
import os
import tempfile
import shutil
import logging
from datetime import datetime
from typing import List, Dict, Any
import asyncio
import subprocess
from git import Repo

logger = logging.getLogger(__name__)

class GitAnalyzer:
    """Handles git repository cloning and commit analysis"""
    
    TOPIC_KEYWORDS = {
        'auth': ['auth', 'login', 'jwt', 'token', 'session', 'user', 'password', 'oauth', 'signin', 'signup'],
        'api': ['api', 'endpoint', 'route', 'controller', 'handler'],
        'database': ['db', 'database', 'migration', 'schema', 'model', 'sql'],
        'ui': ['component', 'view', 'template', 'style', 'css', 'html']
    }
    
    def __init__(self):
        self.temp_dir = None
        self.repo = None
    
    async def analyze_repo(self, repo_url: str, topic: str) -> List[Dict[str, Any]]:
        """Clone repository and extract topic-related commits"""
        try:
            # Clone repository
            self.temp_dir = await self._clone_repo(repo_url)
            self.repo = Repo(self.temp_dir)
            
            # Get all commits
            commits = list(self.repo.iter_commits())
            logger.info(f"Found {len(commits)} total commits")
            
            # Filter commits by topic
            topic_commits = self._filter_commits_by_topic(commits, topic)
            
            # Convert to structured data
            structured_commits = self._structure_commits(topic_commits)
            
            return structured_commits[:20]  # Limit to 20 most recent
            
        finally:
            self._cleanup()
    
    async def _clone_repo(self, repo_url: str) -> str:
        """Clone repository to temporary directory"""
        temp_dir = tempfile.mkdtemp()
        
        try:
            # Use subprocess for better control over cloning
            cmd = ['git', 'clone', '--depth', '100', repo_url, temp_dir]
            process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            
            stdout, stderr = await process.communicate()
            
            if process.returncode != 0:
                raise Exception(f"Git clone failed: {stderr.decode()}")
            
            logger.info(f"Repository cloned to {temp_dir}")
            return temp_dir
            
        except Exception as e:
            shutil.rmtree(temp_dir, ignore_errors=True)
            raise e
    
    def _filter_commits_by_topic(self, commits, topic: str) -> List:
        """Filter commits based on topic keywords and file changes"""
        keywords = self.TOPIC_KEYWORDS.get(topic.lower(), [topic.lower()])
        filtered_commits = []
        
        for commit in commits:
            # Check commit message
            message_match = any(keyword in commit.message.lower() for keyword in keywords)
            
            # Check changed files
            try:
                files_changed = list(commit.stats.files.keys())
                file_match = any(
                    any(keyword in file_path.lower() for keyword in keywords)
                    for file_path in files_changed
                )
            except:
                file_match = False
            
            if message_match or file_match:
                filtered_commits.append(commit)
        
        logger.info(f"Filtered to {len(filtered_commits)} topic-related commits")
        return filtered_commits
    
    def _structure_commits(self, commits) -> List[Dict[str, Any]]:
        """Convert git commits to structured data"""
        structured = []
        
        for commit in commits:
            try:
                # Get file changes
                files_changed = list(commit.stats.files.keys())
                
                # Get diff (simplified)
                diff_text = ""
                try:
                    if commit.parents:
                        diff = commit.parents[0].diff(commit)
                        diff_text = str(diff)[:500]  # Limit diff size
                except:
                    diff_text = "Initial commit or diff unavailable"
                
                structured.append({
                    'hash': commit.hexsha[:8],
                    'author': commit.author.name,
                    'email': commit.author.email,
                    'date': commit.committed_datetime.isoformat(),
                    'message': commit.message.strip(),
                    'files_changed': files_changed,
                    'diff': diff_text,
                    'stats': {
                        'insertions': commit.stats.total['insertions'],
                        'deletions': commit.stats.total['deletions'],
                        'files': commit.stats.total['files']
                    }
                })
                
            except Exception as e:
                logger.warning(f"Error processing commit {commit.hexsha}: {e}")
                continue
        
        return structured
    
    def create_timeline(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Create timeline data for visualization"""
        timeline = []
        
        for commit in commits:
            timeline.append({
                'date': commit['date'],
                'hash': commit['hash'],
                'message': commit['message'][:100] + "..." if len(commit['message']) > 100 else commit['message'],
                'author': commit['author'],
                'changes': commit['stats']['files']
            })
        
        # Sort by date (newest first)
        timeline.sort(key=lambda x: x['date'], reverse=True)
        return timeline
    
    def _cleanup(self):
        """Clean up temporary directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            logger.info("Cleaned up temporary directory")
