# 과정 3 - (문제5) "내일 날씨는 맑음"

import os
import mysql.connector

class MySQLHelper:
    def __init__(self):
        # [보너스 과제] - 환경변수를 이용할 수 있게 수정
        self.connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'swpilot')
        )
        self.cursor = self.connection.cursor()

    def insert_weather(self, mars_date, temp, storm):
        query = (
            'INSERT INTO mars_weather (mars_date, temp, storm) '
            "VALUES ('%s', %s, %s);" % (mars_date, temp, storm)
        )
        self.cursor.execute(query)

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()


def read_csv(filepath):
    try:
        f = open(filepath, 'r', encoding='utf-8')
        lines = f.readlines()
        f.close()
    except Exception as e:
        print('오류 발생:', e)
        return []

    data = []
    for i in range(1, len(lines)):
        line = lines[i].strip()
        parts = line.split(',')

        mars_date = parts[1]
        temp = parts[2] if parts[2] != '' else 'NULL'
        storm = parts[3] if parts[3] != '' else 'NULL'
        data.append((mars_date, temp, storm))

    return data


def insert_all(data, db):
    for row in data:
        db.insert_weather(row[0], row[1], row[2])
    db.commit()


def main():
    db = MySQLHelper()

    data = read_csv('src/Process3/3-5/mars_weathers_data.csv')
    print(len(data), '개의 데이터')

    insert_all(data, db)
    print('데이터 삽입 완료.')

    db.close()

if __name__ == '__main__':
    main()