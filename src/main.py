"""Restaurant Booking Assitant - Main Entry Point"""

from dotenv import load_dotenv
from graph import build_workflow

load_dotenv()

def print_results(result: dict) -> None:
    """Prints workflow results in a readable format"""
    print("\n" + "-"*60)
    print("Restaurant Booking Assistant - Results")
    print("-"*60)
    
    print(f"\n Your Request:")
    print(f"   Query: {result['user_query']}")
    print(f"   Persons count: {result['persons_count']} person(s)")
    print(f"   Dietary needs: {result['dietary_requirements'] or 'None specified'}")
    print(f"   Budget: ${result['budget_per_person']}/person" if result['budget_per_person'] else "   Budget: Not specified")
    print(f"   Location: {result['location']}")
    print(f"   Date/Time: {result['date']} at {result['time']}" if result['date'] else "   Date/Time: Not specified")
    
    print(f"\n Found {len(result['restaurant_candidates'])} Restaurants:")
    for i, restaurant in enumerate(result['restaurant_candidates'], 1):
        print(f"\n   {i}. {restaurant['name']}")
        print(f"      Cuisine: {restaurant['cuisine']}")
        print(f"      Price: ${restaurant['price_range']}/person")
        print(f"      Rating: {restaurant['rating']}⭐")
        print(f"      Location: {restaurant['location']}")


def main():
    """Main execution function"""
    print("\n" + "-"*60)
    print("Welcome to Restaurant Booking Assistant")
    print("-"*60)


    # Test query
    user_query = "Table for 4, vegan options, downtown Seattle, Saturday 7pm, under $30 per person"
    print(f"\n Processing user query: '{user_query}'\n")

    # Build and compile workflow
    app = build_workflow()

    #Initialize state
    initial_state = {
        "user_query": user_query,
        "persons_count": None,
        "budget_per_person": None,
        "date": None,
        "time": None,
        "location": None,
        "cuisine_preference": None,
        "restaurant_candidates": [],
        "dietary_matches": [],
        "final_recommendations": [],
        "messages": []
    }

    # Run workflow
    result = app.invoke(initial_state)

    print_results(result)


if __name__ == "__main__":
    main()
