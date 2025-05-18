import os
import cv2
import matplotlib.pyplot as plt

# 사진을 출력하는 함수
def show_image(image):
    plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    plt.axis("off")
    plt.show()

# 사진 목록을 가져오는 함수
def get_image_files_from_directory(directory):
    image_extensions = {".jpg", ".jpeg", ".png", ".bmp", ".tiff", ".tif", ".gif"}
    image_files = [f for f in os.listdir(directory) if os.path.splitext(f)[1].lower() in image_extensions]
    return sorted(image_files)

# 사람을 찾는 함수
def detect_people(image, cascade):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    people = cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(50, 50))
    print(people)
    return people

# 메인 프로그램
def main():
    image_directory = "CCTV"  # 이미지가 저장된 디렉토리
    cascade_path = "haarcascade_upperbody.xml"  # Haar Cascade 파일 경로
    
    # Haar Cascade 로드 확인
    cascade = cv2.CascadeClassifier(cascade_path)
    if cascade.empty():
        print("Haar Cascade를 로드할 수 없습니다. 경로를 확인하세요.")
        return
    
    # 이미지 목록 가져오기
    image_files = get_image_files_from_directory(image_directory)
    
    if not image_files:
        print("이미지 파일을 찾을 수 없습니다.")
        return

    for image_file in image_files:
        image_path = os.path.join(image_directory, image_file)
        image = cv2.imread(image_path)
        
        if image is None:
            print(f"이미지 파일을 읽을 수 없습니다: {image_file}")
            continue
        
        # 사람 찾기
        people = detect_people(image, cascade)
        
        #보너스 과제
        if len(people) > 0:
            for (x, y, w, h) in people:
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # 이미지를 화면에 출력
            show_image(image)

            input("다음 사진을 보려면 엔터를 누르세요.")
    
    print("검색이 끝났습니다.")

# 메인 함수 실행
if __name__ == "__main__":
    main()