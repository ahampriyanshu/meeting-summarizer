"""Streamlit App for Meeting Summarizer Agent"""

import streamlit as st
import sys
from pathlib import Path

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

    st.markdown(
        """
        <style>
        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 700px;
            margin: 0 !important;
        }
        h1, h2, h3, h4, h5, h6 {
            text-align: left !important;
        }
        p, div, span {
            text-align: left !important;
        }
        .stButton {
            display: flex;
            justify-content: flex-start;
            margin: 0 !important;
            padding: 0 !important;
        }
        .stButton > button {
            background-color: #4A89F3;
            color: white !important;
            border: none;
            border-radius: 0.5rem;
            padding: 0.75rem 2.5rem;
            font-weight: 600;
            width: auto;
            min-width: 175px;
        }
        .stButton > button:hover {
            background-color: #3A79E3;
            color: white !important;
        }
        .stTextArea {
            text-align: left !important;
        }
        .stTextArea > div > div > textarea {
            width: 100%;
        }
        .stTextArea label {
            text-align: left !important;
        }
        .stSelectbox {
            text-align: left !important;
        }
        .stSelectbox > div {
            width: 100%;
        }
        .stSelectbox label {
            text-align: left !important;
        }
        .stMarkdown {
            width: 100%;
            text-align: left !important;
        }
        .transcript-card {
            background-color: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
            width: 100%;
        }
        .summary-card {
            background-color: #e7f3ff;
            border: 1px solid #b3d7ff;
            border-radius: 0.5rem;
            padding: 1.5rem;
            margin: 1rem 0;
            width: 100%;
        }
        .action-item {
            background-color: rgba(74, 137, 243, 0.1);
            border-left: 4px solid #4A89F3;
            padding: 1rem;
            margin: 0.5rem 0;
            border-radius: 0.25rem;
            width: 100%;
            box-sizing: border-box;
        }
        .stAlert {
            width: 100%;
        }
        .stSuccess, .stError, .stWarning, .stInfo {
            width: 100%;
        }
        .stExpander {
            width: 100%;
        }
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

    st.title("Meeting Summarizer Agent")

    try:
        llm_client = get_llm()
        agent = MeetingAgent(llm_client)
    except Exception as e:
        st.error(f"Failed to initialize agent: {e}")
        st.info("Make sure OPENAI_API_KEY is set in your environment")
        return

    sample_transcripts = {
        "Select Sample Transcript": "",
        "Sample 1: Valid Meeting": """Alice: I finished the login feature yesterday. Ready to deploy.
Bob: Great! I'll deploy it tomorrow.
Charlie: I'm working on the dashboard. Should be done by Friday.
Alice: Can someone review my code before we deploy?
Bob: Sure, I'll review it today.""",
        "Sample 2: Article": """Once upon a time, in a faraway kingdom, there lived a brave knight named Sir Arthur. He had a quest to find the legendary sword that could defeat the dragon terrorizing the village. The journey was long and treacherous, but Sir Arthur was determined to succeed.""",
        "Sample 3: Casual Chat": """John: Did you watch the game last night?
Sarah: Yes! It was amazing. That final goal was incredible.
John: I know! I couldn't believe it. Best game of the season.
Sarah: Definitely. We should watch the next one together.
John: Sounds good!""",
    }

    if "transcript" not in st.session_state:
        st.session_state.transcript = ""

    transcript = st.text_area(
        "Enter the meeting transcript or notes to generate a summary:",
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

    if (
        selected_sample != "Select Sample Transcript"
        and sample_transcripts[selected_sample] != st.session_state.transcript
    ):
        st.session_state.transcript = sample_transcripts[selected_sample]
        st.rerun()

    if st.button("Generate Summary", key="summarize"):
        if not transcript or not transcript.strip():
            st.warning("Please enter a meeting transcript")
        else:
            with st.spinner("Analyzing meeting transcript..."):
                try:
                    result = agent.summarize_meeting(transcript)

                    if not validate_meeting_summary(result):
                        st.error("⚠️ Agent returned invalid response structure")
                        st.json(result)
                    elif "error" in result:
                        if result["error"] == "NOT_A_MEETING_TRANSCRIPT":
                            st.error(
                                "❌ This doesn't appear to be a meeting transcript"
                            )
                            st.info(
                                "The input looks like a story, article, or random text. "
                                "Please provide an actual meeting conversation."
                            )
                        elif result["error"] == "NO_ACTION_ITEMS_FOUND":
                            st.error("❌ No action items or agenda found")
                            st.info(
                                "This appears to be casual conversation without business context. "
                                "Meeting transcripts should have an agenda and actionable outcomes."
                            )
                        else:
                            st.error(f"❌ Error: {result['error']}")

                        with st.expander("View Raw Response"):
                            st.json(result)
                    else:
                        st.markdown("### Meeting Summary")

                        st.markdown(f"**Title:** {result['meeting_title']}")
                        st.markdown(f"**Agenda:** {result['agenda']}")

                        st.markdown("### Action Items")

                        if result["action_items"]:
                            for idx, item in enumerate(result["action_items"], 1):
                                st.markdown(
                                    f"""
                                    <div class='action-item'>
                                        <strong>#{idx}: {item['task']}</strong><br>
                                        <small>Owner: {item['owner']}</small><br>
                                        <small>Deadline: {item['deadline']}</small>
                                    </div>
                                """,
                                    unsafe_allow_html=True,
                                )
                        else:
                            st.info("No action items found in this meeting")

                        with st.expander("View Raw JSON"):
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
