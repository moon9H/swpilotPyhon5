# 과정 4 - (문제2) "그때 지구 그리고 한국에서는"

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

def load_and_filter(filepath):
    df = pd.read_csv(filepath, encoding='utf-8')
    df = df[['시점', '성별', '연령별', '일반가구원']]
    return df

def group_by_gender_year(df):
    return df.groupby(['시점', '성별'])['일반가구원'].sum().unstack()

def group_by_age_year(df):
    return df.groupby(['시점', '연령별'])['일반가구원'].sum().unstack()

def plot_gender_age_trend(df):
    df = df[
        (df['성별'] != '계') &
        (~df['연령별'].isin(['합계', '15~64세', '65세이상', '15세미만', '85세이상']))
    ]

    genders = df['성별'].unique()

    for gender in genders:
        plt.figure(figsize=(14, 7))
        gender_df = df[df['성별'] == gender]
        pivot = gender_df.groupby(['시점', '연령별'])['일반가구원'].sum().unstack()

        y_max = pivot.max().max()
        plt.ylim(0, y_max * 1.1)

        for age in pivot.columns:
            plt.plot(pivot.index, pivot[age], marker='o', label=age)

        plt.title(f'{gender} 연령별 일반가구원 통계 (2015년 이후)', fontsize=14)
        plt.xlabel('년도')
        plt.ylabel('인원 수')
        plt.xticks(rotation=45)
        plt.legend(title='연령대', fontsize=8, ncol=2)
        plt.grid(True)
        plt.show()

# [보너스 과제] - 연령별 그래프의 변화를 보고 인구의 변화 트렌드를 데이터를 기반으로 정리한 리포터 작성
def write_markdown_trend(df):
    df = df[
        (~df['연령별'].isin(['합계', '15~64세', '65세이상', '15세미만', '85세이상']))
    ]
    
    for gender in df['성별'].unique():
        filename = f'src/Process4/4-2/{gender}_연령별_변화.md'
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f'# {gender} 연령별 인구 변화 트렌드\n\n')
            gender_df = df[df['성별'] == gender]
            pivot = gender_df.groupby(['시점', '연령별'])['일반가구원'].sum().unstack()

            for age in pivot.columns:
                values = pivot[age].dropna()
                start = values.iloc[0]
                end = values.iloc[-1]
                trend = '증가' if end > start else '감소' if end < start else '유지'
                rate = ((end - start) / start) * 100 if start != 0 else 0

                f.write(f'## {age}\n')
                f.write(f'- {values.index[0]}년: {int(start):,}명 → {values.index[-1]}년: {int(end):,}명\n')
                f.write(f'- 변화율: {rate:.1f}% ({trend})\n\n')

def main():
    filepath = 'src/Process4/4-2/population_statistics.csv'
    df = load_and_filter(filepath)

    print('\n 성별 연도별 일반가구원 통계:')
    gender_year_df = group_by_gender_year(df)
    print(gender_year_df)

    print('\n 연령별 연도별 일반가구원 통계:')
    age_year_df = group_by_age_year(df)
    print(age_year_df)

    plot_gender_age_trend(df)
    write_markdown_trend(df)


if __name__ == '__main__':
    main()