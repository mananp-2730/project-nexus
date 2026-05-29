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

def pm_agent(state: NexusState):
    prompt = f"""
    You are the pragmatic Product Manager.
    Client Brief: {state['client_brief']}
    Current Budget: ${state['budget']}
    
    Here is what Sales and Engineering just argued about:
    {state['debate_log']}
    
    Goal: Step in and make a final, realistic compromise. Tell Sales what they need to cut, and tell Engineering what they must build. 
    
    CRITICAL INSTRUCTION: You MUST calculate a final estimated cost for your compromised MVP. 
    At the very end of your response, you must include this exact tag on a new line: "FINAL_COST: [number]"
    Example: FINAL_COST: 8500
    Do not use commas in the number.
    """
    response = llm.invoke(prompt)
    return {"debate_log": [f"Product Manager: {response.content}"]}

# --- NEW: Technical Writer Agent ---
def tech_writer_agent(state: NexusState):
    debate_history = "\n".join(state["debate_log"])
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", """You are an elite Technical Product Manager. Your job is to read the transcript of a War Room debate and generate a structured Product Requirements Document (PRD) based strictly on the final compromise reached by the Human Director and the PM Agent.
        
        Output the PRD in clean Markdown format with the following sections:
        1. Executive Summary
        2. Scope & Features (What is in the MVP)
        3. Out of Scope (What was cut during the debate)
        4. Budget & Timeline
        5. Technical Stack Recommendations
        
        Do not include any conversational text, just the Markdown PRD."""),
        ("user", "Here is the War Room transcript. Generate the final PRD:\n\n{debate}")
    ])
    
    chain = prompt | llm  # (Make sure 'llm' matches whatever you named your Groq model variable in this file!)
    response = chain.invoke({"debate": debate_history})
    
    return {"prd": response.content}