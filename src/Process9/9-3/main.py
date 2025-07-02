# 과정 9 - (문제3) 데이터 전처리 Min-Max
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, StandardScaler  # [보너스 과제 포함]

def load_abalone_data(data_path, attr_path):
    with open(attr_path, 'r', encoding='utf-8') as f:
        columns = [line.strip() for line in f if line.strip()]

    df = pd.read_csv(data_path, header=None, names=columns)
    return df

def min_max_scaling_manual(df):
    scaled_df = df.copy()
    for column in scaled_df.columns:
        col_min = scaled_df[column].min()
        col_max = scaled_df[column].max()
        scaled_df[column] = (scaled_df[column] - col_min) / (col_max - col_min)
    return scaled_df

def main():
    # 데이터 로드
    data_path = 'src/Process9/9-3/9-3-abalone.txt'
    attr_path = 'src/Process9/9-3/9-3-abalone_attributes.txt'
    df = load_abalone_data(data_path, attr_path)

    # label 추출 및 Sex 컬럼 제거
    label = df['Sex']
    df = df.drop(columns=['Sex'])

    print('원본 데이터 샘플:')
    print(df.head())

    # 수동 Min-Max Scaling
    scaled_manual = min_max_scaling_manual(df)
    print('\n[수동 Min-Max Scaling 결과]')
    print(scaled_manual.head())

    # Scikit-learn Min-Max Scaling
    scaler = MinMaxScaler()
    scaled_auto = pd.DataFrame(scaler.fit_transform(df), columns=df.columns)
    print('\n[Sklearn Min-Max Scaling 결과]')
    print(scaled_auto.head())

    # [보너스 과제] Standard Scaling
    std_scaler = StandardScaler()
    scaled_standard = pd.DataFrame(std_scaler.fit_transform(df), columns=df.columns)
    print('\n[보너스 과제] Standard Scaling 결과:')
    print(scaled_standard.head())


if __name__ == '__main__':
    main()