# 과정 9 - (문제1) 식물 분류 프로젝트
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt

# [보너스 과제] 데이터 분포 시각화
def plot_iris_scatter(data, target, target_names):
    plt.figure(figsize=(8, 6))
    for class_idx, class_label in enumerate(target_names):
        xs = data[target == class_idx, 0]  # sepal length
        ys = data[target == class_idx, 1]  # sepal width
        plt.scatter(xs, ys, label=class_label)

    plt.xlabel('sepal length (cm)')
    plt.ylabel('sepal width (cm)')
    plt.title('Iris Dataset - Sepal Length vs Sepal Width')
    plt.legend(title='target')
    plt.tight_layout()
    plt.show()

def main():
    iris_dataset = load_iris()

    print('DESCR:')
    print(iris_dataset['DESCR'])

    print('\nTarget Names:')
    print(iris_dataset['target_names'])

    print('\nFeature Names:')
    print(iris_dataset['feature_names'])

    data = iris_dataset['data']
    print('\nData Info:')
    print('Shape:', data.shape)
    print('Dimensions:', data.ndim)
    print('Type:', type(data))
    print('First 5 samples:')
    for sample in data[:5]:
        print(sample)

    target = iris_dataset['target']
    print('\nTarget Info:')
    print('Shape:', target.shape)
    print('Dimensions:', target.ndim)
    print('Type:', type(target))
    print('First 5 targets:', target[:5])

    target_names = iris_dataset['target_names']

    # [보너스 과제] 데이터 분포 시각화
    plot_iris_scatter(data, target, target_names)

if __name__ == '__main__':
    main()