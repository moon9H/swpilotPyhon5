# 과정 3 - (문제3) "키트의 추억 최단 경로를 잡아라"

import pandas as pd

def load_data():
    area_map = pd.read_csv('src/Process3/3-1/3-1-area_map.csv')
    area_struct = pd.read_csv('src/Process3/3-1/3-1-area_struct.csv')
    struct_category = pd.read_csv('src/Process3/3-1/3-1-area_category.csv')
    area_struct = area_struct.merge(struct_category, on='category', how='left')
    return area_map, area_struct

def find_base_coords(area_struct):
    home = area_struct[area_struct['struct'] == 'Korea Mars Base'][['x', 'y']].iloc[0]
    us_camp = area_struct[area_struct['struct'] == 'U.S. Mars Base Camp'][['x', 'y']].iloc[0]
    return (home['x'], home['y']), (us_camp['x'], us_camp['y'])

# 암석이 있는 좌표 집합
def get_obstacle_set(area_map):
    return set(zip(area_map[area_map['mountain'] == 1]['x'], area_map[area_map['mountain'] == 1]['y']))

def bfs_shortest_path(start, goal, obstacles, max_x, max_y, min_x, min_y):
    queue = []
    queue.append((start, [start]))
    visited = set()
    visited.add(start)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # 상하좌우

    while queue:
        (x, y), path = queue.pop(0)  # 리스트의 pop(0)으로 큐 동작
        if (x, y) == goal:
            return path
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in visited:
                continue
            if nx < min_x or nx > max_x or ny < min_y or ny > max_y:
                continue
            if (nx, ny) in obstacles:
                continue
            visited.add((nx, ny))
            queue.append(((nx, ny), path + [(nx, ny)]))
    return None

def save_path_csv(path, filename='home_to_us_camp.csv'):
    df = pd.DataFrame(path, columns=['x', 'y'])
    df.to_csv(filename, index=False)

# [보너스 과제] 접근 가능한 모든 구조물만 방문하는 최단 경로 (바위로 둘러쌓인 구조물이 존재)
def get_struct_coords(area_struct, home, obstacles, max_x, max_y, min_x, min_y):
    coords = []
    for _, row in area_struct.iterrows():
        if pd.isna(row['struct']):
            continue
        if row['struct'] in ['Korea Mars Base', 'U.S. Mars Base Camp']:
            continue
        # home에서 구조물까지 경로가 있으면 추가
        if bfs_shortest_path(home, (row['x'], row['y']), obstacles, max_x, max_y, min_x, min_y) is not None:
            coords.append((row['x'], row['y']))
    return coords

def bfs_path(start, goal, obstacles, max_x, max_y, min_x, min_y):
    queue = []
    queue.append((start, [start]))
    visited = set()
    visited.add(start)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    while queue:
        (x, y), path = queue.pop(0)
        if (x, y) == goal:
            return path
        for dx, dy in directions:
            nx, ny = x + dx, y + dy
            if (nx, ny) in visited:
                continue
            if nx < min_x or nx > max_x or ny < min_y or ny > max_y:
                continue
            if (nx, ny) in obstacles:
                continue
            visited.add((nx, ny))
            queue.append(((nx, ny), path + [(nx, ny)]))
    return []

def bonus_structures_path(home, us_camp, struct_coords, obstacles, max_x, max_y, min_x, min_y):
    path = []
    current = home
    all_points = sorted(struct_coords)  # 좌표순 정렬(임의 순서)
    all_points.append(us_camp)
    for target in all_points:
        seg = bfs_path(current, target, obstacles, max_x, max_y, min_x, min_y)
        if not seg:
            return []
        if path:
            seg = seg[1:]  # 중복점 제거
        path.extend(seg)
        current = target
    return path

def main():

    area_map, area_struct = load_data()
    (home_x, home_y), (us_x, us_y) = find_base_coords(area_struct)
    obstacles = get_obstacle_set(area_map)
    max_x, max_y = area_map['x'].max(), area_map['y'].max()
    min_x, min_y = area_map['x'].min(), area_map['y'].min()
    path = bfs_shortest_path((home_x, home_y), (us_x, us_y), obstacles, max_x, max_y, min_x, min_y)
    if path is not None:
        save_path_csv(path, 'src/Process3/3-3/home_to_us_camp.csv')
    else:
        print('경로를 찾을 수 없습니다.')
    
    # [보너스 과제] 접근 가능한 모든 구조물만 방문(순차 경로)
    struct_coords = get_struct_coords(area_struct, (home_x, home_y), obstacles, max_x, max_y, min_x, min_y)
    bonus_path = bonus_structures_path((home_x, home_y), (us_x, us_y), struct_coords, obstacles, max_x, max_y, min_x, min_y)
    if bonus_path:
        save_path_csv(bonus_path, 'src/Process3/3-3/home_to_us_camp_all_structures.csv')
    else:
        print('접근 가능한 모든 구조물을 경유하는 경로를 찾을 수 없습니다.')

if __name__ == '__main__':
    main()