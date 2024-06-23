# -*- coding: utf-8 -*-

# Sample Python code for youtube.commentThreads.insert
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/code-samples#python

from src.auth import get_authenticated_service
from src.models import get_uploaded_videos, set_status_to_commented

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    for video_id, url in get_uploaded_videos("svt_news"):
        print(video_id, url)
        youtube = get_authenticated_service(scopes)
        request = youtube.commentThreads().insert(
            part="snippet",
            body={
              "snippet": {
                "videoId": video_id,
                "topLevelComment": {
                  "snippet": {
                    "textOriginal": f"구독 감사합니다! 😊 원본 기사는 다음 링크를 참조해 주세요.\n\n{url}" 
                  }
                }
              }
            }
        )
        response = request.execute()
        print(response)
        set_status_to_commented("svt_news", video_id)

if __name__ == "__main__":
    main()