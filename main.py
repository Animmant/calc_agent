# This is the main.py file.

import os
import sys

# Try to import dependencies, with helpful error messages if they're missing
try:
    import dotenv
except ImportError:
    print("Error: Required package 'python-dotenv' not found.")
    print("Please install it using: pip install python-dotenv")
    sys.exit(1)

try:
    from src.agent.nlu import understand_query
except ImportError as e:
    print(f"Error importing required modules: {str(e)}")
    print("\nThere might be issues with dependencies. Try the following:")
    print("1. Install required packages: pip install -r requirements.txt")
    print("2. If using Python 3.13, you may need to use Python 3.10 or 3.11 instead,")
    print("   as some libraries don't yet support Python 3.13.")
    print("3. Check that your PYTHONPATH includes the project root directory.")
    sys.exit(1)

def main():
    # Load environment variables from .env file
    dotenv.load_dotenv()
    
    # Check if Google API key is set
    if not os.environ.get("GOOGLE_API_KEY"):
        print("Error: GOOGLE_API_KEY environment variable is not set.")
        print("Please set it using the .env file or directly in your environment.")
        print("\nWindows PowerShell: $env:GOOGLE_API_KEY=\"your-api-key\"")
        print("Windows CMD: set GOOGLE_API_KEY=your-api-key")
        print("Linux/macOS: export GOOGLE_API_KEY=\"your-api-key\"")
        return
    
    print("Calculator Agent NLU Demo")
    print("-------------------------")
    print("Type 'quit' or 'exit' to end the program.")
    
    while True:
        # Get user input
        user_query = input("\nEnter your query: ")
        
        # Check for exit command
        if user_query.lower() in ["quit", "exit"]:
            break
        
        # Process the query
        try:
            result = understand_query(user_query)
            
            # Display the result
            print("\nResult:")
            print(f"Intent: {result['intent']}")
            print(f"Entities: {result['entities']}")
            
            # If there was an error, show it
            if 'error_message' in result:
                print(f"Error: {result['error_message']}")
        except Exception as e:
            print(f"\nAn error occurred: {str(e)}")
        
    print("Goodbye!")

if __name__ == "__main__":
    main()
