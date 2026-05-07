from fastapi import FastAPI
from pydantic import BaseModel
from .engine import nexus_app

app = FastAPI(title="Project Nexus API")

# This defines what information we expect from the user to start a project
class ProjectRequest(BaseModel):
    client_brief: str

@app.get("/")
def read_root():
    return {"status": "Nexus Backend Online!", "version": "0.1.0"}

@app.post("/api/start-debate")
def start_debate(request: ProjectRequest):
    # 1. Set up the initial Whiteboard (State)
    initial_state = {
        "client_brief": request.client_brief,
        "budget": 10000,           
        "timeline_weeks": 4,       
        "tech_stack": [],
        "features": [{"feature": "Core App", "priority": "High", "status": "Proposed"}],
        "debate_log": ["SYSTEM: War Room Initialized."],
        "sales_approved": False,
        "eng_approved": False,
        "pm_approved": False,
        "loop_count": 0
    }
    
    # 2. Run the LangGraph Engine
    final_state = nexus_app.invoke(initial_state)
    
    # 3. Return the conversation log
    return {"debate_log": final_state["debate_log"]}