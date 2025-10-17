"""Test suite for Meeting Summarizer Agent"""

import pytest
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from src.agent import MeetingAgent
from src.llm import get_llm
from src.helpers import validate_meeting_summary
from data.test_transcripts import TEST_TRANSCRIPTS
from judge.llm_judge import judge_meeting_summary


class TestMeetingAgent:
    """Test suite for the Meeting Summarizer Agent"""

    def setup_method(self):
        """Setup test environment"""
        self.llm_client = get_llm()
        self.agent = MeetingAgent(self.llm_client)

    def test_agent_implemented(self):
        """Test that the agent is implemented"""
        try:
            result = self.agent.summarize_meeting("Test meeting transcript")
            assert result is not None, "summarize_meeting() should return a result"
        except NotImplementedError:
            pytest.fail(
                "Candidate must implement summarize_meeting() method in src/agent.py"
            )

    def test_response_structure(self):
        """Test that responses have correct structure"""
        test_case = TEST_TRANSCRIPTS["test_case_standup"]

        result = self.agent.summarize_meeting(test_case["transcript"])

        assert isinstance(result, dict), "Response must be a dictionary"

        # Check required keys
        required_keys = {"meeting_title", "agenda", "action_items"}
        assert required_keys.issubset(
            result.keys()
        ), f"Missing keys: {required_keys - set(result.keys())}"

        # Validate using helper
        assert validate_meeting_summary(result), "Response structure is invalid"

    def test_standup(self):
        """Test: Simple team standup"""
        test_case = TEST_TRANSCRIPTS["test_case_standup"]

        result = self.agent.summarize_meeting(test_case["transcript"])

        # Validate structure
        assert validate_meeting_summary(result), "Invalid response structure"

        # LLM Judge evaluation
        evaluation = judge_meeting_summary(
            transcript=test_case["transcript"],
            agent_summary=result,
            expected=test_case["expected"],
            llm_client=self.llm_client,
        )

        print(f"\n{'='*60}")
        print(f"Test: {test_case['description']}")
        print(f"{'='*60}")
        print(f"Agent Summary: {result}")
        print(f"\nJudge Evaluation:")
        print(f"  Pass: {evaluation['pass']}")
        print(f"  Score: {evaluation['score']}/100")
        print(f"  Feedback: {evaluation['feedback']}")
        if evaluation.get("issues"):
            print(f"  Issues: {evaluation['issues']}")
        print(f"{'='*60}\n")

        assert evaluation[
            "pass"
        ], f"Test failed: {evaluation.get('feedback', 'No feedback')}"
        assert evaluation["score"] >= 60, f"Score too low: {evaluation['score']}/100"

    def test_bug_sync(self):
        """Test: Bug fix sync"""
        test_case = TEST_TRANSCRIPTS["test_case_bug_sync"]

        result = self.agent.summarize_meeting(test_case["transcript"])

        assert validate_meeting_summary(result), "Invalid response structure"

        evaluation = judge_meeting_summary(
            transcript=test_case["transcript"],
            agent_summary=result,
            expected=test_case["expected"],
            llm_client=self.llm_client,
        )

        print(f"\n{'='*60}")
        print(f"Test: {test_case['description']}")
        print(f"{'='*60}")
        print(f"Agent Summary: {result}")
        print(f"\nJudge Evaluation:")
        print(f"  Pass: {evaluation['pass']}")
        print(f"  Score: {evaluation['score']}/100")
        print(f"  Feedback: {evaluation['feedback']}")
        if evaluation.get("issues"):
            print(f"  Issues: {evaluation['issues']}")
        print(f"{'='*60}\n")

        assert evaluation[
            "pass"
        ], f"Test failed: {evaluation.get('feedback', 'No feedback')}"
        assert evaluation["score"] >= 60, f"Score too low: {evaluation['score']}/100"

    def test_client_meeting(self):
        """Test: Client meeting"""
        test_case = TEST_TRANSCRIPTS["test_case_client_meeting"]

        result = self.agent.summarize_meeting(test_case["transcript"])

        assert validate_meeting_summary(result), "Invalid response structure"

        evaluation = judge_meeting_summary(
            transcript=test_case["transcript"],
            agent_summary=result,
            expected=test_case["expected"],
            llm_client=self.llm_client,
        )

        print(f"\n{'='*60}")
        print(f"Test: {test_case['description']}")
        print(f"{'='*60}")
        print(f"Agent Summary: {result}")
        print(f"\nJudge Evaluation:")
        print(f"  Pass: {evaluation['pass']}")
        print(f"  Score: {evaluation['score']}/100")
        print(f"  Feedback: {evaluation['feedback']}")
        if evaluation.get("issues"):
            print(f"  Issues: {evaluation['issues']}")
        print(f"{'='*60}\n")

        assert evaluation[
            "pass"
        ], f"Test failed: {evaluation.get('feedback', 'No feedback')}"
        assert evaluation["score"] >= 60, f"Score too low: {evaluation['score']}/100"

    def test_project_kickoff(self):
        """Test: Project kickoff"""
        test_case = TEST_TRANSCRIPTS["test_case_project_kickoff"]

        result = self.agent.summarize_meeting(test_case["transcript"])

        assert validate_meeting_summary(result), "Invalid response structure"

        evaluation = judge_meeting_summary(
            transcript=test_case["transcript"],
            agent_summary=result,
            expected=test_case["expected"],
            llm_client=self.llm_client,
        )

        print(f"\n{'='*60}")
        print(f"Test: {test_case['description']}")
        print(f"{'='*60}")
        print(f"Agent Summary: {result}")
        print(f"\nJudge Evaluation:")
        print(f"  Pass: {evaluation['pass']}")
        print(f"  Score: {evaluation['score']}/100")
        print(f"  Feedback: {evaluation['feedback']}")
        if evaluation.get("issues"):
            print(f"  Issues: {evaluation['issues']}")
        print(f"{'='*60}\n")

        assert evaluation[
            "pass"
        ], f"Test failed: {evaluation.get('feedback', 'No feedback')}"
        assert evaluation["score"] >= 60, f"Score too low: {evaluation['score']}/100"

    def test_not_a_meeting(self):
        """Test: Reject non-meeting text"""
        test_case = TEST_TRANSCRIPTS["test_case_not_a_meeting"]

        result = self.agent.summarize_meeting(test_case["transcript"])

        assert validate_meeting_summary(result), "Invalid response structure"
        assert "error" in result, "Should return error for non-meeting text"
        assert (
            result["error"] == test_case["expected_error"]
        ), f"Expected error: {test_case['expected_error']}, got: {result.get('error')}"

        print(f"\n{'='*60}")
        print(f"Test: {test_case['description']}")
        print(f"{'='*60}")
        print(f"Agent Response: {result}")
        print(f"✅ Correctly identified as: {result['error']}")
        print(f"{'='*60}\n")

    def test_no_action_items(self):
        """Test: Reject transcripts with no action items"""
        test_case = TEST_TRANSCRIPTS["test_case_no_action_items"]

        result = self.agent.summarize_meeting(test_case["transcript"])

        assert validate_meeting_summary(result), "Invalid response structure"
        assert (
            "error" in result
        ), "Should return error for transcript with no action items"
        assert (
            result["error"] == test_case["expected_error"]
        ), f"Expected error: {test_case['expected_error']}, got: {result.get('error')}"

        print(f"\n{'='*60}")
        print(f"Test: {test_case['description']}")
        print(f"{'='*60}")
        print(f"Agent Response: {result}")
        print(f"✅ Correctly identified as: {result['error']}")
        print(f"{'='*60}\n")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
