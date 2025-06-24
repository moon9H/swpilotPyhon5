# 과정 8 - (문제1) 여러개의 눈

import cv2
import os

class MediaViewer:
    def __init__(self):
        self.image_folder = 'src/Process8/8-1/images'
        self.video_folder = 'src/Process8/8-1/videos'

    def show_camera(self):
        cap = cv2.VideoCapture(0)

        # 해상도 설정
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

        if not cap.isOpened():
            print('카메라를 열 수 없습니다.')
            return

        while True:
            ret, frame = cap.read()
            if not ret:
                print('프레임을 읽을 수 없습니다.')
                break

            cv2.imshow('Camera Output', frame)

            if cv2.waitKey(33) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def show_images(self):
        if not os.path.isdir(self.image_folder):
            print(f'이미지 폴더가 존재하지 않습니다: {self.image_folder}')
            return

        for file_name in os.listdir(self.image_folder):
            if not file_name.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.tif', '.tiff')):
                continue

            file_path = os.path.join(self.image_folder, file_name)
            image = cv2.imread(file_path)

            if image is None:
                print(f'이미지를 열 수 없습니다: {file_path}')
                continue

            cv2.imshow('Image Viewer', image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()

    # [보너스 과제] mp4 영상 출력
    def show_videos(self):
        if not os.path.isdir(self.video_folder):
            print(f'비디오 폴더가 존재하지 않습니다: {self.video_folder}')
            return

        for file_name in os.listdir(self.video_folder):
            if not file_name.lower().endswith('.mp4'):
                continue

            file_path = os.path.join(self.video_folder, file_name)
            cap = cv2.VideoCapture(file_path)

            if not cap.isOpened():
                print(f'비디오를 열 수 없습니다: {file_path}')
                continue

            while True:
                ret, frame = cap.read()
                if not ret:
                    break

                cv2.imshow('Video Viewer', frame)

                if cv2.waitKey(33) & 0xFF == ord('q'):
                    break

            cap.release()
            cv2.destroyAllWindows()

if __name__ == '__main__':
    viewer = MediaViewer()

    print('1. 카메라 출력')
    viewer.show_camera()

    print('2. 이미지 출력')
    viewer.show_images()

    # [보너스 과제] mp4 영상 출력
    print('3. [보너스] 비디오 출력')
    viewer.show_videos()