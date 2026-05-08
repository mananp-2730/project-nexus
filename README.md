# Project Nexus: The AI War Room

Project Nexus is a multi-agent AI orchestrator designed to solve a classic business problem: the disconnect between Sales and Engineering.

By utilizing a state-graph architecture, Nexus creates an automated "War Room" where an AI Sales Agent and an AI Engineering Agent debate client briefs in real-time. It translates vague, ambitious sales requirements into structured, technically feasible constraints before a human Product Manager ever has to step in.

## The Architecture (Phase 1)

This backend is powered by **LangGraph** for state management and agent orchestration, utilizing Meta's **Llama 3.3 70B** model (via Groq) for lightning-fast, highly intelligent inference.

* **The Whiteboard (State):** A shared data structure tracking the client brief, budget, timeline, and the ongoing debate log.
* **The Sales Agent:** Optimized to satisfy the client, pitch ambitious features, and close the deal.
* **The Engineering Agent:** Optimized for technical skepticism, budget reality checks, and feasibility pushback.
* **The Director:** LangGraph nodes and edges that force a sequential, structured debate rather than a chaotic AI generation.

## Tech Stack
* **Backend:** Python, FastAPI, Uvicorn
* **AI Orchestration:** LangGraph, LangChain
* **LLM Engine:** Llama 3.3 70B (via Groq API)
