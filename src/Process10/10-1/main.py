# 과정 10 - (문제1) 토마토의 작황을 알아보자
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np
import mglearn

def evaluate_model(model, x_test, y_test):
    y_pred = model.predict(x_test)
    r2 = model.score(x_test, y_test)
    mae = mean_absolute_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
    return r2, mae, rmse

def main():
    # 데이터 생성
    x, y = mglearn.datasets.make_wave(n_samples=40)

    # 학습/테스트 분할
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.25, random_state=0
    )

    # 결과 저장용
    results = {}

    # n_neighbors = 1, 3, 9 반복 학습 및 평가
    for k in [1, 3, 9]:
        model = KNeighborsRegressor(n_neighbors=k)
        model.fit(x_train, y_train)

        # [보너스 과제] - MAE, RMSE 값 확인
        r2, mae, rmse = evaluate_model(model, x_test, y_test)
        results[k] = {
            'r2': r2,
            'mae': mae,
            'rmse': rmse
        }

        print(f'\n[n_neighbors = {k}]')
        print(f'R² : {r2:.4f}')
        print(f'MAE: {mae:.4f}')
        print(f'RMSE: {rmse:.4f}')

    # [보너스 과제] - 가장 성능이 좋은 모델 찾기 (기준: R²가 가장 높고 RMSE가 가장 낮은 모델)
    best_k = max(results, key=lambda k: (results[k]['r2'], -results[k]['rmse']))
    print(f'\n✅ 가장 성능이 좋은 모델: n_neighbors = {best_k}')


if __name__ == '__main__':
    main()