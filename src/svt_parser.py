import requests
from bs4 import BeautifulSoup

def get_latest_news() -> list:
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
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find and filter all relevant links
    links = soup.find_all('a', href=True)
    filtered_links = [
        base_url + link['href'] for link in links
        if link['href'].startswith(postfix)
        and len(link['href'].split('/')) == 4
        and link['href'].split('/')[3]
        and not link['href'].split('/')[3].startswith("?")
    ]

    return filtered_links

if __name__ == "__main__":
    latest_news = get_latest_news()
    url = latest_news[0]
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Get the title
    title = soup.title.string

    # Get the contents (e.g., paragraphs)
    contents = []
    for paragraph in soup.find_all('p'):
        contents.append(paragraph.text)

    print("Title:", title)
    print("\nContents:")
    for content in contents:
        print(content)