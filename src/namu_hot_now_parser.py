import requests
from bs4 import BeautifulSoup
import time
from dataclasses import dataclass
import re

# Base URL
base_url = 'https://arca.live/b/namuhotnow'

@dataclass
class NamuHotNowPost:
    title: str
    likes: int
    comment_count: int
    url: int
    datetime: str
    content: str = ""

# Function to fetch HTML content of a page
def fetch_page(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        print(f"Failed to retrieve page: {url}")
        return None

# Function to extract subpage links from the main page
def extract_links(html_content):
    soup = BeautifulSoup(html_content, 'html.parser')
    links = []
    for link in soup.find_all('a', href=True):
        href = link['href']
        if href.startswith('/b/namuhotnow/'):
            full_url = 'https://arca.live' + href
            # Extract comment count from the main page
            if not link.find('span', class_='comment-count') or not link.find('time'):
                continue
            title = link.find('span', class_='title').text.strip()
            comment_count = link.find('span', class_='comment-count').text
            likes = link.find('span', class_='vcol col-rate').text
            datetime = link.find('time')['datetime']
            if  int(likes) > 30:
                links.append(NamuHotNowPost(title=title, likes=int(likes), comment_count=int(re.search(r'\d+', comment_count).group()), url=full_url, datetime=datetime))
    return links

# Function to scrape subpages
def get_namu_hot_now_posts(base_url = base_url):
    main_page_content = fetch_page(base_url)
    if main_page_content:
        namu_hot_now_posts = extract_links(main_page_content)
        for namu_hot_now_post in namu_hot_now_posts:
            print(namu_hot_now_post)
            subpage_content = fetch_page(namu_hot_now_post.url)
            if subpage_content:
                # Here you can process the subpage content as needed
                soup = BeautifulSoup(subpage_content, 'html.parser')
                # Example: Extract the title of the subpage
                article_body = soup.find('div', class_='article-body')  # Finding the div with class 'article-body'
                article_content = article_body.find('div', class_='fr-view article-content')  # Finding the div with class 'fr-view article-content'
                # Extracting the text content of the article
                article_text = article_content.get_text().strip()
                print(article_text)
                # Sleep to avoid overwhelming the server0
                time.sleep(1)
                namu_hot_now_post.content = article_text
    return namu_hot_now_posts 

