import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def get_dir(i_old, j_old, i_new, j_new):
    if i_new == i_old:
        return 'h'
    elif j_new == j_old:
        return 'v'

def solve_maze_dijkstra(maze, i_start, j_start, i_end, j_end, dir_start, n_rows, n_cols):
    distances = [[float('inf') for _ in range(n_cols)] for _ in range(n_rows)]
    visited = [[False for _ in range(n_cols)] for _ in range(n_rows)]
    previous = [[None for _ in range(n_cols)] for _ in range(n_rows)]
    queue = [(i_start, j_start)]
    dir_queue = [dir_start]
    distance_queue = [0]
    while queue:
        pos = distance_queue.index(min(distance_queue))
        i, j = queue.pop(pos)
        distance = distance_queue.pop(pos)
        dir = dir_queue.pop(pos)
        visited[i][j] = True
        if i == i_end and j == j_end:
            break

        for i_offset, j_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            i_new = i + i_offset
            j_new = j + j_offset
            if i_new >= 0 and i_new < n_rows and j_new >= 0 and j_new < n_cols and maze[i_new][j_new] != '#' and not visited[i_new][j_new]:
                new_dir = get_dir(i, j, i_new, j_new)
                if new_dir != dir:
                    new_distance = distance + 1001
                else:
                    new_distance = distance + 1

                if new_distance <= distances[i_new][j_new]:
                    distances[i_new][j_new] = new_distance
                    previous[i_new][j_new] = (i, j)

                if (i_new, j_new) not in queue:
                    queue.append((i_new, j_new))
                    distance_queue.append(distances[i_new][j_new])
                    dir_queue.append(new_dir)
                else:
                    pos = queue.index((i_new, j_new))
                    distance_queue[pos] = distances[i_new][j_new]
                    dir_queue[pos] = new_dir

    i = i_end
    j = j_end
    path = [(i_end, j_end)]
    while i != i_start or j != j_start:
        i, j = previous[i][j]
        path.append((i, j))

    return path, distances[i_end][j_end]

def print_maze(maze, path):
    for i in range(len(maze)):
        row = []
        for j in range(len(maze[i])):
            if (i, j) in path:
                row.append('O')
            else:
                row.append(maze[i][j])
        print("".join(row))

def compute_cost_from_path(path, dir_start):
    cost = len(path) - 1
    # add 1000 for each turn
    old_dir = dir_start
    for i in range(1, len(path) - 1):
        new_dir = get_dir(path[i - 1][0], path[i - 1][1], path[i][0], path[i][1])
        if new_dir != old_dir:
            cost += 1000

        old_dir = new_dir

    return cost

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    n_rows = len(data)
    n_cols = len(data[0])

    i_end = 0
    j_end = 0
    i_start = 0
    j_start = 0
    dir_start = 'h'
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] == 'S':
                i_start = i
                j_start = j
            elif data[i][j] == 'E':
                i_end = i
                j_end = j

    if part == '1':
        path, cost = solve_maze_dijkstra(data, i_start, j_start, i_end, j_end, dir_start, n_rows, n_cols)
        print_maze(data, path)
        print("Result of part 1: ", cost)
        print("Cost of path: ", compute_cost_from_path(path[::-1], dir_start))

    elif part == '2':
        result2 = 0
        print("Result of part 2: ", result2)