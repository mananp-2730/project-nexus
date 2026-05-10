from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from .engine import nexus_app

app = FastAPI(title="Project Nexus API")

# Add CORS middleware to allow the Next.js frontend to talk to this backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Next.js runs here
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ProjectRequest(BaseModel):
    client_brief: str

@app.get("/")
def read_root():
    return {"status": "Nexus Backend Online!", "version": "0.1.0"}

@app.post("/api/start-debate")
def start_debate(request: ProjectRequest):
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
    
    final_state = nexus_app.invoke(initial_state)
    return {"debate_log": final_state["debate_log"]}