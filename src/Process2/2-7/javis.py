# 필요한 라이브러리 가져오기
import pyaudio
import wave
import os
import datetime
import threading  # 키보드 입력을 감지하기 위해 추가
import queue  # 쓰레드 간 통신을 위해 추가

# 녹음 기본 설정
FORMAT = pyaudio.paInt16  # 샘플 포맷
CHANNELS = 1              # 모노 녹음
RATE = 44100              # 샘플링 속도
CHUNK = 1024              # 샘플링 청크 사이즈

# 보너스 과제
# 파일 이름에서 날짜 정보를 추출하는 함수
def extract_datetime_from_filename(file_name):
    try:
        date_str = file_name.split(".wav")[0]
        return datetime.datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    except ValueError:
        return None

# 주어진 날짜 범위의 녹음 파일을 찾는 함수
def get_files_within_date_range(start_date, end_date):
    if not os.path.exists(record_folder):
        print("녹음 폴더가 존재하지 않습니다.")
        return []

    files_in_range = []
    for file_name in os.listdir(record_folder):
        file_path = os.path.join(record_folder, file_name)
        file_date = extract_datetime_from_filename(file_name)
        if file_date and start_date <= file_date <= end_date:
            files_in_range.append(file_path)
    
    return files_in_range

# 녹음 파일이 저장될 경로
record_folder = "records"
if not os.path.exists(record_folder):
    os.mkdir(record_folder)

print('어떤 기능을 사용하시겠습니까?')
menu = int(input('1. 녹음 2. 날짜로 녹음파일 조회하기\n'))

# 녹음 기능
if menu == 1 :
    # 녹음 파일 이름 생성 (현재 날짜와 시간 사용)
    now = datetime.datetime.now()
    file_name = now.strftime("%Y-%m-%d %H:%M:%S") + ".wav"  # 디렉토리 구조 문제 해결
    file_path = os.path.join(record_folder, file_name)

    # PyAudio를 통해 녹음을 시작합니다.
    audio = pyaudio.PyAudio()

    # 녹음 스트림 열기
    stream = audio.open(format=FORMAT,
                        channels=CHANNELS,
                        rate=RATE,
                        input=True,
                        frames_per_buffer=CHUNK)

    # 종료 신호를 전달하기 위한 큐 생성
    stop_signal = queue.Queue()

    # 키보드 입력을 감지하는 함수
    def listen_for_exit():
        input()
        stop_signal.put("STOP")  # 종료 신호를 큐에 넣습니다.

    # 입력 감지 쓰레드 시작
    listener_thread = threading.Thread(target=listen_for_exit)
    listener_thread.start()

    print("녹음을 시작합니다. 'Q' 입력이 올 때까지 녹음됩니다.")

    frames = []

    # 종료 신호가 올 때까지 녹음
    while stop_signal.empty():  # 큐가 비어 있으면 계속 녹음
        data = stream.read(CHUNK)
        frames.append(data)

    print("녹음이 완료되었습니다.")

    # 스트림 종료
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 녹음된 데이터로 WAV 파일 저장
    with wave.open(file_path, 'wb') as wf:
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(audio.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))

    print(f"녹음 파일이 '{file_path}'에 저장되었습니다.")

# 보너스 과제
elif menu == 2:
    # 사용자 입력으로 날짜 범위를 지정
    start_date_str = input("시작 날짜를 입력하세요 (형식: YYYY-MM-DD): ")
    end_date_str = input("끝 날짜를 입력하세요 (형식: YYYY-MM-DD): ")

    try:
        start_date = datetime.datetime.strptime(start_date_str, "%Y-%m-%d")
        end_date = datetime.datetime.strptime(end_date_str, "%Y-%m-%d") + datetime.timedelta(days=1, seconds=-1)
    except ValueError:
        print("날짜 형식이 올바르지 않습니다.")
        exit(1)

    # 날짜 범위의 녹음 파일 가져오기
    files = get_files_within_date_range(start_date, end_date)

    # 결과 출력
    if files:
        print("지정된 날짜 범위의 녹음 파일 목록:")
        for file_path in files:
            print(file_path)
    else:
        print("지정된 날짜 범위에 해당하는 녹음 파일이 없습니다.")