import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from .state import NexusState

# Load the API key from your .env file
load_dotenv()

# Initialize Gemini
llm = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest", temperature=0.2)

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