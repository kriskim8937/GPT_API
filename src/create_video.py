from moviepy.editor import ImageSequenceClip, AudioFileClip

# List of image file paths
image_files = ["image1.jpg", "image2.jpg", "image3.jpg"]

# Generate a video clip from images
clip = ImageSequenceClip(image_files, durations=[2, 2, 2])  # duration of each image

# Repeat the sequence to match audio length
audio = AudioFileClip("audio.mp3")

# Loop the image sequence to fit the length of the audio
video = clip.loop(duration=audio.duration)

# Set the audio to the video
video = video.set_audio(audio)

# Write the result to a video file
video.write_videofile("output_looped.mp4", codec="libx264", audio_codec="aac")
