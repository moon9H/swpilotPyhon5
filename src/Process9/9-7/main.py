# 과정 9 - (문제7) 맛있는 토마토 찾기
import matplotlib.pyplot as plt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import mglearn
import matplotlib

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

def plot_scatter(x, y, title='산점도 시각화'):
    plt.figure(figsize=(8, 5))
    for label, marker, color in zip([0, 1], ['o', '^'], ['navy', 'orangered']):
        plt.scatter(
            x[y == label, 0], x[y == label, 1],
            marker=marker, color=color, label=f'클래스 {label}', edgecolor='black'
        )
    plt.xlabel('첫 번째 특성')
    plt.ylabel('두 번째 특성')
    plt.legend()
    plt.title(title)
    plt.tight_layout()
    plt.show()

def main():
    # 데이터 생성
    x, y = mglearn.datasets.make_forge()

    # 산점도 시각화
    plot_scatter(x, y, '훈련 데이터 산점도')

    # 데이터 분할
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, random_state=0
    )

    # KNN 학습 및 평가 (n_neighbors=3)
    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(x_train, y_train)
    accuracy = model.score(x_test, y_test)
    print('기본 모델 정확도 (n_neighbors=3):', accuracy)

    # [보너스 과제] n_neighbors = 1 ~ 9 변화에 따른 정확도
    print('\n[보너스 과제] n_neighbors 변화에 따른 테스트 정확도:')
    for k in range(1, 10):
        knn = KNeighborsClassifier(n_neighbors=k)
        knn.fit(x_train, y_train)
        acc = knn.score(x_test, y_test)
        print(f'n_neighbors = {k} → 정확도: {acc:.2f}')


if __name__ == '__main__':
    main()