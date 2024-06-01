from gpt_4 import get_gpt4_response
from dall_e_3 import get_dall_e_3_response, DallE3
from tts_1 import generate_audio
from svt_parser import get_news
from moviepy.editor import (
    ImageClip,
    concatenate_videoclips,
    AudioFileClip,
    TextClip,
    CompositeVideoClip
)
import os
os.environ['IMAGEMAGICK_BINARY'] = 'C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe'  # Update the path accordingly

def translate_and_summarize(news):
    prompt = f"The article titled {news.title} is provided below. translate into Korean with honorifics and summarized in 5 sentences, eliminate any irrelevant details. Don't use dash '-'. Don't use English at all. Should be less than 300 characters:\n\n{news.content}"
    return get_gpt4_response(prompt)


def get_new_title(updated_news):
    prompt = f"Generate a title of the below news in Korean in one sentence. Should be less then 20 characters:\n\n{updated_news}"
    return get_gpt4_response(prompt)


def get_revised_prompt(prompt):
    prompt = "Remove sensitive words from below sentence:\n\n" + prompt
    return get_gpt4_response(prompt)


def main():
    news_list = get_news()
    for i in news_list :
        print(i.title)
        print(i.link)
    # updated_news = translate_and_summarize(news_list[0])
    # new_title = get_new_title(updated_news)
    # print("new_title: ", new_title)
    # print("updated_news: ", updated_news)
    # audio_path = generate_audio(updated_news)
    # create_video_from_text(updated_news, audio_path, new_title)


def create_video_from_text(text, audio_path, new_title):
    # Create audio
    audio_clip = AudioFileClip(audio_path)

    # Create title text clip
    title_clip = TextClip(new_title, fontsize=70, color='white', bg_color='white', font='NanumGothic', size=(1920, 100)).set_duration(audio_clip.duration)
    title_clip = title_clip.set_position(('center', 'top'))

    # Split text for each image (assuming each image holds one sentence for simplicity)
    sentences = text.split(". ")
    image_files = []
    clips = []
    dall_e_3_client = DallE3()

    for i, sentence in enumerate(sentences):
        image_path = dall_e_3_client.save_image(sentence)
        print(image_path)
        image_files.append(image_path)

        image_clip = ImageClip(image_path).set_duration(
            audio_clip.duration / len(sentences)
        )
        clips.append(image_clip)

    # Concatenate all image clips
    final_clip = concatenate_videoclips(clips, method="compose")

    # Add title text clip to the video
    final_clip_with_title = CompositeVideoClip([final_clip, title_clip])

    # Combine audio and video with title
    final_video = final_clip_with_title.set_audio(audio_clip)

    # Write the final video file
    final_video.write_videofile(f"outputs/videos/{new_title}.mp4", fps=24)


if __name__ == "__main__":
    main()