"""Input Parser Agent - Extracts structured data from natural language.
Uses LLM to parse user input into structured requirements
"""
from langchain_groq import ChatGroq
import os
import json
from dotenv import load_dotenv
from utils.state import AgentState

load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
groq_model = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# Initialize LLM
llm = ChatGroq(model=groq_model, api_key=groq_api_key, temperature=0)


def input_parser_agent(state: AgentState) -> AgentState:
    """Parses natural langugae input into structured requirements
    Args: 
        state: current agent state with user query
    Returns:
        Updated state with parsed requirements
    """
    user_query = state["user_query"]
    print(f"[Input Parser Agent] Parsing: '{user_query}'")

    # Create prompt for structured extraction
    prompt = f"""
    You are an expert at extracting structured information from natural language.

User Query: {user_query}

Extract the following information. If something is not mentioned, return null.
Return only valid JSON in this exact format:
{{
    "persons_count": <number or null>,
    "dietary_requirements": "<string or null>"
    "budget_per_person": <number or null>,
    "date": "<string or null>",
    "time": "<string or null>",
    "location": "<string or null>",
    "cuisine_prference": "<string or null>"
}}

Examples: 
- "Table for 4, vegan options, downtown Seattle, Saturday 7pm"
-> {{"persons_count": 4, "dietary_requirements": "vegan", "budget_per_person": null, "date": "Saturday", "time": "7pm", "location": "downtown Seattle", "cuisine_prference": null}}

- "Italian restaurant for 2, budget $50 per person"
-> {{"persons_count": 2, "dietary_requirements": null, "budget_per_person": 50, "date": null, "time": null, "location": null, "cuisine_prference": "Italian"}}

Now parse the user query above. Return ONLY the JSON, no other text.
"""

    # Get LLM response
    response = llm.invoke(prompt)

    try: 
        # Parse JSON response
        parsed_data = json.loads(response.content)

        # Update state with parsed values
        state["persons_count"] = parsed_data.get("persons_count")
        state["dietary_requirements"] = parsed_data.get("dietary_requirements")
        state["budget_per_person"] = parsed_data.get("budget_per_person")
        state["date"] = parsed_data.get("date")
        state["time"] = parsed_data.get("time")
        state["location"] = parsed_data.get("location")
        state["cuisine_preference"] = parsed_data.get("cuisine_preference")

        # Log successful parse
        state["messages"].append(f"Input Parser: Extracted requirements from query")
        print(f"[Input Parser Agent] Parsed data: {state}")

    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print(f"Raw response: {response.content}")
        state["messages"].append(f"Input Parser: Failed to extract requirements from query")

    return state


