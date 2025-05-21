# 과정 3 - (문제8) "나만의 식물창고 1"

import os
import math
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

    def count_plants(self):
        self.cursor.execute('SELECT COUNT(*) FROM mars_plant')
        return self.cursor.fetchone()[0]

    def get_plants_by_page(self, offset, limit):
        query = (
            'SELECT plant_id, scientific_name, cultivation_method '
            'FROM mars_plant '
            'ORDER BY plant_id ASC '
            'LIMIT %s OFFSET %s'
        )
        self.cursor.execute(query, (limit, offset))
        return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.connection.close()


def show_plant_list(db):
    limit = 10
    total_count = db.count_plants()
    total_pages = math.ceil(total_count / limit)
    current_page = 1

    while True:
        offset = (current_page - 1) * limit
        rows = db.get_plants_by_page(offset, limit)

        print('\n[식물 데이터 목록]')
        print('ID | 학명                           | 재배 방식')
        print('---|-------------------------------|-----------')
        for row in rows:
            print(f'{row[0]:<3}| {row[1]:<30}| {row[2]}')

        print(f'\n[페이지] {current_page} / {total_pages}')
        print('[이전(P)] [다음(N)] [돌아가기(B)]')

        choice = input('선택: ').strip().lower()

        # [보너스 과제] 현제 페이지 아래에 출력
        if choice == 'n' and current_page < total_pages:
            current_page += 1
        elif choice == 'p' and current_page > 1:
            current_page -= 1
        elif choice == 'b':
            break
        else:
            print('잘못된 입력')


def show_menu():
    print('\n[메뉴]')
    print('1. 식물 데이터 목록')
    print('0. 종료')


def main():
    db = MySQLHelper()
    while True:
        show_menu()
        choice = input('번호를 선택하세요: ').strip()

        if choice == '1':
            show_plant_list(db)
        elif choice == '0':
            print('종료합니다.')
            break
        else:
            print('잘못된 입력입니다.')
    db.close()


if __name__ == '__main__':
    main()