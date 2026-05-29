from typing import TypedDict, List, Annotated
import operator

class NexusState(TypedDict):
    client_brief: str
    budget: int
    timeline_weeks: int
    tech_stack: List[str]
    features: Annotated[List[dict], operator.add]
    debate_log: Annotated[List[str], operator.add]
    sales_approved: bool
    eng_approved: bool
    pm_approved: bool
    loop_count: int
    prd: str