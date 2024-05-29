from openai.types.images_response import Image
from openai import OpenAI
client = OpenAI()
def get_gpt4_response(prompt) -> Image: 
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024"
    )


    # Check if the request was successful
    return response.data[0]

def main():
    conversation_history = []
    print("Welcome to the Image generation! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == 'exit':
            print("Goodbye!")
            break
        # Construct the prompt with context
        conversation_history.append(f"You: {user_input}")
        prompt = "\n".join(conversation_history)
        gpt4_response = get_gpt4_response(prompt)
        # Add GPT-4's response to the conversation history
        conversation_history.append(f"GPT-4: {gpt4_response}")
        print(f"GPT-4: {gpt4_response.revised_prompt}")
        print(f"URL: {gpt4_response.url}")

if __name__ == "__main__":
    main()