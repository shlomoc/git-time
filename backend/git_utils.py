
import os
import tempfile
import shutil
import logging
from datetime import datetime, timedelta
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
    
    TOPIC_PATHS = {
        'auth': ['auth', 'security', 'login', 'user', 'session', 'jwt', 'oauth'],
        'api': ['api', 'endpoint', 'route', 'controller', 'handler', 'fastapi', 'flask'],
        'database': ['db', 'database', 'migration', 'schema', 'model', 'sql', 'orm'],
        'ui': ['component', 'view', 'template', 'style', 'css', 'html', 'react', 'vue']
    }
    
    # Performance constants
    MAX_COMMITS = 100
    MAX_DIFF_SIZE = 200
    DEFAULT_MONTHS_BACK = 30
    FALLBACK_MONTHS_BACK = 48
    MIN_COMMITS_THRESHOLD = 5
    
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
    
    def _filter_commits_by_topic_optimized(self, commits, topic: str) -> List:
        """Optimized filtering with early exit and path-based filtering"""
        keywords = self.TOPIC_KEYWORDS.get(topic.lower(), [topic.lower()])
        topic_paths = self.TOPIC_PATHS.get(topic.lower(), [topic.lower()])
        filtered_commits = []
        
        for commit in commits:
            # Early exit if we have enough commits
            if len(filtered_commits) >= self.MAX_COMMITS:
                break
                
            # Check commit message first (fastest check)
            message_match = any(keyword in commit.message.lower() for keyword in keywords)
            
            # Check changed files with path-based filtering
            file_match = False
            path_match = False
            try:
                files_changed = list(commit.stats.files.keys())
                
                # Limit file analysis to avoid performance hits
                files_to_check = files_changed[:10]  # Check only first 10 files
                
                # Check for keyword matches in filenames
                file_match = any(
                    any(keyword in file_path.lower() for keyword in keywords)
                    for file_path in files_to_check
                )
                
                # Check for path-based matches (more specific)
                path_match = any(
                    any(path in file_path.lower() for path in topic_paths)
                    for file_path in files_to_check
                )
                
            except Exception as e:
                logger.debug(f"Error checking files for commit {commit.hexsha[:8]}: {e}")
                file_match = False
                path_match = False
            
            # Include commit if any match is found
            if message_match or file_match or path_match:
                filtered_commits.append(commit)
        
        logger.info(f"Filtered to {len(filtered_commits)} topic-related commits (optimized)")
        return filtered_commits
    
    def _filter_commits_by_topic(self, commits, topic: str) -> List:
        """Legacy method - calls optimized version"""
        return self._filter_commits_by_topic_optimized(commits, topic)
    
    def _structure_commits_optimized(self, commits) -> List[Dict[str, Any]]:
        """Convert git commits to structured data with performance optimizations"""
        structured = []
        
        for commit in commits:
            try:
                # Get file changes with limit
                files_changed = list(commit.stats.files.keys())
                files_changed_limited = files_changed[:3]  # Limit to 3 most relevant files
                
                # Get diff with smaller limit for performance
                diff_text = ""
                try:
                    if commit.parents:
                        diff = commit.parents[0].diff(commit)
                        diff_str = str(diff)
                        # Smart truncation - try to keep complete lines
                        if len(diff_str) > self.MAX_DIFF_SIZE:
                            truncated = diff_str[:self.MAX_DIFF_SIZE]
                            # Find last complete line
                            last_newline = truncated.rfind('\n')
                            if last_newline > self.MAX_DIFF_SIZE // 2:
                                diff_text = truncated[:last_newline] + "\n[...]"
                            else:
                                diff_text = truncated + "[...]"
                        else:
                            diff_text = diff_str
                except Exception as e:
                    diff_text = "Initial commit or diff unavailable"
                
                structured.append({
                    'hash': commit.hexsha[:8],
                    'author': commit.author.name,
                    'email': commit.author.email,
                    'date': commit.committed_datetime.isoformat(),
                    'message': commit.message.strip(),
                    'files_changed': files_changed_limited,  # Limited for performance
                    'files_changed_count': len(files_changed),  # Keep total count
                    'diff': diff_text,
                    'stats': {
                        'insertions': commit.stats.total['insertions'],
                        'deletions': commit.stats.total['deletions'],
                        'files': commit.stats.total['files']
                    }
                })
                
            except Exception as e:
                logger.warning(f"Error processing commit {commit.hexsha[:8]}: {e}")
                continue
        
        return structured
    
    def _structure_commits(self, commits) -> List[Dict[str, Any]]:
        """Legacy method - calls optimized version"""
        return self._structure_commits_optimized(commits)
    
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
    
    def generate_visualization_data(self, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Generate data for Q&A visualizations"""
        return {
            'ownership': self._calculate_ownership(commits),
            'hotspots': self._calculate_hotspots(commits),
            'complexity_trend': self._calculate_complexity_trend(commits),
            'evolution': self._extract_evolution_moments(commits)
        }
    
    def _calculate_ownership(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Aggregate commit and change data by author"""
        ownership = {}
        
        for commit in commits:
            author = commit['author']
            if author not in ownership:
                ownership[author] = {
                    'author': author,
                    'commits': 0,
                    'lines_changed': 0,
                    'first_commit': commit['date'],
                    'last_commit': commit['date']
                }
            
            ownership[author]['commits'] += 1
            ownership[author]['lines_changed'] += commit['stats']['insertions'] + commit['stats']['deletions']
            
            # Update date range
            if commit['date'] < ownership[author]['first_commit']:
                ownership[author]['first_commit'] = commit['date']
            if commit['date'] > ownership[author]['last_commit']:
                ownership[author]['last_commit'] = commit['date']
        
        # Sort by commits count (descending)
        return sorted(ownership.values(), key=lambda x: x['commits'], reverse=True)
    
    def _calculate_hotspots(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find files with most changes (hotspots)"""
        hotspots = {}
        
        for commit in commits:
            for file_path in commit['files_changed']:
                if file_path not in hotspots:
                    hotspots[file_path] = {
                        'file': file_path,
                        'commits_touching': 0,
                        'lines_changed': 0
                    }
                
                hotspots[file_path]['commits_touching'] += 1
                # Approximate lines changed per file (total stats / number of files)
                files_count = len(commit['files_changed'])
                if files_count > 0:
                    approx_lines = (commit['stats']['insertions'] + commit['stats']['deletions']) // files_count
                    hotspots[file_path]['lines_changed'] += approx_lines
        
        # Sort by commits touching (descending) and return top 10
        return sorted(hotspots.values(), key=lambda x: x['commits_touching'], reverse=True)[:10]
    
    def _calculate_complexity_trend(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Calculate monthly complexity trends"""
        trends = {}
        
        for commit in commits:
            # Group by month (YYYY-MM format)
            date_obj = datetime.fromisoformat(commit['date'].replace('Z', '+00:00'))
            period = date_obj.strftime('%Y-%m')
            
            if period not in trends:
                trends[period] = {
                    'period': period,
                    'lines_added': 0,
                    'lines_deleted': 0,
                    'files_touched': 0
                }
            
            trends[period]['lines_added'] += commit['stats']['insertions']
            trends[period]['lines_deleted'] += commit['stats']['deletions']
            trends[period]['files_touched'] += commit['stats']['files']
        
        # Sort by period (chronological)
        return sorted(trends.values(), key=lambda x: x['period'])
    
    def _extract_evolution_moments(self, commits: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract key evolution moments from commits"""
        evolution = []
        
        # Take significant commits (high change count or key words)
        significant_commits = []
        
        for commit in commits:
            # Consider significant if many files changed or contains key terms
            total_changes = commit['stats']['insertions'] + commit['stats']['deletions']
            has_keywords = any(word in commit['message'].lower() 
                             for word in ['add', 'implement', 'introduce', 'refactor', 'remove'])
            
            if total_changes > 20 or has_keywords or commit['stats']['files'] > 3:
                significant_commits.append(commit)
        
        # Limit to top 8 most significant and sort by date
        significant_commits = sorted(significant_commits, 
                                   key=lambda x: x['stats']['insertions'] + x['stats']['deletions'], 
                                   reverse=True)[:8]
        significant_commits.sort(key=lambda x: x['date'])
        
        for commit in significant_commits:
            evolution.append({
                'when': commit['date'][:10],  # YYYY-MM-DD format
                'hash': commit['hash'],
                'title': self._extract_commit_title(commit['message']),
                'detail': commit['message'][:100] + "..." if len(commit['message']) > 100 else commit['message'],
                'files': commit['files_changed'][:5]  # Limit to first 5 files
            })
        
        return evolution
    
    def _extract_commit_title(self, message: str) -> str:
        """Extract a short title from commit message"""
        lines = message.strip().split('\n')
        title = lines[0]
        
        # Shorten if too long
        if len(title) > 50:
            title = title[:47] + "..."
        
        return title
    
    def _cleanup(self):
        """Clean up temporary directory"""
        if self.temp_dir and os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir, ignore_errors=True)
            logger.info("Cleaned up temporary directory")
