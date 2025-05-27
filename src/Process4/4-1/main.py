# 과정 4 - (문제1) "스페이스 타이타닉 사건"

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

def load_and_merge(train_path, test_path):
    train_df = pd.read_csv(train_path)
    test_df = pd.read_csv(test_path)
    test_df['Transported'] = pd.NA  # 테스트 데이터에 없는 열 추가 (Transported)
    merged_df = pd.concat([train_df, test_df], ignore_index=True)
    return merged_df


def report_shape(df):
    print(f'총 행 개수: {df.shape[0]}')
    print(f'총 열 개수: {df.shape[1]}')


def analyze_correlation(df):
    df_numeric = df.copy()
    df_numeric['Transported'] = df_numeric['Transported'].map({True: 1, False: 0})
    correlation = df_numeric.corr(numeric_only=True)
    correlation_target = correlation['Transported'].drop(labels=['Transported']).sort_values(ascending=False)

    print('\n[Transported와의 상관계수 상위 5개]')
    print(correlation_target.head(5))


def plot_age_groups(train_df):
    bins = [0, 19, 29, 39, 49, 59, 69, 79]
    labels = ['10대', '20대', '30대', '40대', '50대', '60대', '70대']
    train_df['AgeGroup'] = pd.cut(train_df['Age'], bins=bins, labels=labels, right=True)
    age_group_transport = train_df.groupby('AgeGroup')['Transported'].mean()

    plt.figure(figsize=(10, 6))
    age_group_transport.plot(kind='bar', color='skyblue', edgecolor='black')
    plt.title('연령대별 Transported 비율')
    plt.xlabel('연령대')
    plt.ylabel('Transported 비율')
    plt.ylim(0, 1)
    plt.grid(axis='y')
    plt.tight_layout()
    plt.show()

# [보너스 과제] - Destination 별로 승객들의 연령대 분포 시각화
def plot_destination_age_pie(df):
    df = df[df['Age'].notna() & df['Destination'].notna()]

    bins = [0, 19, 29, 39, 49, 59, 69, 79]
    labels = ['10대', '20대', '30대', '40대', '50대', '60대', '70대']
    df['AgeGroup'] = pd.cut(df['Age'], bins=bins, labels=labels, right=True)

    # Destination별 연령대 분포 시각화 (원형 그래프)
    destinations = df['Destination'].unique()
    fig, axes = plt.subplots(1, len(destinations), figsize=(6 * len(destinations), 6))

    if len(destinations) == 1:
        axes = [axes]

    for ax, dest in zip(axes, destinations):
        group_counts = df[df['Destination'] == dest]['AgeGroup'].value_counts().sort_index()
        ax.pie(
            group_counts, 
            labels=group_counts.index, 
            autopct='%1.1f%%', 
            startangle=90,
            textprops={'fontsize': 7},
            )
        ax.set_title(f'{dest} - 연령대 분포')

    plt.tight_layout()
    plt.show()

def main():
    train_path = 'src/Process4/4-1/train.csv'
    test_path = 'src/Process4/4-1/test.csv'

    merged_df = load_and_merge(train_path, test_path)

    print('[데이터 수량]')
    report_shape(merged_df)

    print('\n[상관 분석]')
    analyze_correlation(merged_df)

    plot_age_groups(merged_df)

    plot_destination_age_pie(merged_df)


if __name__ == '__main__':
    main()