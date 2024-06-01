from openai import OpenAI
from dotenv import load_dotenv
from common import ensure_directory_exists, get_current_datetime_str
import os

load_dotenv()

client = OpenAI()


def generate_audio(script):
    # Ensure the output directory exists
    output_dir = "./outputs/audios"
    ensure_directory_exists(output_dir)

    # Define the file name and path
    current_datetime_str = get_current_datetime_str()
    file_name = f"audio_{current_datetime_str}.mp3"
    output_path = os.path.join(output_dir, file_name)

    response = client.audio.speech.create(
        model="tts-1",
        voice="alloy",
        input=script,
    )
    response.stream_to_file(output_path)
    return output_path
