"""
Tools for the Candidate Recruitment multi-agent workflow.
These tools wrap the actual worker agent instances.
"""

import asyncio
from langchain_core.messages import HumanMessage
from langchain_core.tools import StructuredTool
from pydantic import BaseModel, Field

class WorkerInput(BaseModel):
    """Input schema for worker tools."""
    message: str = Field(description="The user's message or context to respond to")
    context: str = Field(description="Background context or specific role details", default="")

_agent_cache = {}

def _get_agent(agent_class):
    """Lazily instantiate and cache agent instances."""
    name = agent_class.__name__
    if name not in _agent_cache:
        _agent_cache[name] = agent_class()
    return _agent_cache[name]

def _build_state_from_context(context: str) -> dict:
    """Build a minimal state dict from a context string for agent prompt formatting."""
    messages = []
    if context:
        messages.append(HumanMessage(content=context))
    return {"messages": messages}

def _create_agent_tool_fn(agent_class):
    """Create a tool function that delegates to an actual agent instance."""
    def agent_tool_fn(message: str, context: str = "") -> str:
        agent = _get_agent(agent_class)
        state = _build_state_from_context(context)

        # Workaround to handle nested event loops if running from async context
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = None

        if loop and loop.is_running():
            import nest_asyncio
            nest_asyncio.apply()
        
        result = asyncio.run(agent.process_query(message, state))
        return result.get(agent.get_result_key(), "")

    return agent_tool_fn

def _build_tools():
    """Build all agent tools."""
    from app.agents.resume_helper_agent import ResumeHelperAgent
    from app.agents.tech_interview_agent import TechInterviewAgent
    from app.agents.hr_interview_agent import HRInterviewAgent
    from app.agents.general_knowledge_agent import GeneralKnowledgeAgent

    resume_helper = StructuredTool.from_function(
        func=_create_agent_tool_fn(ResumeHelperAgent),
        name="resume_helper",
        description="Helper for reviewing resumes against job roles. Use when user wants resume evaluated or improved for roles like Software Developer, Data Scientist, etc. Inputs should include resume content and target role.",
        args_schema=WorkerInput,
    )

    tech_interview = StructuredTool.from_function(
        func=_create_agent_tool_fn(TechInterviewAgent),
        name="tech_interview",
        description="Helper for technical interview prep. Generate tech questions, mock Q&A, and explain tech concepts based on specific job role.",
        args_schema=WorkerInput,
    )

    hr_interview = StructuredTool.from_function(
        func=_create_agent_tool_fn(HRInterviewAgent),
        name="hr_interview",
        description="Helper for HR/Behavioral interviews. Generates HR questions, uses STAR method, suggests sample answers.",
        args_schema=WorkerInput,
    )

    general_info = StructuredTool.from_function(
        func=_create_agent_tool_fn(GeneralKnowledgeAgent),
        name="general_knowledge",
        description="Helper providing company-specific information: background, mission/vision, recent achievements, and general interview process.",
        args_schema=WorkerInput,
    )

    return resume_helper, tech_interview, hr_interview, general_info

def get_recruitment_tools():
    """Get all agent-backed tools for the orchestrator."""
    return list(_build_tools())
