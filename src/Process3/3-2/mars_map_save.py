import pandas as pd
import matplotlib.pyplot as plt
import matplotlib

matplotlib.rc('font', family='AppleGothic')
plt.rcParams['axes.unicode_minus'] = False

def load_data():
    area_map = pd.read_csv('src/Process3/3-1/3-1-area_map.csv')
    area_struct = pd.read_csv('src/Process3/3-1/3-1-area_struct.csv')
    struct_category = pd.read_csv('src/Process3/3-1/3-1-area_category.csv')
    area_struct = area_struct.merge(struct_category, on='category', how='left')
    return area_map, area_struct

def draw_mars_map(area_map, area_struct, save_path='mars_map.png'):
    fig, ax = plt.subplots(figsize=(10, 10))
    max_x, max_y = area_map['x'].max(), area_map['y'].max()
    min_x, min_y = area_map['x'].min(), area_map['y'].min()

    # 그리드 라인
    for x in range(min_x, max_x + 1):
        ax.axvline(x - 0.5, color='lightgrey', linewidth=0.8, zorder=0)
    for y in range(min_y, max_y + 1):
        ax.axhline(y - 0.5, color='lightgrey', linewidth=0.8, zorder=0)

    # 암석(갈색 원, 구조물과 겹치면 그리지 않음. 단, struct가 NaN인 곳은 암석을 그림)
    struct_coords = set(
        zip(
            area_struct[~pd.isna(area_struct['struct'])]['x'],
            area_struct[~pd.isna(area_struct['struct'])]['y']
        )
    )
    rocks = area_map[
        (area_map['mountain'] == 1) &
        (~area_map[['x', 'y']].apply(tuple, axis=1).isin(struct_coords))
    ]
    ax.scatter(rocks['x'], rocks['y'], s=400, color='#8B4513', edgecolors='black', label='암석', zorder=3)

    # 구조물(회색 사각형)
    for _, row in area_struct.iterrows():
        if pd.isna(row['struct']):
            continue
        if row['struct'] in ['Korea Mars Base', 'U.S. Mars Base Camp']:
            continue
        ax.scatter(row['x'], row['y'], marker='s', s=300, color='grey', edgecolors='black', label='구조물', zorder=4)

    # 기지 (녹색 삼각형)
    korea_base = area_struct[area_struct['struct'] == 'Korea Mars Base']
    us_base = area_struct[area_struct['struct'] == 'U.S. Mars Base Camp']
    ax.scatter(korea_base['x'], korea_base['y'], marker='^', s=400, color='lightgreen', edgecolors='black', label='화성 기지', zorder=5)
    ax.scatter(us_base['x'], us_base['y'], marker='^', s=400, color='green', edgecolors='black', label='미국 전진 기지', zorder=5)

    # 범례(중복 제거)
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='upper left', fontsize=12)

    # 축 설정
    ax.set_xlim(min_x - 0.5, max_x + 0.5)
    ax.set_ylim(max_y + 0.5, min_y - 0.5)
    ax.set_xticks(range(min_x, max_x + 1))
    ax.set_yticks(range(min_y, max_y + 1))
    ax.set_xlabel('X 좌표')
    ax.set_ylabel('Y 좌표')
    ax.set_title('화성 지도')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def main():
    area_map, area_struct = load_data()
    draw_mars_map(area_map, area_struct, save_path='src/Process3/3-2/mars_map.png')

if __name__ == '__main__':
    main()