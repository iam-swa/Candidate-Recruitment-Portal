"""
Orchestrator Agent for the Recruitment Portal
Routes conversations to appropriate agent based on user requirement
"""

from typing import Any, Dict, List, Optional
import structlog
from langchain_core.tools import BaseTool
from pydantic import BaseModel, Field

from app.agents.agent_types import ORCHESTRATOR_NAME
from app.agents.base_agent import BaseAgent
from app.agents.llm_models import LLMModels
from app.agents.state import RecruitmentState
from app.tools.recruitment_tools import get_recruitment_tools

logger = structlog.get_logger(__name__)

class OrchestratorResponse(BaseModel):
    """Response format for the orchestrator agent."""
    selected_agent: str = Field(description="The agent selected to handle this query")
    reasoning: str = Field(description="Why this agent was selected")
    context_summary: str = Field(description="Summary of conversation context")

ORCHESTRATOR_PROMPT = """
# Persona
You are the Orchestrator Agent of a Candidate Recruitment Portal multi-agent system. You are an expert API router and intent analyzer, responsible for directing user queries to the most appropriate specialized worker agent.

# Instructions
1. Analyze the user's input and consider the `CURRENT CLASSIFIED INTENT`.
2. Review the available tool agents:
   - resume_helper: For resume review, skill evaluation, and resume improvements.
   - tech_interview: For technical interview questions, coding prep, and mock tech Q&A.
   - hr_interview: For behavioral questions, soft skills, and HR round mock interviews.
   - general_knowledge: For company background, mission/vision, achievements, and interview process details.
3. Call the correct tool, passing the user's full message and context (e.g., specific role or resume text).
4. **CRITICAL:** If the user is just saying "hi", "hello", or engaging in casual greetings, DO NOT call any tools. Just respond directly with a friendly greeting or acknowledgement outlining what you can help with.
5. After receiving a tool's result (if any), present the final helpful response directly to the user.

# Chain of thought
1. Is this a casual greeting? If yes, just introduce yourself and ask how you can help.
2. What is the core intent of the user's query? What tools do I have?
3. Which specific worker agent handles this domain?
4. Execute the tool call with the required parameters.
5. Synthesize the tool's output into a cohesive response.

# Few shot
User: Can you ask me some technical questions for a Python Backend Developer role?
Thought: The user wants to prep for a technical round for a specific role. This falls under the tech_interview tool.
Action: call tech_interview with message="Can you ask me some technical questions for a Python Backend Developer role?"

User: What is the interview process here?
Thought: The user is asking about the general company interview process. This falls under general_knowledge.
Action: call general_knowledge with message="What is the interview process here?"

User: Review my resume for Data Data Scientist. It says I know Python and SQL.
Thought: The user wants their resume reviewed. This requires the resume_helper tool.
Action: call resume_helper with message="Review my resume...", context="Data Scientist"

CURRENT CLASSIFIED INTENT: {intent}
"""

class OrchestratorAgent(BaseAgent):
    """Orchestrator agent for routing recruitment workflows."""

    def __init__(
        self,
        agent_name: str = ORCHESTRATOR_NAME,
        api_key: Optional[str] = None,
        temperature: float = 0.7,
        model_name: str = LLMModels.GEMINI_2_5_FLASH,
    ) -> None:
        super().__init__(
            agent_name=agent_name,
            api_key=api_key,
            temperature=temperature,
            model_name=model_name,
        )

    def get_tools(self) -> List[BaseTool]:
        """Get agent-backed tools for the orchestrator."""
        return get_recruitment_tools()

    def get_result_key(self) -> str:
        return "orchestrator_result"

    def get_prompt(self, state: Optional[RecruitmentState] = None) -> str:
        intent = state.get("user_intent", "unknown") if state else "unknown"
        return ORCHESTRATOR_PROMPT.format(intent=intent)

    def get_response_format(self) -> type[BaseModel]:
        return OrchestratorResponse

    async def process_query(
        self,
        query: str,
        state: Optional[RecruitmentState] = None,
    ) -> Dict[str, Any]:
        """Process a query through the orchestrator."""
        try:
            from langgraph.prebuilt import create_react_agent

            tools = self.get_tools()
            prompt = self.get_prompt(state)

            agent = create_react_agent(self.model, tools, prompt=prompt)
            result = await agent.ainvoke({"messages": state.get("messages", []) if state else []})

            return {
                "success": True,
                "orchestrator_result": result,
                "messages": result.get("messages", []),
                "error": [],
            }
        except Exception as e:
            logger.error("Orchestrator processing failed", error=str(e))
            return {
                "success": False,
                "orchestrator_result": None,
                "error": [str(e)],
            }
