from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI()


def generate_audio(script, output_path):
    # Ensure the output directory exists
    response = client.audio.speech.create(
        model="tts-1",
        voice="nova",
        input=script,
    )
    response.stream_to_file(output_path)
