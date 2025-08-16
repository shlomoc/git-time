
import os
import logging
from typing import List, Dict, Any
import openai
from openai import AsyncOpenAI
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

class GPTSummarizer:
    """Handles GPT-based commit summarization"""
    
    def __init__(self):
        # Load environment variables from .env.local file
        import os.path
        env_path = os.path.join(os.path.dirname(__file__), '..', '.env.local')
        load_dotenv(env_path)
        
        api_key = os.environ.get('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable is required")
        
        self.client = AsyncOpenAI(api_key=api_key)
        self.temperature = 0.3
        self.max_completion_tokens = 1000
    
    async def summarize_commits(self, commits: List[Dict[str, Any]], topic: str) -> str:
        """Generate GPT summary of commits for a specific topic"""
        try:
            # Build prompt from commits
            prompt = self._build_prompt(commits, topic)
            
            logger.info(f"Sending {len(commits)} commits to GPT for summarization")
            
            # Call GPT API
            response = await self.client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=self.max_completion_tokens
            )
            
            summary = response.choices[0].message.content
            logger.info("GPT summarization completed")
            
            return summary
            
        except Exception as e:
            logger.error(f"GPT summarization failed: {e}")
            return self._fallback_summary(commits, topic)
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for GPT"""
        return """You are a senior software architect and version control expert. Your task is to analyze a list of git commits and explain how a specific feature evolved over time in the codebase.

Your output should be a clear, structured summary of how the feature changed, what decisions were made, and any architectural or business implications.

Focus only on the specified topic. Identify initial implementation, major changes, refactors, and architecture shifts. Infer motivation if possible. Highlight important contributors.

Use a narrative tone like a changelog for humans. Be concise but insightful."""
    
    def _build_prompt(self, commits: List[Dict[str, Any]], topic: str) -> str:
        """Build the prompt for GPT from commits"""
        prompt = f"Topic: {topic}\n\nCommits:\n"
        
        for commit in commits[:15]:  # Limit to avoid token limits
            prompt += f"- Commit: {commit['hash']}\n"
            prompt += f"  Author: {commit['author']}\n"
            prompt += f"  Date: {commit['date'][:10]}\n"
            prompt += f"  Message: {commit['message'][:200]}\n"
            prompt += f"  Files: {', '.join(commit['files_changed'][:5])}\n"
            if commit['diff']:
                prompt += f"  Diff: {commit['diff'][:300]}...\n"
            prompt += "\n"
        
        prompt += "\nProvide a structured summary of how this feature evolved:"
        
        return prompt
    
    def _fallback_summary(self, commits: List[Dict[str, Any]], topic: str) -> str:
        """Provide fallback summary when GPT fails"""
        summary = f"## Evolution Summary: {topic.title()}\n\n"
        summary += f"**Analysis Period**: {len(commits)} commits analyzed\n\n"
        
        if commits:
            earliest = min(commits, key=lambda x: x['date'])
            latest = max(commits, key=lambda x: x['date'])
            
            summary += f"**Timeline**: {earliest['date'][:10]} to {latest['date'][:10]}\n\n"
            
            # Key contributors
            authors = {}
            for commit in commits:
                authors[commit['author']] = authors.get(commit['author'], 0) + 1
            
            top_authors = sorted(authors.items(), key=lambda x: x[1], reverse=True)[:3]
            summary += f"**Key Contributors**: {', '.join([f'{author} ({count} commits)' for author, count in top_authors])}\n\n"
            
            # Major changes
            summary += "**Major Changes**:\n"
            for commit in commits[:5]:
                summary += f"- {commit['date'][:10]}: {commit['message'][:100]}\n"
        
        summary += "\n*Note: This is a fallback summary. Full AI analysis was unavailable.*"
        
        return summary
    
    async def process_qa(self, question: str, commits: List[Dict[str, Any]], topic: str, visualizations: Dict[str, Any]) -> Dict[str, Any]:
        """Process Q&A request using the qa-feature-ui.md template"""
        try:
            # Build Q&A prompt
            qa_prompt = self._build_qa_prompt(question, topic, commits)
            
            logger.info(f"Processing Q&A question: {question}")
            
            # Call GPT API with Q&A system prompt
            response = await self.client.chat.completions.create(
                model="gpt-5",
                messages=[
                    {"role": "system", "content": self._get_qa_system_prompt()},
                    {"role": "user", "content": qa_prompt}
                ],
                max_completion_tokens=800
            )
            
            content = response.choices[0].message.content
            
            # Parse response into answer and evidence
            parsed_qa = self._parse_qa_response(content, commits)
            
            # Add visualization data
            parsed_qa["visualizations"] = visualizations
            
            logger.info("Q&A processing completed")
            
            return parsed_qa
            
        except Exception as e:
            logger.error(f"Q&A processing failed: {e}")
            return self._fallback_qa_response(question, commits, visualizations)
    
    def _get_qa_system_prompt(self) -> str:
        """Get system prompt for Q&A processing based on qa-feature-ui.md"""
        return """You are a concise software historian. Given git commits and diffs, you will answer the user's question about code evolution.

