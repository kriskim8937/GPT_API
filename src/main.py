from gpt_4 import get_gpt4_response
from dall_e_3 import DallE3, save_image
from tts_1 import generate_audio
from svt_parser import News, get_news_titles_and_urls, get_content
from moviepy.editor import (
    ImageClip,
    concatenate_videoclips,
    AudioFileClip,
    TextClip,
    CompositeVideoClip,
)
from models import (
    news_exists,
    add_news,
    process_news,
    execute_query,
)
import os

os.environ["IMAGEMAGICK_BINARY"] = (
    "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"  # Update the path accordingly
)  


def translate_and_summarize(news):
    prompt = f"The article titled {news.title} is provided below. translate into Korean with honorifics and summarized in 5 sentences, eliminate any irrelevant details. Don't use dash '-'. Should be less than 290 characters:\n\n{news.content}"
    return get_gpt4_response(prompt)


def get_new_title(title, updated_news):
    select_query = """
    SELECT new_title
    FROM svt_news
    WHERE title = ?;
    """
    new_title = execute_query(select_query, (title,))
    if new_title:
        new_title = new_title[0][0]
    print(new_title)
    if not new_title:
        prompt = f"Generate a title of the below news in Korean in one sentence. Should be less then 18 characters:\n\n{updated_news}"
        new_title = get_gpt4_response(prompt)
        execute_query("""
            UPDATE svt_news
            SET new_title = ?
            WHERE title = ?
        """, (new_title, title))
    return new_title


def get_revised_prompt(prompt):
    prompt = "Remove sensitive words from below sentence:\n\n" + prompt
    return get_gpt4_response(prompt)


def main():
    news_list = get_news_titles_and_urls()
    for news in news_list:
        if news_exists(news.title):
            print(f"This news({news.title}) already registered in db")
        else:
            add_news(news.title, news.link)
            print(f"{news.title} added")
    for news in read_unprocessed_news():
        print(f"Start to process news({news.title})")
        raw_content = get_content(news.link)
        news.content = raw_content
        updated_content = translate_and_summarize(news)
        new_title = get_new_title(news.title, updated_content)
        print("new_title: ", new_title)
        print("updated_news: ", updated_content)
        audio_path = generate_audio(updated_content)
        create_video_from_text(updated_content, audio_path, new_title)
        process_news(news.title)


def read_unprocessed_news():
    query = "SELECT title, url FROM svt_news WHERE processed = 0"
    return [News(title, "", url) for title, url in execute_query(query)]


def create_video_from_text(text, audio_path, new_title):
    """
    Create a video from text by combining audio and images.

    Args:
        text (str): The text to be converted into a video.
        audio_path (str): The path to the audio file.
        new_title (str): The title of the video.

    Returns:
        None
    """
    # Create audio
    audio_clip = AudioFileClip(audio_path)

    # Create title text clip
    title_clip = TextClip(
        new_title,
        fontsize=60,
        color="white",
        bg_color="black",
        font="Malgun-Gothic-Bold",
        size=(1024, 100),
    ).set_duration(audio_clip.duration)
    title_clip = title_clip.set_position(("center", "top"))

    # Split text for each image (assuming each image holds one sentence for simplicity)
    sentences = text.split(". ")
    image_files = []
    clips = []
    dall_e_3_client = DallE3()

    for i, sentence in enumerate(sentences):
        output_path = f"./outputs/images/{new_title}_{i}.png"
        if os.path.exists(output_path):
            print(f"Image:{output_path} already exists")
        else:
            response = dall_e_3_client.get_image_data(sentence)
            # Extract the base64 image data from the response
            image_data = response.b64_json
            save_image(image_data, output_path)
            print(output_path)
        image_files.append(output_path)
        image_clip = ImageClip(output_path).set_duration(
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
