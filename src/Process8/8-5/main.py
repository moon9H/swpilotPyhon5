# 과정 8 - (문제5) 공간을 바꾸고 뒤집으면 보이는 것들
import cv2
import os
import numpy as np
import matplotlib.pyplot as plt

class ImageInverter:
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

    def convert_to_gray(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.show_image('Grayscale Image', gray)
        return gray

    def invert_image(self):
        inverted = cv2.bitwise_not(self.image)
        self.show_image('Inverted Image', inverted)
        return inverted

    # [보너스 과제] - 히스토그램 출력
    def plot_histogram(self, image, title):
        if len(image.shape) == 3:
            # 컬러 이미지
            colors = ('b', 'g', 'r')
            for i, color in enumerate(colors):
                hist = cv2.calcHist([image], [i], None, [256], [0, 256])
                plt.plot(hist, color=color)
        else:
            # 흑백 이미지
            hist = cv2.calcHist([image], [0], None, [256], [0, 256])
            plt.plot(hist, color='gray')

        plt.title(title)
        plt.xlabel('Pixel Value')
        plt.ylabel('Frequency')
        plt.xlim([0, 256])
        plt.grid(True)
        plt.show()

if __name__ == '__main__':
    image_path = 'src/Process8/8-1/images/4.jpg'

    if not os.path.exists(image_path):
        print(f'파일이 존재하지 않습니다: {image_path}')
    else:
        inverter = ImageInverter(image_path)

        # 색상 전환: RGB → GRAY
        gray_image = inverter.convert_to_gray()

        # 역상 이미지
        inverted_image = inverter.invert_image()

        # [보너스 과제] - 히스토그램 출력
        inverter.plot_histogram(inverter.image, 'Original Image Histogram')     # 원본
        inverter.plot_histogram(inverted_image, 'Inverted Image Histogram')     # 역상