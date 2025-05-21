# 과정 3 - (문제7) "화성 정복"

import os
import mysql.connector
from datetime import datetime

class MySQLHelper:
    def __init__(self):
        self.connection = mysql.connector.connect(
            host=os.getenv('MYSQL_HOST', 'localhost'),
            user=os.getenv('MYSQL_USER', 'root'),
            password=os.getenv('MYSQL_PASSWORD', ''),
            database=os.getenv('MYSQL_DATABASE', 'swpilot')
        )
        self.cursor = self.connection.cursor()

    def insert_plant(self, data):
        if not validate_input(data):
            print('유효하지 않은 입력입니다.')
            return

        query = (
            'INSERT INTO mars_plant '
            '(scientific_name, common_names, plant_classification, '
            'plant_characteristics, growth_conditions, growth_period, '
            'optimal_growing_environment, cultivation_method, created_at, updated_at) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)'
        )

        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        values = (
            data.get('scientific_name'),
            data.get('common_names'),
            data.get('plant_classification'),
            data.get('plant_characteristics'),
            data.get('growth_conditions'),
            data.get('growth_period'),
            data.get('optimal_growing_environment'),
            data.get('cultivation_method'),
            now,
            now
        )

        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            print('식물 정보가 성공적으로 추가되었습니다.')
        except Exception as e:
            print('삽입 중 오류 발생:', e)

    def close(self):
        self.cursor.close()
        self.connection.close()

# [보너스 과제] - 입력 데이터 유효성 검사 코드
def validate_input(data):
    if not data.get('scientific_name'):
        print('scientific_name은 필수 항목입니다.')
        return False
    if data.get('cultivation_method') not in ['soil', 'hydroponic']:
        print('cultivation_method는 "soil" 또는 "hydroponic"이어야 합니다.')
        return False
    return True

