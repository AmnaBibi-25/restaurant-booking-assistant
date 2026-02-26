"""Dietary Analyzer Agent - Uses RAG to find menu items matching dietary requirements.
This is the key intelligent agent using semantic search over menus
"""

from src.utils.state import AgentState
from src.rag.menu_vectorstore import search_menus, get_restaurant_dishes

def dietary_analyzer_agent(state: AgentState) -> AgentState:
    """Analyzes restaurant menus using RAG to find dietary-compatible dishes.
    Uses semantic search to find dishes that match dietary requirements, 
    not just keyword matching. For example, "creamy vegan pasta" will find 
    "cashew alfredo pasta" even without the word "creamy".

    Args: 
        state: Current agent state with restaurant_candidates and dietary_requirements

    Returns: 
        Updated state with dietary_matches
    """

    dietary_requirements = state["dietary_requirements"]
    restaurant_candidates = state["restaurant_candidates"]

    if not dietary_requirements:
        print("\n[Dietary Analyzer Agent] No dietary requirements specified, skipping")
        state["dietary_matches"] = restaurant_candidates
        state["messages"].append("Dietary Analyzer: No dietary restrictions")
        return state
    print(f"\n[Dietary Analyzer Agent] Analyzing menus for: {dietary_requirements}")

    # For each restaurant candidate, check if they have suitable dishes
    matching_restaurants = []
    for restaurant in restaurant_candidates:
        restaurant_name = restaurant["name"]

        # Use RAG to find dishes at this restaurant matching dietary needs
        dishes = get_restaurant_dishes(
            restaurant_name=restaurant_name,
            dietary_filter=dietary_requirements
        )

        if dishes:
            # Add dish information to restaurant data
            restaurant_with_dishes = restaurant.copy()
            restaurant_with_dishes["matching_dishes"] = [
                {
                    "name": d.metadata["dish_name"],
                    "price": d.metadata["price"],
                    "category": d.metadata["category"],
                    "description": d.page_content.split("Description: ")[1].split("\n")[0] if "Description: " in d.page_content else ""
                }
                for d in dishes[:5]
            ]
            restaurant_with_dishes["matching_dish_count"] = len(dishes)
            matching_restaurants.append(restaurant_with_dishes)
            print(f"{restaurant_name}: Found {len(dishes)} {dietary_requirements} dishes")
        else:
            print(f"{restaurant_name}: No {dietary_requirements} options found")

    # Update state
    state["dietary_matches"] = matching_restaurants
    state["messages"].append(
        f"Dietary Analyzer: Found {len(matching_restaurants)} restaurants with {dietary_requirements} options"
    )

    if not matching_restaurants:
        print(f"\n No restaurants found with {dietary_requirements} options")

    return state

        


    