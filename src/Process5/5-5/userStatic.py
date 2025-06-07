# 과정 5 - (문제5) "접속한 사용자 정보를 살펴보자" 
# [보너스 과제] - webserver_user.log 파일을 읽어서 접속자들의 운영체계 및 웹 브라우저 별 통계를 내고 원 그래프로 시각화

import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 이름
LOG_FILE = 'src/Process5/5-5/webserver_user.log.csv'

def analyze_user_agents(csv_file):
    try:
        # CSV 파일 읽기
        df = pd.read_csv(csv_file)
        
        # 운영체계별 통계
        os_counts = df['Operating System'].value_counts()
        
        # 웹 브라우저별 통계
        browser_counts = df['Browser'].value_counts()
        
        # 시각화: 운영체계별 원 그래프
        plt.figure(figsize=(10, 6))
        plt.subplot(1, 2, 1)
        os_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Operating System Distribution')
        plt.ylabel('')
        
        # 시각화: 웹 브라우저별 원 그래프
        plt.subplot(1, 2, 2)
        browser_counts.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Web Browser Distribution')
        plt.ylabel('')
        
        # 그래프 출력
        plt.tight_layout()
        plt.show()
        
    except Exception as e:
        print(f'Error analyzing user agents: {e}')

# 메인 함수
def main():
    analyze_user_agents(LOG_FILE)

if __name__ == '__main__':
    main()