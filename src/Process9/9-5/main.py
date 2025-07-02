# 과정 9 - (문제5) 차원의 저주를 풀어라
from sklearn.datasets import load_digits
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
import numpy as np

def main():
    # 데이터셋 불러오기
    digits = load_digits()

    # DESCR 항목 출력
    print('DESCR:')
    print(digits['DESCR'])

    # data, label 추출
    data = digits['data']
    label = digits['target']

    print('\nData shape:', data.shape)
    print('Label shape:', label.shape)

    # 첫 번째 샘플을 8x8 행렬로 변환하여 시각 확인
    first_image = data[0].reshape((8, 8))

    plt.figure(figsize=(3, 3))
    plt.imshow(first_image, cmap='gray')
    plt.title(f'Digit: {label[0]}')
    plt.axis('off')
    plt.tight_layout()
    plt.show()

    # PCA를 통한 2차원 축소
    pca = PCA(n_components=2)
    data_pca = pca.fit_transform(data)

    print('\nPCA 결과 shape:', data_pca.shape)

    # [보너스 과제] 2차원 시각화
    plt.figure(figsize=(8, 6))
    for digit in np.unique(label):
        idx = label == digit
        plt.scatter(data_pca[idx, 0], data_pca[idx, 1], label=str(digit), alpha=0.7)

    plt.title('Digits PCA (2D)')
    plt.xlabel('Principal Component 1')
    plt.ylabel('Principal Component 2')
    plt.legend(title='Digit')
    plt.grid(False)  # 격자 제거
    plt.tight_layout()
    plt.show()

if __name__ == '__main__':
    main()