from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .engine import nexus_app

app = FastAPI(title="Project Nexus API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 1. Update the expected request from the frontend
class ProjectRequest(BaseModel):
    client_brief: str
    budget: int            # NEW
    timeline_weeks: int    # NEW

@app.get("/")
def read_root():
    return {"status": "Nexus Backend Online!", "version": "0.1.0"}

@app.post("/api/start-debate")
def start_debate(request: ProjectRequest):
    # 2. Map the user's inputs directly into the LangGraph state
    initial_state = {
        "client_brief": request.client_brief,
        "budget": request.budget,                  # Updated!
        "timeline_weeks": request.timeline_weeks,  # Updated!
        "tech_stack": [],
        "features": [{"feature": "Core App", "priority": "High", "status": "Proposed"}],
        "debate_log": ["SYSTEM: War Room Initialized."],
        "sales_approved": False,
        "eng_approved": False,
        "pm_approved": False,
        "loop_count": 0
    }
    
    final_state = nexus_app.invoke(initial_state)
    return {"debate_log": final_state["debate_log"]}