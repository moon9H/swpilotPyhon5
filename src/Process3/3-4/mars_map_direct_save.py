# 과정 3 - (문제4) "한장의 지도에 새겨진 길"

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

def load_path_csv(filename):
    df = pd.read_csv(filename)
    return list(zip(df['x'], df['y']))

def find_base_coords(area_struct):
    home = area_struct[area_struct['struct'] == 'Korea Mars Base'][['x', 'y']].iloc[0]
    us_camp = area_struct[area_struct['struct'] == 'U.S. Mars Base Camp'][['x', 'y']].iloc[0]
    return (home['x'], home['y']), (us_camp['x'], us_camp['y'])

def get_obstacle_set(area_map):
    return set(zip(area_map[area_map['mountain'] == 1]['x'], area_map[area_map['mountain'] == 1]['y']))

def get_struct_coords(area_struct):
    coords = []
    for _, row in area_struct.iterrows():
        if pd.isna(row['struct']):
            continue
        if row['struct'] in ['Korea Mars Base', 'U.S. Mars Base Camp']:
            continue
        coords.append((row['x'], row['y']))
    return coords

def find_turn_points(path):
    # 방향이 바뀌는 지점(코너)만 추출
    turn_points = []
    if len(path) < 3:
        return turn_points
    for i in range(1, len(path) - 1):
        x0, y0 = path[i - 1]
        x1, y1 = path[i]
        x2, y2 = path[i + 1]
        dx1, dy1 = x1 - x0, y1 - y0
        dx2, dy2 = x2 - x1, y2 - y1
        if (dx1, dy1) != (dx2, dy2):
            turn_points.append((x1, y1))
    return turn_points

def draw_mars_map_with_path(area_map, area_struct, path, turn_points, save_path, bonus_path=None, bonus_turn_points=None):
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

    # 기지 (연두 - korea, 초록 - US)
    korea_base = area_struct[area_struct['struct'] == 'Korea Mars Base']
    us_base = area_struct[area_struct['struct'] == 'U.S. Mars Base Camp']
    ax.scatter(korea_base['x'], korea_base['y'], marker='^', s=400, color='lightgreen', edgecolors='black', label='화성 기지', zorder=5)
    ax.scatter(us_base['x'], us_base['y'], marker='^', s=400, color='green', edgecolors='black', label='미국 전진 기지', zorder=5)

    # [보너스 과제] - 모든 구조물 거치는 최단 경로
    if bonus_path:
        px, py = zip(*bonus_path)
        ax.plot(px, py, color='yellow', linewidth=5, label='모든 구조물 경유 경로', zorder=7)
        if bonus_turn_points:
            bx, by = zip(*bonus_turn_points)
            # 코너는 범례 없이 그림
            ax.scatter(bx, by, s=250, color='yellow', edgecolors='black', linewidths=2, zorder=8)

    # 최단 경로(빨간색)
    if path:
        px, py = zip(*path)
        ax.plot(px, py, color='red', linewidth=5, label='최단 경로', zorder=10)
    if turn_points:
        tx, ty = zip(*turn_points)
        # 코너는 범례 없이 그림
        ax.scatter(tx, ty, s=250, color='red', edgecolors='black', linewidths=2, zorder=11)

    # 범례(중복 제거, 코너는 제외)
    handles, labels = ax.get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    ax.legend(by_label.values(), by_label.keys(), loc='lower right', fontsize=12)

    # 축 설정
    ax.set_xlim(min_x - 0.5, max_x + 0.5)
    ax.set_ylim(max_y + 0.5, min_y - 0.5)
    ax.set_xticks(range(min_x, max_x + 1))
    ax.set_yticks(range(min_y, max_y + 1))
    ax.set_xlabel('X 좌표')
    ax.set_ylabel('Y 좌표')
    ax.set_title('화성 지도 - 최단 경로')

    plt.gca().set_aspect('equal', adjustable='box')
    plt.tight_layout()
    plt.savefig(save_path)
    plt.close()

def main():
    area_map, area_struct = load_data()
    # 최단 경로 불러오기
    path = load_path_csv('src/Process3/3-3/home_to_us_camp.csv')
    turn_points = find_turn_points(path)

    # [보너스 과제] 모든 구조물 경유 경로 불러오기 (3번 문제에서 해결)
    try:
        bonus_path = load_path_csv('src/Process3/3-3/home_to_us_camp_all_structures.csv')
        bonus_turn_points = find_turn_points(bonus_path)
    except Exception:
        bonus_path = None
        bonus_turn_points = None

    # 최단 경로 지도
    draw_mars_map_with_path(
        area_map, area_struct, path, turn_points,
        save_path='src/Process3/3-4/mars_map_final.png'
    )

    # [보너스 과제] 모든 구조물 경유 경로 지도에 표시
    if bonus_path:
        draw_mars_map_with_path(
            area_map, area_struct, path, turn_points,
            save_path='src/Process3/3-4/mars_map_all_around.png',
            bonus_path=bonus_path,
            bonus_turn_points=bonus_turn_points
        )

if __name__ == '__main__':
    main()