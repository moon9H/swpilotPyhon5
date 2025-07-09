# 과정 10 - (문제5) 이전에 없었던 물질을 분석하자
import matplotlib.pyplot as plt
import matplotlib
from sklearn.datasets import make_blobs
from sklearn.cluster import KMeans

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

def main():
    # 데이터 생성
    x, y = make_blobs(random_state=1)

    # 클러스터 수 3으로 설정
    model = KMeans(n_clusters=3, random_state=0)
    model.fit(x)
    labels = model.labels_
    print('클러스터 레이블:', labels)

    # [보너스 과제] 클러스터 시각화 (n_clusters = 1, 3, 5)
    for n_clusters in [1, 3, 5]:
        model = KMeans(n_clusters=n_clusters, random_state=0)
        model.fit(x)
        labels = model.labels_

        plt.figure(figsize=(6, 4))
        plt.title(f'클러스터 수: {n_clusters}')
        for cluster in range(n_clusters):
            plt.scatter(
                x[labels == cluster, 0],
                x[labels == cluster, 1],
                label=f'클러스터 {cluster}'
            )
        plt.xlabel('특성 0')
        plt.ylabel('특성 1')
        plt.legend()
        plt.tight_layout()
        plt.show()


if __name__ == '__main__':
    main()