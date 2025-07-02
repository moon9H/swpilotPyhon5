# 과정 9 - (문제2) 컴퓨터에게 학습을 시켜보자
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

def main():
    # iris 데이터셋 로드
    iris = load_iris()
    data = iris['data']
    target = iris['target']

    # train/test 데이터 분할
    x_train, x_test, y_train, y_test = train_test_split(
        data, target, test_size=0.25, random_state=42
    )

    # 분할된 데이터 정보 출력
    print('X_train shape:', x_train.shape)
    print('X_test shape:', x_test.shape)
    print('y_train shape:', y_train.shape)
    print('y_test shape:', y_test.shape)

    # 모델 학습 (KNN, 이웃 수 = 1)
    model = KNeighborsClassifier(n_neighbors=1)
    model.fit(x_train, y_train)

    # 새로운 데이터 예측
    sample = [[5, 2.9, 1, 0.2]]
    prediction = model.predict(sample)
    print('\nPrediction for sample [5, 2.9, 1, 0.2]:', prediction)
    print('Predicted target name:', iris['target_names'][prediction[0]])

    # [보너스 과제] 모델 평가
    train_score = model.score(x_train, y_train)
    test_score = model.score(x_test, y_test)
    print('\n[보너스 과제] Accuracy')
    print('Training accuracy:', train_score)
    print('Test accuracy:', test_score)


if __name__ == '__main__':
    main()