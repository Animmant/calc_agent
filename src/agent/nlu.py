import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.schema import HumanMessage
import json

# Ensure GOOGLE_API_KEY is set in your environment variables
# For example: os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
# (This line is for user information, the worker should not try to set a fake key)

def understand_query(query: str) -> dict:
    """
    Understands the user query using Langchain and Gemini
    and returns a structured representation.
    """
    try:
        # Note: GOOGLE_API_KEY environment variable must be set for this to work.
        # You can set it using: os.environ["GOOGLE_API_KEY"] = "YOUR_API_KEY"
        # Ensure this is done before running the application.
        llm = ChatGoogleGenerativeAI(model="gemini-pro", convert_system_message_to_human=True)
        
        prompt_text = (
            "Analyze the following user query to identify the main intent and any key entities. "
            "The intent should be a short descriptive string (e.g., 'solve_math_problem', 'generate_report', 'answer_question'). "
            "Entities should be a dictionary of key-value pairs extracted from the query. "
            "Return your analysis as a JSON object with two keys: 'intent' and 'entities'. "
            "For example: {\"intent\": \"calculate_sum\", \"entities\": {\"numbers\": [1, 2, 3]}}. "
            "If the query is unclear or you cannot determine a specific intent, use 'unknown_intent'. "
            "User query: " + query
        )
        
        messages = [HumanMessage(content=prompt_text)]
        response = llm.invoke(messages)
        
        # The response content should ideally be a JSON string
        response_content = response.content
        
        # Try to parse the JSON response
        if isinstance(response_content, str):
            # Ensure the string is valid JSON, sometimes LLMs add markdown backticks
            if response_content.startswith("```json"):
                response_content = response_content[7:]
            if response_content.endswith("```"):
                response_content = response_content[:-3]
            
            parsed_response = json.loads(response_content.strip())
            
            # Basic validation of the parsed structure
            if isinstance(parsed_response, dict) and "intent" in parsed_response and "entities" in parsed_response:
                return {
                    "intent": parsed_response.get("intent", "unknown_intent"),
                    "entities": parsed_response.get("entities", {}),
                    "original_query": query
                }
            else:
                # Fallback if JSON doesn't have expected keys
                return {"intent": "llm_parse_error", "entities": {}, "raw_response": response_content, "original_query": query}

        else:
            # Fallback if response_content is not a string
             return {"intent": "llm_unexpected_response_type", "entities": {}, "raw_response": str(response_content), "original_query": query}

    except Exception as e:
        # Fallback for any other errors during LLM call or parsing
        return {"intent": "error", "entities": {}, "error_message": str(e), "original_query": query}
