from video_generator import VideoGenerator
from namu_hot_now_parser import NamuHotNowParser
from gpt_4 import get_gpt4_response
from common import contains_specific_special_characters
from models import execute_query
from svt_parser import SvtParser

class SvtVideoGenerator(VideoGenerator):
    def __init__(self, contents_parser):
        super().__init__(contents_parser)
        self.table_name = "svt_news"
        self.num_sentences = 4

    def get_new_title(self, title, updated_news):
        select_query = "SELECT new_title FROM svt_news WHERE title = ?;"
        new_title = execute_query(select_query, (title,))
        if new_title and new_title[0][0]:
            print(f"New title:{new_title[0][0]} already exists in the database.")
            return new_title[0][0]
        while True:
            prompt = f"Generate a title of the below news in Korean in one sentence. Should be less than 18 characters. Don't use special characters that are not allowed in file name:\n\n{updated_news}"
            new_title = get_gpt4_response(prompt)
            if not contains_specific_special_characters(new_title):
                execute_query("UPDATE svt_news SET new_title = ? WHERE title = ?", (new_title, title))
                return new_title


SvtVideoGenerator(SvtParser()).generate_video()
