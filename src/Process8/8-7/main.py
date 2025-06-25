# 과정 8 - (문제7) 색에도 성분이 있다.
import cv2
import os

class HsvAnalyzer:
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

    def convert_to_hsv(self):
        hsv_image = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        return hsv_image

    def split_and_show_hsv(self, hsv_image):
        h_channel, s_channel, v_channel = cv2.split(hsv_image)

        self.show_image('H Channel', h_channel)
        self.show_image('S Channel', s_channel)
        self.show_image('V Channel', v_channel)

    # [보너스 과제] - 채널 분리 기법
    def compare_with_bgr_split(self):
        b_channel, g_channel, r_channel = cv2.split(self.image)

        self.show_image('B Channel (BGR)', b_channel)
        self.show_image('G Channel (BGR)', g_channel)
        self.show_image('R Channel (BGR)', r_channel)

if __name__ == '__main__':
    image_path = 'src/Process8/8-1/images/5.png'

    if not os.path.exists(image_path):
        print(f'파일이 존재하지 않습니다: {image_path}')
    else:
        analyzer = HsvAnalyzer(image_path)

        # HSV 변환 및 분리 출력
        hsv_img = analyzer.convert_to_hsv()
        analyzer.split_and_show_hsv(hsv_img)

        # [보너스 과제] BGR 채널 분리 비교
        analyzer.compare_with_bgr_split()