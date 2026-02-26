"""Budget Filter Agent - Filters restaurant by budget per person."""

from src.utils.state import AgentState

def budget_filter_agent(state: AgentState) -> AgentState:
    """Filters restaurants that fit within the user's budget.
    Args: 
        state: current agent state with dietary_matches and budget_per_person
    Returns: 
        Updated state with budget-filtered restaurants in dietary_matches
    """

    budget = state["budget_per_person"]
    restaurants = state["dietary_matches"]

    if not budget:
        print(f"\n [Budget Filter Agent] No budget specified, keeping all restaurants")
        state["messages"].append("Budget Filter: No budget contraint")
        return state

    print(f"\n[Budget Filter Agent] Filtering by budget: ${budget}/person")

    # Filter restaurants within budget
    within_budget = []
    over_budget = []
    for restaurant in restaurants:
        price = restaurant.get("price_range", 0)

        if price <= budget:
            within_budget.append(restaurant)
            print(f"{restaurant['name']}: ${price}/person (within budget)")
        else:
            over_budget.append(restaurant)
            print(f"{restaurant['name']}: ${price}/person (over budget) by ${price - budget}")

    # Update state with filtered results
    state["dietary_matches"] = within_budget
    state["messages"].append(
        f"Budget Filter: {len(within_budget)} of {len(restaurants)} restaurants within ${budget} budget"
    )

    if not within_budget:
        print(f"\n No restaurants within ${budget}/person budget")
        if over_budget:
            cheapest = min(over_budget, key=lambda r: r.get("price_range", float('inf')))
            print(f"Cheapest option: {cheapest['name']} at ${cheapest.get('price_range')}/person")

    return state