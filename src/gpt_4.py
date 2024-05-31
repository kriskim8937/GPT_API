import os
from openai import OpenAI
from dotenv import load_dotenv
from typing import List

load_dotenv()

MODEL = "gpt-4o"
API_KEY = os.getenv("OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>")
print(API_KEY)
if not API_KEY:
    raise ValueError(
        "API key for OpenAI is not provided. Please set the OPENAI_API_KEY environment variable."
    )

client = OpenAI(api_key=API_KEY)


def get_gpt4_response(prompt: str, client: OpenAI, model: str = MODEL) -> str:
    completion = client.chat.completions.create(
        model=model, messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content


def read_input_from_file(filename: str = "input.txt") -> str:
    try:
        with open(filename, "r", encoding='utf-8') as file:
            return file.read().strip()
    except FileNotFoundError:
        print(f"File '{filename}' not found.")
        return ""


def update_conversation_history(
    conversation_history: List[str], user_input: str, gpt4_response: str
):
    conversation_history.append(f"You: {user_input}")
    conversation_history.append(f"GPT-4: {gpt4_response}")


def main():
    conversation_history = []
    print("Welcome to the GPT-4 chatbot! Type 'exit' to end the conversation.")

    while True:
        user_input = input("You: ").strip()

        if not user_input:
            print("No input provided. Reading from file.")
            user_input = read_input_from_file()

        if user_input.lower() == "exit":
            print("Goodbye!")
            break

        prompt = "\n".join(conversation_history + [f"You: {user_input}", "GPT-4: "])
        gpt4_response = get_gpt4_response(prompt, client)

        update_conversation_history(conversation_history, user_input, gpt4_response)
        print(f"GPT-4: {gpt4_response}")


if __name__ == "__main__":
    main()
