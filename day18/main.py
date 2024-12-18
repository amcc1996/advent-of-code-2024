import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def find_path_dijkstra(i_start, j_start, i_end, j_end, obstacle, n_rows, n_cols):
    distances = [[float('inf') for _ in range(n_cols)] for _ in range(n_rows)]
    distances[i_start][j_start] = 0
    prev = [[None for _ in range(n_cols)] for _ in range(n_rows)]
    visited = [[False for _ in range(n_cols)] for _ in range(n_rows)]
    queue = [(i_start, j_start)]
    queue_distances = [distances[i_start][j_start]]
    while len(queue) > 0:
        pos_min = queue_distances.index(min(queue_distances))
        i, j = queue.pop(pos_min)
        _ = queue_distances.pop(pos_min)
        visited[i][j] = True
        if i == i_end and j == j_end:
            break
        for i_next, j_next in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
            if i_next >= 0 and i_next < n_rows and j_next >= 0 and j_next < n_cols and not visited[i_next][j_next] and not obstacle[i_next][j_next]:
                if distances[i_next][j_next] > distances[i][j] + 1:
                    distances[i_next][j_next] = distances[i][j] + 1
                    prev[i_next][j_next] = (i, j)
                    if (i_next, j_next) in queue:
                        pos = queue.index((i_next, j_next))
                        queue_distances[pos] = distances[i_next][j_next]

                if (i_next, j_next) not in queue:
                    queue.append((i_next, j_next))
                    queue_distances.append(distances[i_next][j_next])

    i_path = i_end
    j_path = j_end
    path = [(i_path, j_path)]
    while i_path != i_start or j_path != j_start:
        i_path, j_path = prev[i_path][j_path]
        path.append((i_path, j_path))

    return path, distances[i_end][j_end]

def print_grid(obstacles, path):
    for i in range(len(obstacles)):
        row = []
        for j in range(len(obstacles[i])):
            if obstacles[i][j]:
                row.append("#")
            elif (i, j) in path:
                row.append("O")
            else:
                row.append(".")
        print("".join(row))

def prin_filled_area(grid, obstacle):
    for i in range(len(grid)):
        row = []
        for j in range(len(grid[i])):
            if obstacle[i][j]:
                row.append("#")
            elif grid[i][j]:
                row.append("O")
            else:
                row.append(".")
        print("".join(row))

def bucket_fill(grid, obstacles, i_start, j_start, n_rows, n_cols):
    queue = [(i_start, j_start)]
    res = 0
    while queue:
        i, j = queue.pop(0)
        if i < 0 or i >= n_rows or j < 0 or j >= n_cols:
            continue
        elif obstacles[i][j]:
            continue
        elif grid[i][j]:
            continue
        else:
            grid[i][j] = True
            res += 1
            for i, j in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
                queue.append((i, j))

    return res

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    n_rows = 71
    n_cols = 71

    # n_rows = 7
    # n_cols = 7

    obstacle = [[False for _ in range(n_cols)] for _ in range(n_rows)]
    if part == '1':
        n_btyes = 1024
        # n_btyes = 12
        for line in data[0:n_btyes]:
            i = int(line.split(",")[0])
            j = int(line.split(",")[1])
            obstacle[i][j] = True

        i_start = 0
        j_start = 0
        i_end = n_rows - 1
        j_end = n_cols - 1
        path, distance = find_path_dijkstra(i_start, j_start, i_end, j_end, obstacle, n_rows, n_cols)
        print_grid(obstacle, path)
        print("Result of part 1: ", distance)

    elif part == '2':
        i_start = 0
        j_start = 0
        i_end = n_rows - 1
        j_end = n_cols - 1
        for iobstacle, line in enumerate(data):
            i = int(line.split(",")[0])
            j = int(line.split(",")[1])
            obstacle[i][j] = True
            grid = [[False for _ in range(n_cols)] for _ in range(n_rows)]
            area = bucket_fill(grid, obstacle, i_start, j_start, n_rows, n_cols)
            if area < n_rows * n_cols - (iobstacle + 1) and not grid[i_end][j_end]:
                break

        print("Result of part 2: {0},{1}".format(i, j))