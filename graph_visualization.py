"""
Visualizes the multi-agent graph architecture.
"""

# Mermaid graph corresponding to the implementation
MERMAID_GRAPH = """
graph TD
    User([User Input]) --> Orchestrator
    
    subgraph Multi-Agent LangGraph
        Orchestrator{{React Orchestrator Agent}}
        
        %% Worker Tools
        Resume[Resume Helper Agent]
        Tech[Tech Interview Agent]
        HR[HR Interview Agent]
        Info[General Knowledge Agent]
        
        %% Routing Based on Intent Analysis
        Orchestrator -. "resume_review" .-> Resume
        Orchestrator -. "tech_interview" .-> Tech
        Orchestrator -. "hr_interview" .-> HR
        Orchestrator -. "company_info" .-> Info
        
        Resume -. Returns Result .-> Orchestrator
        Tech -. Returns Result .-> Orchestrator
        HR -. Returns Result .-> Orchestrator
        Info -. Returns Result .-> Orchestrator
    end
    
    Orchestrator --> FinalResponse([Final Response])
"""
