#과정 3 - (문제6) "제갈공명"

import os
import mysql.connector

class MySQLHelper:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'swpilot')
        )
        self.cursor = self.connection.cursor()
    #[보너스 과제] - SQL 쿼리만 주면 실행하고 결과를 던저주는 유틸리티성 클래스 작성
    def run_query(self, query, params=None):
        try:
            if params is not None:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception as e:
            print('쿼리 실행 중 오류 발생:', e)
            return []

    def close(self):
        self.cursor.close()
        self.connection.close()


def show_storm_over_70(db):
    query = (
        'SELECT mars_date, temp, storm '
        'FROM mars_weather '
        'WHERE storm >= 70 '
        'ORDER BY mars_date;'
    )
    rows = db.run_query(query)
    print('[폭풍 확률 70% 이상 데이터]')
    print('날짜              | 기온 (°C) | 폭풍 확률 (%)')
    print('------------------|-----------|----------------')
    for row in rows:
        date_str = str(row[0].date())
        temp_str = str(int(row[1])) if row[1] is not None else 'N/A'
        storm_str = str(int(row[2])) if row[2] is not None else 'N/A'
        print(f'{date_str:^18} | {temp_str:^10}°C | {storm_str:^14}%')


def show_monthly_average(db):
    query = (
        'SELECT DATE_FORMAT(mars_date, "%Y-%m") AS month, '
        'AVG(temp) AS avg_temp, AVG(storm) AS storm_prob '
        'FROM mars_weather '
        'GROUP BY month '
        'ORDER BY month;'
    )
    rows = db.run_query(query)
    print('[월별 평균 기온 및 폭풍 확률]')
    for row in rows:
        print('월:', row[0], '| 평균 기온:', round(row[1], 2), '| 폭풍 확률:', round(row[2], 1), '%')


def show_data_around_date(db):
    target = input('날짜를 입력하세요 (예: 2025-01-15): ').strip()
    query = (
        'SELECT mars_date, temp, storm '
        'FROM mars_weather '
        'WHERE mars_date BETWEEN DATE_SUB(%s, INTERVAL 5 DAY) '
        'AND DATE_ADD(%s, INTERVAL 5 DAY) '
        'ORDER BY mars_date;'
    )
    rows = db.run_query(query, (target, target))
    print('[입력 날짜 ±5일의 데이터]')
    print('날짜              | 기온 (°C) | 폭풍 확률 (%)')
    print('------------------|-----------|----------------')
    for row in rows:
        date_str = str(row[0].date())
        temp_str = str(int(row[1])) if row[1] is not None else 'N/A'
        storm_str = str(int(row[2])) if row[2] is not None else 'N/A'
        print(f'{date_str:^18} | {temp_str:^10}°C | {storm_str:^14}%')


def show_menu():
    print('\n[메뉴]')
    print('1. 폭풍 확률 70% 이상의 데이터')
    print('2. 월별 평균 데이터')
    print('3. 특정 날짜의 ±5일 데이터')
    print('0. 종료')


def main():
    db = MySQLHelper()
    while True:
        show_menu()
        choice = input('번호를 선택하세요: ').strip()

        if choice == '1':
            show_storm_over_70(db)
        elif choice == '2':
            show_monthly_average(db)
        elif choice == '3':
            show_data_around_date(db)
        elif choice == '0':
            print('종료합니다.')
            break
        else:
            print('잘못된 입력입니다. 다시 선택해주세요.')
    db.close()


if __name__ == '__main__':
    main()