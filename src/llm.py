"""LLM Helper - Provides LLM instance for the agent"""

import os
from typing import Optional
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI

load_dotenv()


class LLMClient:
    """Simple LLM client for text completions"""
    
    def __init__(self):
        """Initialize LLM client with environment validation"""
        self._validate_environment()
        self._llm = None
    
    def _validate_environment(self):
        """Validate required environment variables"""
        if not os.getenv("OPENAI_API_KEY"):
            raise ValueError(
                "OpenAI API key is required for LLM operations. "
                "Please set environment variables:\n"
                "OPENAI_API_KEY=your_api_key\n"
                "OPENAI_API_BASE=https://api.openai.com/v1 (optional)\n"
                "Example: OPENAI_API_KEY=sk-your-key python app.py"
            )
    
    @property
    def llm(self) -> OpenAI:
        """Get LLM instance (lazy initialization)"""
        if self._llm is None:
            self._llm = OpenAI(
                model="gpt-4o-mini",
                max_tokens=4096,
                temperature=0.1,
            )
        return self._llm
    
    def complete(self, prompt: str) -> str:
        """
        Complete a text prompt
        
        Args:
            prompt: The text prompt to complete
            
        Returns:
            The LLM response text
        """
        try:
            response = self.llm.complete(prompt)
            return response.text
        except Exception as e:
            raise Exception(f"LLM completion failed: {e}") from e


_llm_client: Optional[LLMClient] = None


def get_llm() -> LLMClient:
    """Get the global LLM client instance (singleton pattern)"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client

