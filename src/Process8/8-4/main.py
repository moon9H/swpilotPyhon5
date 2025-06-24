# 과정 8 - (문제4) 이미지의 크기를 바꾸면 다시 보이는 것들
import cv2
import os
import copy

class ImageProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.image = cv2.imread(file_path)

        if self.image is None:
            print(f'이미지를 불러올 수 없습니다: {file_path}')
            exit(1)

    def show_image(self, title, image):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def resize_absolute(self, width, height):
        resized = cv2.resize(self.image, (width, height))
        self.show_image(f'Resized to {width}x{height}', resized)

    def resize_relative(self, fx, fy):
        resized = cv2.resize(self.image, None, fx=fx, fy=fy, interpolation=cv2.INTER_LINEAR)
        self.show_image(f'Scaled by fx={fx}, fy={fy}', resized)

    def crop_region(self, x, y, w, h):
        region = self.image[y:y+h, x:x+w]
        copied = copy.deepcopy(region)  # deep copy
        self.show_image('Cropped Region (Deep Copy)', copied)

    # [보너스 과제] 얼굴 개별 추출
    def detect_and_crop_faces(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

        print(f'감지된 얼굴 수: {len(faces)}')

        for idx, (x, y, w, h) in enumerate(faces):
            face = self.image[y:y+h, x:x+w]
            copied_face = copy.deepcopy(face)
            self.show_image(f'Face #{idx + 1}', copied_face)

if __name__ == '__main__':
    image_path = 'src/Process8/8-1/images/5.png'

    if not os.path.exists(image_path):
        print(f'파일이 존재하지 않습니다: {image_path}')
    else:
        processor = ImageProcessor(image_path)

        # 절대 크기로 리사이즈
        processor.resize_absolute(640, 480)
        processor.resize_absolute(1024, 768)

        # 상대 크기로 리사이즈
        processor.resize_relative(fx=0.3, fy=0.7)

        # 특정 영역 잘라내기 (예: 이미지 좌상단 200x200 크기)
        processor.crop_region(50, 50, 200, 200)

        # [보너스 과제] 얼굴 개별 추출
        processor.detect_and_crop_faces()