import csv
import os
import speech_recognition as sr
from pydub import AudioSegment

def get_files_list():
    if not os.path.exists(record_folder):
        print("녹음 폴더가 존재하지 않습니다.")
        return []

    files_list = []
    for file_name in os.listdir(record_folder):
        file_path = os.path.join(record_folder, file_name)
        print(file_name)
    
    return files_list

def IsExistFile(find_name) :
    for file_name in os.listdir(record_folder) :
        if file_name == find_name :
            return file_name
    return None

# 보너스 과제
def search_keyword_in_csv(csv_file_path, keyword):
    results = []
    if not os.path.exists(csv_file_path):
        print("CSV 파일이 존재하지 않습니다.")
        return results

    with open(csv_file_path, 'r', newline='', encoding='utf-8') as csvfile:
        csv_reader = csv.reader(csvfile)
        # 헤더를 건너뛰고 내용만 탐색
        next(csv_reader, None)
        for row in csv_reader:
            # 행의 텍스트 부분에서 키워드를 검색
            if keyword.lower() in row[1].lower():
                results.append((row[0], row[1]))

    return results

record_folder = "records"
if not os.path.exists(record_folder):
    os.mkdir(record_folder)

print('-- 녹음 음성파일 목록 --')
get_files_list()
STT_file = input('음성 인식할 파일을 입력하세요 (형식: YYYY-MM-DD HH:MM:SS): ')
STT_file += '.wav'

if IsExistFile(STT_file):
    # STT를 수행할 음성 파일의 경로
    audio_file_path = os.path.join(record_folder, STT_file)

    # 파일 이름에서 확장자를 제거하고 CSV 파일 이름을 생성
    csv_file_path = os.path.splitext(audio_file_path)[0] + '.csv'

    # SpeechRecognition을 사용하여 음성에서 텍스트를 추출
    recognizer = sr.Recognizer()

    # 음성 파일을 읽기
    with sr.AudioFile(audio_file_path) as source:
        audio_segment = AudioSegment.from_file(audio_file_path)
        duration = audio_segment.duration_seconds

        # 인식 구간을 5초로 설정
        segment_duration = 5  # 구간 길이
        num_segments = int(duration // segment_duration) + 1  # 구간 수

        # CSV에 기록
        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(["구간 시작 시간 (5초 단위)", "인식된 텍스트"])  # CSV 헤더 작성

            for i in range(num_segments):
                start_time = i * segment_duration
                offset = start_time  # 시작 시간
                with sr.AudioFile(audio_file_path) as source:
                    audio = recognizer.record(source, duration=segment_duration, offset=offset)

                try:
                    text = recognizer.recognize_google(audio, language='ko-KR')
                except sr.UnknownValueError:
                    text = "인식되지 않음"
                except sr.RequestError as e:
                    text = f"Google Speech Recognition API 에러: {e}"

                # CSV에 구간의 시작 시간과 인식된 텍스트 기록
                csv_writer.writerow([start_time, text])
    print(f"텍스트 인식 정보가 {csv_file_path}에 저장되었습니다.")
    
    #보너스 과제 키워드 입력받기
    keyword = input("해당 CSV 파일에서 찾을 키워드를 입력하세요: ")

    # CSV 파일에서 키워드를 검색하고 결과 출력
    results = search_keyword_in_csv(csv_file_path, keyword)

    if results:
        print(f"키워드 '{keyword}'가 포함된 결과:")
        for result in results:
            print(f"시간: {result[0]}s, 내용: {result[1]}")
    else:
        print(f"키워드 '{keyword}'가 포함된 내용이 없습니다.")

else:
    print('해당 파일이 존재하지 않습니다.')