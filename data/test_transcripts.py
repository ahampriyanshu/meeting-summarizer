"""Test meeting transcripts for evaluating the Meeting Summarizer Agent"""

TEST_TRANSCRIPTS = {
    "test_case_standup": {
        "transcript": """Alice: I finished the login feature yesterday. Ready to deploy.
Bob: Great! I'll deploy it tomorrow.
Charlie: I'm working on the dashboard. Should be done by Friday.
Alice: Can someone review my code before we deploy?
Bob: Sure, I'll review it today.""",
        "description": "Simple team standup with clear action items and owners",
        "expected": {
            "should_contain_action_items": [
                "review code",
                "deploy login feature",
                "complete dashboard",
            ],
            "should_have_owners": ["Alice", "Bob", "Charlie"],
            "should_have_deadlines": ["today", "tomorrow", "Friday"],
        },
    },
    "test_case_bug_sync": {
        "transcript": """Mike: Quick sync on the bug fixes everyone. I fixed the critical login bug.
Lisa: That's great! When will it be deployed?
Mike: I'll deploy it this afternoon.
Team Lead: Excellent. Lisa, what's the status on the performance issue?
Lisa: Still working on it. I expect to have it done by end of week.
Team Lead: Sounds good. Let us know if you need any help.
Lisa: Will do, thanks!""",
        "description": "Bug fix coordination meeting",
        "expected": {
            "should_contain_action_items": [
                "deploy login bug fix",
                "complete performance issue fix",
            ],
            "should_have_owners": ["Mike", "Lisa"],
            "should_have_deadlines": ["this afternoon", "end of week"],
        },
    },
    "test_case_client_meeting": {
        "transcript": """Client: Can we get a progress update on the new dashboard?
Tom: Sure! It's coming along well. I'll send you screenshots by tomorrow.
Client: That would be great, thank you.
Emily: Would you like to schedule a demo to see it in action?
Client: Yes, that would be helpful.
Emily: Perfect. I'll schedule a demo for next Monday.
Tom: We should update the documentation before the demo.
Emily: Good point. I'll update the documentation before the demo.""",
        "description": "Client meeting with follow-up tasks",
        "expected": {
            "should_contain_action_items": [
                "send screenshots",
                "schedule demo",
                "update documentation",
            ],
            "should_have_owners": ["Tom", "Emily"],
            "should_have_deadlines": ["tomorrow", "next Monday", "before the demo"],
        },
    },
    "test_case_project_kickoff": {
        "transcript": """Manager: Let's kick off the new analytics project. Rachel, can you set up the repository?
Rachel: Yes, I'll set it up today.
Manager: Great. David, we need a project plan. When can you have it ready?
David: I can create the project plan by end of this week.
Manager: Perfect. Design team, we'll need mockups as well.
Designer: We can provide mockups by next Friday.
Manager: Excellent. Let's schedule a follow-up meeting to review progress.
Rachel: How about next Tuesday?
Manager: Next Tuesday works. I'll send out a calendar invite.""",
        "description": "Project kickoff with multiple parallel tasks",
        "expected": {
            "should_contain_action_items": [
                "set up repository",
                "create project plan",
                "provide mockups",
                "schedule follow-up meeting",
            ],
            "should_have_owners": ["Rachel", "David", "design team"],
            "should_have_deadlines": [
                "today",
                "end of this week",
                "next Friday",
                "next Tuesday",
            ],
        },
    },
    "test_case_not_a_meeting": {
        "transcript": """Once upon a time, in a faraway kingdom, there lived a brave knight named Sir Arthur. He had a quest to find the legendary sword that could defeat the dragon terrorizing the village. The journey was long and treacherous, but Sir Arthur was determined to succeed.""",
        "description": "Story text that is not a meeting transcript",
        "expected_error": "NOT_A_MEETING_TRANSCRIPT",
    },
    "test_case_no_action_items": {
        "transcript": """John: Did you watch the game last night?
Sarah: Yes! It was amazing. That final goal was incredible.
John: I know! I couldn't believe it. Best game of the season.
Sarah: Definitely. We should watch the next one together.
John: Sounds good!""",
        "description": "Casual conversation with no action items or agenda",
        "expected_error": "NO_ACTION_ITEMS_FOUND",
    },
}


def get_test_transcript(test_case_name: str):
    """
    Get a test transcript by name

    Args:
        test_case_name: Name of the test case

    Returns:
        dict: Test transcript data
    """
    return TEST_TRANSCRIPTS.get(test_case_name)


def get_all_test_transcripts():
    """
    Get all test transcripts

    Returns:
        dict: All test transcript data
    """
    return TEST_TRANSCRIPTS
