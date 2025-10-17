"""Test meeting transcripts for evaluating the Meeting Summarizer Agent"""

TEST_TRANSCRIPTS = {
    "test_case_1_standup": {
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
    "test_case_2_planning": {
        "transcript": """Manager: We need to finalize the Q2 roadmap today. What should we prioritize?
Sarah: I think we should focus on mobile app development over new features.
Tom: I agree with Sarah. Mobile is more critical right now.
Manager: Great! Sarah, can you lead the mobile team?
Sarah: Absolutely, I'll take the lead.
Manager: Perfect. We also need to hire 2 more developers by March.
Sarah: I'll work with HR on that. Should we involve marketing?
Manager: Yes, marketing should start preparing the launch campaign.
Tom: I'll coordinate with the marketing team.""",
        "description": "Planning meeting with team assignments and hiring needs",
        "expected": {
            "should_contain_action_items": [
                "lead mobile team",
                "hire developers",
                "prepare launch campaign",
            ],
            "should_have_owners": ["Sarah", "marketing"],
            "should_have_deadlines": ["March"],
        },
    },
    "test_case_3_bug_sync": {
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
    "test_case_4_client_meeting": {
        "transcript": """Client: Can we get a progress update on the new dashboard?
Tom: Sure! It's coming along well. I can send you screenshots.
Client: That would be great. When can you send them?
Tom: I'll send them by tomorrow.
Emily: Would you like to schedule a demo to see it in action?
Client: Yes, that would be helpful.
Emily: I'll schedule a demo for next Monday then.
Tom: We should update the documentation before the demo.
Emily: Agreed. Let's make sure that's done.""",
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
    "test_case_5_project_kickoff": {
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
