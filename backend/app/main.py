import os
import uuid
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv
from supabase import create_client, Client
from PyPDF2 import PdfReader
import io
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
    
# --- NEW: Human-in-the-Loop Resume Request ---
class ResumeRequest(BaseModel):
    thread_id: str
    human_compromise: str

@app.post("/api/resume-debate")
def resume_debate(request: ResumeRequest):
    # 1. Find the exact frozen memory using the thread_id
    config = {"configurable": {"thread_id": request.thread_id}}
    
    try:
        # 2. Inject the human's compromise into the whiteboard (State)
        human_message = f"Human Director: {request.human_compromise}"
        nexus_app.update_state(config, {"debate_log": [human_message]})
        
        # 3. Resume the graph from where it paused! (Passing None means "just keep going")
        final_state = nexus_app.invoke(None, config=config)
        
        # --- 4. RESTORE ANALYTICS & DATABASE LOGIC ---
        pm_message = final_state["debate_log"][-1]
        original_budget = final_state["budget"] 
        final_cost = original_budget # Default fallback
        
        # Extract the secret tag
        if "FINAL_COST:" in pm_message:
            try:
                cost_str = pm_message.split("FINAL_COST:")[1].strip()
                cost_str = ''.join(filter(str.isdigit, cost_str))
                final_cost = int(cost_str)
            except Exception as e:
                print("Failed to parse cost:", e)
                
        budget_saved = original_budget - final_cost
        
        # Scrub the secret tag
        clean_log = [msg.split("FINAL_COST:")[0].strip() for msg in final_state["debate_log"]]
        
        # Save the completed War Room to Supabase
        try:
            supabase.table("past_debates").insert({
                "client_brief": final_state["client_brief"],
                "original_budget": original_budget,
                "timeline_weeks": final_state["timeline_weeks"],
                "final_cost": final_cost,
                "budget_saved": budget_saved,
                "debate_log": clean_log
            }).execute()
        except Exception as e:
            print(f"Failed to save to database: {e}")
        
        # Send the final data to the frontend
        return {
            "debate_log": clean_log,
            "analytics": {
                "original_budget": original_budget,
                "final_cost": final_cost,
                "budget_saved": budget_saved
            },
            "status": "completed"
        }
        
    except Exception as e:
        print(f"Graph resume failed: {e}")
        return {"error": str(e)}
    
# --- NEW: RAG Document Upload Endpoint ---
@app.post("/api/upload-brief")
async def upload_brief(file: UploadFile = File(...)):
    try:
        # 1. Read the file into memory
        contents = await file.read()
        pdf_file = io.BytesIO(contents)

        # 2. Parse the PDF
        reader = PdfReader(pdf_file)
        extracted_text = ""

        # 3. Loop through every page and extract the text
        for page in reader.pages:
            extracted_text += page.extract_text() + "\n\n"

        return {"filename": file.filename, "extracted_text": extracted_text.strip()}

    except Exception as e:
        print(f"Failed to read PDF: {e}")
        return {"error": "Could not parse the PDF file."}