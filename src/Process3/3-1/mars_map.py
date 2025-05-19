# 과정 3 - (문제1) "우주_해적"

import pandas as pd

def read_and_print_csv(file_path):
    df = pd.read_csv(file_path)
    print(f'\n{file_path} 내용:')
    print(df)
    return df

def merge_dataframes(area_map, area_struct, struct_category):
    # 시설 종류명을 area_struct에 병합 (category 컬럼 기준)
    area_struct = area_struct.merge(struct_category, on='category', how='left')
    # area_map과 area_struct 병합 (x, y 기준)
    merged = area_struct.merge(area_map, on=['x', 'y'], how='left')
    return merged

def filter_area_one(df):
    return df[df['area'] == 1]

# [보너스 과제] - 지형 지물과 각종 시설물을 종류 별로 요약한 리포트 출력
def report_summary(df):
    print('\n[지형 지물 및 시설물 종류별 요약]')
    summary = df.groupby('struct').size().reset_index(name='count')
    print(summary)

def main():
    # 파일 경로
    area_map_path = 'src/Process3/3-1/3-1-area_map.csv'
    area_struct_path = 'src/Process3/3-1/3-1-area_struct.csv'
    struct_category_path = 'src/Process3/3-1/3-1-area_category.csv'

    # CSV 파일 읽기 및 출력
    area_map = read_and_print_csv(area_map_path)
    area_struct = read_and_print_csv(area_struct_path)
    struct_category = read_and_print_csv(struct_category_path)

    # 주요 시설이 어느 area에 집중되어 있는지 확인
    print('\n[주요 시설의 지역별 분포]')
    area_counts = area_struct['area'].value_counts().sort_index()
    print(area_counts)

    # 시설 종류명을 숫자 대신 이름으로 출력
    area_struct_named = area_struct.merge(struct_category, on='category', how='left')
    print('\n[시설 종류명을 이름으로 출력]')
    print(area_struct_named[['area', 'x', 'y', 'struct']])

    # 모든 데이터 병합
    merged = merge_dataframes(area_map, area_struct, struct_category)
    print('\n[모든 데이터 병합 결과]')
    print(merged)

    # area 1 데이터만 필터링
    area1_data = filter_area_one(merged)
    print('\n[area 1 데이터만 필터링]')
    print(area1_data)

    # 보너스: 종류별 요약 리포트
    report_summary(area1_data)

if __name__ == '__main__':
    main()