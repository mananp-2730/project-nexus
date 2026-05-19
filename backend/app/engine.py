from langgraph.graph import StateGraph, END
from .state import NexusState
# We imported the pm_agent here!
from .nodes import sales_agent, engineering_agent, pm_agent
from langgraph.checkpoint.memory import MemorySaver

# 1. Initialize the Graph
workflow = StateGraph(NexusState)

# 2. Add the Seats to the War Room
workflow.add_node("sales", sales_agent)
workflow.add_node("engineering", engineering_agent)
workflow.add_node("pm", pm_agent)  # Added the PM's seat

# 3. Define the Flow of Conversation
workflow.set_entry_point("sales")
workflow.add_edge("sales", "engineering")
workflow.add_edge("engineering", "pm")  # Eng now passes the mic to the PM
workflow.add_edge("pm", END)            # PM ends the meeting

# 4. Compile the Engine
nexus_app = workflow.compile()