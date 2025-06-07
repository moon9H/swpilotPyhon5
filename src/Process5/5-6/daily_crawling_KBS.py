# 과정 5 - (문제6) "지구와 연결된 네트워크"
# 보너스 과제 - 하루에 한 번 정기적으로 실행하는 방법 (code ver.)

import schedule
import time
def job():
    print('Running KBS news crawling...')
    html_content = get_kbs_html()
    if html_content:
        headline_news = extract_headlines(html_content)
        print('--------------------오늘의 헤드라인 뉴스--------------------')
        for headline in headline_news:
            print(headline)

# schedule에 작업 등록 (매일 오전 9시에 실행)
schedule.every().day.at("09:00").do(job)

# 무한 루프로 스케줄러 실행
while True:
    schedule.run_pending()
    time.sleep(60)  # 1분마다 체크하여 실행

# 보너스 과제 - 하루에 한 번 정기적으로 실행하는 방법 (using Windows ver.)
# Windows에서의 작업 스케줄러 설정
# 1. 작업 스케줄러 열기:
#     시작 메뉴에서 '작업 스케줄러'를 검색하여 실행합니다.
# 2. 새 작업 만들기:
#     오른쪽 창의 "기본 작업 만들기"를 클릭합니다.
# 3. 기본 정보 설정:
#     이름과 설명을 입력합니다. 예를 들어, "Daily KBS News Crawling".
# 4. 트리거 설정:
#     "새로 만들기"를 클릭하고, 시작을 설정합니다.
#     원하는 트리거(일일, 특정 시간 등)를 선택하고 설정합니다.
# 5. 동작 설정:
#     동작 탭에서 "새로 만들기"를 클릭하여 실행할 프로그램을 설정합니다.
#     프로그램/스크립트란에는 Python 실행 파일의 경로를 입력합니다.
#     인수 추가란에는 실행할 스크립트 파일의 경로를 입력합니다.
# 6. 추가 설정:
#     필요에 따라 다른 설정(권한, 네트워크 조건 등)을 구성합니다.