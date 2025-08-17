
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
        self.max_completion_tokens = 300  # Much smaller for brief summaries
        self.max_qa_tokens = 250  # Smaller for concise Q&A
    
    async def summarize_commits(self, commits: List[Dict[str, Any]], topic: str) -> str:
        """Generate GPT summary of commits for a specific topic"""
        try:
            # Build optimized prompt from commits
            prompt = self._build_prompt_optimized(commits, topic)
            
            logger.info(f"Sending {len(commits)} commits to GPT for summarization (optimized)")
            
            # Call GPT API with optimized settings
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_completion_tokens=self.max_completion_tokens
            )
            
            summary = response.choices[0].message.content
            logger.info(f"GPT summarization completed. Summary length: {len(summary) if summary else 0}")
            
            if not summary or len(summary.strip()) == 0:
                logger.warning("GPT returned empty summary, using fallback")
                return self._fallback_summary(commits, topic)
            
            return summary
            
        except Exception as e:
            logger.error(f"GPT summarization failed: {e}")
            return self._fallback_summary(commits, topic)
    
    async def summarize_and_qa_batch(self, commits: List[Dict[str, Any]], topic: str, question: str = None) -> Dict[str, Any]:
        """Batch processing for summary and Q&A in a single call"""
        try:
            # Use default question if none provided
            if not question:
                question = f"How did {topic} evolve in this codebase?"
            
            # Build combined prompt
            summary_prompt = self._build_prompt_optimized(commits, topic)
            qa_prompt = self._build_qa_prompt_optimized(question, topic, commits)
            
            combined_prompt = f"""Please provide both a summary and answer the question below.
            
SUMMARY REQUEST:
{summary_prompt}

QUESTION TO ANSWER:
{qa_prompt}

Format your response as:
SUMMARY:
[Your summary here]

ANSWER:
[Your Q&A response here]"""
            
            logger.info(f"Batch processing summary + Q&A for {len(commits)} commits")
            
            response = await self.client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self._get_combined_system_prompt()},
                    {"role": "user", "content": combined_prompt}
                ],
                max_completion_tokens=self.max_completion_tokens + 100  # Slightly more for combined
            )
            
            content = response.choices[0].message.content
            return self._parse_combined_response(content, commits)
            
        except Exception as e:
            logger.error(f"Batch GPT processing failed: {e}")
            # Fallback to individual calls
            summary = self._fallback_summary(commits, topic)
            qa_data = self._fallback_qa_response(question or f"How did {topic} evolve?", commits, {})
            return {"summary": summary, "qa_data": qa_data}
    
    def _get_combined_system_prompt(self) -> str:
        """System prompt for combined summary + Q&A processing"""
        return """You are a software architect. Keep responses EXTREMELY SHORT.

For the SUMMARY: EXACTLY 3-4 bullet points (one sentence each):
• Initial: What was built first
• Changes: Key updates made
• Current: How it works now  
• Impact: Main benefit

For the ANSWER: ONE sentence with evidence:
Answer: <one sentence only>
Key Evidence:
<hash> — "<commit message>"

Be ultra-brief."""
    
    def _parse_combined_response(self, content: str, commits: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Parse combined summary + Q&A response"""
        try:
            parts = content.split("ANSWER:")
            summary_part = parts[0].replace("SUMMARY:", "").strip()
            
            if len(parts) > 1:
                qa_part = parts[1].strip()
                qa_data = self._parse_qa_response(qa_part, commits)
            else:
                # Fallback if format is not as expected
                qa_data = {"answer": "Combined processing format error", "evidence": []}
            
            return {
                "summary": summary_part,
                "qa_data": qa_data
            }
        except Exception as e:
            logger.error(f"Error parsing combined response: {e}")
            return {
                "summary": content[:500] + "..." if len(content) > 500 else content,
                "qa_data": {"answer": "Parsing error occurred", "evidence": []}
            }
    
    def _get_system_prompt(self) -> str:
        """Get the system prompt for GPT"""
        return """You are a software architect. Provide an EXTREMELY BRIEF summary.

Use EXACTLY 3-4 short bullet points:
• Initial: What was built first
• Changes: Key updates made  
• Current: How it works now
• Impact: Main benefit

Each bullet point should be ONE sentence only. No explanations or details."""
    
    def _build_prompt_optimized(self, commits: List[Dict[str, Any]], topic: str) -> str:
        """Build optimized prompt with reduced token usage"""
        prompt = f"Topic: {topic}\n\nCommits ({len(commits)} total):\n"
        
        # Limit to 10 commits and reduce content per commit
        for commit in commits[:10]:
            prompt += f"- {commit['hash']}: {commit['message'][:150]}\n"
            prompt += f"  {commit['author']} | {commit['date'][:10]}\n"
            
            # Show only most relevant files
            files_to_show = commit.get('files_changed', [])[:3]
            if files_to_show:
                prompt += f"  Files: {', '.join(files_to_show)}\n"
            
            # Shorter diff excerpts
            if commit.get('diff') and len(commit['diff'].strip()) > 10:
                diff_excerpt = commit['diff'][:150].strip()
                if diff_excerpt:
                    prompt += f"  Changes: {diff_excerpt}...\n"
            prompt += "\n"
        
        prompt += "\nProvide a structured summary of how this feature evolved:"
        return prompt
    
    def _build_prompt(self, commits: List[Dict[str, Any]], topic: str) -> str:
        """Legacy method - calls optimized version"""
        return self._build_prompt_optimized(commits, topic)
    
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
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": self._get_qa_system_prompt()},
                    {"role": "user", "content": qa_prompt}
                ],
                max_completion_tokens=self.max_qa_tokens
            )
            
            content = response.choices[0].message.content
            logger.info(f"GPT Q&A completed. Response length: {len(content) if content else 0}")
            
            if not content or len(content.strip()) == 0:
                logger.warning("GPT returned empty Q&A response, using fallback")
                return self._fallback_qa_response(question, commits, visualizations)
            
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
    
    def _build_qa_prompt_optimized(self, question: str, topic: str, commits: List[Dict[str, Any]]) -> str:
        """Build optimized Q&A prompt with reduced token usage"""
        prompt = f"Question: {question}\n"
        
        if topic:
            prompt += f"Topic: {topic}\n"
        
        prompt += "\nKey Commits:\n"
        
        # Limit to 8 commits and use compact format
        for commit in commits[:8]:
            prompt += f"{commit['hash']}: {commit['message'][:100]}\n"
            prompt += f"  By {commit['author']} on {commit['date'][:10]}\n"
            
            # Only include diff if it's meaningful
            diff = commit.get('diff', '').strip()
            if diff and len(diff) > 20:
                prompt += f"  Key changes: {diff[:120]}...\n"
            prompt += "\n"
        
        return prompt
    
    def _build_qa_prompt(self, question: str, topic: str, commits: List[Dict[str, Any]]) -> str:
        """Legacy method - calls optimized version"""
        return self._build_qa_prompt_optimized(question, topic, commits)
    
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
