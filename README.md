# Candidate-Recruitment-Portal
AI-Powered Candidate Recruitment Portal

**Introduction**

The AI-Powered Candidate Recruitment Portal is a multi-agent intelligent system designed to simulate and streamline the recruitment process. The platform evaluates candidates through resume analysis, technical interviews, behavioral assessment, and performance evaluation using coordinated AI agents.The system is built using a multi-agent architecture where a central orchestrator manages communication between specialized agents. Each agent is responsible for a distinct stage of the recruitment workflow, ensuring modularity, scalability, and efficient decision-making.

This platform aims to:
Automate candidate screening
Provide structured interview simulations
Deliver constructive feedback
Generate comprehensive evaluation reports
System Architecture

The system follows a multi-agent orchestration model consisting of:

1 **Orchestrator Agent**

4 **Specialized Worker Agents**

Each worker agent performs a dedicated task, and the orchestrator coordinates the workflow.
The Four Agents

**1. Resume Helper Agent**

The Resume Helper Agent analyzes candidate resumes based on the selected job role.
Responsibilities:
Validate resume content against role requirements
Identify missing technical skills
Suggest improvements in structure and clarity
Recommend enhancements aligned with industry standards
Provide role-specific optimization feedback
This agent ensures the candidate’s resume is aligned with the job expectations before proceeding to interviews.

**2. Technical Interview Agent**

The Technical Interview Agent conducts role-specific technical assessments.
Responsibilities:
Generate technical questions based on the selected role
Evaluate candidate responses
Assess conceptual clarity and practical knowledge
Adapt question difficulty dynamically
Provide structured technical feedback
This agent simulates a real-world technical interview experience.

**3. Behavioral / HR Interview Agent**

The Behavioral Interview Agent evaluates soft skills and professional suitability.
Responsibilities:
Ask situational and behavioral questions
Assess communication clarity
Evaluate problem-solving approach
Analyze leadership and teamwork responses
Measure cultural fit indicators
This agent ensures that the candidate meets organizational behavioral expectations.

**4. Evaluation & Scoring Agent**

The Evaluation Agent consolidates outputs from all other agents.
Responsibilities:
Aggregate resume, technical, and behavioral scores
Generate overall candidate rating
Highlight strengths and weaknesses
Provide hiring recommendation
Produce a structured final report
This agent acts as the final decision-support system.

Manages data flow between agents
Ensures structured execution of the workflow
