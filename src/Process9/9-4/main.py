# 과정9 - (문제4) 데이터 전처리 Sampling
import pandas as pd
from collections import Counter
from sklearn.preprocessing import LabelEncoder
from sklearn.utils import resample
from imblearn.over_sampling import SMOTE  # [보너스 과제]

def load_abalone_data(data_path, attr_path):
    with open(attr_path, 'r', encoding='utf-8') as f:
        columns = [line.strip() for line in f if line.strip()]

    df = pd.read_csv(data_path, header=None, names=columns)
    return df

def random_over_sampling(data, label):
    df = data.copy()
    df['label'] = label
    max_count = df['label'].value_counts().max()
    resampled_list = []

    for value, group in df.groupby('label'):
        if len(group) < max_count:
            upsampled = resample(group, replace=True, n_samples=max_count, random_state=42)
        else:
            upsampled = group
        resampled_list.append(upsampled)

    result = pd.concat(resampled_list).sample(frac=1, random_state=42).reset_index(drop=True)
    return result.drop(columns=['label']), result['label']

def random_under_sampling(data, label):
    df = data.copy()
    df['label'] = label
    min_count = df['label'].value_counts().min()
    resampled_list = []

    for value, group in df.groupby('label'):
        downsampled = resample(group, replace=False, n_samples=min_count, random_state=42)
        resampled_list.append(downsampled)

    result = pd.concat(resampled_list).sample(frac=1, random_state=42).reset_index(drop=True)
    return result.drop(columns=['label']), result['label']

def apply_smote(data, label):
    smote = SMOTE(random_state=42)
    return smote.fit_resample(data, label)

def print_label_distribution(label, title):
    print(f'\n{title} 분포:')
    counts = Counter(label)
    for k, v in counts.items():
        print(f'{k}: {v}')

def main():
    data_path = 'src/Process9/9-4/9-4-abalone.txt'
    attr_path = 'src/Process9/9-4/9-4-abalone_attributes.txt'

    # 데이터 로드
    df = load_abalone_data(data_path, attr_path)

    # label: 성별, data: 수치형 정보
    label = df['Sex']
    data = df.drop(columns=['Sex'])

    # label을 숫자로 인코딩 (SMOTE를 위해 필요)
    le = LabelEncoder()
    encoded_label = le.fit_transform(label)

    # 원본 분포
    print_label_distribution(label, '원본')

    # Random Over Sampling
    over_data, over_label = random_over_sampling(data, label)
    print_label_distribution(over_label, 'Random Over Sampling')

    # Random Under Sampling
    under_data, under_label = random_under_sampling(data, label)
    print_label_distribution(under_label, 'Random Under Sampling')

    # [보너스 과제] SMOTE
    smote_data, smote_label = apply_smote(data, encoded_label)
    decoded_smote_label = le.inverse_transform(smote_label)
    print_label_distribution(decoded_smote_label, '[보너스 과제] SMOTE 결과')

if __name__ == '__main__':
    main()