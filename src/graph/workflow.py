"""Workflow Graph Builder - Orchestrates multi-agent workflow using Langgraph."""

from langgraph.graph import StateGraph, END
from utils.state import AgentState
from agents import input_parser_agent, restaurant_search_agent


def build_workflow():
    """Builds and compiles the multi-agent workflow graph"""

    # Initialize graph with state schema
    graph_builder = StateGraph(AgentState)

    # Add Agent Nodes
    graph_builder.add_node("input_parser", input_parser_agent)
    graph_builder.add_node("restaurant_search", restaurant_search_agent)

    # Define workflow Edges
    graph_builder.set_entry_point("input_parser")
    graph_builder.add_edge("input_parser", "restaurant_search")
    graph_builder.add_edge("restaurant_search", END)

    # Compile and return the graph
    return graph_builder.compile()