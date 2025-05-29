# 과정 4 - (문제4) "스마트 팜 데이터의 저장과 활용"

import threading
import time
import random
from datetime import datetime
import mysql.connector
import os

sensor_log = []
print_lock = threading.Lock()

class ParmSensor:
    def __init__(self, name):
        self.name = name
        self.temperature = 0
        self.light = 0
        self.humidity = 0

    def set_data(self):
        self.temperature = random.randint(20, 30)
        self.light = random.randint(5000, 10000)
        self.humidity = random.randint(40, 70)

    def get_data(self):
        return self.temperature, self.light, self.humidity

def insert_sensor_data(sensor_name, temperature, light, humidity):
    try:
        conn = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'swpilot')
        )
        cursor = conn.cursor()
        query = '''
            INSERT INTO parm_data (sensor_name, timestamp, temperature, light, humidity)
            VALUES (%s, %s, %s, %s, %s)
        '''
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute(query, (sensor_name, now, temperature, light, humidity))
        conn.commit()
        cursor.close()
        conn.close()
    except Exception as e:
        with print_lock:
            print(f'[DB 오류] {sensor_name} → {e}')

def sensor_worker(sensor):
    while True:
        
        sensor.set_data()
        temp, light, humi = sensor.get_data()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with print_lock:
            print(f'{timestamp} {sensor.name} — temp {temp}, light {light}, humi {humi}')
            sensor_log.append({
                'sensor_name': sensor.name,
                'timestamp': timestamp,
                'temperature': temp,
                'light': light,
                'humidity': humi
            })
            insert_sensor_data(sensor.name, temp, light, humi)
        
        time.sleep(10)

def start_sensors():
    sensors = [ParmSensor(f'Parm-{i}') for i in range(1, 6)]
    for s in sensors:
        t = threading.Thread(target=sensor_worker, args=(s,))
        t.daemon = True
        t.start()

def main():
    start_sensors()
    while True:
        time.sleep(1)  # 메인 스레드 유지용

if __name__ == '__main__':
    main()