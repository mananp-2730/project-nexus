import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client
from .engine import nexus_app
import uuid

# Load environment variables
load_dotenv(override=True)

app = FastAPI(title="Project Nexus API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- NEW: Connect to Supabase ---
supabase_url: str = os.getenv("SUPABASE_URL")
supabase_key: str = os.getenv("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

class ProjectRequest(BaseModel):
    client_brief: str
    budget: int
    timeline_weeks: int

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
    # 1. Create a unique ID for this specific War Room session
    thread_id = str(uuid.uuid4())
    config = {"configurable": {"thread_id": thread_id}}
    
    initial_state = {
        "client_brief": request.client_brief,
        "budget": request.budget,
        "timeline_weeks": request.timeline_weeks,
        "tech_stack": [],
        "features": [{"feature": "Core App", "priority": "High", "status": "Proposed"}],
        "debate_log": ["SYSTEM: War Room Initialized."],
        "sales_approved": False,
        "eng_approved": False,
        "pm_approved": False,
        "loop_count": 0
    }
    
    # 2. Run the graph with the config (It will freeze before the PM agent!)
    try:
        current_state = nexus_app.invoke(initial_state, config=config)
        
        # 3. Return the partial debate and the thread_id so the frontend can reply later
        return {
            "thread_id": thread_id,
            "debate_log": current_state["debate_log"],
            "status": "waiting_for_human"
        }
    except Exception as e:
        print(f"Graph execution failed: {e}")
        return {"error": str(e)}

@app.get("/api/history")
def get_history():
    try:
        # Ask Supabase for the 10 most recent debates, sorted by newest first
        response = supabase.table("past_debates").select("*").order("created_at", desc=True).limit(10).execute()
        return {"history": response.data}
    except Exception as e:
        print(f"Failed to fetch history: {e}")
        return {"history": []}