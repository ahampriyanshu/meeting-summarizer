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
                "complete dashboard"
            ],
            "should_have_owners": ["Alice", "Bob", "Charlie"],
            "should_have_deadlines": ["today", "tomorrow", "Friday"]
        }
    },
    
    "test_case_2_planning": {
        "transcript": """We need to finalize the Q2 roadmap today. The team agreed to prioritize 
mobile app development over new features. Sarah will lead the mobile team. 
We need to hire 2 more developers by March. Marketing should start preparing 
the launch campaign.""",
        "description": "Planning meeting with team assignments and hiring needs",
        "expected": {
            "should_contain_action_items": [
                "lead mobile team",
                "hire developers",
                "prepare launch campaign"
            ],
            "should_have_owners": ["Sarah", "Marketing"],
            "should_have_deadlines": ["March"]
        }
    },
    
    "test_case_3_bug_sync": {
        "transcript": """Quick sync on the bug fixes. Mike said the critical login bug is 
fixed and will be deployed this afternoon. Lisa is still working on the 
performance issue, expects to have it done by end of week.""",
        "description": "Bug fix coordination meeting",
        "expected": {
            "should_contain_action_items": [
                "deploy login bug fix",
                "complete performance issue fix"
            ],
            "should_have_owners": ["Mike", "Lisa"],
            "should_have_deadlines": ["this afternoon", "end of week"]
        }
    },
    
    "test_case_4_client_meeting": {
        "transcript": """Client asked for a progress update on the new dashboard. 
Tom will send them screenshots by tomorrow. Emily agreed to schedule a 
demo for next Monday. We should also update the documentation before 
the demo.""",
        "description": "Client meeting with follow-up tasks",
        "expected": {
            "should_contain_action_items": [
                "send screenshots",
                "schedule demo",
                "update documentation"
            ],
            "should_have_owners": ["Tom", "Emily"],
            "should_have_deadlines": ["tomorrow", "next Monday", "before the demo"]
        }
    },
    
    "test_case_5_project_kickoff": {
        "transcript": """Kicking off the new analytics project. Rachel will set up the 
repository today. David needs to create the project plan by end of this week. 
The design team should provide mockups by next Friday. Let's have a 
follow-up meeting next Tuesday to review progress.""",
        "description": "Project kickoff with multiple parallel tasks",
        "expected": {
            "should_contain_action_items": [
                "set up repository",
                "create project plan",
                "provide mockups",
                "schedule follow-up meeting"
            ],
            "should_have_owners": ["Rachel", "David", "design team"],
            "should_have_deadlines": ["today", "end of this week", "next Friday", "next Tuesday"]
        }
    }
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

