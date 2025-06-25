# 과정 8 - (문제6) 마음이 아려오는 이미지들...
import cv2
import os

class EdgeAndBlurProcessor:
    def __init__(self, binary_image_path, blur_image_path):
        self.binary_image_path = binary_image_path
        self.blur_image_path = blur_image_path

        self.image = cv2.imread(binary_image_path)
        self.blur_image = cv2.imread(blur_image_path)

        if self.image is None:
            print(f'이진화용 이미지를 불러올 수 없습니다: {binary_image_path}')
            exit(1)

        if self.blur_image is None:
            print(f'흐림 효과용 이미지를 불러올 수 없습니다: {blur_image_path}')
            exit(1)

    def show_image(self, title, image):
        cv2.imshow(title, image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    def convert_to_gray(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
        self.show_image('Grayscale', gray)
        return gray

    def binary_threshold(self, gray_image):
        _, binary = cv2.threshold(gray_image, 127, 255, cv2.THRESH_BINARY)
        self.show_image('Binary Image', binary)

    def detect_edges(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

        # Sobel (x + y 방향)
        sobelx = cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3)
        sobely = cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)
        sobel = cv2.magnitude(sobelx, sobely)
        sobel = cv2.convertScaleAbs(sobel)
        self.show_image('Sobel Edge', sobel)

        # Laplacian
        laplacian = cv2.Laplacian(gray, cv2.CV_64F)
        laplacian = cv2.convertScaleAbs(laplacian)
        self.show_image('Laplacian Edge', laplacian)

        # Canny
        canny = cv2.Canny(gray, 100, 200)
        self.show_image('Canny Edge', canny)

    def apply_blur(self):
        blurred = cv2.GaussianBlur(self.blur_image, (15, 15), 0)
        self.show_image('Blurred Image', blurred)

    def blur_region_only(self):
        # [보너스 과제] 이미지의 일부분만 흐림 적용 (중앙 사각형)
        result = self.blur_image.copy()

        h, w = result.shape[:2]
        x1 = w // 3
        y1 = h // 3
        x2 = x1 + w // 3
        y2 = y1 + h // 3

        roi = result[y1:y2, x1:x2]
        blurred_roi = cv2.GaussianBlur(roi, (31, 31), 0)
        result[y1:y2, x1:x2] = blurred_roi

        self.show_image('Partial Blur (보너스)', result)

if __name__ == '__main__':
    bin_img_path = 'src/Process8/8-1/images/4.jpg'
    blur_img_path = 'src/Process8/8-1/images/4.jpg'

    if not os.path.exists(bin_img_path) or not os.path.exists(blur_img_path):
        print('필요한 이미지 파일이 존재하지 않습니다.')
    else:
        processor = EdgeAndBlurProcessor(bin_img_path, blur_img_path)

        # 그레이스케일 → 이진화
        gray_img = processor.convert_to_gray()
        processor.binary_threshold(gray_img)

        # 가장자리 검출
        processor.detect_edges()

        # 흐림 효과 전체
        processor.apply_blur()

        # [보너스] 특정 영역만 흐림
        processor.blur_region_only()