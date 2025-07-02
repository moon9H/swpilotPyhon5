# 과정 9 - (문제8) 진짜 맛있는 토마토 찾기
import matplotlib.pyplot as plt
from mglearn.datasets import make_forge
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import mglearn
import numpy as np
import matplotlib

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

def plot_decision_boundary(model, x, y, title):
    mglearn.plots.plot_2d_separator(model, x, fill=True, alpha=0.4)
    mglearn.discrete_scatter(x[:, 0], x[:, 1], y)
    plt.title(title)
    plt.xlabel('첫 번째 특성')
    plt.ylabel('두 번째 특성')
    plt.tight_layout()
    plt.show()

def main():
    # 데이터 생성 및 분리
    x, y = mglearn.datasets.make_forge()
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, random_state=0
    )

    training_accuracy = []
    test_accuracy = []
    neighbor_settings = range(1, 11)

    for n_neighbors in neighbor_settings:
        model = KNeighborsClassifier(n_neighbors=n_neighbors)
        model.fit(x_train, y_train)
        train_acc = model.score(x_train, y_train)
        test_acc = model.score(x_test, y_test)
        training_accuracy.append(train_acc)
        test_accuracy.append(test_acc)

    # 꺾은선 그래프 출력
    plt.figure(figsize=(8, 5))
    plt.plot(neighbor_settings, training_accuracy, label='훈련 정확도')
    plt.plot(neighbor_settings, test_accuracy, label='테스트 정확도')
    plt.xlabel('n_neighbors')
    plt.ylabel('정확도 (accuracy)')
    plt.title('KNN 정확도 비교')
    plt.legend()
    plt.ylim(0.5, 1)
    plt.tight_layout()
    plt.grid(False)
    plt.show()

    # [보너스 과제] 결정 경계 시각화 (n = 1, 3, 9)
    for k in [1, 3, 9]:
        model = KNeighborsClassifier(n_neighbors=k)
        model.fit(x, y)
        plot_decision_boundary(model, x, y, f'결정 경계 (n_neighbors = {k})')

if __name__ == '__main__':
    main()