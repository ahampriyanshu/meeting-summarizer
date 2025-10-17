"""LLM Judge for evaluating Meeting Agent summaries"""

from typing import Dict, Any


JUDGE_SYSTEM_PROMPT = """You are an expert evaluator for meeting summarizer systems.
Your job is to assess whether an AI agent correctly extracted information from a meeting transcript.

Evaluate based on these criteria:
1. **Action Items Completeness (40%)**: Did it find all action items from the transcript?
2. **Ownership Accuracy (20%)**: Are the owners correctly identified?
3. **Deadline Accuracy (20%)**: Are deadlines correctly extracted?
4. **Meeting Context (10%)**: Is the title and agenda appropriate?
5. **Output Quality (10%)**: Is the output clear and well-structured?

Return your evaluation as JSON with this structure:
{
  "pass": true/false,
  "score": 0-100,
  "feedback": "Overall assessment",
  "criteria_scores": {
    "action_items_completeness": 0-40,
    "ownership_accuracy": 0-20,
    "deadline_accuracy": 0-20,
    "meeting_context": 0-10,
    "output_quality": 0-10
  },
  "issues": ["list of any problems found"]
}

Be fair but thorough. Missing one action item shouldn't fail the test, but missing multiple or getting owners/deadlines wrong should result in failure.
The agent should pass with a score >= 60.
"""


def judge_meeting_summary(
    transcript: str, agent_summary: Dict[str, Any], expected: Dict[str, Any], llm_client
) -> Dict[str, Any]:
    """
    Use LLM to judge the quality of a meeting summary using semantic evaluation

    Args:
        transcript: The meeting transcript
        agent_summary: The agent's summary
        expected: Expected patterns (action items, owners, deadlines)
        llm_client: LLM client instance

    Returns:
        dict: Judge evaluation with pass/fail, score, and feedback
    """

    full_prompt = f"""{JUDGE_SYSTEM_PROMPT}


# MEETING TRANSCRIPT
```
{transcript}
```

# AGENT'S SUMMARY
```json
{agent_summary}
```

# EXPECTED PATTERNS
The summary should contain these elements (use semantic matching, not exact strings):

Action Items (should extract tasks similar to):
{chr(10).join(f"- {item}" for item in expected.get('should_contain_action_items', []))}

Owners (should identify people/teams including):
{chr(10).join(f"- {owner}" for owner in expected.get('should_have_owners', []))}

Deadlines (should extract timeframes like):
{chr(10).join(f"- {deadline}" for deadline in expected.get('should_have_deadlines', []))}

# YOUR TASK
Evaluate the agent's summary. Use SEMANTIC MATCHING - don't require exact word matches.

For example:
- "Deploy login feature" matches "deploy login bug fix" (similar meaning)
- "Bob" matches if listed as owner
- "tomorrow" matches "tomorrow" or "the next day"

Check:
1. **Action Items Completeness (40%)**:
   - Did it extract all meaningful action items from the transcript?
   - Are the tasks clearly described?
   - Missing one minor item is acceptable, missing multiple is not

2. **Ownership Accuracy (20%)**:
   - Are the owners correctly identified?
   - "Not specified" is acceptable when no owner is mentioned
   - Incorrect attribution should be penalized

3. **Deadline Accuracy (20%)**:
   - Are deadlines correctly extracted?
   - "Not specified" is acceptable when no deadline is mentioned
   - Incorrect deadlines should be penalized

4. **Meeting Context (10%)**:
   - Is the meeting title appropriate and descriptive?
   - Does the agenda capture the main purpose?

5. **Output Quality (10%)**:
   - Is the output well-structured and clear?
   - Are all required fields present?

A summary should PASS if:
- It extracts most action items (missing 1 out of 3-4 is ok)
- Owners are correctly identified or marked "Not specified"
- Deadlines are accurate or marked "Not specified"
- Title and agenda are reasonable
- Score >= 60

A summary should FAIL if:
- Multiple action items are missing
- Owners are frequently wrong (not just "Not specified")
- Deadlines are incorrect
- Output structure is invalid
- Score < 60
"""

    try:
        response_text = llm_client.complete(full_prompt)

        # Parse JSON from response
        import json
        import re

        json_match = re.search(
            r"```(?:json)?\s*(\{.*?\})\s*```", response_text, re.DOTALL
        )
        if json_match:
            json_str = json_match.group(1)
        else:
            json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
            if json_match:
                json_str = json_match.group(0)
            else:
                json_str = response_text

        evaluation = json.loads(json_str)

        # Ensure required fields
        if "pass" not in evaluation:
            evaluation["pass"] = evaluation.get("score", 0) >= 60
        if "score" not in evaluation:
            evaluation["score"] = 60 if evaluation.get("pass") else 40
        if "feedback" not in evaluation:
            evaluation["feedback"] = "Evaluation completed"

        return evaluation

    except Exception as e:
        # Fallback evaluation if LLM judge fails
        return {
            "pass": False,
            "score": 0,
            "feedback": f"Judge evaluation failed: {str(e)}",
            "criteria_scores": {},
            "issues": [f"Judge error: {str(e)}"],
        }
