# 과정 3 - (문제7) "화성 정복"

import os
import mysql.connector
from datetime import datetime

class MySQLHelper:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'swpilot')
        )
        self.cursor = self.connection.cursor()

    def insert_plant(self, data):
        if not validate_input(data):
            print('유효하지 않은 입력입니다.')
            return

        query = (
            'INSERT INTO mars_plant '
            '(scientific_name, common_names, plant_classification, '
            'plant_characteristics, growth_conditions, growth_period, '
            'optimal_growing_environment, cultivation_method, created_at, updated_at) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        )

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        values = (
            data.get('scientific_name'),
            data.get('common_names'),
            data.get('plant_classification'),
            data.get('plant_characteristics'),
            data.get('growth_conditions'),
            data.get('growth_period'),
            data.get('optimal_growing_environment'),
            data.get('cultivation_method'),
            now,
            now
        )

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print('식물 정보가 성공적으로 추가되었습니다.')
        except Exception as e:
            print('삽입 중 오류 발생:', e)

    def close(self):
        self.cursor.close()
        self.connection.close()

# [보너스 과제] - 입력 데이터 유효성 검사 코드
def validate_input(data):
    if not data.get('scientific_name'):
        print('scientific_name은 필수 항목입니다.')
        return False
    if data.get('cultivation_method') not in ['soil', 'hydroponic']:
        print('cultivation_method는 "soil" 또는 "hydroponic"이어야 합니다.')
        return False
    return True

def main():
    # 예시 데이터 입력
    plant_data = {
        'scientific_name': 'Solanum lycopersicum',
        'common_names': 'Tomato, 토마토',
        'plant_classification': 'Solanaceae > Solanum > lycopersicum',
        'plant_characteristics': '1~3m, 일년생, 따뜻한 기후 선호',
        'growth_conditions': '22~28도, 습도 60~70%, 직사광 필요',
        'growth_period': '90일',
        'optimal_growing_environment': '햇볕이 잘 드는 토양',
        'cultivation_method': 'soil'
    }

    db = MySQLHelper()
    db.insert_plant(plant_data)
    db.close()

if __name__ == '__main__':
    main()