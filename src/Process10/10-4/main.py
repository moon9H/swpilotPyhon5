# 과정 10 - (문제4) 미생물 분류
import matplotlib.pyplot as plt
from sklearn.datasets import make_blobs
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
import matplotlib

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

def main():
    # 데이터 생성
    x, y = make_blobs(centers=4, random_state=8)
    y = y % 2

    # 시각화
    plt.figure(figsize=(8, 5))
    for label, marker, color in zip([0, 1], ['o', '^'], ['navy', 'orangered']):
        plt.scatter(
            x[y == label, 0], x[y == label, 1],
            marker=marker, color=color, edgecolor='black', label=f'클래스 {label}'
        )
    plt.xlabel('특성 0')
    plt.ylabel('특성 1')
    plt.legend()
    plt.tight_layout()
    plt.show()

    # 데이터 분할
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, random_state=0
    )

    # SVC 학습 및 평가 (C: -1, 0, 3 / gamma: -1 ~ 2)
    print('[SVC 실험]')
    for c in [-1, 0, 3]:
        for g in [-1, 0, 1, 2]:
            if c <= 0 or g < 0:
                continue  # SVC는 C > 0, gamma >= 0 필요
            model = SVC(C=c, gamma=g)
            model.fit(x_train, y_train)
            train_score = model.score(x_train, y_train)
            test_score = model.score(x_test, y_test)
            print(f'C={c}, gamma={g} → 훈련 정확도: {train_score:.2f}, 테스트 정확도: {test_score:.2f}')

    # [보너스 과제] MLPClassifier 사용
    print('\n[MLPClassifier 실험]')
    model = MLPClassifier(random_state=0, max_iter=1000)
    model.fit(x_train, y_train)
    train_score = model.score(x_train, y_train)
    test_score = model.score(x_test, y_test)
    print(f'MLP → 훈련 정확도: {train_score:.2f}, 테스트 정확도: {test_score:.2f}')


if __name__ == '__main__':
    main()