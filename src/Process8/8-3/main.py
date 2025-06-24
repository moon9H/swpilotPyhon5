# 과정 8 - (문제3) 사진들의 리터칭

import cv2
import os

class ImageTransformer:
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

    def show_original(self):
        self.show_image('Original Image', self.image)

    def flip_vertical(self):
        flipped = cv2.flip(self.image, 0)
        self.show_image('Vertical Flip', flipped)

    def flip_horizontal(self):
        flipped = cv2.flip(self.image, 1)
        self.show_image('Horizontal Flip', flipped)

    def rotate_90_clockwise(self):
        rotated = cv2.rotate(self.image, cv2.ROTATE_90_CLOCKWISE)
        self.show_image('Rotate 90 Degrees CW', rotated)

    def rotate_180(self):
        rotated = cv2.rotate(self.image, cv2.ROTATE_180)
        self.show_image('Rotate 180 Degrees', rotated)

    def upsample_image(self):
        # [보너스 과제] 이미지 크기를 2배로 업샘플링
        upsampled = cv2.resize(self.image, None, fx=2.0, fy=2.0, interpolation=cv2.INTER_LINEAR)
        self.show_image('Upsampled x2', upsampled)


if __name__ == '__main__':
    image_path = 'src/Process8/8-1/images/2.jpg'

    if not os.path.exists(image_path):
        print(f'파일이 존재하지 않습니다: {image_path}')
    else:
        transformer = ImageTransformer(image_path)
        transformer.show_original()
        transformer.flip_vertical()
        transformer.flip_horizontal()
        transformer.rotate_90_clockwise()
        transformer.rotate_180()
        transformer.upsample_image()