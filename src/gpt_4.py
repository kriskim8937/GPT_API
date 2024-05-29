import os
from openai import OpenAI

MODEL = "gpt-4o"
client = OpenAI(
    api_key=os.environ.get(
        "OPENAI_API_KEY", "<your OpenAI API key if not set as an env var>"
    )
)


def get_gpt4_response(prompt):
    completion = client.chat.completions.create(
        model=MODEL, messages=[{"role": "user", "content": prompt}]
    )
    return completion.choices[0].message.content


def main():
    conversation_history = []
    print("Welcome to the GPT-4 chatbot! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        conversation_history.append(f"You: {user_input}")
        # Construct the prompt with context
        prompt = "\n".join(conversation_history) + "\nGPT-4:"
        gpt4_response = get_gpt4_response(prompt)
        # Add GPT-4's response to the conversation history
        conversation_history.append(f"GPT-4: {gpt4_response}")
        print(f"GPT-4: {gpt4_response}")


if __name__ == "__main__":
    main()
