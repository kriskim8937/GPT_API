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
        # Extract the base64 image data from the response
        image_data = response.data[0].b64_json

        # Ensure the output directory exists
        output_dir = "./outputs/images"
        ensure_directory_exists(output_dir)

        # Define the file name and path
        current_datetime_str = get_current_datetime_str()
        file_name = f"image_{current_datetime_str}.png"
        output_path = os.path.join(output_dir, file_name)

        # Save the image
        save_image(image_data, output_path)

        return response.data[0], output_path
    except Exception as e:
        print(f"An error occurred: {e}")
        return None, None

def get_non_sensitive_prompt(prompt):
    prompt = "Remove sensitive words from below sentence:\n\n" + prompt
    return get_gpt4_response(prompt)

class DallE3:
    conversation_history = []
    def save_image(self, input):
        self.conversation_history.append(f"You: {input}")
        prompt = "\n".join(self.conversation_history)
        response, output_dir = get_dall_e_3_response(prompt)
        while not response:
            input = get_non_sensitive_prompt(input)
            print("non-sensitive-prompt: ", input)
            self.conversation_history = self.conversation_history[:-1]
            self.conversation_history.append(f"You: {input}")
            prompt = "\n".join(self.conversation_history)
            response, output_dir = get_dall_e_3_response(prompt)
        self.conversation_history.append(f"GPT-4: {response.revised_prompt}")
        print(f"GPT-4: {response.revised_prompt}")
        return output_dir

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

        gpt4_response, _ = get_dall_e_3_response(prompt)
        if gpt4_response:
            # Add GPT-4's response to the conversation history
            conversation_history.append(f"GPT-4: {gpt4_response.revised_prompt}")
            print(f"GPT-4: {gpt4_response.revised_prompt}")


if __name__ == "__main__":
    main()
