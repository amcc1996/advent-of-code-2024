import os
import sys
import time
from collections import deque
from heapq import heappop, heappush

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
    count = 0
    while queue:
        count += 1
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

    # print("Number of iterations: ", count)
    return path, distances[dir_end][i_end][j_end]

def solve_maze_dijkstra_better(maze, i_start, j_start, i_end, j_end, dir_start, n_rows, n_cols, distance_threshold):
    """
    Optimised version of the Dijkstra algorithm. The idea is to use a heap to store the
    nodes to visitq, and a deque to store the visited nodes, in addition to other minor
    optimisations.
    """
    heap = [(0, i_start, j_start, dir_start)]
    visited = set()
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    found = False
    shortest_distance = float('inf')
    count = 0
    while heap:
        count += 1
        distance, i, j, dir = heappop(heap)

        if (i, j, dir) in visited:
            continue

        visited.add((i, j, dir))

        if i == i_end and j == j_end:
            shortest_distance = distance
            found = True
            break

        if distance > distance_threshold:
            break

        for i_offset, j_offset in DIRECTIONS:
            i_new = i + i_offset
            j_new = j + j_offset
            dir_new = get_dir(i, j, i_new, j_new)
            if i_new >= 0 and i_new < n_rows and j_new >= 0 and j_new < n_cols and maze[i_new][j_new] != '#' and (i_new, j_new, dir_new) not in visited:
                if is_corner(dir, dir_new):
                    new_distance = distance + 1001
                else:
                    new_distance = distance + 1

                heappush(heap, (new_distance, i_new, j_new, dir_new))

    # print("Number of iterations: ", count)
    return shortest_distance, found

def find_all_best_paths(maze, i_start, j_start, i_end, j_end, dir_start, n_rows, n_cols):
    # ts = time.time()
    # best_path, shortest_distance = solve_maze_dijkstra(maze, i_start, j_start, i_end, j_end, dir_start, n_rows, n_cols)
    # print("Time to solve: ", time.time() - ts)
    # print("Shortest distance: ", shortest_distance)
    # print((''))
    # ts = time.time()
    shortest_distance, found = solve_maze_dijkstra_better(maze, i_start, j_start, i_end, j_end, dir_start, n_rows, n_cols, float('inf'))
    # print("Time to solve 2: ", time.time() - ts)
    # print("Shortest distance 2: ", shortest_distance2)

    # Do a BFS and periodically check with Dijsktra if there is a possible best path
    # to find all paths with the same distance (brute-force, but honest).
    # Doing a BFS allows to prune a lot of bad paths from start.
    # Alternatively, we could start at the target node and go backwards in the direction of
    # decreasing distanced, but I am not so comfortable with this
    list_best_paths = []
    distance_stack = deque([0])
    path_stack = deque([[(i_start, j_start)]])
    dir_stack = deque([dir_start])
    count = 0
    DIRECTIONS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    output_frequency = 100
    best_path_frequency = 100
    best_path_cleanup_size = 50
    count_cleanup = 0
    is_cleanup = False
    ts = time.time()
    while distance_stack:
        count += 1
        distance = distance_stack.popleft()
        path = path_stack.popleft()
        dir = dir_stack.popleft()
        i, j = path[-1]
        if count % output_frequency == 0:
            t = time.time() - ts
            ts = time.time()
            print("n: {0:>10n}    t: {1:>8.3e}    queue size: {2:>10n}    distance: {3:>10n}    path size: {4:>10n}".format(count, t, len(distance_stack), distance, len(path)))

        # Check if we have reached the target node
        if i == i_end and j == j_end and distance == shortest_distance:
            list_best_paths.append(path)
            continue

        # Check for possible loops
        if (i, j) in path[:-1]:
            continue

        # Apply some heuristics to prune the search space
        virtual_distance = compute_virtual_distance(i, j, dir, i_end, j_end)
        if distance + virtual_distance > shortest_distance:
            continue

        # Apply a second best path search and see if we can find a path with the same distance
        # as the shortest path
        if count % best_path_frequency == 0:
            is_cleanup = True

        if is_cleanup:
            count_cleanup += 1
            if count_cleanup == best_path_cleanup_size:
                is_cleanup = False
                count_cleanup = 0
            shortest_distance_trial, found_trial = solve_maze_dijkstra_better(maze, i, j, i_end, j_end, dir, n_rows, n_cols, shortest_distance - distance)
            if not found_trial:
                continue
            elif shortest_distance_trial + distance != shortest_distance:
                continue

        for i_offset, j_offset in DIRECTIONS:
            i_new = i + i_offset
            j_new = j + j_offset
            dir_new = get_dir(i, j, i_new, j_new)
            if i_new >= 0 and i_new < n_rows and j_new >= 0 and j_new < n_cols and maze[i_new][j_new] != '#':
                if is_corner(dir, dir_new):
                    new_distance = distance + 1001
                else:
                    new_distance = distance + 1

                distance_stack.append(new_distance)
                path_stack.append(path + [(i_new, j_new)])
                dir_stack.append(dir_new)

    best_seats = set()
    for path in list_best_paths:
        for i, j in path:
            best_seats.add((i, j))

    return len(best_seats), best_seats

def compute_virtual_distance(i, j, dir, i_end, j_end):
    virtual_distace = abs(i - i_end) + abs(j - j_end)
    if i == i_end:
        if j < j_end and dir == 'l':
            virtual_distace += 2 * 1000
        elif j > j_end and dir == 'r':
            virtual_distace += 2 * 1000
    elif j == j_end:
        if i < i_end and dir == 'u':
            virtual_distace += 2 * 1000
        elif i > i_end and dir == 'd':
            virtual_distace += 2 * 1000
    elif i < i_end and j < j_end:
        if dir == 'u' or dir == 'l':
            virtual_distace += 2 * 1000
        elif dir == 'd' or dir == 'r':
            virtual_distace += 1000
    elif i < i_end and j > j_end:
        if dir == 'u' or dir == 'r':
            virtual_distace += 2 * 1000
        elif dir == 'd' or dir == 'l':
            virtual_distace += 1000
    elif i > i_end and j < j_end:
        if dir == 'd' or dir == 'l':
            virtual_distace += 2 * 1000
        elif dir == 'u' or dir == 'r':
            virtual_distace += 1000
    elif i > i_end and j > j_end:
        if dir == 'd' or dir == 'r':
            virtual_distace += 2 * 1000
        elif dir == 'u' or dir == 'l':
            virtual_distace += 1000

    return virtual_distace

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
        n_best_seats, best_seats = find_all_best_paths(data, i_start, j_start, i_end, j_end, dir_start, n_rows, n_cols)
        # print_maze(data, best_seats)
        print("Result of part 2: ", n_best_seats)