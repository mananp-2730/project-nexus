import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from .state import NexusState

# Force Python to read the .env file fresh
load_dotenv(override=True)

# Pull the Groq key securely
api_key = os.getenv("GROQ_API_KEY")

# Initialize Groq with Meta's Llama 3 (70 Billion Parameters)
llm = ChatGroq(
    model="llama-3.3-70b-versatile", 
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