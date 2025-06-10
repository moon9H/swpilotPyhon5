# 과정 6 - (문제6) 여론조사

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser

# API 키 설정
API_KEY = 'AIzaSyCAG0cScjIc52hzoaCZvYksbFJiX0-6se0'

# YouTube Data API 클라이언트를 빌드
youtube = build('youtube', 'v3', developerKey=API_KEY)

def search_videos(query):
    try:
        search_response = youtube.search().list(
            q=query,
            part='snippet',
            maxResults=10  # 최대 10개의 결과
        ).execute()

        # 검색 결과에서 각 동영상의 제목과 댓글을 추출
        for search_result in search_response.get('items', []):
            if search_result['id']['kind'] == 'youtube#video':
                video_id = search_result['id']['videoId']
                video_title = search_result['snippet']['title']
                
                print(f"동영상 제목: {video_title}")
                
                # [보너스 과제] - 동영상의 댓글을 가져와 출력
                comments_response = youtube.commentThreads().list(
                    part='snippet',
                    videoId=video_id,
                    textFormat='plainText',
                    maxResults=10  # 각 동영상당 최대 10개의 댓글
                ).execute()

                for comment in comments_response['items']:
                    comment_text = comment['snippet']['topLevelComment']['snippet']['textDisplay']
                    print(f"- {comment_text}")

                print()  # 각 동영상의 댓글 목록을 구분하기 위한 빈 줄 출력

    except HttpError as e:
        print('An HTTP error %d occurred:\n%s' % (e.resp.status, e.content))

if __name__ == '__main__':
    # '우주'라는 키워드로 검색
    search_videos('우주')