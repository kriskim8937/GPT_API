import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List


@dataclass
class News:
    title: str
    content: str
    url: str

    def __post_init__(self):
        if self.title.endswith(" | SVT Nyheter"):
            self.title = self.title[: -len(" | SVT Nyheter")]


class SvtParser:
    def get_news_urls(self) -> list:
        """Fetches the latest inrikes news urls from the SVT website."""

        base_url = "https://www.svt.se"
        postfix = "/nyheter/inrikes"
        full_url = base_url + postfix

        try:
            response = requests.get(full_url)
            response.raise_for_status()  # Raises an HTTPError for bad responses
        except requests.RequestException as e:
            print(f"Failed to retrieve the webpage. Error: {e}")
            return []

        # Parse the HTML content
        soup = BeautifulSoup(response.content, "html.parser")

        # Find and filter all relevant urls
        urls = soup.find_all("a", href=True)
        filtered_urls = [
            base_url + url["href"]
            for url in urls
            if url["href"].startswith(postfix)
            and len(url["href"].split("/")) == 4
            and url["href"].split("/")[3]
            and not url["href"].split("/")[3].startswith("?")
        ]

        return filtered_urls


    def get_contents(self) -> List[News]:
        news = []
        news_urls = self.get_news_urls()
        for news_url in news_urls:
            if "nattens-nyheter" not in news_url:
                title, content = self.get_title_and_content(news_url)
                news.append(News(title, content, news_url))
        return news


    def get_news_titles_and_urls(self) -> List[News]:
        news = []
        news_urls = self.get_news_urls()
        for news_url in news_urls:
            if "nattens-nyheter" not in news_url:
                title = self.get_title(news_url)
                news.append(News(title, "", news_url))
        return news

    def get_title_and_content(self, news_url):
        response = requests.get(news_url)
        soup = BeautifulSoup(response.text, "html.parser")

        # Get the title
        title = soup.title.string

        # Get the contents (e.g., paragraphs, h2, and li) in order
        contents = []

        for tag in soup.find_all(["p", "h2", "li"]):
            if tag.name == "p":
                contents.append(tag.text)
            elif tag.name == "h2":
                contents.append(tag.text)
            elif tag.name == "li":
                contents.append(tag.text)

        # Combine all the contents into a single string
        content = "\n".join(contents)

        return title, content


    def get_title(self, news_url):
        response = requests.get(news_url)
        soup = BeautifulSoup(response.text, "html.parser")
        # Get the title
        title = soup.title.string
        return title