def main():
    # 예시 데이터 입력
    plant_samples = [
    {
        'scientific_name': 'Capsicum annuum',
        'common_names': 'Bell Pepper, 파프리카',
        'plant_classification': 'Solanaceae > Capsicum > annuum',
        'plant_characteristics': '0.5~1m, 다년생, 온대',
        'growth_conditions': '20~27도, 습도 70%, 햇빛',
        'growth_period': '85일',
        'optimal_growing_environment': '비옥한 흙',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Lactuca sativa',
        'common_names': 'Lettuce, 상추',
        'plant_classification': 'Asteraceae > Lactuca > sativa',
        'plant_characteristics': '잎채소, 일년생',
        'growth_conditions': '15~20도, 습도 65%, 반음지',
        'growth_period': '55일',
        'optimal_growing_environment': '배수 잘 되는 토양',
        'cultivation_method': 'hydroponic'
    },
    {
        'scientific_name': 'Ocimum basilicum',
        'common_names': 'Basil, 바질',
        'plant_classification': 'Lamiaceae > Ocimum > basilicum',
        'plant_characteristics': '향신초, 일년생',
        'growth_conditions': '20~30도, 습도 60%, 햇빛',
        'growth_period': '60일',
        'optimal_growing_environment': '모래 섞인 흙',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Allium fistulosum',
        'common_names': 'Green Onion, 파',
        'plant_classification': 'Amaryllidaceae > Allium > fistulosum',
        'plant_characteristics': '짧은 줄기, 다년생',
        'growth_conditions': '18~25도, 습도 55%',
        'growth_period': '70일',
        'optimal_growing_environment': '배수 양호한 토양',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Spinacia oleracea',
        'common_names': 'Spinach, 시금치',
        'plant_classification': 'Amaranthaceae > Spinacia > oleracea',
        'plant_characteristics': '잎채소, 일년생',
        'growth_conditions': '10~20도, 습도 60%',
        'growth_period': '40일',
        'optimal_growing_environment': '유기물 많은 토양',
        'cultivation_method': 'hydroponic'
    },
    {
        'scientific_name': 'Raphanus sativus',
        'common_names': 'Radish, 무',
        'plant_classification': 'Brassicaceae > Raphanus > sativus',
        'plant_characteristics': '뿌리채소, 일년생',
        'growth_conditions': '15~22도, 습도 65%',
        'growth_period': '45일',
        'optimal_growing_environment': '모래질 흙',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Daucus carota',
        'common_names': 'Carrot, 당근',
        'plant_classification': 'Apiaceae > Daucus > carota',
        'plant_characteristics': '뿌리채소, 이년생',
        'growth_conditions': '16~22도, 습도 60%',
        'growth_period': '80일',
        'optimal_growing_environment': '심토 깊은 토양',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Brassica oleracea',
        'common_names': 'Cabbage, 양배추',
        'plant_classification': 'Brassicaceae > Brassica > oleracea',
        'plant_characteristics': '잎채소, 이년생',
        'growth_conditions': '15~20도, 습도 70%',
        'growth_period': '95일',
        'optimal_growing_environment': '중성 토양',
        'cultivation_method': 'hydroponic'
    },
    {
        'scientific_name': 'Fragaria × ananassa',
        'common_names': 'Strawberry, 딸기',
        'plant_classification': 'Rosaceae > Fragaria > × ananassa',
        'plant_characteristics': '딸기류, 다년생',
        'growth_conditions': '18~25도, 습도 60%',
        'growth_period': '120일',
        'optimal_growing_environment': '산성 토양',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Cucumis sativus',
        'common_names': 'Cucumber, 오이',
        'plant_classification': 'Cucurbitaceae > Cucumis > sativus',
        'plant_characteristics': '덩굴성, 일년생',
        'growth_conditions': '22~28도, 습도 70%',
        'growth_period': '55일',
        'optimal_growing_environment': '배수가 좋은 모래흙',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Zea mays',
        'common_names': 'Corn, 옥수수',
        'plant_classification': 'Poaceae > Zea > mays',
        'plant_characteristics': '1~3m, 일년생 곡물',
        'growth_conditions': '20~30도, 습도 60%',
        'growth_period': '100일',
        'optimal_growing_environment': '양분 많은 땅',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Glycine max',
        'common_names': 'Soybean, 콩',
        'plant_classification': 'Fabaceae > Glycine > max',
        'plant_characteristics': '두류, 일년생',
        'growth_conditions': '20~25도, 습도 60%',
        'growth_period': '90일',
        'optimal_growing_environment': '배수 좋은 평야',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Beta vulgaris',
        'common_names': 'Beet, 비트',
        'plant_classification': 'Amaranthaceae > Beta > vulgaris',
        'plant_characteristics': '근채류, 이년생',
        'growth_conditions': '15~22도, 습도 65%',
        'growth_period': '60일',
        'optimal_growing_environment': '중성~산성 토양',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Coriandrum sativum',
        'common_names': 'Coriander, 고수',
        'plant_classification': 'Apiaceae > Coriandrum > sativum',
        'plant_characteristics': '향신초, 일년생',
        'growth_conditions': '18~24도, 습도 55%',
        'growth_period': '45일',
        'optimal_growing_environment': '배수 좋은 토양',
        'cultivation_method': 'hydroponic'
    },
    {
        'scientific_name': 'Mentha × piperita',
        'common_names': 'Peppermint, 페퍼민트',
        'plant_classification': 'Lamiaceae > Mentha > × piperita',
        'plant_characteristics': '허브류, 다년생',
        'growth_conditions': '15~25도, 습도 70%',
        'growth_period': '60일',
        'optimal_growing_environment': '음지, 축축한 흙',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Petroselinum crispum',
        'common_names': 'Parsley, 파슬리',
        'plant_classification': 'Apiaceae > Petroselinum > crispum',
        'plant_characteristics': '허브, 이년생',
        'growth_conditions': '18~25도, 습도 60%',
        'growth_period': '75일',
        'optimal_growing_environment': '모래질 혼합토',
        'cultivation_method': 'hydroponic'
    },
    {
        'scientific_name': 'Brassica rapa subsp. pekinensis',
        'common_names': 'Napa Cabbage, 배추',
        'plant_classification': 'Brassicaceae > Brassica > rapa',
        'plant_characteristics': '잎채소, 일년생',
        'growth_conditions': '15~20도, 습도 75%',
        'growth_period': '70일',
        'optimal_growing_environment': '양질의 토양',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Cucurbita moschata',
        'common_names': 'Pumpkin, 단호박',
        'plant_classification': 'Cucurbitaceae > Cucurbita > moschata',
        'plant_characteristics': '덩굴, 일년생',
        'growth_conditions': '22~30도, 습도 65%',
        'growth_period': '90일',
        'optimal_growing_environment': '배수 양호한 땅',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Phaseolus vulgaris',
        'common_names': 'Common Bean, 강낭콩',
        'plant_classification': 'Fabaceae > Phaseolus > vulgaris',
        'plant_characteristics': '덩굴성, 일년생',
        'growth_conditions': '18~26도, 습도 60%',
        'growth_period': '80일',
        'optimal_growing_environment': '배수 양호한 토양',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Cichorium endivia',
        'common_names': 'Endive, 엔다이브',
        'plant_classification': 'Asteraceae > Cichorium > endivia',
        'plant_characteristics': '잎채소, 일년생',
        'growth_conditions': '10~20도, 습도 60%',
        'growth_period': '65일',
        'optimal_growing_environment': '유기질 풍부한 흙',
        'cultivation_method': 'hydroponic'
    },
    {
        'scientific_name': 'Allium cepa',
        'common_names': 'Onion, 양파',
        'plant_classification': 'Amaryllidaceae > Allium > cepa',
        'plant_characteristics': '근채류, 이년생',
        'growth_conditions': '13~24도, 습도 55%',
        'growth_period': '120일',
        'optimal_growing_environment': '사질양토',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Lycopersicon esculentum',
        'common_names': 'Cherry Tomato, 방울토마토',
        'plant_classification': 'Solanaceae > Lycopersicon > esculentum',
        'plant_characteristics': '덩굴형, 일년생',
        'growth_conditions': '22~28도, 습도 60%',
        'growth_period': '75일',
        'optimal_growing_environment': '햇빛 많고 배수 좋은 토양',
        'cultivation_method': 'hydroponic'
    },
    {
        'scientific_name': 'Vigna unguiculata',
        'common_names': 'Cowpea, 눈콩',
        'plant_classification': 'Fabaceae > Vigna > unguiculata',
        'plant_characteristics': '덩굴형, 일년생',
        'growth_conditions': '22~30도, 습도 65%',
        'growth_period': '85일',
        'optimal_growing_environment': '건조한 흙',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Citrullus lanatus',
        'common_names': 'Watermelon, 수박',
        'plant_classification': 'Cucurbitaceae > Citrullus > lanatus',
        'plant_characteristics': '덩굴형, 일년생',
        'growth_conditions': '25~32도, 습도 70%',
        'growth_period': '100일',
        'optimal_growing_environment': '고온건조 배수 양호',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Helianthus annuus',
        'common_names': 'Sunflower, 해바라기',
        'plant_classification': 'Asteraceae > Helianthus > annuus',
        'plant_characteristics': '1~3m, 일년생 화초',
        'growth_conditions': '20~28도, 습도 60%',
        'growth_period': '75일',
        'optimal_growing_environment': '양지 바른 땅',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Brassica napus',
        'common_names': 'Canola, 유채',
        'plant_classification': 'Brassicaceae > Brassica > napus',
        'plant_characteristics': '1~1.5m, 이년생',
        'growth_conditions': '15~25도, 습도 70%',
        'growth_period': '100일',
        'optimal_growing_environment': '배수 좋은 평야',
        'cultivation_method': 'soil'
    },
    {
        'scientific_name': 'Eruca vesicaria',
        'common_names': 'Arugula, 루꼴라',
        'plant_classification': 'Brassicaceae > Eruca > vesicaria',
        'plant_characteristics': '잎채소, 일년생',
        'growth_conditions': '18~24도, 습도 60%',
        'growth_period': '40일',
        'optimal_growing_environment': '통풍 좋은 곳',
        'cultivation_method': 'hydroponic'
    },
    {
        'scientific_name': 'Lavandula angustifolia',
        'common_names': 'Lavender, 라벤더',
        'plant_classification': 'Lamiaceae > Lavandula > angustifolia',
        'plant_characteristics': '허브류, 다년생',
        'growth_conditions': '20~30도, 습도 55%',
        'growth_period': '120일',
        'optimal_growing_environment': '건조한 석회질 토양',
        'cultivation_method': 'soil'
    }
    ]
    db = MySQLHelper()
    for data in plant_samples :
        db.insert_plant(data)
    db.close()

if __name__ == '__main__':
    main()