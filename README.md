# Project Nexus: The AI War Room

**Live Demo:** [project-nexus-khaki-mu.vercel.app](https://project-nexus-khaki-mu.vercel.app/) *(Note: The backend is hosted on a free Render tier. If it has been asleep, the first debate may take ~45 seconds to wake the server up!)*

Project Nexus is a full-stack, multi-agent AI orchestrator designed to solve a classic business problem: the chaotic disconnect between Sales and Engineering.

By utilizing a state-graph architecture, Nexus creates an automated "War Room" where AI agents debate client briefs in real-time. It translates vague, ambitious sales requirements into structured, technically feasible constraints, automating the product compromise process before a human ever has to step in.

## Evolution & Features

* **V1.1 - The Analytics Engine:** A custom extraction pipeline forces the AI PM to quantify decisions. The system intercepts the output, calculates the budget delta, and displays a real-time ROI dashboard.

## Version 1.1: The Analytics Engine
Nexus doesn't just generate text; it generates business intelligence. The backend features a custom extraction pipeline that forces the AI Product Manager to quantify its decisions. The system intercepts the AI's response, extracts the final MVP cost, calculates the budget delta, and displays a real-time ROI dashboard on the frontend—proving the financial value of the PM's compromise.

## The Architecture (Phase 1)

This application is powered by **LangGraph** for state management and agent orchestration, utilizing Meta's **Llama 3.3 70B** model (via Groq) for lightning-fast, highly intelligent inference.

* **The Whiteboard (State):** A shared data structure tracking the client brief, dynamic budget, timeline constraints, and the ongoing debate log.
* **The Sales Agent:** Optimized to satisfy the client, pitch ambitious features, and attempt to close the deal at all costs.
* **The Engineering Agent:** Optimized for technical skepticism, budget reality checks, and fierce feasibility pushback.
* **The Product Manager Agent:** The adult in the room. This agent reviews the argument, ruthlessly cuts scope, defines a realistic Minimum Viable Product (MVP), and mathematically calculates the final cost.
* **The Director:** LangGraph nodes and edges that force a sequential, structured debate (Sales -> Eng -> PM).
* **The Data Extractor:** A Python pipeline that intercepts the PM's final output, isolates the cost metrics, and feeds clean analytics to the frontend dashboard.

## Tech Stack

**Frontend (Client)**
* **Framework:** Next.js (React)
* **Styling:** Tailwind CSS
* **UX:** Custom live-typing streaming effect and dynamic ROI calculation dashboard
* **Hosting:** Vercel

**Backend (API & AI)**
* **Framework:** Python, FastAPI, Uvicorn
* **AI Orchestration:** LangGraph, LangChain
* **LLM Engine:** Llama 3.3 70B (via Groq API)
* **Hosting:** Render

## Local Setup & Installation

Want to run the War Room locally? Follow these steps:

**1. Clone the repository**
```bash
   git clone [https://github.com/mananp-2730/project-nexus.git](https://github.com/mananp-2730/project-nexus.git)```
```

**2. Setup the Python Backend**
```bash
   cd project-nexus/backend
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Mac/Linux: source venv/bin/activate

   pip install -r requirements.txt
```

Create a .env file in the backend directory and add your Groq API key:
```bash
   GROQ_API_KEY="your_api_key_here"
```

Start the API:
```bash
   uvicorn app.main:app --reload
```

**3. Setup the Next.js Frontend**
Open a new terminal window:
```bash
   cd project-nexus/frontend
   npm install
   npm run dev
```

**4. Open the War Room**
Navigate to http://localhost:3000 in your browser to start a debate!
