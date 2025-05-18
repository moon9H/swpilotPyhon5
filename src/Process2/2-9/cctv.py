import os
import zipfile
from PIL import Image
import matplotlib.pyplot as plt

# 보너스 과제
class MasImageHelper:
    def __init__(self, zip_file, extract_folder):
        self.zip_file = zip_file
        self.extract_folder = extract_folder
        self.image_files = []
        self.current_image_index = 0
        
        # 압축 해제 및 이미지 파일 목록 생성
        self.extract_zip_file()
        self.create_image_list()

    def extract_zip_file(self):
        # 압축 해제 폴더가 없으면 생성
        if not os.path.exists(self.extract_folder):
            os.mkdir(self.extract_folder)
        
        # 압축 해제
        if os.path.exists(self.zip_file):
            with zipfile.ZipFile(self.zip_file, 'r') as zip_ref:
                zip_ref.extractall(self.extract_folder)

    def create_image_list(self):
        # 이미지 파일 목록 생성
        self.image_files = sorted(
            [f for f in os.listdir(self.extract_folder) if f.lower().endswith(('.png', '.jpg', '.jpeg'))]
        )

    def display_image(self, image_index=None):
        # 이미지 인덱스가 지정되지 않으면 현재 인덱스를 사용
        if image_index is None:
            image_index = self.current_image_index

        img_path = os.path.join(self.extract_folder, self.image_files[image_index])
        img = Image.open(img_path)
        plt.imshow(img)
        plt.title(f"CCTV {image_index + 1} of {len(self.image_files)}: {self.image_files[image_index]}")
        plt.axis('off')

    def on_key_event(self, event):
        # 키 이벤트 핸들러
        if event.key == 'right':
            if self.current_image_index < len(self.image_files) - 1:
                self.current_image_index += 1
            plt.clf()  # 그림을 지우고
            self.display_image(self.current_image_index)  # 새로운 그림을 표시
            plt.draw()  # 그래프를 다시 그립니다.
        elif event.key == 'left':
            if self.current_image_index > 0:
                self.current_image_index -= 1
            plt.clf()
            self.display_image(self.current_image_index)
            plt.draw()

    def start_image_display(self):
        # 이미지 표시 시작 및 이벤트 연결
        fig, ax = plt.subplots()
        self.display_image()
        fig.canvas.mpl_connect('key_press_event', self.on_key_event)  # 이벤트 연결
        plt.show()  # 그래프 표시

zip_file = 'CCTV.zip'
extract_folder = 'CCTV'

# MasImageHelper 클래스 생성
image_helper = MasImageHelper(zip_file, extract_folder)

# 이미지 표시 시작
image_helper.start_image_display()