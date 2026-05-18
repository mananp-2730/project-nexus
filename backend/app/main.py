import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client
from .engine import nexus_app

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
    
    final_state = nexus_app.invoke(initial_state)
    
    # --- NEW ANALYTICS LOGIC ---
    pm_message = final_state["debate_log"][-1]
    final_cost = request.budget # Default fallback
    
    # 1. Search for our secret tag
    if "FINAL_COST:" in pm_message:
        try:
            # 2. Extract the number from the string
            cost_str = pm_message.split("FINAL_COST:")[1].strip()
            # Clean up any extra punctuation the AI might have accidentally added
            cost_str = ''.join(filter(str.isdigit, cost_str))
            final_cost = int(cost_str)
        except Exception as e:
            print("Failed to parse cost:", e)
            
    # 3. Calculate the ROI / Budget Delta
    budget_saved = request.budget - final_cost
    
    # 4. Scrub the secret tag from the message
    clean_log = [msg.split("FINAL_COST:")[0].strip() for msg in final_state["debate_log"]]
    
    # --- NEW: Save the memory to Supabase! ---
    try:
        supabase.table("past_debates").insert({
            "client_brief": request.client_brief,
            "original_budget": request.budget,
            "timeline_weeks": request.timeline_weeks,
            "final_cost": final_cost,
            "budget_saved": budget_saved,
            "debate_log": clean_log
        }).execute()
        print("Successfully saved to Supabase!")
    except Exception as e:
        print(f"Failed to save to database: {e}")
    
    # 5. Send data to the frontend
    return {
        "debate_log": clean_log,
        "analytics": {
            "original_budget": request.budget,
            "final_cost": final_cost,
            "budget_saved": budget_saved
        }
    }

@app.get("/api/history")
def get_history():
    try:
        # Ask Supabase for the 10 most recent debates, sorted by newest first
        response = supabase.table("past_debates").select("*").order("created_at", desc=True).limit(10).execute()
        return {"history": response.data}
    except Exception as e:
        print(f"Failed to fetch history: {e}")
        return {"history": []}