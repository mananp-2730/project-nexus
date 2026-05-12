# Project Nexus: The AI War Room

**Live Demo:** [project-nexus-khaki-mu.vercel.app](https://project-nexus-khaki-mu.vercel.app/) *(Note: The backend is hosted on a free Render tier. If it has been asleep, the first debate may take ~45 seconds to wake the server up!)*

Project Nexus is a full-stack, multi-agent AI orchestrator designed to solve a classic business problem: the chaotic disconnect between Sales and Engineering.

By utilizing a state-graph architecture, Nexus creates an automated "War Room" where AI agents debate client briefs in real-time. It translates vague, ambitious sales requirements into structured, technically feasible constraints, automating the product compromise process before a human ever has to step in.

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
