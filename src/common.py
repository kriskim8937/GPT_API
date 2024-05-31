from datetime import datetime
def get_current_datetime_str() -> str:
    # Get current date and time and format it as a string including seconds
    return datetime.now().strftime("%Y-%m-%d-%H-%M-%S")