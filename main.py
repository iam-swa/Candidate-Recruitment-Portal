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
    
    print("\nWorkflow initialized and ready to handle queries.")
    
    while True:
        try:
            query = input("\n👤 USER: ")
            if query.lower() in ['exit', 'quit']:
                print("Goodbye!")
                break
                
            if not query.strip():
                continue
                
            result = workflow.chat(query)
            print(f"\n🤖 AGENT: {result}")
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nGoodbye!")
            break
        except Exception as e:
            print(f"\n❌ ERROR: {e}")

if __name__ == "__main__":
    main()
