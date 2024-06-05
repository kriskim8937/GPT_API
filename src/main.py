import os
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


def translate_and_summarize(news):
    """
    Translates and summarizes the news content into Korean with honorifics in less than 290 characters. 

    Args:
    news (News): News object containing the title and content.

    Returns:
    str: Translated and summarized content.
    """
    prompt = f"The article titled {news.title} is provided below. Translate into Korean with honorifics and summarize in 5 sentences, eliminating any irrelevant details. Don't use dash '-'. Should be less than 290 characters in total:\n\n{news.content}"
    return get_gpt4_response(prompt)


def get_new_title(title, updated_news):
    """
    Retrieves or generates a new title for the news in Korean.

    Args:
    title (str): Original title of the news.
    updated_news (str): Updated news content.

    Returns:
    str: New title in Korean.
    """
    select_query = "SELECT new_title FROM svt_news WHERE title = ?;"
    new_title = execute_query(select_query, (title,))

    if new_title:
        new_title = new_title[0][0]

    if not new_title:
        prompt = f"Generate a title of the below news in Korean in one sentence. Should be less than 18 characters. Don't use special characters that are not allowed in file name:\n\n{updated_news}"
        new_title = get_gpt4_response(prompt)
        execute_query("UPDATE svt_news SET new_title = ? WHERE title = ?", (new_title, title))

    return new_title


def split_text(text):
    """
    Splits the text into two parts roughly equal in length.

    Args:
    text (str): Text to be split.

    Returns:
    tuple: Two parts of the text.
    """
    middle_index = len(text) // 2

    before = text.rfind(' ', 0, middle_index)
    after = text.find(' ', middle_index)

    if before == -1:
        split_index = after
    elif after == -1:
        split_index = before
    else:
        split_index = before if middle_index - before <= after - middle_index else after

    part1 = text[:split_index]
    part2 = text[split_index+1:]

    return part1, part2


def read_unprocessed_news():
    """
    Reads unprocessed news from the database.

    Returns:
    list: List of unprocessed news objects.
    """
    #query = "SELECT title, url FROM svt_news WHERE status IS NULL;"
    query = "SELECT title, url FROM svt_news WHERE date = '2024-06-05';"
    return [News(title, "", url) for title, url in execute_query(query)]


def main():
    """
    Main function to orchestrate the news processing.
    """
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
        new_title = get_new_title(news.title, updated_content).replace('"', "")

        print("new_title: ", new_title)
        print("updated_news: ", updated_content)
        user_input = input("Do you want to progress? (y/n): ")
        if user_input.lower() == 'y':
            print("Progressing...")
        else:
            print("Continuing...")
            continue
        sentences = updated_content.split(". ")
        dall_e_3_client = DallE3()
        final_clips = []

        for idx, sentence in enumerate(sentences):
            audio_output_dir = "./outputs/audios/"
            image_output_dir = "./outputs/images/"
            video_output_dir = "./outputs/videos/"
            os.makedirs(audio_output_dir, exist_ok=True)
            os.makedirs(image_output_dir, exist_ok=True)
            os.makedirs(video_output_dir, exist_ok=True)

            audio_output_path = os.path.join(audio_output_dir, f"{new_title}_{idx}.mp3")
            generate_audio(sentence, audio_output_path)

            image_output_path = os.path.join(image_output_dir, f"{new_title}_{idx}.png")
            if not os.path.exists(image_output_path):
                response = dall_e_3_client.get_image_data(sentence)
                image_data = response.b64_json
                save_image(image_data, image_output_path)

            audio_clip = AudioFileClip(audio_output_path)
            image_clip = ImageClip(image_output_path).set_duration(audio_clip.duration)

            title_clip = TextClip(new_title, fontsize=60, color="white", bg_color="black", font="Malgun-Gothic-Bold", size=(1024, 100)).set_duration(audio_clip.duration)
            title_clip = title_clip.set_position(("center", "top"))

            subtitle_1, subtitle_2 = split_text(sentence)
            subtitle_clip_1 = TextClip(subtitle_1, fontsize=35, color='white', bg_color='black', font="Malgun-Gothic").set_duration(audio_clip.duration).set_pos(('center', image_clip.size[1] - 90))
            subtitle_clip_2 = TextClip(subtitle_2, fontsize=35, color='white', bg_color='black', font="Malgun-Gothic").set_duration(audio_clip.duration).set_pos(('center', image_clip.size[1] - 45))

            video_clip = image_clip.set_audio(audio_clip).set_audio(audio_clip)
            video_clip = CompositeVideoClip([video_clip, title_clip, subtitle_clip_1, subtitle_clip_2]) 

            video_output_path = os.path.join(video_output_dir, f"{new_title}_{idx}.mp4")
            video_clip.write_videofile(video_output_path, fps=24)
            final_clips.append(video_clip)

        merged_clip = concatenate_videoclips(final_clips)
        merged_clip.write_videofile(os.path.join(video_output_dir, f"{new_title}.mp4"), fps=24)

        process_news(news.title)

if __name__ == "__main__":
    main()