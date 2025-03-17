import os
import sys

from collections import deque
from heapq import heappop, heappush

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def find_path_dijkstra(i_start, j_start, i_end, j_end, maze, n_rows, n_cols, distance_threshold=float('inf')):
    visited = set()
    prev = {}
    heap = [(0, i_start, j_start, i_start, j_start)]
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    shortest_distance = float('inf')
    found = False
    while heap:
        distance, i, j, i_prev, j_prev = heappop(heap)

        if (i, j) in visited:
            continue

        visited.add((i, j))
        prev[(i, j)] = (i_prev, j_prev)

        if i == i_end and j == j_end:
            shortest_distance = distance
            found = True
            break

        estimated_distance = abs(i_end - i) + abs(j_end - j)
        if distance + estimated_distance > distance_threshold:
            break

        for i_offset, j_offset in DIRECTIONS:
            i_new = i + i_offset
            j_new = j + j_offset
            if i_new >= 0 and i_new < n_rows and j_new >= 0 and j_new < n_cols and maze[i_new][j_new] != '#' and (i_new, j_new) not in visited:
                new_distance = distance + 1
                heappush(heap, (new_distance, i_new, j_new, i, j))

    if found:
        i_path = i_end
        j_path = j_end
        path = [(i_path, j_path)]
        while i_path != i_start or j_path != j_start:
            i_path, j_path = prev[(i_path, j_path)]
            path.append((i_path, j_path))
    else:
        path = []

    return shortest_distance, path[::-1]

def find_list_cheats(maze):
    cheats = set()
    for i in range(1,len(maze)-1):
        for j in range(1,len(maze[i])-2):
            if (maze[i][j] == '#' and (maze[i][j-1] != '#' and maze[i][j+1] != '#')):
                cheats.add((i, j))

    for i in range(1, len(maze)-2):
        for j in range(len(maze[i])):
            if (maze[i][j] == '#' and (maze[i-1][j] != '#' and maze[i+1][j] != '#')):
                cheats.add((i, j))

    return cheats

def apply_cheat(maze, cheat):
    i, j = cheat
    maze[i][j] = '.'

def undo_cheat(maze, cheat):
    i, j = cheat
    maze[i][j] = '#'

def find_savings(maze, i_start, j_start, i_end, j_end, min_saving):
    base_time, path = find_path_dijkstra(i_start, j_start, i_end, j_end, maze, n_rows, n_cols)
    cheats = find_list_cheats(maze)
    savings = {}
    count_cheats = 0
    n_cheats = len(cheats)
    for cheat in (cheats):
        count_cheats += 1
        print("Processing cheat {0}/{1}".format(count_cheats, n_cheats))
        apply_cheat(maze, cheat)
        new_time, path = find_path_dijkstra(i_start, j_start, i_end, j_end, maze, n_rows, n_cols, distance_threshold=base_time-min_saving)
        undo_cheat(maze, cheat)
        speedup = base_time - new_time
        if speedup not in savings:
            savings[speedup] = 1
        else:
            savings[speedup] += 1

    return savings

def find_all_shortest_distances_dijkstra(i_end, j_end, maze, n_rows, n_cols):
    visited = set()
    heap = [(0, i_end, j_end)]
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    distances = [[float('inf') for _ in range(n_cols)] for _ in range(n_rows)]
    while heap:
        distance, i, j = heappop(heap)

        if (i, j) in visited:
            continue

        visited.add((i, j))
        distances[i][j] = distance

        for i_offset, j_offset in DIRECTIONS:
            i_new = i + i_offset
            j_new = j + j_offset
            if i_new >= 0 and i_new < n_rows and j_new >= 0 and j_new < n_cols and maze[i_new][j_new] != '#' and (i_new, j_new) not in visited:
                new_distance = distance + 1
                heappush(heap, (new_distance, i_new, j_new))

    return distances

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
    dir_start = 'h'
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == 'S':
                i_start = i
                j_start = j
            elif maze[i][j] == 'E':
                i_end = i
                j_end = j

    if part == '1':
        min_saving = 0
        savings = find_savings(maze, i_start, j_start, i_end, j_end, min_saving)
        res = count_savings_greater_than(savings, min_saving, verbose=True)

        print("Result of part 1: {0}".format(res))

    elif part == '2':
        distances = find_all_shortest_distances_dijkstra(i_end, j_end, maze, n_rows, n_cols)
        print("Distances from the end point:")
        for i in range(len(distances)):
            for j in range(len(distances[i])):
                if distances[i][j] == float('inf'):
                    print("  #", end="")
                else:
                    print(f"{distances[i][j]:3d}", end="")
            print()

        print("Result of part 2: {0},{1}".format(i, j))