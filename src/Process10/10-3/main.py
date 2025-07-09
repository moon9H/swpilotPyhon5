# 과정 10 - (문제3) 뜻밖의 발암물질들…
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import plot_tree
import matplotlib.pyplot as plt

def main():
    # 데이터 로드
    data = load_breast_cancer()
    x = data.data
    y = data.target

    # 데이터 분할
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, random_state=42
    )

    # 첫 번째 실험: 기본 DecisionTreeClassifier
    model1 = DecisionTreeClassifier()
    model1.fit(x_train, y_train)
    print('기본 모델 결과')
    print('훈련 정확도:', model1.score(x_train, y_train))
    print('테스트 정확도:', model1.score(x_test, y_test))

    # 두 번째 실험: max_depth=4, random_state=0 지정
    model2 = DecisionTreeClassifier(max_depth=4, random_state=0)
    model2.fit(x_train, y_train)
    print('\nmax_depth=4 모델 결과')
    print('훈련 정확도:', model2.score(x_train, y_train))
    print('테스트 정확도:', model2.score(x_test, y_test))

    # [보너스 과제] 결정 트리 시각화
    plt.figure(figsize=(20, 10))
    plot_tree(model2, filled=True,
              feature_names=data.feature_names,
              class_names=data.target_names)
    plt.tight_layout()
    plt.show()


if __name__ == '__main__':
    main()