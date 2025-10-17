"""Streamlit App for Meeting Summarizer Agent"""

import streamlit as st
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.agent import MeetingAgent
from src.llm import get_llm
from src.helpers import validate_meeting_summary


def main():
    st.set_page_config(
        page_title="Meeting Summarizer Agent",
        page_icon="📝",
        layout="centered",
        initial_sidebar_state="collapsed",
        menu_items=None,
    )

    # Custom CSS
    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1000px;
        }
        .stButton > button {
            background-color: #4A89F3;
            color: white !important;
            border: none;
            border-radius: 0.5rem;
            padding: 0.75rem 2rem;
            font-weight: 600;
            width: 100%;
        }
        .stButton > button:hover {
            background-color: #3A79E3;
            color: white !important;
        }
        .transcript-card {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        .summary-card {
            background-color: #e7f3ff;
            border: 1px solid #b3d7ff;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
        }
        .action-item {
            background-color: white;
            border-left: 4px solid #4A89F3;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0.25rem;
        }
        /* Hide Streamlit header */
        header {
            visibility: hidden;
        }
        #MainMenu {
            visibility: hidden;
        }
        footer {
            visibility: hidden;
        }
        </style>
    """,
        unsafe_allow_html=True,
    )

    st.title("📝 Meeting Summarizer Agent")
    st.markdown(
        "Automatically extract action items, agenda, and key information from meetings"
    )

    # Initialize agent
    try:
        llm_client = get_llm()
        agent = MeetingAgent(llm_client)
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        st.info("Make sure OPENAI_API_KEY is set in your environment")
        return

    st.divider()

    st.markdown("Enter the meeting transcript or notes to generate a summary")

    # Sample transcripts for quick testing
    sample_transcripts = {
        "None": "",
        "Sample 1: Team Standup": """Alice: I finished the login feature yesterday. Ready to deploy.
Bob: Great! I'll deploy it tomorrow.
Charlie: I'm working on the dashboard. Should be done by Friday.
Alice: Can someone review my code before we deploy?
Bob: Sure, I'll review it today.""",
        "Sample 2: Planning Meeting": """Sarah: Let's finalize the Q2 roadmap today. I think we should prioritize mobile app development.
Tom: I agree. Mobile is more important than new features right now.
Sarah: Great! I'll lead the mobile team then.
Tom: Sounds good. We need to hire 2 more developers by March.
Sarah: Yes, and marketing should start preparing the launch campaign.
Tom: I'll talk to the marketing team tomorrow.""",
        "Sample 3: Bug Fix Sync": """Mike: Quick sync on the bug fixes everyone. I fixed the critical login bug.
Lisa: That's great! When will it be deployed?
Mike: This afternoon. Lisa, how's the performance issue?
Lisa: Still working on it. Should be done by end of week.
Mike: Perfect. Let me know if you need any help.""",
    }

    # Initialize session state for transcript
    if "transcript" not in st.session_state:
        st.session_state.transcript = ""

    transcript = st.text_area(
        "Enter meeting transcript:",
        placeholder="Paste your meeting notes or transcript here...",
        height=200,
        value=st.session_state.transcript,
        key="transcript_input",
    )

    selected_sample = st.selectbox(
        "Or try a sample transcript:",
        options=list(sample_transcripts.keys()),
        help="Select a pre-written transcript to test the agent",
    )

    # Update transcript when sample is selected
    if (
        selected_sample != "None"
        and sample_transcripts[selected_sample] != st.session_state.transcript
    ):
        st.session_state.transcript = sample_transcripts[selected_sample]
        st.rerun()

    _, col2, _ = st.columns([1, 2, 1])

    with col2:
        if st.button("🚀 Generate Summary", key="summarize"):
            if not transcript or not transcript.strip():
                st.warning("Please enter a meeting transcript")
            else:
                with st.spinner("Analyzing meeting transcript..."):
                    try:
                        result = agent.summarize_meeting(transcript)

                        # Validate response
                        if not validate_meeting_summary(result):
                            st.error("⚠️ Agent returned invalid response structure")
                            st.json(result)
                        else:
                            st.success("✅ Meeting summary generated successfully!")

                            # Display results
                            st.markdown("### 📋 Meeting Summary")

                            # Meeting Title and Agenda
                            st.markdown(f"**Title:** {result['meeting_title']}")
                            st.markdown(f"**Agenda:** {result['agenda']}")

                            st.markdown("### ✅ Action Items")

                            if result["action_items"]:
                                for idx, item in enumerate(result["action_items"], 1):
                                    st.markdown(
                                        f"""
                                        <div class='action-item'>
                                            <strong>#{idx}: {item['task']}</strong><br>
                                            <small>👤 Owner: {item['owner']}</small><br>
                                            <small>📅 Deadline: {item['deadline']}</small>
                                        </div>
                                    """,
                                        unsafe_allow_html=True,
                                    )
                            else:
                                st.info("No action items found in this meeting")

                            with st.expander("📊 View Raw JSON"):
                                st.json(result)

                    except NotImplementedError:
                        st.error("❌ Agent not implemented yet!")
                        st.info(
                            "Please implement the `summarize_meeting()` method in `src/agent.py`"
                        )
                    except Exception as e:
                        st.error(f"❌ Error processing transcript: {str(e)}")
                        st.exception(e)


if __name__ == "__main__":
    main()
