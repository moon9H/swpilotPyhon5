# 과정 4 - (문제3) "스마트 팜의 시작"

import threading
import time
import random
from datetime import datetime
import pandas as pd

# 데이터 저장용 리스트
sensor_log = []

# 출력 꼬임 방지 lock
print_lock = threading.Lock()

# 스마트팜 센서 클래스
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

# 센서 작동 쓰레드
def sensor_thread(sensor):
    while True:
        sensor.set_data()
        temp, light, humi = sensor.get_data()
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log = {
            'timestamp': timestamp,
            'sensor': sensor.name,
            'temperature': temp,
            'light': light,
            'humidity': humi
        }
        sensor_log.append(log)
        with print_lock:
            print(f'{timestamp} {sensor.name} — temp {temp}, light {light}, humi {humi}')
        time.sleep(10)

def average_logger():
    while True:
        time.sleep(300)
        if not sensor_log:
            with print_lock:
                print('\n[5분 단위 평균] 데이터 없음\n')
            continue

        df = pd.DataFrame(sensor_log)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        df.set_index('timestamp', inplace=True)

        numeric_cols = ['temperature', 'light', 'humidity']
        resampled = df[numeric_cols].resample('5min').mean().round(2)

        if resampled.empty:
            with print_lock:
                print('\n[5분 단위 평균] 유효한 데이터 없음\n')
            continue

        latest = resampled.tail(1).iloc[0]
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        with print_lock:
            print(f'\n[누적 데이터의 5분 단위 평균 - {current_time} 기준]')
            print('온도'.rjust(6), '조도'.rjust(10), '습도'.rjust(6))
            print('-' * 30)
            print(f'{latest["temperature"]:>6} {latest["light"]:>10} {latest["humidity"]:>6}')

def main():
    sensors = [ParmSensor(f'Parm-{i}') for i in range(1, 6)]

    for sensor in sensors:
        t = threading.Thread(target=sensor_thread, args=(sensor,))
        t.daemon = True
        t.start()

    avg_thread = threading.Thread(target=average_logger)
    avg_thread.daemon = True
    avg_thread.start()

    # 메인 쓰레드 대기
    while True:
        time.sleep(1)

if __name__ == '__main__':
    main()