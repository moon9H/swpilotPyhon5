# 과정 10 - (문제2) 토마토의 출하량을 예측해 보자
import mglearn
from sklearn.linear_model import LinearRegression, Ridge
from sklearn.model_selection import train_test_split

def main():
    x, y = mglearn.datasets.make_wave(n_samples=60)

    x_train, x_test, y_train, y_test = train_test_split(
        x, y, random_state=42
    )

    model = LinearRegression()
    model.fit(x_train, y_train)

    print('\n----------선형 회귀 결과----------')
    print('가중치:', model.coef_)
    print('절편:', model.intercept_)
    print('훈련 세트 점수:', model.score(x_train, y_train))
    print('테스트 세트 점수:', model.score(x_test, y_test))

    # [보너스 과제] - Ridge 알고리즘 사용
    print('\n----------릿지 회귀 결과----------')
    for alpha in [i / 10 for i in range(1, 11)]:
        ridge = Ridge(alpha=alpha)
        ridge.fit(x_train, y_train)
        print(f'alpha = {alpha:.1f}')
        print('  가중치:', ridge.coef_)
        print('  절편:', ridge.intercept_)
        print('  훈련 세트 점수:', ridge.score(x_train, y_train))
        print('  테스트 세트 점수:', ridge.score(x_test, y_test))

if __name__ == '__main__':
    main()