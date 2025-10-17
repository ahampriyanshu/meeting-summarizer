# Meeting Summarizer Agent

After every meeting, someone needs to manually extract key information from the discussion - what was decided, who needs to do what, and by when. This is time-consuming and important details often get missed.

Build an AI agent that automatically:
- Extracts the meeting's main agenda
- Identifies all action items with clear owners and deadlines
- Generates a concise meeting title

### Task

Build a simple AI agent that processes meeting transcripts and extracts structured information. Your agent should:

- **Infer the meeting title** from the content
- **Identify the main agenda** (1-2 sentences)
- **Extract action items** with task, owner, and deadline

### Requirements

To complete this task, you need to implement:

#### 1. Prompt File

Write a prompt file that defines agent behavior:

- `prompts/meeting_summary_prompt.txt`: Prompt for extracting meeting information

#### 2. Core Logic

Implement the main agent class in `src/meeting_agent.py`:

- `MeetingAgent` class with a `summarize_meeting()` method that:
  - Takes a meeting transcript as input
  - Analyzes the conversation
  - Returns a structured summary

#### 3. Output Format

Your `summarize_meeting()` method must return a dictionary with this exact structure:

```json
{
  "meeting_title": "Brief descriptive title",
  "agenda": "Main purpose or topic of the meeting in 1-2 sentences",
  "action_items": [
    {
      "task": "Specific action to be taken",
      "owner": "Person responsible (or 'Not specified')",
      "deadline": "When it's due (or 'Not specified')"
    }
  ]
}
```

### Extraction Guidelines

#### Meeting Title
- Should be brief (3-6 words)
- Capture the meeting type or main topic
- Examples: "Q2 Planning Meeting", "Product Launch Review", "Team Standup"

#### Agenda
- Summarize the main purpose in 1-2 sentences
- Focus on what the meeting aimed to accomplish
- Be concise and clear

#### Action Items
- Extract ALL tasks that someone needs to do
- Include explicit and implicit action items
- Format:
  - **task**: Clear, actionable description
  - **owner**: Person's name, team name, or "Not specified"
  - **deadline**: "Today", "Tomorrow", "End of week", "By [date]", or "Not specified"

### Action Item Rules

**Extract as action items:**
- Explicit commitments: "I'll do X by Friday"
- Assignments: "Bob will handle the deployment"
- Agreements: "We decided Alice should lead this"
- Future work: "Need to hire 2 developers by March"

**Owner extraction:**
- Use person's name if mentioned: "Alice", "Bob"
- Use team if no person: "Marketing team", "Engineering"
- Use "Not specified" if unclear

**Deadline extraction:**
- Relative: "today", "tomorrow", "this week", "next Monday"
- Absolute: "by March 15", "end of Q2"
- Use "Not specified" if no deadline mentioned

### Sample Test Cases

#### Case 1: Simple Team Standup

**Input:**
```
Alice: I finished the login feature. Ready to deploy.
Bob: Great! I'll deploy it tomorrow.
Charlie: Working on the dashboard. Should be done by Friday.
Alice: Can someone review my code before we deploy?
Bob: I'll review it today.
```

**Expected Output:**
```json
{
  "meeting_title": "Team Standup",
  "agenda": "Team members share progress updates and coordinate on upcoming tasks",
  "action_items": [
    {
      "task": "Review Alice's code",
      "owner": "Bob",
      "deadline": "Today"
    },
    {
      "task": "Deploy login feature",
      "owner": "Bob",
      "deadline": "Tomorrow"
    },
    {
      "task": "Complete dashboard work",
      "owner": "Charlie",
      "deadline": "Friday"
    }
  ]
}
```

#### Case 2: Product Planning

**Input:**
```
We need to finalize the Q2 roadmap. The team agreed to prioritize 
mobile app development over new features. Sarah will lead the mobile 
team. We need to hire 2 more developers by March. Marketing should 
start preparing the launch campaign.
```

**Expected Output:**
```json
{
  "meeting_title": "Q2 Roadmap Planning",
  "agenda": "Finalize Q2 priorities and assign team leadership for mobile app development",
  "action_items": [
    {
      "task": "Lead mobile team",
      "owner": "Sarah",
      "deadline": "Not specified"
    },
    {
      "task": "Hire 2 developers",
      "owner": "Not specified",
      "deadline": "By March"
    },
    {
      "task": "Prepare launch campaign",
      "owner": "Marketing",
      "deadline": "Not specified"
    }
  ]
}
```

#### Case 3: Quick Sync

**Input:**
```
Quick sync on the bug fixes. Mike said the critical login bug is 
fixed and will be deployed this afternoon. Lisa is still working 
on the performance issue, expects to have it done by end of week.
```

**Expected Output:**
```json
{
  "meeting_title": "Bug Fix Sync",
  "agenda": "Review status of critical bug fixes and coordinate deployment timeline",
  "action_items": [
    {
      "task": "Deploy login bug fix",
      "owner": "Mike",
      "deadline": "This afternoon"
    },
    {
      "task": "Complete performance issue fix",
      "owner": "Lisa",
      "deadline": "End of week"
    }
  ]
}
```

### Best Practices

1. **Prompt Engineering:**
   - Write clear extraction rules
   - Include examples showing the exact output format
   - Specify how to handle edge cases (missing info, unclear ownership)

2. **Information Extraction:**
   - Look for action verbs (will, should, need to, going to)
   - Identify ownership patterns (I'll, Bob will, team should)
   - Extract time references (today, Friday, by March)

3. **Handling Missing Information:**
   - Use "Not specified" for missing owners or deadlines
   - Don't invent information that's not in the transcript
   - Be conservative - only extract clear action items

4. **Output Quality:**
   - Keep meeting titles concise and descriptive
   - Summarize agenda in 1-2 clear sentences
   - Make action items specific and actionable
   - Ensure all required fields are present

### Testing

Use the Streamlit interface to test your agent interactively:

```bash
bash scripts/run.sh
```

Run the automated test suite:

```bash
bash scripts/test.sh
```

Your implementation will be evaluated on:
- Correct extraction of all action items
- Accurate identification of owners and deadlines
- Appropriate meeting title and agenda
- Proper handling of edge cases
- Valid output structure

