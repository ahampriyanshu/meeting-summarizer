"""Helper functions for the Meeting Summarizer Agent"""

import json
import re
from typing import Dict, Any


def validate_meeting_summary(summary: Dict[str, Any]) -> bool:
    """
    Validate that the meeting summary has the correct structure

    Accepts both success responses and error responses

    Args:
        summary: Summary dictionary from the agent

    Returns:
        bool: True if valid, False otherwise
    """
    # Check if this is an error response
    if "error" in summary:
        valid_errors = {"NOT_A_MEETING_TRANSCRIPT", "NO_ACTION_ITEMS_FOUND"}
        return (
            len(summary) == 1
            and isinstance(summary["error"], str)
            and summary["error"] in valid_errors
        )

    # Otherwise validate as a normal success response
    required_keys = {"meeting_title", "agenda", "action_items"}

    # Check all required keys exist
    if not all(key in summary for key in required_keys):
        return False

    # Validate meeting_title is non-empty string
    if (
        not isinstance(summary["meeting_title"], str)
        or not summary["meeting_title"].strip()
    ):
        return False

    # Validate agenda is non-empty string
    if not isinstance(summary["agenda"], str) or not summary["agenda"].strip():
        return False

    # Validate action_items is a list
    if not isinstance(summary["action_items"], list):
        return False

    # Validate each action item has required fields
    for item in summary["action_items"]:
        if not isinstance(item, dict):
            return False

        required_item_keys = {"task", "owner", "deadline"}
        if not all(key in item for key in required_item_keys):
            return False

        # Check that all fields are non-empty strings
        if not isinstance(item["task"], str) or not item["task"].strip():
            return False
        if not isinstance(item["owner"], str) or not item["owner"].strip():
            return False
        if not isinstance(item["deadline"], str) or not item["deadline"].strip():
            return False

    return True


def parse_json_response(text: str) -> Dict[str, Any]:
    """
    Parse JSON from LLM response, handling markdown code blocks

    Args:
        text: Raw text response from LLM

    Returns:
        dict: Parsed JSON object

    Raises:
        json.JSONDecodeError: If JSON cannot be parsed
    """
    # Try to extract JSON from markdown code blocks
    json_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find JSON object in the text
        json_match = re.search(r"\{.*\}", text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            json_str = text

    return json.loads(json_str)
