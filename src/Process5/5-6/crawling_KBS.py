# 과정 5 - (문제6) "지구와 연결된 네트워크"

import requests

def get_kbs_html() :
    URL = 'https://news.kbs.co.kr/news/pc/main/main.html'
    
    try :
        response = requests.get(URL)
        response.raise_for_status()  # 요청이 성공적으로 이루어졌는지 확인
        
        # HTTP 응답에서 HTML 문자열 가져오기
        html = response.text
        return html

    except requests.exceptions.RequestException as e :
        print(f'Error Getting KBS news : {e}')
        return None

def extract_headlines(html) :
    headlines = []
    
    # 헤드라인 뉴스가 포함된 특정 패턴 찾기
    start_pattern = """<div class="txt-wrapper">
                    <p class="title">"""
    end_pattern = '</p>'

    start_idx = html.find(start_pattern)
    
    while start_idx != -1 :
        end_idx = html.find(end_pattern, start_idx)

        if end_idx != -1 :
            headlines.append(html[start_idx + len(start_pattern):end_idx].strip().replace('<br>',""))
        
        start_idx = html.find(start_pattern, end_idx)
    
    return headlines

def main() :
    html_content = get_kbs_html()
    
    headline_news = extract_headlines(html_content)

    print('--------------------오늘의 헤드라인 뉴스--------------------')
    for headline in headline_news :
        print(headline)

if __name__ == '__main__' :
    main()