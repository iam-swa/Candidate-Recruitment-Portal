"""
Candidate Recruitment Portal - Main Entry Point

Demonstrates the LangGraph multi-agent workflow.
"""

from dotenv import load_dotenv

# Load environment variables (e.g., GOOGLE_API_KEY)
load_dotenv()

from app.agents.orchestrator_agent import OrchestratorAgent
from app.nodes.orchestrator_node import OrchestratorNode
from app.workflows.recruitment_workflow import RecruitmentWorkflow

def main():
    print("Welcome to the Candidate Recruitment Portal!")
    print("Initializing Multi-Agent Workflow...")
    
    # Initialize the orchestrator agent and node
    orchestrator_agent = OrchestratorAgent()
    orchestrator_node = OrchestratorNode(orchestrator_agent)
    
    # Initialize the LangGraph workflow
    workflow = RecruitmentWorkflow(orchestrator_node)
    
    print("\nWorkflow initialized and ready to handle queries.")
    
    # Example Test Queries demonstrating routing and capabilities
    test_queries = [
        "What is the background of this company and the interview process?", # Should route to general_info
        "Here is my resume: Python, Java, 1.5 years experience. Is it good for a Data Scientist role?", # Should route to resume_helper
        "Can you ask me some technical questions for a Frontend Developer role?", # Should route to tech_interview
        "I have a behavioral round next week. What are common questions and how should I answer using the STAR method?", # Should route to hr_interview
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n[{i}] 👤 USER: {query}")
        result = workflow.chat(query)
        print(f"🤖 AGENT: {result}")
        print("-" * 50)
        # Reset workflow for fresh state between independent test examples (optional)
        workflow.reset()

if __name__ == "__main__":
    main()
