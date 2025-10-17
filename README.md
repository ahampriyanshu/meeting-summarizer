Teams hold multiple meetings daily, with action items, owners, and deadlines scattered across notes. Manually extracting this information is time-consuming and error prone. You are given the task to automate this process.

### Task

Build an AI agent that can automatically extract action items from meeting transcripts, identify owners and deadlines, and detect invalid inputs. The agent should:

- **Infer the meeting title** from the content
- **Identify the main agenda** (1-2 sentences)
- **Extract action items** with task, owner, and deadline

### Requirements

To complete this task, you need to implement:

#### 1. Prompt File

Write a prompt file that defines agent behavior:

- `prompts/summary.txt`: Prompt for extracting meeting information

#### 2. Core Logic

Implement the main agent class in `src/agent.py`:

- `MeetingAgent` class with a `summarize_meeting()` method that:
  - Takes a meeting transcript as input
  - Analyzes the conversation
  - Returns a structured summary

#### 3. Output Format

Your `summarize_meeting()` method must return a dictionary with this exact structure:

**Success Response:**
```json
{
  "meeting_title": "Brief descriptive title",
  "agenda": "Main purpose or topic of the meeting in 1-2 sentences",
  "action_items": [
    {
      "task": "Specific action to be taken",
      "owner": "Person responsible or 'Not specified'",
      "deadline": "When it's due or 'Not specified'"
    }
  ]
}
```

**Error Responses:**

When the input is not a valid meeting transcripto or the transcript has no agenda:
```json
{
  "error": "NO_ACTION_ITEMS_FOUND" or "NOT_A_MEETING_TRANSCRIPT"
}
```

### Sample Cases

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

#### Case 2: Not a Meeting Transcript

**Input:**
```
Once upon a time, in a faraway kingdom, there lived a brave knight 
named Sir Arthur. He had a quest to find the legendary sword that 
could defeat the dragon terrorizing the village. The journey was 
long and treacherous, but Sir Arthur was determined to succeed.
```

**Expected Output:**
```json
{
  "error": "NOT_A_MEETING_TRANSCRIPT"
}
```

#### Case 3: No Action Items

**Input:**
```
John: Did you watch the game last night?
Sarah: Yes! It was amazing. That final goal was incredible.
John: I know! I couldn't believe it. Best game of the season.
Sarah: Definitely. We should watch the next one together.
John: Sounds good!
```

**Expected Output:**
```json
{
  "error": "NO_ACTION_ITEMS_FOUND"
}
```

### Best Practices

- **Prompt Engineering**: Write clear extraction rules. Include examples showing the exact output format. Specify how to handle edge cases (missing info, unclear ownership).
- **Information Extraction:**
  - Look for action verbs (will, should, need to, going to)
  - Identify ownership patterns (I'll, Bob will, team should)
  - Extract time references (today, Friday, by March)
- **Handling Missing Information:** Use "Not specified" for missing owners or deadlines. Don't invent information that's not in the transcript. Be conservative - only extract clear action items.
- **Output Quality:** Keep meeting titles concise and descriptive. Summarize agenda in 1-2 clear sentences. Make action items specific and actionable.
- **Interactive Testing:** Use preview to test your full pipeline in real time.
