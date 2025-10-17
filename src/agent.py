"""Meeting Summarizer Agent - CANDIDATE IMPLEMENTS THIS FILE"""

from pathlib import Path
from typing import Dict, Any


class MeetingAgent:
    """
    Meeting Summarizer Agent

    This agent analyzes meeting transcripts and extracts:
    - Meeting title (inferred from content)
    - Main agenda (1-2 sentence summary)
    - Action items with task, owner, and deadline
    """

    def __init__(self, llm_client):
        """
        Initialize the MeetingAgent

        Args:
            llm_client: LLM client instance from src.llm.get_llm()
        """
        self.llm_client = llm_client
        self.prompt_template = self._load_prompt()

    def _load_prompt(self) -> str:
        """
        Load the meeting summary prompt from file

        Returns:
            str: Prompt template content
        """
        prompt_path = Path(__file__).parent.parent / "prompts" / "summary.txt"
        with open(prompt_path, "r") as f:
            return f.read()

    def summarize_meeting(self, transcript: str) -> Dict[str, Any]:
        """
        CANDIDATE IMPLEMENTS: Summarize a meeting transcript

        This method should:
        1. Use the LLM with the loaded prompt to analyze the transcript
        2. Extract the meeting title, agenda, and action items
        3. Return a properly formatted dictionary

        Args:
            transcript (str): Meeting transcript or notes

        Returns:
            dict: Summary dictionary with the following structure:
                {
                    "meeting_title": str,    # Brief descriptive title
                    "agenda": str,           # Main purpose in 1-2 sentences
                    "action_items": [        # List of action items
                        {
                            "task": str,     # What needs to be done
                            "owner": str,    # Who is responsible
                            "deadline": str  # When it's due
                        }
                    ]
                }

        Example:
            >>> agent = MeetingAgent(llm)
            >>> result = agent.summarize_meeting(
            ...     "Alice: I'll finish the report by Friday. Bob: I'll review it."
            ... )
            >>> print(result)
            {
                "meeting_title": "Project Update",
                "agenda": "Coordinate on report completion and review",
                "action_items": [
                    {
                        "task": "Finish the report",
                        "owner": "Alice",
                        "deadline": "Friday"
                    },
                    {
                        "task": "Review the report",
                        "owner": "Bob",
                        "deadline": "Not specified"
                    }
                ]
            }
        """
        raise NotImplementedError(
            "Candidate must implement the summarize_meeting() method"
        )
