import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from .state import NexusState

# The magic word 'override=True' forces Python to ignore cached terminal keys 
# and ONLY use what is currently saved in the .env file.
load_dotenv(override=True)

# Pull the key securely from the environment
api_key = os.getenv("GEMINI_API_KEY")

# Initialize Gemini 2.0 Flash
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash", 
    temperature=0.2,
    api_key=api_key
)

def sales_agent(state: NexusState):
    prompt = f"""
    You are the Sales Lead. 
    Client Brief: {state['client_brief']}
    Current Budget: ${state['budget']}
    
    Goal: Try to promise the client exactly what they asked for, but keep it under budget.
    Keep your response to 2 sentences.
    """
    response = llm.invoke(prompt)
    return {"debate_log": [f"Sales: {response.content}"]}

def engineering_agent(state: NexusState):
    prompt = f"""
    You are the strict Lead Architect.
    Client Brief: {state['client_brief']}
    Current Budget: ${state['budget']}
    
    Goal: Point out why the client's request is technically too difficult for that budget. Be highly skeptical.
    Keep your response to 2 sentences.
    """
    response = llm.invoke(prompt)
    return {"debate_log": [f"Engineering: {response.content}"]}