from video_generator import VideoGenerator
from namu_hot_now_parser import NamuHotNowParser
from gpt_4 import get_gpt4_response
from models import execute_query
from common import contains_specific_special_characters

class NamuVideoGenerator(VideoGenerator):
    def __init__(self, contents_parser):
        super().__init__(contents_parser)
        self.table_name = "namu_hot_posts"
        self.num_sentences = 4
        self.num_images = 2
        self.max_content_length = 1000

    def get_new_title(self, title, updated_news):
        select_query = f"SELECT new_title FROM {self.table_name} WHERE title = ?;"
        new_title = execute_query(select_query, (title,))
        if new_title and new_title[0][0]:
            print(f"New title:{new_title[0][0]} already exists in the database.")
            return new_title[0][0]
        while True:
            prompt = f"Generate a title of the below news in Korean in one sentence. Should be less than 18 characters. Don't use special characters that are not allowed in file name:\n\n{updated_news}"
            new_title = get_gpt4_response(prompt)
            if not contains_specific_special_characters(new_title):
                return new_title
    
    def translate_and_summarize(self, title, content):
        prompt = f"The article titled {title} is provided below. Translate into Korean. Should be formal since it is news. Summarize in {self.num_sentences} sentences, eliminating any irrelevant details. Don't use dash '-’. The Generated article The sentence must not exceed {self.max_content_length} characters.:\n\n{content}"
        while True:
            updated_news = get_gpt4_response(prompt)
            if len(updated_news) <= self.max_content_length and len(updated_news.split(". ")) <= self.num_sentences:
                return updated_news
            print(f"The length of the text:{len(updated_news)} exceeds {self.max_content_length} characters. Please try again.")


NamuVideoGenerator(NamuHotNowParser(minimum_likes=30)).generate_video()