Be evidence-based. When you infer motivation, cite the commit(s) that support it.
If evidence is weak, say "Insufficient evidence" and offer the most likely explanation clearly marked as a hypothesis.

Keep prose brief (executive summary style). Focus on the Topic if provided; otherwise answer broadly.

Output format:
Answer
Summary: <2-4 sentences answering the question>

Key Evidence
<hash> — "<commit message or quoted fragment>"
<hash> — "<commit message or quoted fragment>"

Do not invent commit hashes or authors; only use what's provided."""
    
    def _build_qa_prompt(self, question: str, topic: str, commits: List[Dict[str, Any]]) -> str:
        """Build Q&A prompt following qa-feature-ui.md format"""
        prompt = f"Question: {question}\n"
        
        if topic:
            prompt += f"Topic: {topic}\n"
        
        prompt += "\nCommits:\n"
        
        for commit in commits[:15]:  # Limit for token management
            prompt += f"- {{\n"
            prompt += f"  hash: \"{commit['hash']}\",\n"
            prompt += f"  author: \"{commit['author']}\",\n"
            prompt += f"  date: \"{commit['date'][:10]}\",\n"
            prompt += f"  message: \"{commit['message'][:150]}\",\n"
            prompt += f"  files_changed: {commit['files_changed'][:3]},\n"
            prompt += f"  diff_excerpt: \"{commit['diff'][:200]}...\"\n"
            prompt += "}\n"
        
        return prompt
    
    def _parse_qa_response(self, content: str, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Parse GPT Q&A response into structured format"""
        lines = content.strip().split('\n')
        
        answer = ""
        evidence = []
        
        current_section = None
        
        for line in lines:
            line = line.strip()
            
            if line.startswith("Answer") or line.startswith("Summary:"):
                current_section = "answer"
                if line.startswith("Summary:"):
                    answer += line[8:].strip() + " "
                continue
            elif line.startswith("Key Evidence"):
                current_section = "evidence"
                continue
            elif line and current_section == "answer":
                answer += line + " "
            elif line and current_section == "evidence" and "—" in line:
                # Parse evidence line: "hash — description"
                parts = line.split("—", 1)
                if len(parts) == 2:
                    hash_part = parts[0].strip()
                    description = parts[1].strip().strip('"')
                    evidence.append({
                        "hash": hash_part,
                        "description": description
                    })
        
        return {
            "answer": answer.strip(),
            "evidence": evidence
        }
    
    def _fallback_qa_response(self, question: str, commits: List[Dict[str, Any]], visualizations: Dict[str, Any]) -> Dict[str, Any]:
        """Provide fallback Q&A response when GPT fails"""
        if len(commits) < 2:
            return {
                "answer": "Insufficient evidence.",
                "evidence": [],
                "visualizations": visualizations
            }
        
        # Simple pattern matching for common questions
        question_lower = question.lower()
        
        if "why" in question_lower or "introduced" in question_lower:
            answer = f"Based on {len(commits)} commits, this feature appears to have evolved through incremental changes and refactoring."
        elif "how" in question_lower and "evolv" in question_lower:
            answer = f"The feature evolved across {len(commits)} commits, with contributions from multiple developers over time."
        else:
            answer = f"Analysis of {len(commits)} commits shows the development timeline of this feature."
        
        # Use first few commits as evidence
        evidence = []
        for commit in commits[:3]:
            evidence.append({
                "hash": commit['hash'],
                "description": commit['message'][:80] + "..." if len(commit['message']) > 80 else commit['message']
            })
        
        return {
            "answer": answer,
            "evidence": evidence,
            "visualizations": visualizations
        }
