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
        test_case = TEST_TRANSCRIPTS["test_case_1_standup"]

        result = self.agent.summarize_meeting(test_case["transcript"])

        assert isinstance(result, dict), "Response must be a dictionary"

        # Check required keys
        required_keys = {"meeting_title", "agenda", "action_items"}
        assert required_keys.issubset(
            result.keys()
        ), f"Missing keys: {required_keys - set(result.keys())}"

        # Validate using helper
        assert validate_meeting_summary(result), "Response structure is invalid"

    def test_case_1_standup(self):
        """Test Case 1: Simple team standup"""
        test_case = TEST_TRANSCRIPTS["test_case_1_standup"]

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
        print(f"Test Case 1: {test_case['description']}")
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

    def test_case_2_planning(self):
        """Test Case 2: Planning meeting"""
        test_case = TEST_TRANSCRIPTS["test_case_2_planning"]

        result = self.agent.summarize_meeting(test_case["transcript"])

        assert validate_meeting_summary(result), "Invalid response structure"

        evaluation = judge_meeting_summary(
            transcript=test_case["transcript"],
            agent_summary=result,
            expected=test_case["expected"],
            llm=self.llm,
        )

        print(f"\n{'='*60}")
        print(f"Test Case 2: {test_case['description']}")
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

    def test_case_3_bug_sync(self):
        """Test Case 3: Bug fix sync"""
        test_case = TEST_TRANSCRIPTS["test_case_3_bug_sync"]

        result = self.agent.summarize_meeting(test_case["transcript"])

        assert validate_meeting_summary(result), "Invalid response structure"

        evaluation = judge_meeting_summary(
            transcript=test_case["transcript"],
            agent_summary=result,
            expected=test_case["expected"],
            llm=self.llm,
        )

        print(f"\n{'='*60}")
        print(f"Test Case 3: {test_case['description']}")
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

    def test_case_4_client_meeting(self):
        """Test Case 4: Client meeting"""
        test_case = TEST_TRANSCRIPTS["test_case_4_client_meeting"]

        result = self.agent.summarize_meeting(test_case["transcript"])

        assert validate_meeting_summary(result), "Invalid response structure"

        evaluation = judge_meeting_summary(
            transcript=test_case["transcript"],
            agent_summary=result,
            expected=test_case["expected"],
            llm=self.llm,
        )

        print(f"\n{'='*60}")
        print(f"Test Case 4: {test_case['description']}")
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

    def test_case_5_project_kickoff(self):
        """Test Case 5: Project kickoff"""
        test_case = TEST_TRANSCRIPTS["test_case_5_project_kickoff"]

        result = self.agent.summarize_meeting(test_case["transcript"])

        assert validate_meeting_summary(result), "Invalid response structure"

        evaluation = judge_meeting_summary(
            transcript=test_case["transcript"],
            agent_summary=result,
            expected=test_case["expected"],
            llm=self.llm,
        )

        print(f"\n{'='*60}")
        print(f"Test Case 5: {test_case['description']}")
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


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
