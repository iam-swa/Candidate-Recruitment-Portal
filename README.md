---
title: Candidate Recruitment Portal
emoji: 🚀
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: "4.44.0"
python_version: "3.10"
app_file: ui.py
pinned: false
---
**Multi-Agent Career Assistance System**

**Overview**

This project implements a LangGraph-based multi-agent system designed to assist users with career preparation. The system follows a modular architecture inspired by the existing repository in the workspace and adheres to its coding style and structural patterns.

The architecture consists of:

1 Orchestrator Agent (ReAct-based)

4 Worker Agents

The orchestrator analyzes user intent and routes the request to the appropriate worker agent, which is exposed as a tool.

System Architecture

**Orchestrator Agent (ReAct Agent)**

The main orchestrator agent:

- Uses the ReAct reasoning pattern

- Identifies user intent

- Selects the appropriate worker agent

- Routes the request

- Returns the final consolidated response

Intent Categories

The orchestrator classifies user queries into:

- resume_review

- tech_interview

- hr_interview

- company_info

Each intent maps to one worker agent tool.

**WORKER AGENTS**

**1. Resume Helper Agent**

Purpose:
Provides resume evaluation and improvement suggestions based on job roles.

**Capabilities:**

Contains structured role-based data including:

- Required skills

- Preferred skills

- Experience expectations

- Resume structure expectations

_Behavior:_

Accepts resume content and target role.

Compares resume against role requirements.

- Identifies missing skills.

- Suggests improvements.

- Recommends rewording and impact-driven bullet points.

- Provides structured feedback.

**2. Tech Interview Helper Agent**

Purpose:
Supports technical interview preparation.

_Capabilities:_

- Generates role-specific technical interview questions.

- Explains technical concepts clearly.

- Provides sample answers.

- Simulates mock Q&A sessions.

_Behavior:_

When a role is specified:

- Generates relevant technical questions.

When a concept is requested:

- Provides explanation and examples.

- Can guide users through practice sessions.

**3. HR Interview Helper Agent**

Purpose:
Assists with HR round preparation.

_Capabilities:_

- Generates common HR interview questions.

- Provides structured sample answers.

- Helps refine user responses.

- Guides users using behavioral frameworks (e.g., STAR method).

_Behavior:_

- Provides role-independent HR preparation.

- Refines user-submitted answers.

- Suggests improvements for clarity and impact.

**4. General Knowledge Agent (Company Info Agent)**

Purpose:
Provides structured company-related information.

_Capabilities:_

- Company background

- Mission and vision

- Recent achievements

- Interview process overview

_Behavior:_

Responds to company-specific queries.

Provides organized and concise company insights.
