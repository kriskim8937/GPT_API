from datetime import datetime
import os


def get_current_datetime_str() -> str:
    # Get current date and time and format it as a string including seconds
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")


def ensure_directory_exists(directory: str) -> None:
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Created directory: {directory}")
