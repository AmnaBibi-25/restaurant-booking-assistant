"""Restaurant Search Agent - Finds restaurants based on location and cuisine
Note: Currently using mock data
"""

from src.utils.state import AgentState

MOCK_RESTAURANTS = [
     {
        "name": "Green Leaf Bistro",
        "cuisine": "American",
        "location": "downtown Seattle",
        "price_range": 25,
        "rating": 4.6,
        "has_vegan": True,
        "has_vegetarian": True,
        "has_gluten_free": True
    },
    {
        "name": "Mediterranean Kitchen",
        "cuisine": "Mediterranean",
        "location": "downtown Seattle",
        "price_range": 22,
        "rating": 4.4,
        "has_vegan": True,
        "has_vegetarian": True,
        "has_gluten_free": False
    },
    {
        "name": "Pasta Paradise",
        "cuisine": "Italian",
        "location": "Capitol Hill Seattle",
        "price_range": 30,
        "rating": 4.7,
        "has_vegan": False,
        "has_vegetarian": True,
        "has_gluten_free": True
    },
    {
        "name": "Spice Route",
        "cuisine": "Indian",
        "location": "downtown Seattle",
        "price_range": 18,
        "rating": 4.5,
        "has_vegan": True,
        "has_vegetarian": True,
        "has_gluten_free": True
    },
    {
        "name": "Ocean View Grill",
        "cuisine": "Seafood",
        "location": "Waterfront Seattle",
        "price_range": 45,
        "rating": 4.8,
        "has_vegan": False,
        "has_vegetarian": False,
        "has_gluten_free": True
    }
]

def restaurant_search_agent(state: AgentState) -> AgentState:
    """ Searches for restaurants based on location and cuisine preference.
    Args:
        state: current agent state with parsed requirements
    Returns:
        Updated state restaurant_candidates
    """

    location = state["location"] or "Seattle"
    cuisine = state["cuisine_preference"]

    print(f"[Restaurant Search Agent] Searching in {location} ...")
    if cuisine:
        print(f"Filtering by cuisine: {cuisine}")

    # Filter restaturants
    restaurant_candidates = []
    for restaurant in MOCK_RESTAURANTS:
        # Check location match (simple string matching for now)
        location_match = location.lower() in restaurant["location"].lower()

        # Check cusine match (if specified)
        cuisine_match = True
        if cuisine:
            cuisine_match = cuisine.lower() in restaurant["cuisine"].lower()
        if location_match and cuisine_match:
            restaurant_candidates.append(restaurant)

    # Update state
    state["restaurant_candidates"] = restaurant_candidates
    state["messages"].append(f"Restaurant Search: Found {len(restaurant_candidates)} restaurants")

    print(f"Found {len(restaurant_candidates)} restaurants:")
    for r in restaurant_candidates:
        print(f" - {r['name']} ({r['cuisine']}) - ${r['price_range']}/person")

    return state

      
