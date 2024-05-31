from openai.types.images_response import Image
from openai import OpenAI
import base64
import os
from dotenv import load_dotenv
from src import get_current_datetime_str

load_dotenv()
client = OpenAI()

def ensure_directory_exists(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")

def save_image(image_data: str, output_path: str) -> None:
    image_binary = base64.b64decode(image_data)
    with open(output_path, "wb") as image_file:
        image_file.write(image_binary)
    print(f"Image saved to {output_path}")

def get_gpt4_response(prompt: str) -> Image:
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

        return response.data[0]
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

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

        gpt4_response = get_gpt4_response(prompt)
        if gpt4_response:
            # Add GPT-4's response to the conversation history
            conversation_history.append(f"GPT-4: {gpt4_response.revised_prompt}")
            print(f"GPT-4: {gpt4_response.revised_prompt}")

if __name__ == "__main__":
    main()