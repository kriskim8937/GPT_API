from openai import OpenAI
from dotenv import load_dotenv
from common import ensure_directory_exists, get_current_datetime_str
import os

load_dotenv()

client = OpenAI()


def generate_audio(script, output_path):
    # Ensure the output directory exists
    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=script,
    )
    response.stream_to_file(output_path)
