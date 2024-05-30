from openai.types.images_response import Image
from openai import OpenAI
import base64
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI()


def get_gpt4_response(prompt) -> Image:
    response = client.images.generate(
        model="dall-e-3",
        prompt=prompt,
        n=1,
        size="1024x1024",
        response_format="b64_json",
    )
    # Extract the base64 image data from the response
    image_data = response.data[0].b64_json

    # Decode the base64 data
    image_binary = base64.b64decode(image_data)
    # Define the specific directory and file name where you want to save the image
    directory = "./outputs/images"
    file_name = "output_image.png"
    output_path = os.path.join(directory, file_name)
    # Save the image binary data to the specified file
    with open(output_path, "wb") as image_file:
        image_file.write(image_binary)

    print(f"Image saved to {output_path}")
    return response.data[0]


def main():
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
        # Add GPT-4's response to the conversation history
        conversation_history.append(f"GPT-4: {gpt4_response}")
        print(f"GPT-4: {gpt4_response.revised_prompt}")


if __name__ == "__main__":
    main()
