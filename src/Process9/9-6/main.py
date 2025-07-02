# 과정 9 - (문제6) 분명하게 말해 두기
import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
import numpy as np

def load_abalone_data(data_path, attr_path):
    with open(attr_path, 'r', encoding='utf-8') as f:
        columns = [line.strip() for line in f if line.strip()]

    df = pd.read_csv(data_path, header=None, names=columns)
    return df

def label_encode(label_series):
    encoder = LabelEncoder()
    encoded = encoder.fit_transform(label_series)
    print('Label Encoding 결과:', encoded[:10])
    print('클래스:', list(encoder.classes_))
    return encoded, encoder

def one_hot_encode(encoded_labels):
    encoder = OneHotEncoder(sparse_output=False)
    encoded_2d = np.array(encoded_labels).reshape(-1, 1)
    one_hot = encoder.fit_transform(encoded_2d)
    print('\nOne-Hot Encoding 결과 (앞 5개):\n', one_hot[:5])
    print('카테고리:', encoder.categories_)
    return one_hot

def handle_missing_values(df):
    print('\n[보너스 과제] 결측값 처리 예시')
    df_with_nan = df.copy()
    df_with_nan.iloc[0, 1] = np.nan  # 임의 결측치 삽입
    print('결측값 전:\n', df_with_nan.head())
    df_filled = df_with_nan.fillna(df_with_nan.mean(numeric_only=True))
    print('결측값 처리 후:\n', df_filled.head())

def handle_noise(df):
    print('\n[보너스 과제] 노이즈 처리 예시')
    df_noisy = df.copy()
    df_noisy.iloc[0, 2] = 9999  # 임의 노이즈 삽입
    print('노이즈 전:\n', df_noisy.head())
    # 단순 평균 대체
    col_mean = df_noisy[df_noisy.iloc[:, 2] < 1000].iloc[:, 2].mean()
    df_noisy.iloc[0, 2] = col_mean
    print('노이즈 처리 후:\n', df_noisy.head())

def handle_outliers(df):
    print('\n[보너스 과제] 이상값 처리 예시')
    df_outlier = df.copy()
    col = df_outlier.iloc[:, 3]
    q1 = col.quantile(0.25)
    q3 = col.quantile(0.75)
    iqr = q3 - q1
    lower_bound = q1 - 1.5 * iqr
    upper_bound = q3 + 1.5 * iqr
    outliers = (col < lower_bound) | (col > upper_bound)
    print('이상값 개수:', outliers.sum())
    df_outlier.loc[outliers, col.name] = col.median()
    print('이상값 처리 후 일부:\n', df_outlier[outliers].head())

def main():
    data_path = 'src/Process9/9-4/9-4-abalone.txt'
    attr_path = 'src/Process9/9-4/9-4-abalone_attributes.txt'

    df = load_abalone_data(data_path, attr_path)

    label = df['Sex']
    data = df.drop(columns=['Sex'])

    # Label Encoding
    encoded_label, label_encoder = label_encode(label)

    # One-Hot Encoding
    one_hot_encoded = one_hot_encode(encoded_label)

    # [보너스 과제] 데이터 전처리 예시
    handle_missing_values(data)
    handle_noise(data)
    handle_outliers(data)

if __name__ == '__main__':
    main()