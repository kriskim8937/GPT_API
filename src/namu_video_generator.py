from video_generator import VideoGenerator
from namu_hot_now_parser import NamuHotNowParser

class NamuVideoGenerator(VideoGenerator):
    def __init__(self, contents_parser):
        super().__init__(contents_parser)
        self.table_name = "namu_hot_posts"
        self.num_sentences = 3
        self.num_images = 2

    def get_new_title(self, title, updated_news):
        return title


NamuVideoGenerator(NamuHotNowParser()).generate_video()
