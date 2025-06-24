# 과정 8 - (문제2) 클립과 사진을 모아보자

import cv2
import os
from datetime import datetime


class VideoPlayer:
    def __init__(self, file_path):
        self.file_path = file_path
        self.capture = cv2.VideoCapture(file_path)
        self.writer = None
        self.recording = False
        self.codec_index = 0  # [보너스 과제] 코덱 전환용
        self.codec_list = ['XVID', 'mp4v']  # [보너스 과제] 두 가지 코덱 사용

        if not self.capture.isOpened():
            print('비디오 파일을 열 수 없습니다.')
            exit(1)

        self.frame_width = int(self.capture.get(cv2.CAP_PROP_FRAME_WIDTH))
        self.frame_height = int(self.capture.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.fps = int(self.capture.get(cv2.CAP_PROP_FPS))

        if self.fps == 0:
            self.fps = 30  # fallback

    def get_filename(self, ext):
        now = datetime.now()
        timestamp = now.strftime('%Y_%m_%d-%H-%M-%S')
        return f'{timestamp}.{ext}'

    def start_recording(self):
        file_name = self.get_filename('mp4')
        fourcc = cv2.VideoWriter_fourcc(*self.codec_list[self.codec_index])
        self.writer = cv2.VideoWriter('src/Process8/8-2/videos/'+file_name, fourcc, self.fps,
                                      (self.frame_width, self.frame_height))
        self.recording = True
        print(f'녹화 시작: {file_name} (코덱: {self.codec_list[self.codec_index]})')

    def stop_recording(self):
        if self.writer:
            self.writer.release()
            self.writer = None
            print('녹화 중지')
        self.recording = False

    def capture_image(self, frame):
        file_name = self.get_filename('jpg')
        cv2.imwrite('src/Process8/8-2/images/' + file_name, frame)
        print(f'이미지 캡처 완료: {file_name}')

    def play(self):
        print('영상 재생을 시작합니다.')
        print('ESC: 종료, Ctrl+Z: 캡처, Ctrl+X: 녹화 시작, Ctrl+C: 녹화 중지')

        while True:
            ret, frame = self.capture.read()
            if not ret:
                break

            cv2.imshow('Video Player', frame)

            key = cv2.waitKey(33) & 0xFF

            # ESC 키
            if key == 27:
                break

            # Ctrl+Z: 26 (0x1A)
            elif key == 26:
                self.capture_image(frame)

            # Ctrl+X: 24 (0x18)
            elif key == 24:
                if not self.recording:
                    self.start_recording()

            # Ctrl+C: 3 (0x03)
            elif key == 3:
                if self.recording:
                    self.stop_recording()

            if self.recording and self.writer:
                self.writer.write(frame)

        self.capture.release()
        if self.writer:
            self.writer.release()
        cv2.destroyAllWindows()


if __name__ == '__main__':
    video_path = 'src/Process8/8-1/videos/1.mp4'

    if not os.path.exists(video_path):
        print(f'파일이 존재하지 않습니다: {video_path}')
    else:
        player = VideoPlayer(video_path)
        player.play()