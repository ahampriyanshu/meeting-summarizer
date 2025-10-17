"""LLM Helper - Provides LLM instance for the agent"""

import os
import json
import hashlib
from typing import Optional
from dotenv import load_dotenv
from llama_index.llms.openai import OpenAI

load_dotenv()


def _get_cache_file(input_hash: str) -> str:
    """Get cache file path based on input content hash for persistence across runs."""
    cache_dir = os.path.join(os.getcwd(), ".pytest_cache")
    os.makedirs(cache_dir, exist_ok=True)
    return os.path.join(cache_dir, f"cache_{input_hash[:8]}.json")


def _get_input_hash(prompt: str, model: str, max_tokens: int) -> str:
    """Create a hash of input parameters for caching."""
    input_str = f"{prompt}|{model}|{max_tokens}"
    return hashlib.sha256(input_str.encode()).hexdigest()


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
        Complete a text prompt with caching

        Args:
            prompt: The text prompt to complete

        Returns:
            The LLM response text
        """
        cache_key = _get_input_hash(prompt, "gpt-4o-mini", 4096)
        cache_file = _get_cache_file(cache_key)

        try:
            if os.path.exists(cache_file):
                with open(cache_file, "r", encoding="utf-8") as f:
                    cache_data = json.load(f)
                    if cache_key in cache_data:
                        return cache_data[cache_key]
        except (json.JSONDecodeError, IOError, OSError):
            pass

        try:
            response = self.llm.complete(prompt)
            content = response.text

            try:
                cache_data = {}
                if os.path.exists(cache_file):
                    with open(cache_file, "r", encoding="utf-8") as f:
                        cache_data = json.load(f)

                cache_data[cache_key] = content

                with open(cache_file, "w", encoding="utf-8") as f:
                    json.dump(cache_data, f, indent=2)
            except Exception:
                pass

            return content
        except Exception as e:
            raise Exception(f"LLM completion failed: {e}") from e


_llm_client: Optional[LLMClient] = None


def get_llm() -> LLMClient:
    """Get the global LLM client instance (singleton pattern)"""
    global _llm_client
    if _llm_client is None:
        _llm_client = LLMClient()
    return _llm_client
