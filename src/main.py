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
        sentences = updated_content.split(". ")
        dall_e_3_client = DallE3()
        final_clips = []
        for idx, sentence in enumerate(sentences):
            audio_output_path = f"./outputs/audios/{new_title}_{idx}.mp3"
            # if os.path.exists(audio_output_path):
            #     print(f"Audio:{audio_output_path} already exists")
            generate_audio(sentence, audio_output_path)
            image_output_path = f"./outputs/images/{new_title}_{idx}.png"
            if os.path.exists(image_output_path):
                print(f"Image:{image_output_path} already exists")
            else:
                response = dall_e_3_client.get_image_data(sentence)
                image_data = response.b64_json
                save_image(image_data, image_output_path)
            audio_clip = AudioFileClip(audio_output_path)
            image_clip = ImageClip(image_output_path).set_duration(audio_clip.duration)
            title_clip = TextClip(
                new_title,
                fontsize=60,
                color="white",
                bg_color="black",
                font="Malgun-Gothic-Bold",
                size=(1024, 100),
            ).set_duration(audio_clip.duration)
            title_clip = title_clip.set_position(("center", "top"))
            subtitle_clip = TextClip(sentence + ".", fontsize=24, color='white', bg_color='black', font="Malgun-Gothic").set_duration(audio_clip.duration)
            subtitle_clip = subtitle_clip.set_pos('bottom')
            # Set audio to image clip
            video_clip = image_clip.set_audio(audio_clip)
            # Overlay subtitle on video
            video_clip = CompositeVideoClip([video_clip, title_clip, subtitle_clip])
            # Write individual clip to file
            video_output_path = f"./outputs/videos/{new_title}_{idx}.mp4"
            video_clip.write_videofile(video_output_path, fps=24)
            # Append to final clips list
            final_clips.append(video_clip)
        # Concatenate all individual clips
        merged_clip = concatenate_videoclips(final_clips)

        # Write the final merged video to a file
        merged_clip.write_videofile(f"outputs/videos/{new_title}.mp4", fps=24)
        break
        #process_news(news.title)


def read_unprocessed_news():
    query = "SELECT title, url FROM svt_news WHERE processed = 0"
    return [News(title, "", url) for title, url in execute_query(query)]

if __name__ == "__main__":
    main()
