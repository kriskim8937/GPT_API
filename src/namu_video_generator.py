from video_generator import VideoGenerator

class NamuVideoGenerator(VideoGenerator):
    def __init__(self):
        super().__init__()
        self.table_name = "namu_hot_posts"
        self.num_sentences = 3

    def get_new_title(self, title, updated_news):
        return title

NamuVideoGenerator().generate_video()
