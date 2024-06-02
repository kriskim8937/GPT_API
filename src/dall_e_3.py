from openai.types.images_response import Image
from openai import OpenAI
import base64
import os
from gpt_4 import get_gpt4_response
from dotenv import load_dotenv
from common import ensure_directory_exists, get_current_datetime_str

load_dotenv()
client = OpenAI()


def save_image(image_data: str, output_path: str) -> None:
    image_binary = base64.b64decode(image_data)
    with open(output_path, "wb") as image_file:
        image_file.write(image_binary)
    print(f"Image saved to {output_path}")


def get_dall_e_3_response(prompt: str) -> Image:
    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt,
            n=1,
            size="1024x1024",
            response_format="b64_json",
        )
        return response.data[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def get_non_sensitive_prompt(prompt):
    prompt = "Remove sensitive words from below sentence:\n\n" + prompt
    return get_gpt4_response(prompt)

class DallE3:
    def get_image_data(self, input_text):
        self.conversation_history = []
        self.conversation_history.append(f"You: {input_text}. Don't put numbers on the image.")
        prompt = "\n".join(self.conversation_history)
        response = get_dall_e_3_response(prompt)
        while not response:
            input_text = get_non_sensitive_prompt(input_text)
            print("non-sensitive-prompt: ", input_text)
            self.conversation_history = self.conversation_history[:-1]
            self.conversation_history.append(f"You: {input_text}")
            prompt = "\n".join(self.conversation_history)
            print(prompt)
            response = get_dall_e_3_response(prompt)
        self.conversation_history.append(f"GPT-4: {response.revised_prompt}")
        print(f"GPT-4: {response.revised_prompt}")
        return response

def main() -> None:
    conversation_history = []
    print("Welcome to the Image generation! Type 'exit' to end the conversation.")
    while True:
        user_input = input("You: ")
        if user_input.lower() == "exit":
            print("Goodbye!")
            break
        # Construct the prompt with context
        conversation_history.append(f"You: {user_input}")
        prompt = "\n".join(conversation_history)

        gpt4_response = get_dall_e_3_response(prompt)
        if gpt4_response:
            save_image(gpt4_response.b64_json, f"outputs/images/image_{get_current_datetime_str()}.png")
            # Add GPT-4's response to the conversation history
            conversation_history.append(f"GPT-4: {gpt4_response.revised_prompt}")
            print(f"GPT-4: {gpt4_response.revised_prompt}")


if __name__ == "__main__":
    main()
