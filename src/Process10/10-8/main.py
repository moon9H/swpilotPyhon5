# 과정 10 - (문제8) 집으로 가는 길
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
import joblib

def main():
    iris = load_iris()
    x = iris.data
    y = iris.target

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=0
    )

    model = KNeighborsClassifier(n_neighbors=3)
    model.fit(x_train, y_train)

    accuracy = model.score(x_test, y_test)
    print('테스트 정확도:', accuracy)

    joblib.dump(model, 'iris_model.pkl')


if __name__ == '__main__':
    main()