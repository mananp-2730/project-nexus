from langgraph.graph import StateGraph, END
from .state import NexusState
# NEW: We added tech_writer_agent to the import list!
from .nodes import sales_agent, engineering_agent, pm_agent, tech_writer_agent
from langgraph.checkpoint.memory import MemorySaver

# 1. Initialize the Graph
workflow = StateGraph(NexusState)

# 2. Add the Seats to the War Room
workflow.add_node("sales", sales_agent)
workflow.add_node("engineering", engineering_agent)
workflow.add_node("pm", pm_agent)
workflow.add_node("tech_writer", tech_writer_agent)  # <-- NEW: Added the Tech Writer's seat

# 3. Define the Flow of Conversation
workflow.set_entry_point("sales")
workflow.add_edge("sales", "engineering")
workflow.add_edge("engineering", "pm") 
workflow.add_edge("pm", "tech_writer")  # <-- NEW: PM passes the mic to the Tech Writer
workflow.add_edge("tech_writer", END)   # <-- NEW: Tech Writer ends the meeting

# Create a memory bank to hold the state while paused
memory = MemorySaver()

# Compile the graph with the memory AND a breakpoint!
nexus_app = workflow.compile(
    checkpointer=memory,
    interrupt_before=["pm"] # This tells the AI to freeze right before the PM speaks!
)