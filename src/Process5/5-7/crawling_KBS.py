#과정 5 - (문제7) "정기적으로 배달되는 지구소식"

import requests
from bs4 import BeautifulSoup

import requests

def get_kbs_headlines() :
    URL = 'https://news.kbs.co.kr/news/pc/main/main.html'
    
    try :
        response = requests.get(URL)
        response.raise_for_status()  # 요청이 성공적으로 이루어졌는지 확인
        # HTTP 응답에서 HTML 문자열 가져오기
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')

        # <p> tag 중 class="title"인 요소 찾아서 list로 저장
        headline_tags = soup.find_all('p', class_='title') 
        
        headline_list = []

        for tag in headline_tags :
            headline = tag.text.strip()
            if headline :
                headline_list.append(headline)

        # 헤드라인에 해당하지 않는 요소 제거
        headline_list.pop()             
        headline_list.pop(0)
        
        return headline_list

    except requests.exceptions.RequestException as e :
        print(f'Error Getting KBS news : {e}')
        return None

# [보너스 과제] - 네이버 날씨 가져오기
def get_weather() :
    URL = 'https://search.naver.com/search.naver?where=nexearch&sm=top_hty&fbm=0&ie=utf8&query=%EB%82%A0%EC%94%A8'
    
    try :
        response = requests.get(URL)
        response.raise_for_status()
        
        html = response.text
        soup = BeautifulSoup(html, 'html.parser')
        
        weather_section = soup.find('section',class_='sc_new cs_weather_new _cs_weather')

        location_info = weather_section.find('h2',class_='title')

        today_weather_info = weather_section.find('div',class_='_today')

        weekly_weather_info = weather_section.find_all('li', class_='week_item')

        print('위치 : ',location_info.text)
        print('오늘의 날씨 : ',today_weather_info.text.strip())
        print('주간 날씨')
        for weather in weekly_weather_info :
            print(weather.text.strip())
    
    except requests.exceptions.RequestException as e :
        print(f'Error Getting Naver Weather : {e}')
        return None


def main() :
    headline_news = get_kbs_headlines()
    print('--------------------오늘의 헤드라인 뉴스--------------------')
    for headline in headline_news :
        print(headline)

    print()
    
    print('--------------------오늘의 날씨--------------------')
    # 보너스 과제 - 네이버 날씨 가져오기
    weather = get_weather()
    

if __name__ == '__main__' :
    main()
