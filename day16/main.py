import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def get_dir(i_old, j_old, i_new, j_new):
    if i_new < i_old:
        return 'u'
    elif i_new > i_old:
        return 'd'
    elif j_new < j_old:
        return 'l'
    elif j_new > j_old:
        return 'r'

def is_corner(dir1, dir2):
    if dir1 in ['u', 'd'] and dir2 in ['l', 'r']:
        return True
    elif dir1 in ['l', 'r'] and dir2 in ['u', 'd']:
        return True
    return False

def solve_maze_dijkstra(maze, i_start, j_start, i_end, j_end, dir_start, n_rows, n_cols):
    distances = {'u' : [[float('inf') for _ in range(n_cols)] for _ in range(n_rows)],
                 'd' : [[float('inf') for _ in range(n_cols)] for _ in range(n_rows)],
                 'l' : [[float('inf') for _ in range(n_cols)] for _ in range(n_rows)],
                 'r' : [[float('inf') for _ in range(n_cols)] for _ in range(n_rows)]}
    visited = {'u' : [[False for _ in range(n_cols)] for _ in range(n_rows)],
               'd' : [[False for _ in range(n_cols)] for _ in range(n_rows)],
               'l' : [[False for _ in range(n_cols)] for _ in range(n_rows)],
               'r' : [[False for _ in range(n_cols)] for _ in range(n_rows)]}
    previous = {'u' : [[None for _ in range(n_cols)] for _ in range(n_rows)],
                'd' : [[None for _ in range(n_cols)] for _ in range(n_rows)],
                'l' : [[None for _ in range(n_cols)] for _ in range(n_rows)],
                'r' : [[None for _ in range(n_cols)] for _ in range(n_rows)]}
    queue = [(i_start, j_start, dir_start)]
    distance_queue = [0]
    while queue:
        pos = distance_queue.index(min(distance_queue))
        i, j, dir = queue.pop(pos)
        distance = distance_queue.pop(pos)
        visited[dir][i][j] = True
        if i == i_end and j == j_end:
            dir_end = dir
            break

        for i_offset, j_offset in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            i_new = i + i_offset
            j_new = j + j_offset
            dir_new = get_dir(i, j, i_new, j_new)
            if i_new >= 0 and i_new < n_rows and j_new >= 0 and j_new < n_cols and maze[i_new][j_new] != '#' and not visited[dir_new][i_new][j_new]:
                if is_corner(dir, dir_new):
                    new_distance = distance + 1001
                else:
                    new_distance = distance + 1

                if new_distance < distances[dir_new][i_new][j_new]:
                    distances[dir_new][i_new][j_new] = new_distance
                    previous[dir_new][i_new][j_new] = (i, j, dir)

                if (i_new, j_new, dir_new) not in queue:
                    queue.append((i_new, j_new, dir_new))
                    distance_queue.append(distances[dir_new][i_new][j_new])
                else:
                    pos = queue.index((i_new, j_new, dir_new))
                    distance_queue[pos] = distances[dir_new][i_new][j_new]

    i = i_end
    j = j_end
    dir = dir_end
    path = [(i_end, j_end)]
    while i != i_start or j != j_start:
        i, j, dir = previous[dir][i][j]
        path.append((i, j))

    return path, distances[dir_end][i_end][j_end]

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
    dir_old = dir_start
    for i in range(1, len(path) - 1):
        dir_new = get_dir(path[i - 1][0], path[i - 1][1], path[i][0], path[i][1])
        if is_corner(dir_old, dir_new):
            cost += 1000

        dir_old = dir_new

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
    dir_start = 'r'
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