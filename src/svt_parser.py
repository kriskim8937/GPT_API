import requests
from bs4 import BeautifulSoup
from dataclasses import dataclass
from typing import List


@dataclass
class News:
    title: str
    content: str
    link: str

    def __post_init__(self):
        if self.title.endswith(" | SVT Nyheter"):
            self.title = self.title[: -len(" | SVT Nyheter")]


def get_news_links() -> list:
    """Fetches the latest inrikes news links from the SVT website."""

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

    # Find and filter all relevant links
    links = soup.find_all("a", href=True)
    filtered_links = [
        base_url + link["href"]
        for link in links
        if link["href"].startswith(postfix)
        and len(link["href"].split("/")) == 4
        and link["href"].split("/")[3]
        and not link["href"].split("/")[3].startswith("?")
    ]

    return filtered_links


def get_news() -> List[News]:
    news = []
    news_links = get_news_links()
    for news_link in news_links:
        if "nattens-nyheter" not in news_link:
            title, content = get_title_and_content(news_link)
            news.append(News(title, content, news_link))
    return news


def get_news_titles_and_urls() -> List[News]:
    news = []
    news_links = get_news_links()
    for news_link in news_links:
        if "nattens-nyheter" not in news_link:
            title = get_title(news_link)
            news.append(News(title, "", news_link))
    return news


def get_content(news_link):
    response = requests.get(news_link)
    soup = BeautifulSoup(response.text, "html.parser")
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
    return content


def get_title_and_content(news_link):
    response = requests.get(news_link)
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


def get_title(news_link):
    response = requests.get(news_link)
    soup = BeautifulSoup(response.text, "html.parser")
    # Get the title
    title = soup.title.string
    return title
