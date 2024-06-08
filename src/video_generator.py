import os
from gpt_4 import get_gpt4_response
from dall_e_3 import DallE3, save_image
from tts_1 import generate_audio
from svt_parser import get_content
from moviepy.editor import ImageClip, concatenate_videoclips, AudioFileClip, TextClip, CompositeVideoClip
from models import news_exists, add_news, execute_query

class VideoGenerator:
    SPECIAL_CHARACTERS = "#!@%-'_&$^*()+=:;?/"
    AUDIO_OUTPUT_DIR = "./outputs/audios/"
    IMAGE_OUTPUT_DIR = "./outputs/images/"
    VIDEO_OUTPUT_DIR = "./outputs/videos/"

    def __init__(self, contents_parser):
        self.num_sentences = 4
        self.max_content_length = 290
        self.table_name = "should_be_overridden_in_child_class"
        self.contents_parser = contents_parser

    def translate_and_summarize(self, title, content):
        prompt = f"The article titled {title} is provided below. Translate into Korean. Should be formal since it is news. Summarize in {self.num_sentences} sentences, eliminating any irrelevant details. Don't use dash '-’. Should be less than {self.max_content_length} characters in total:\n\n{content}"
        while True:
            updated_news = get_gpt4_response(prompt)
            if len(updated_news) <= self.max_content_length and len(updated_news.split(". ")) == self.num_sentences:
                return updated_news
            print(f"The length of the text exceeds {self.max_content_length} characters. Please try again.")

    def contains_specific_special_characters(self, text):
        return any(char in self.SPECIAL_CHARACTERS for char in text)

    def get_new_title(self, title, updated_news):
        select_query = f"SELECT new_title FROM {self.table_name} WHERE title = ?;"
        new_title = execute_query(select_query, (title,))
        if new_title and new_title[0][0]:
            print(f"New title:{new_title[0][0]} already exists in the database.")
            return new_title[0][0]
        while True:
            prompt = f"Generate a title of the below news in Korean in one sentence. Should be less than 18 characters. Don't use special characters that are not allowed in file name:\n\n{updated_news}"
            new_title = get_gpt4_response(prompt)
            if not self.contains_specific_special_characters(new_title):
                execute_query(f"UPDATE {self.table_name} SET new_title = ? WHERE title = ?", (new_title, title))
                return new_title

    def split_text(self, text):
        middle_index = len(text) // 2
        before = text.rfind(' ', 0, middle_index)
        after = text.find(' ', middle_index)
        split_index = before if before != -1 else after
        if before != -1 and after != -1:
            split_index = before if middle_index - before <= after - middle_index else after
        return text[:split_index], text[split_index+1:]

    def read_unprocessed_news(self, table):
        query = f"SELECT title, url FROM {table} WHERE status IS NULL;"
        return [(title, url) for title, url in execute_query(query)]

    def process_news_content(self, title, url):
        raw_content = get_content(url)
        updated_content = self.translate_and_summarize(title, raw_content)
        new_title = self.get_new_title(title, updated_content)
        print("new_title: ", new_title)
        print("updated_news: ", updated_content)
        return new_title, updated_content

    def should_generate_video(self):
        while True:
            user_input = input("Do you want to generate video based on content? (y/r/else(skip)): ")
            if user_input.lower() == 'y':
                return True
            if user_input.lower() == 'r':
                return False
            print("Skipping...")
            return None

    def create_directories(self, directories):
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def generate_video_clips(self, new_title, sentences):
        dall_e_3_client = DallE3()
        final_clips = []

        for idx, sentence in enumerate(sentences):
            audio_output_path = os.path.join(self.AUDIO_OUTPUT_DIR, f"{new_title}_{idx}.mp3")
            generate_audio(sentence, audio_output_path)

            image_output_path = os.path.join(self.IMAGE_OUTPUT_DIR, f"{new_title}_{idx}.png")
            if not os.path.exists(image_output_path):
                response = dall_e_3_client.get_image_data(sentence)
                image_data = response.b64_json
                save_image(image_data, image_output_path)

            audio_clip = AudioFileClip(audio_output_path)
            image_clip = ImageClip(image_output_path).set_duration(audio_clip.duration)

            title_clip = TextClip(new_title, fontsize=60, color="white", bg_color="black", font="Malgun-Gothic-Bold", size=(1024, 100)).set_duration(audio_clip.duration).set_position(("center", "top"))

            part1, part2 = self.split_text(sentence)
            subtitle_clip_1 = TextClip(part1, fontsize=35, color='white', bg_color='black', font="Malgun-Gothic").set_duration(audio_clip.duration).set_position(('center', image_clip.size[1] - 90))
            subtitle_clip_2 = TextClip(part2, fontsize=35, color='white', bg_color='black', font="Malgun-Gothic").set_duration(audio_clip.duration).set_position(('center', image_clip.size[1] - 45))

            video_clip = CompositeVideoClip([image_clip.set_audio(audio_clip), title_clip, subtitle_clip_1, subtitle_clip_2])

            video_output_path = os.path.join(self.VIDEO_OUTPUT_DIR, f"{new_title}_{idx}.mp4")
            video_clip.write_videofile(video_output_path, fps=24)
            final_clips.append(video_clip)

        return final_clips

    def generate_video(self):
        contents = self.contents_parser.get_contents()

        for content in contents:
            if news_exists(self.table_name, content.title):
                print(f"This news({content.title}) already registered in db")
            else:
                add_news(self.table_name, content.title, content.url)
                print(f"{content.title} added")

        for title, url in self.read_unprocessed_news(self.table_name):
            print(f"Start to process news({title})")

            try:
                new_title, updated_content = self.process_news_content(title, url)

                while (choice := self.should_generate_video()) is False:
                    new_title, updated_content = self.process_news_content(title, url)

                if choice is None:
                    continue

                sentences = updated_content.split(". ")
                self.create_directories([self.AUDIO_OUTPUT_DIR, self.IMAGE_OUTPUT_DIR, self.VIDEO_OUTPUT_DIR])
                final_clips = self.generate_video_clips(new_title, sentences)

                merged_clip = concatenate_videoclips(final_clips)
                merged_clip.write_videofile(os.path.join(self.VIDEO_OUTPUT_DIR, f"{new_title}.mp4"), fps=24)
                #set_status_to_video_generated(new_title)

            except Exception as e:
                print(f"An error occurred while processing news ({title}): {e}")