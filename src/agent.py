import json
import os
import re
from typing import Dict, Any


class MeetingAgent:
    """Agent responsible for analyzing meeting transcripts and extracting
    structured information"""

    def __init__(self, llm_client):
        self.llm_client = llm_client
        self.summary_prompt = self._load_summary_prompt()

    def _load_summary_prompt(self) -> str:
        """Load the meeting summary prompt from file"""
        try:
            prompt_path = os.path.join(
                os.path.dirname(__file__),
                "..",
                "prompts",
                "summary.txt",
            )
            with open(prompt_path, "r", encoding="utf-8") as f:
                return f.read().strip()
        except FileNotFoundError:
            return (
                "Analyze the meeting transcript and extract meeting title, "
                "agenda, and action items."
            )

    def summarize_meeting(self, transcript: str) -> Dict[str, Any]:
        prompt = f"""
            {self.summary_prompt}
            Meeting Transcript:
            {transcript}
        """

        response = self.llm_client.complete(prompt)
        response_text = response.text if hasattr(response, "text") else str(response)

        return self._parse_summary_response(response_text)

    @staticmethod
    def _parse_summary_response(response_text: str) -> Dict[str, Any]:
        """Parse summary output while handling fenced or malformed JSON."""
        try:
            return json.loads(response_text)
        except json.JSONDecodeError as err:
            markdown_json_match = re.search(
                r"```json\s*(\{.*?\})\s*```", response_text, re.DOTALL
            )
            if markdown_json_match:
                try:
                    return json.loads(markdown_json_match.group(1))
                except json.JSONDecodeError:
                    pass

            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group())
                except json.JSONDecodeError:
                    pass

            raise ValueError("Summary response does not contain valid JSON") from err
