import pandas as pd
from collections import deque

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

def get_obstacle_set(area_map):
    return set(zip(area_map[area_map['mountain'] == 1]['x'], area_map[area_map['mountain'] == 1]['y']))

def bfs_shortest_path(start, goal, obstacles, max_x, max_y, min_x, min_y):
    queue = deque()
    queue.append((start, [start]))
    visited = set()
    visited.add(start)
    directions = [(-1,0), (1,0), (0,-1), (0,1)]  # 상하좌우

    while queue:
        (x, y), path = queue.popleft()
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

def main():
    area_map, area_struct = load_data()
    (home_x, home_y), (us_x, us_y) = find_base_coords(area_struct)
    obstacles = get_obstacle_set(area_map)
    max_x, max_y = area_map['x'].max(), area_map['y'].max()
    min_x, min_y = area_map['x'].min(), area_map['y'].min()
    path = bfs_shortest_path((home_x, home_y), (us_x, us_y), obstacles, max_x, max_y, min_x, min_y)
    if path is not None:
        save_path_csv(path, 'home_to_us_camp.csv')
    else:
        print('경로를 찾을 수 없습니다.')

if __name__ == '__main__':
    main()