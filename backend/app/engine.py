from langgraph.graph import StateGraph, END
from .state import NexusState
from .nodes import sales_agent, engineering_agent

# 1. Initialize the Graph (Bring the Whiteboard into the room)
workflow = StateGraph(NexusState)

# 2. Add the Seats to the War Room
workflow.add_node("sales", sales_agent)
workflow.add_node("engineering", engineering_agent)

# 3. Define the Flow of Conversation
workflow.set_entry_point("sales")
workflow.add_edge("sales", "engineering")
workflow.add_edge("engineering", END)

# 4. Compile the Engine (Turn it into a runnable app)
nexus_app = workflow.compile()