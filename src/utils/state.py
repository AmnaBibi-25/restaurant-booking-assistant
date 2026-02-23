"""State Management for the Restaurant Booking Assistant.
Defines the shared state strucutre passed between agents
"""

from ast import operator
from typing import TypedDict, Annotated, Optional
import operator


class AgentState(TypedDict):
    """Shared state passed between all agents in the workflow"""

    # User Input
    user_query: str

    # Parsed Requirements
    persons_count: Optional[int]
    dietary_requirements: Optional[str]
    budget_per_person: Optional[float]
    date: Optional[str]
    time: Optional[str]
    location: Optional[str]
    cuisine_preference: Optional[str]

    # Agent Outputs
    restaurant_candidates: list
    dietary_matches: list
    final_recommendations: list

    # Workflow Log
    messages: Annotated[list, operator.add]
   
    