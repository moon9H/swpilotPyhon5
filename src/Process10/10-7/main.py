# 과정 10 - (문제7) 교차 검증
from sklearn.datasets import load_iris
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score, train_test_split

def main():
    # 데이터 로드
    iris = load_iris()
    x = iris.data
    y = iris.target

    # 로지스틱 회귀 모델
    model = LogisticRegression(max_iter=1000)

    # 교차 검증 (기본 3-Fold)
    scores_3 = cross_val_score(model, x, y, cv=3)
    print('3-Fold 교차 검증 결과:', scores_3)
    print('3-Fold 평균 정확도:', scores_3.mean())

    # 교차 검증 (5-Fold)
    scores_5 = cross_val_score(model, x, y, cv=5)
    print('\n5-Fold 교차 검증 결과:', scores_5)
    print('5-Fold 평균 정확도:', scores_5.mean())

    # [보너스 과제] train_test_split과 비교
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=0
    )
    model.fit(x_train, y_train)
    score_split = model.score(x_test, y_test)
    print('\ntrain_test_split 테스트 정확도:', score_split)


if __name__ == '__main__':
    main()