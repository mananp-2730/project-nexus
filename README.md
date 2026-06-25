# Project Nexus: The AI War Room

**Live Demo:** [project-nexus-khaki-mu.vercel.app](https://project-nexus-khaki-mu.vercel.app/) *(Note: The backend is hosted on a free Render tier. If it has been asleep, the first debate may take ~45 seconds to wake the server up!)*

Project Nexus is a full-stack, multi-agent AI orchestrator designed to solve a classic business problem: the chaotic disconnect between Sales and Engineering.

By utilizing a state-graph architecture, Nexus creates an automated "War Room" where AI agents debate client briefs in real-time. It translates vague, ambitious sales requirements into structured, technically feasible constraints, automating the product compromise process before a human ever has to step in.

## Evolution & Features


* **V1.1 - The Analytics Engine:** A custom extraction pipeline forces the AI PM to quantify decisions. The system intercepts the output, calculates the budget delta, and displays a real-time ROI dashboard.
* **V1.2 - The Memory Engine:** Integrated with a cloud PostgreSQL database (Supabase), the backend automatically logs every session. The Next.js frontend features a sidebar dashboard to fetch and review historical debates instantly.
* **V1.3 - Human-in-the-Loop (HITL) Co-Pilot:** Nexus is an active Co-Pilot. The LangGraph architecture features a strategic breakpoint. After Sales and Engineering debate, the AI graph dynamically pauses, awaiting human intervention. The user steps in via a UI command console to provide strategic direction, which the AI PM then ingests to calculate a final, mathematically sound compromise.
* **V1.4 - RAG & Document Uploads:** Nexus features a Retrieval-Augmented Generation (RAG) pipeline via Context Stuffing. Users can drag and drop PDF Request for Proposals (RFPs). The Python backend extracts the unstructured text and seamlessly injects the enterprise constraints directly into the War Room's state for the agents to analyze.
* **V2.0 - The PRD Exporter:** Nexus goes beyond orchestration to become an enterprise productivity tool. A dedicated Technical Writer Agent processes the final War Room compromise and automatically generates a highly structured Product Requirements Document (PRD). The Next.js UI renders the PRD and allows users to instantly export it as a Markdown (`.md`) file.
* **V2.1 - Executive Portfolio Dashboard:** Nexus tracks macro-level business impact. The UI features a global analytics panel that queries the cloud database to aggregate the total capital saved, total budget processed, and overall War Room volume across all historical AI simulations.
* **V3.0 - The Market Research Agent (Live Web Search):** Nexus features autonomous Agentic Tool Use. Before calculating a compromise, the PM Agent secretly queries the live internet (via DuckDuckGo) to pull real-world competitor pricing, market trends, and standard feature sets, ensuring the final PRD is grounded in hard, current market data.


## The Architecture


This application is powered by **LangGraph** for state management and agent orchestration, utilizing Meta's **Llama 3.3 70B** model (via Groq) for lightning-fast, highly intelligent inference.


* **The RAG Pipeline:** A FastAPI endpoint equipped with PyPDF that catches uploaded PDF documents, parses the unstructured text, and injects it into the LangGraph state.
* **The Whiteboard (State):** A shared data structure tracking the client brief, dynamic budget, timeline constraints, and the ongoing debate log.
* **The Sales Agent:** Optimized to satisfy the client, pitch ambitious features, and attempt to close the deal at all costs.
* **The Engineering Agent:** Optimized for technical skepticism, budget reality checks, and fierce feasibility pushback.
* **The Human Director:** A strategic pause in the graph execution that allows the human user to inject constraints and commands before the AI PM finalizes the scope.
* **The Product Manager Agent:** The adult in the room. Equipped with live web-search capabilities, this agent reviews the argument, researches real-world competitor data, ingests Human Director guidance, ruthlessly cuts scope, and mathematically calculates the final cost.
* **The Technical Writer Agent:** The documentation specialist. It reads the finalized debate log and translates the PM's compromise into a structured PRD (Executive Summary, Scope, Exclusions, and Financials).
* **The Data Extractor & Database:** A Python pipeline that intercepts the PM's final output, isolates cost metrics, and pushes the entire session to a Supabase PostgreSQL database.


## Tech Stack


**Frontend (Client)**
* **Framework:** Next.js (React)
* **Styling:** Tailwind CSS
* **UX:** Custom live-typing streaming effect, dynamic ROI calculation dashboard, global executive analytics panel, interactive Co-Pilot console, drag-and-drop file upload, and Markdown file generation/export.
* **Hosting:** Vercel


**Backend (API, AI & Database)**
* **Framework:** Python, FastAPI, Uvicorn
* **AI Orchestration:** LangGraph, LangChain
* **Agentic Tool Use:** DuckDuckGo Search API
* **LLM Engine:** Llama 3.3 70B (via Groq API)
* **Data Extraction:** PyPDF, python-multipart
* **Database:** Supabase (PostgreSQL)
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
   GROQ_API_KEY="your_groq_api_key_here"
   SUPABASE_URL="your_supabase_project_url"
   SUPABASE_KEY="your_supabase_anon_public_key"
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