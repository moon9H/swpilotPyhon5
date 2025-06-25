# 과정 8 - (문제8) 도형 그리기
import cv2
import os
import numpy as np

class ObjectAnnotator:
    def __init__(self, file_path):
        self.file_path = file_path
        self.image = cv2.imread(file_path)

        if self.image is None:
            print(f'이미지를 불러올 수 없습니다: {file_path}')
            exit(1)

        # 사전 정의된 객체 위치와 유형 (예제용)
        self.objects = [
            {'name': 'Box', 'type': 'box', 'pos': (100, 100, 100, 100)},   # (x, y, w, h)
            {'name': 'Ball', 'type': 'ball', 'pos': (250, 120, 80, 80)},
            {'name': 'Cone', 'type': 'cone', 'pos': (400, 130, 100, 100)},
        ]

    def annotate_objects(self):
        for obj in self.objects:
            name = obj['name']
            shape_type = obj['type']
            x, y, w, h = obj['pos']

            center_x = x + w // 2
            center_y = y + h // 2

            # [보너스 과제] - 도형 그리기 (빨간색, 물품 종류에 따라 다른 모양으로 구분)
            color = (0, 0, 255)
            thickness = 2

            if shape_type == 'box':
                cv2.rectangle(self.image, (x, y), (x + w, y + h), color, thickness)

            elif shape_type == 'ball':
                radius = min(w, h) // 2
                cv2.circle(self.image, (center_x, center_y), radius, color, thickness)

            elif shape_type == 'cone':
                point1 = (x + w // 2, y)
                point2 = (x, y + h)
                point3 = (x + w, y + h)
                triangle = np.array([point1, point2, point3])
                cv2.polylines(self.image, [triangle], isClosed=True, color=color, thickness=thickness)

            # 텍스트 위치 및 연결선
            text_x = x + w + 40
            text_y = y + 20
            cv2.putText(self.image, name, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

            line_start = (center_x, center_y)
            line_end = (text_x, text_y)
            cv2.line(self.image, line_start, line_end, color, 1)

    def show_result(self):
        cv2.imshow('Annotated Image', self.image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

if __name__ == '__main__':
    image_path = 'src/Process8/8-1/images/6.jpg'

    if not os.path.exists(image_path):
        print(f'파일이 존재하지 않습니다: {image_path}')
    else:
        annotator = ObjectAnnotator(image_path)
        annotator.annotate_objects()
        annotator.show_result()