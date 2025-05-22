# 과정 3 - (문제9) "나만의 식물창고 2"

import os
import mysql.connector
from datetime import datetime

#[보너스 과제] - 전체 CRUD를 담당하는 기능들을 하나의 클래스로 작성
class MarsPlantManager:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'swpilot')
        )
        self.cursor = self.connection.cursor()

    def list_plants(self):
        self.cursor.execute(
            'SELECT plant_id, scientific_name, cultivation_method FROM mars_plant ORDER BY plant_id')
        rows = self.cursor.fetchall()
        print('\n[식물 목록]')
        print('-' * 80)
        print(f"{'ID':<4} | {'학명':<35} | {'재배 방식':<15}")
        print('-' * 80)
        for row in rows:
            print(f'{row[0]:<4} | {row[1]:<35} | {row[2]:<15}')
        print('-' * 80)

    def search_plants(self, keyword):
        query = (
            'SELECT plant_id, scientific_name, common_names, cultivation_method FROM mars_plant '
            'WHERE scientific_name LIKE %s OR common_names LIKE %s '
            'ORDER BY plant_id'
        )
        self.cursor.execute(query, (f'%{keyword}%', f'%{keyword}%'))
        rows = self.cursor.fetchall()

        if not rows:
            print('\n[검색 결과 없음]')
            return

        print('\n[검색 결과]')
        print('-' * 120)
        print(f"{'ID':<4} | {'학명':<35} | {'일반 이름':<35} | {'재배 방식':<15}")
        print('-' * 120)
        for row in rows:
            print(f'{row[0]:<4} | {row[1]:<35} | {row[2]:<35} | {row[3]:<15}')
        print('-' * 120)

        while True:
            action = input('\n[M] 수정  [D] 삭제  [B] 돌아가기: ').strip().lower()
            if action == 'm':
                self.modify_plant()
                break
            elif action == 'd':
                self.delete_plant()
                break
            elif action == 'b':
                break
            else:
                print('잘못된 입력')

    def modify_plant(self):
        plant_id = input('\n수정할 식물의 ID를 입력 : ').strip()
        self.cursor.execute('SELECT * FROM mars_plant WHERE plant_id = %s', (plant_id,))
        row = self.cursor.fetchone()

        if not row:
            print('존재하지 않는 ID')
            return

        column_names = [desc[0] for desc in self.cursor.description]
        updated_data = {}
        print('\n[수정 대상 데이터 확인]')
        for idx, col in enumerate(column_names[1:-2], start=1):  # exclude ID, created/updated_at
            print(f'{col}: {row[idx]}')
            if input(f'{col} → 수정하시겠습니까? (y/n): ').strip().lower() == 'y':
                updated_data[col] = input(f'새로운 {col}: ').strip()

        if updated_data:
            set_clause = ', '.join([f"{key} = %s" for key in updated_data.keys()])
            values = list(updated_data.values()) + [plant_id]
            query = f'UPDATE mars_plant SET {set_clause}, updated_at = NOW() WHERE plant_id = %s'
            self.cursor.execute(query, values)
            self.connection.commit()
            print('\n수정 완료')
        else:
            print('\n변경된 내용이 없어 수정이 취소되었습니다.')

    def delete_plant(self):
        plant_id = input('\n삭제할 식물의 ID 입력 : ').strip()
        self.cursor.execute('SELECT scientific_name FROM mars_plant WHERE plant_id = %s', (plant_id,))
        row = self.cursor.fetchone()

        if not row:
            print('존재하지 않는 ID')
            return

        print(f'\n[{plant_id}] {row[0]} 식물을 삭제하시겠습니까?')
        confirm = input('삭제하려면 "y" 입력: ').strip().lower()
        if confirm == 'y':
            self.cursor.execute('DELETE FROM mars_plant WHERE plant_id = %s', (plant_id,))
            self.connection.commit()
            print('삭제 완료')
        else:
            print('삭제 취소')

    def close(self):
        self.cursor.close()
        self.connection.close()


def show_menu():
    print('\n[메뉴]')
    print('1. 식물 데이터 목록')
    print('2. 식물 데이터 검색')
    print('0. 종료')


def main():
    manager = MarsPlantManager()

    while True:
        show_menu()
        choice = input('번호 입력 : ').strip()

        if choice == '1':
            manager.list_plants()
        elif choice == '2':
            keyword = input('검색어를 입력 : ').strip()
            manager.search_plants(keyword)
        elif choice == '0':
            print('종료합니다.')
            break
        else:
            print(' 잘못된 입력 ')

    manager.close()


if __name__ == '__main__':
    main()