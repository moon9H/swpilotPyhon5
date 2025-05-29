# 과정 4 - (문제5) "중간 지점으로 큐를 사용해 볼까?"

import threading
import random
import time
from datetime import datetime
from queue import Queue
import os
import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
import matplotlib

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

print_lock = threading.Lock()

class ParmSensor:
    def __init__(self, name):
        self.name = name

    def set_data(self):
        return {
            'sensor_name': self.name,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'temperature': random.randint(20, 30),
            'light': random.randint(5000, 10000),
            'humidity': random.randint(40, 90)
        }

def insert_sensor_data(data):
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
    cursor.execute(query, (
        data['sensor_name'],
        data['timestamp'],
        data['temperature'],
        data['light'],
        data['humidity']
    ))
    conn.commit()
    cursor.close()
    conn.close()

def sensor_thread(sensor, queue):
    while True:
        data = sensor.set_data()
        with print_lock:
            print(f"{data['timestamp']} {data['sensor_name']} — temp {data['temperature']}, light {data['light']}, humi {data['humidity']}")
            queue.put(data)
        
        time.sleep(10)

def db_writer_thread(queue):
    while True:
        if not queue.empty():
            with print_lock:
                data = queue.get()
                insert_sensor_data(data)
        time.sleep(1)

def get_sensor_data():
    conn = mysql.connector.connect(
        host=os.getenv('MYSQL_HOST', 'localhost'),
        user=os.getenv('MYSQL_USER', 'root'),
        password=os.getenv('MYSQL_PASSWORD', ''),
        database=os.getenv('MYSQL_DATABASE', 'swpilot')
    )
    # 최근 10분 필터링
    query = '''
        SELECT * FROM parm_data
        WHERE timestamp >= NOW() - INTERVAL 10 MINUTE
    '''
    
    df = pd.read_sql(query, con=conn)
    conn.close()
    return df

def visualize_timeblock_averages_from_df(df):
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    numeric_df = df[['temperature', 'light', 'humidity']]

    avg_df = numeric_df.resample('20s').mean().round(2).reset_index()

    avg_df['time_label'] = avg_df['timestamp'].dt.strftime('%H:%M:%S')

    metrics = {
        'temperature': '평균 온도',
        'light': '평균 조도',
        'humidity': '평균 습도'
    }

    for col, label in metrics.items():
        plt.figure(figsize=(10, 5))
        # [보너스 과제] - # 습도 90% 이상은 빨간색, 그 외는 파란색
        if col == 'humidity':
            colors = ['red' if val > 90 else 'skyblue' for val in avg_df[col]]
        else:
            colors = 'skyblue'
        plt.bar(avg_df['time_label'], avg_df[col], width=0.6, align='center',color=colors)
        plt.title(f'{label} (최근 10분, 30초 단위 평균)', fontsize=14)
        plt.xlabel('시간대')
        plt.ylabel(label)
        plt.xticks(rotation=45)
        plt.grid(True, axis='y')
        plt.tight_layout()
        plt.show()

def main():
    # 큐 및 센서 초기화
    sensor_q = Queue()
    sensors = [ParmSensor(f'Parm-{i}') for i in range(1, 6)]

    # 센서 데이터 생성 쓰레드 시작
    for s in sensors:
        threading.Thread(target=sensor_thread, args=(s, sensor_q), daemon=True).start()

    # DB 저장 쓰레드 시작
    threading.Thread(target=db_writer_thread, args=(sensor_q,), daemon=True).start()

    # 메인 루프 유지 + 주기적으로 시각화 호출 (예: 60초마다)
    try:
        while True:
            time.sleep(60)
            df = get_sensor_data()
            visualize_timeblock_averages_from_df(df)
    except KeyboardInterrupt:
        print('\n[종료] 사용자가 프로그램을 중단했습니다.')

if __name__ == '__main__':
    main()