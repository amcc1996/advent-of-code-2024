import os
import sys

from collections import deque

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def find_path_distance(i_start, j_start, i_end, j_end, maze, n_rows, n_cols):
    visited = set()
    queue = deque([(0, i_end, j_end)])
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    distance_grid = [[float('inf') for _ in range(n_cols)] for _ in range(n_rows)]
    path = []
    while queue:
        distance, i, j = queue.popleft()

        if (i, j) in visited:
            continue

        visited.add((i, j))
        path.append((i, j))
        distance_grid[i][j] = distance

        if i == i_start and j == j_start:
            return distance_grid, path[::-1]

        for i_offset, j_offset in DIRECTIONS:
            i_new = i + i_offset
            j_new = j + j_offset
            if i_new >= 0 and i_new < n_rows and j_new >= 0 and j_new < n_cols and maze[i_new][j_new] != '#' and (i_new, j_new) not in visited:
                queue.append((distance + 1, i_new, j_new))

    return distance_grid, path[::-1]

def print_path_distance(distance_grid, maze):
    for i in range(len(distance_grid)):
        for j in range(len(distance_grid[i])):
            if distance_grid[i][j] == float('inf'):
                print("  #", end="")
            else:
                print(f"{distance_grid[i][j]:3d}", end="")
        print()

def find_cheats(i_path, j_path, maze, n_rows, n_cols, cheat_length):
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    reachable_points = set()
    for i_offset in range(-cheat_length, cheat_length + 1):
        i_new = i_path + i_offset
        if i_new < 0 or i_new >= n_rows:
            continue
        for j_offset in range(-cheat_length, cheat_length + 1):
            j_new = j_path + j_offset
            if j_new < 0 or j_new >= n_cols:
                continue

            # Unreachable point in the cheat duration
            distance = abs(i_offset) + abs(j_offset)
            if distance > cheat_length:
                continue

            # Reachable point
            if maze[i_new][j_new] != '#':
                reachable_points.add((i_new, j_new))

    return reachable_points

def compute_shortcut_savings(path, distance_grid, n_rows, n_cols, cheat_length):
    path_length = len(path) - 1
    savings = {}
    used_cheats = set()
    for distance_start, (i_path, j_path) in enumerate(path):
        cheats = find_cheats(i_path, j_path, maze, n_rows, n_cols, cheat_length)
        for i_end_cheat, j_end_cheat in cheats:
            if distance_grid[i_end_cheat][j_end_cheat] >= distance_grid[i_path][j_path]:
                continue

            new_distance = distance_start + abs(i_end_cheat-i_path) + abs(j_end_cheat-j_path) + distance_grid[i_end_cheat][j_end_cheat]
            speedup = path_length - new_distance

            if speedup <= 0:
                continue

            if (i_path, j_path, i_end_cheat, j_end_cheat) in used_cheats:
                continue

            used_cheats.add((i_path, j_path, i_end_cheat, j_end_cheat))
            if speedup not in savings:
                savings[speedup] = 1
            else:
                savings[speedup] += 1

    return savings

def count_savings_greater_than(savings, threshold, verbose=False):
    res = 0
    for key in sorted(savings.keys(), reverse=True):
        if verbose:
            print("{0:3n}: {1:3n}".format(key, savings[key]))
        if key >= threshold:
            res += savings[key]

    return res

def print_maze(maze):
    for i in range(len(maze)):
        print("".join(maze[i]))

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]
    maze = [[c for c in line] for line in data]

    n_rows = len(maze)
    n_cols = len(maze[0])

    i_end = 0
    j_end = 0
    i_start = 0
    j_start = 0
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'S':
                i_start = i
                j_start = j
            elif maze[i][j] == 'E':
                i_end = i
                j_end = j

    if part == '1':
        cheat_length = 2
        min_saving = 100
        distances, path = find_path_distance(i_start, j_start, i_end, j_end, maze, n_rows, n_cols)
        #print_path_distance(distances, maze)
        savings = compute_shortcut_savings(path, distances, n_rows, n_cols, cheat_length)
        res = count_savings_greater_than(savings, min_saving, verbose=True)

        print("Result of part 1: {0}".format(res))

    elif part == '2':
        cheat_length = 20
        min_saving = 100
        distances, path = find_path_distance(i_start, j_start, i_end, j_end, maze, n_rows, n_cols)
        # print_path_distance(distances, maze)
        savings = compute_shortcut_savings(path, distances, n_rows, n_cols, cheat_length)
        res = count_savings_greater_than(savings, min_saving, verbose=True)

        print("Result of part 2: {0}".format(res))