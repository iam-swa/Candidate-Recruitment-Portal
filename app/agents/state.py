"""
State definition for the agent workflow.
"""

from typing import Annotated, List, Optional

from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages
from typing_extensions import TypedDict

class RecruitmentState(TypedDict):
    """State shared across all nodes in the recruitment workflow."""

    messages: Annotated[List[BaseMessage], add_messages]
    user_query: str
    user_intent: str
    session_summary: str
    turn_count: int
    current_response: Optional[str]
    error: List[str]
    orchestrator_result: Optional[str]

def get_initial_state() -> RecruitmentState:
    """Get the initial recruitment state."""
    return RecruitmentState(
        messages=[],
        user_query="",
        user_intent="unknown",
        session_summary="",
        turn_count=0,
        current_response=None,
        error=[],
        orchestrator_result=None,
    )
