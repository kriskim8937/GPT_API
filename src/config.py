import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "..", "data", "news.db")
os.environ["IMAGEMAGICK_BINARY"] = (
    "C:\\Program Files\\ImageMagick-7.1.1-Q16-HDRI\\magick.exe"  # Update the path accordingly
)  