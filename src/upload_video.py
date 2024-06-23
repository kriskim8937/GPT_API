import googleapiclient.discovery
import googleapiclient.errors
from src.models import execute_query, set_status_to_video_uploaded, set_video_id
from src.auth import get_authenticated_service

# Define the scopes required for the application
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]
CLIENT_SECRETS_FILE = "client_secret.json"
CREDENTIALS_FILE = "youtube_credentials.json"

def read_generated_news():
    """
    Reads unprocessed news from the database.

    Returns:
    list: List of unprocessed news objects.
    """
    query = "SELECT new_title, url FROM svt_news WHERE status = 'video_generated';"
    return [(new_title, url) for new_title, url in execute_query(query)]

def upload_video(youtube, video_file, title, description, tags, category_id, privacy_status):
    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags,
            "categoryId": category_id
        },
        "status": {
            "privacyStatus": privacy_status
        }
    }

    media_file = googleapiclient.http.MediaFileUpload(video_file, chunksize=-1, resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media_file
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if status:
            print(f"Uploaded {int(status.progress() * 100)}%")

    print(f"Upload Complete! Video ID: {response['id']}")
    return response['id']


def main():
    youtube = get_authenticated_service(SCOPES) 
    # Print the list of file names
    for new_title, url in read_generated_news():
        print(f"Upload video title: {new_title}")
        video_file = f"outputs/videos/{new_title}.mp4"
        description = f"원본 링크는 다음을 참조해 주세요 : {url}"
        tags = ["test", "upload"]
        category_id = "22"  # 22 is the category ID for "People & Blogs"
        privacy_status = "public"  # or 'private', 'unlisted'
        video_id = upload_video(youtube, video_file, new_title, description, tags, category_id, privacy_status)
        set_status_to_video_uploaded("svt_news", new_title)
        set_video_id("svt_news", new_title, video_id)
        print(f"Uploaded video ID: {video_id}")

if __name__ == "__main__":
    main()