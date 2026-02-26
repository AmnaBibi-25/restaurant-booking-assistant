"""Workflow Graph Builder - Orchestrates multi-agent workflow using Langgraph."""

from langgraph.graph import StateGraph, END
from src.utils.state import AgentState
from src.agents import input_parser_agent, restaurant_search_agent, dietary_analyzer_agent, budget_filter_agent


def build_workflow():
    """Builds and compiles the multi-agent workflow graph"""

    # Initialize graph with state schema
    graph_builder = StateGraph(AgentState)

    # Add Agent Nodes
    graph_builder.add_node("input_parser", input_parser_agent)
    graph_builder.add_node("restaurant_search", restaurant_search_agent)
    graph_builder.add_node("dietary_analyzer", dietary_analyzer_agent)
    graph_builder.add_node("budget_filter", budget_filter_agent)

    # Define workflow Edges
    graph_builder.set_entry_point("input_parser")
    graph_builder.add_edge("input_parser", "restaurant_search")
    graph_builder.add_edge("restaurant_search", "dietary_analyzer")
    graph_builder.add_edge("dietary_analyzer", "budget_filter")
    graph_builder.add_edge("budget_filter", END)

    # Compile and return the graph
    return graph_builder.compile()