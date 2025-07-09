# 과정 10 - (문제5) 이전에 없었던 물질을 분석하자 II
import matplotlib.pyplot as plt
import matplotlib
from sklearn.datasets import make_blobs
from sklearn.cluster import AgglomerativeClustering
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, linkage

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

def main():
    x, y = make_blobs(random_state=1)

    # 병합 군집 (n_clusters=3)
    model = AgglomerativeClustering(n_clusters=3)
    labels = model.fit_predict(x)
    print('클러스터 레이블:', labels)

    # 덴드로그램 그리기 (기본 ward)
    linked = linkage(x, method='ward')
    plt.figure(figsize=(10, 5))
    dendrogram(linked)
    plt.title('덴드로그램 (linkage=ward)')
    plt.xlabel('샘플 인덱스')
    plt.ylabel('거리')
    plt.tight_layout()
    plt.show()

    # [보너스 과제] linkage별 성능 비교 및 적합한 옵션 선택
    best_method = None
    best_score = -1
    print('\n[linkage 옵션별 실루엣 점수 비교]')
    for method in ['ward', 'average', 'complete']:
        model = AgglomerativeClustering(n_clusters=3, linkage=method)
        labels = model.fit_predict(x)
        score = silhouette_score(x, labels)
        print(f'{method}: 실루엣 점수 = {score:.4f}')
        if score > best_score:
            best_score = score
            best_method = method

        # 덴드로그램 시각화
        linked = linkage(x, method=method)
        plt.figure(figsize=(10, 5))
        dendrogram(linked)
        plt.title(f'덴드로그램 (linkage={method})')
        plt.xlabel('샘플 인덱스')
        plt.ylabel('거리')
        plt.tight_layout()
        plt.show()

    print(f'\n가장 적합한 linkage 방식: {best_method} (실루엣 점수: {best_score:.4f})')


if __name__ == '__main__':
    main()