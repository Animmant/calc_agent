import unittest
from unittest.mock import patch, MagicMock
import json

# Assuming src.agent.nlu is the path to your nlu module.
# Adjust if your project structure is different and Python can't find the module.
# This might require adding src to PYTHONPATH or using relative imports if running with `python -m unittest`.
# For now, let's assume direct importability for simplicity in this subtask.
from src.agent.nlu import understand_query

class TestNLU(unittest.TestCase):

    @patch('src.agent.nlu.ChatGoogleGenerativeAI')
    def test_understand_query_success_json_response(self, MockChatGoogleGenerativeAI):
        # Configure the mock LLM and its response
        mock_llm_instance = MockChatGoogleGenerativeAI.return_value
        mock_response_content = {
            "intent": "test_intent",
            "entities": {"key": "value"}
        }
        # Langchain's AIMessage has a 'content' attribute.
        # The mock response should mimic this structure.
        mock_ai_message = MagicMock()
        mock_ai_message.content = json.dumps(mock_response_content) # Simulate JSON string output from LLM
        mock_llm_instance.invoke.return_value = mock_ai_message

        query = "This is a test query"
        result = understand_query(query)

        # Assertions
        self.assertEqual(result['intent'], "test_intent")
        self.assertEqual(result['entities'], {"key": "value"})
        self.assertEqual(result['original_query'], query)
        MockChatGoogleGenerativeAI.assert_called_once_with(model="gemini-pro", convert_system_message_to_human=True)
        mock_llm_instance.invoke.assert_called_once()

    @patch('src.agent.nlu.ChatGoogleGenerativeAI')
    def test_understand_query_llm_error(self, MockChatGoogleGenerativeAI):
        # Configure the mock LLM to raise an exception
        mock_llm_instance = MockChatGoogleGenerativeAI.return_value
        mock_llm_instance.invoke.side_effect = Exception("LLM API Error")

        query = "Another test query"
        result = understand_query(query)

        # Assertions
        self.assertEqual(result['intent'], "error")
        self.assertIn("LLM API Error", result['error_message'])
        self.assertEqual(result['original_query'], query)

    @patch('src.agent.nlu.ChatGoogleGenerativeAI')
    def test_understand_query_json_parse_error(self, MockChatGoogleGenerativeAI):
        # Configure the mock LLM to return malformed JSON
        mock_llm_instance = MockChatGoogleGenerativeAI.return_value
        mock_ai_message = MagicMock()
        mock_ai_message.content = "This is not valid JSON"
        mock_llm_instance.invoke.return_value = mock_ai_message
        
        query = "Query leading to parse error"
        result = understand_query(query)

        self.assertEqual(result['intent'], "llm_parse_error")
        self.assertEqual(result['original_query'], query)
        self.assertIn("This is not valid JSON", result['raw_response'])
        
    @patch('src.agent.nlu.ChatGoogleGenerativeAI')
    def test_understand_query_llm_response_missing_keys(self, MockChatGoogleGenerativeAI):
        # Configure the mock LLM to return JSON with missing keys
        mock_llm_instance = MockChatGoogleGenerativeAI.return_value
        mock_response_content = {"some_other_key": "some_value"} # Missing 'intent' and 'entities'
        mock_ai_message = MagicMock()
        mock_ai_message.content = json.dumps(mock_response_content)
        mock_llm_instance.invoke.return_value = mock_ai_message

        query = "Query leading to missing keys"
        result = understand_query(query)

        self.assertEqual(result['intent'], "llm_parse_error") # Or a more specific intent if you prefer
        self.assertEqual(result['original_query'], query)
        self.assertIn("some_other_key", json.loads(result['raw_response']))


if __name__ == '__main__':
    unittest.main()
