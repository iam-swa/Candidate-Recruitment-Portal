"""
Orchestrator Node for the Recruitment Workflow.
"""

from typing import Any, Dict
import structlog

from app.agents.base_agent import BaseAgent
from app.agents.state import RecruitmentState
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langgraph.prebuilt import create_react_agent
from app.tools.recruitment_tools import get_recruitment_tools

logger = structlog.get_logger(__name__)

class OrchestratorNode:
    """Node for processing conversations through the orchestrator agent."""

    def __init__(self, orchestrator_agent: BaseAgent) -> None:
        self.orchestrator_agent = orchestrator_agent
        
    @staticmethod
    def _extract_text(content) -> str:
        """Extract text from content that may be a string or a list of content blocks."""
        if isinstance(content, str):
            return content
        if isinstance(content, list):
            parts = []
            for block in content:
                if isinstance(block, dict) and block.get("type") == "text":
                    parts.append(block["text"])
                elif isinstance(block, str):
                    parts.append(block)
            return "\n".join(parts)
        return str(content)

    def process(self, state: RecruitmentState) -> Dict[str, Any]:
        """Process the current state through the orchestrator."""
        try:
            user_msg = ""
            for msg in reversed(state.get("messages", [])):
                if isinstance(msg, HumanMessage):
                    user_msg = msg.content
                    break

            current_intent = state.get("user_intent", "unknown")

            # Update state with the intent so it's passed to prompt correctly
            tools = get_recruitment_tools()
            state_with_intent = dict(state)
            state_with_intent["user_intent"] = current_intent
            
            prompt = self.orchestrator_agent.get_prompt(state_with_intent)

            agent = create_react_agent(
                self.orchestrator_agent.model,
                tools,
                prompt=prompt,
            )

            result = agent.invoke({"messages": state.get("messages", [])})
            orchestrator_response = ""

            for msg in reversed(result.get("messages", [])):
                if isinstance(msg, AIMessage) and msg.content and not getattr(msg, "tool_calls", None):
                    orchestrator_response = self._extract_text(msg.content)
                    break
            
            if not orchestrator_response:
                # Fallback in case no suitable AIMessage is found
                logger.warning("No AIMessage found in agent response. Defaulting to a generic response.", agent_result=result)
                orchestrator_response = "I'm sorry, I couldn't process that. Could you please rephrase?"

            return {
                "messages": result.get("messages", []),
                "user_intent": current_intent,
                "orchestrator_result": orchestrator_response,
            }

        except Exception as e:
            error_msg = f"Orchestrator node failed: {str(e)}"
            logger.error("Orchestrator node failed", error=str(e))
            return {
                "orchestrator_result": "I'm sorry, but I encountered an error. Please try again.",
                "error": [error_msg],
            }
