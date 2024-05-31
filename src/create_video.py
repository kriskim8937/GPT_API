from moviepy.editor import ImageSequenceClip, AudioFileClip
from common import get_current_datetime_str
# List of image file paths
input_path = "./outputs/images/"
image_files = [input_path + "image_2024-05-30-20-49-40.png", input_path + "image_2024-05-30-20-57-00.png", input_path + "image_2024-05-30-21-00-34.png"]

# Generate a video clip from images
clip = ImageSequenceClip(image_files, durations=[2, 2, 2])  # duration of each image

# Repeat the sequence to match audio length
audio = AudioFileClip("./outputs/audios/audio.mp3")

# Loop the image sequence to fit the length of the audio
video = clip.loop(duration=audio.duration)

# Set the audio to the video
video = video.set_audio(audio)

# Write the result to a video file
video.write_videofile(f"./outputs/videos/video-{get_current_datetime_str()}.mp4", codec="libx264", audio_codec="aac", fps=24)
