import unittest
from unittest.mock import patch, MagicMock, mock_open
from src.gpt_4 import (
    get_gpt4_response,
    read_input_from_file,
    update_conversation_history,
)


class TestChatbot(unittest.TestCase):
    @patch("src.gpt_4.OpenAI")
    def test_get_gpt4_response(self, MockOpenAI):
        mock_client = MockOpenAI.return_value
        mock_completion = MagicMock()
        mock_completion.choices[0].message.content = "Hello, how can I help you?"
        mock_client.chat.completions.create.return_value = mock_completion

        prompt = "Hi"
        response = get_gpt4_response(prompt, mock_client)

        self.assertEqual(response, "Hello, how can I help you?")
        mock_client.chat.completions.create.assert_called_once_with(
            model="gpt-4o", messages=[{"role": "user", "content": prompt}]
        )

    @patch("builtins.open", new_callable=mock_open, read_data="This is a test input.")
    def test_read_input_from_file(self, mock_file):
        self.assertEqual(read_input_from_file("input.txt"), "This is a test input.")
        mock_file.assert_called_once_with("input.txt", "r")

    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_read_input_from_file_no_data(self, mock_file):
        self.assertEqual(read_input_from_file("input.txt"), "")
        mock_file.assert_called_once_with("input.txt", "r")

    def test_read_input_from_file_not_found(self):
        with patch("builtins.open", side_effect=FileNotFoundError):
            self.assertEqual(read_input_from_file("input.txt"), "")

    def test_update_conversation_history(self):
        history = []
        user_input = "Hi there!"
        gpt4_response = "Hello! How can I assist you today?"

        update_conversation_history(history, user_input, gpt4_response)

        self.assertEqual(
            history, ["You: Hi there!", "GPT-4: Hello! How can I assist you today?"]
        )


if __name__ == "__main__":
    unittest.main()
