from src.auth import get_authenticated_service

def main():
    youtube = get_authenticated_service()

    # Example: Perform a search query
    request = youtube.search().list(
        part="snippet",
        maxResults=5,  # Number of results to retrieve
        q="YOUR_SEARCH_QUERY"  # Replace with your search query
    )
    response = request.execute()

    # Print video IDs
    for item in response.get('items', []):
        if item['id']['kind'] == 'youtube#video':
            print(f"Video ID: {item}")

if __name__ == "__main__":
    main()