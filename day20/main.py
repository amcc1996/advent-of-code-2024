import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def find_path_dijkstra(i_start, j_start, i_end, j_end, maze, n_rows, n_cols):
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
            if i_next >= 0 and i_next < n_rows and j_next >= 0 and j_next < n_cols and not visited[i_next][j_next] and maze[i_next][j_next] != '#':
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

    return distances[i_end][j_end], path[::-1]

def find_list_cheats(maze):
    cheats = []
    for i in range(1,len(maze)-1):
        for j in range(1,len(maze[i])-2):
            if (maze[i][j] == '#' and maze[i][j+1] != '#') or (maze[i][j] != '#' and maze[i][j+1] == '#'):
                cheats.append(((i, j), (i, j+1)))
                cheats.append(((i, j+1), (i, j)))

    for i in range(1, len(maze)-2):
        for j in range(len(maze[i])):
            if (maze[i][j] == '#' and maze[i+1][j] != '#') or (maze[i][j] != '#' and maze[i+1][j] == '#'):
                cheats.append(((i, j), (i+1, j)))
                cheats.append(((i+1, j), (i, j)))

    return cheats

def apply_cheat(maze, cheat):
    i1, j1 = cheat[0]
    i2, j2 = cheat[1]
    save = (maze[i1][j1], maze[i2][j2])
    maze[i1][j1] = '.'
    maze[i2][j2] = '.'

    return save

def undo_cheat(maze, cheat, save):
    i1, j1 = cheat[0]
    i2, j2 = cheat[1]
    maze[i1][j1] = save[0]
    maze[i2][j2] = save[1]

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
        base_time, path = find_path_dijkstra(i_start, j_start, i_end, j_end, maze, n_rows, n_cols)
        cheats = find_list_cheats(maze)
        savings = {}
        for i in range(len(cheats)):
            print(i,"/",len(cheats))
            save = apply_cheat(maze, cheats[i])
            time, path = find_path_dijkstra(i_start, j_start, i_end, j_end, maze, n_rows, n_cols)
            undo_cheat(maze, cheats[i], save)
            if cheats[i][0] in path and cheats[i][1] in path:
                pos1 = path.index(cheats[i][0])
                pos2 = path.index(cheats[i][1])
                if pos2 > pos1:
                    speedup = base_time - time
                    if speedup not in savings:
                        savings[speedup] = 1
                    else:
                        savings[speedup] += 1

        print("Result of part 1: ")
        res = 0
        for key in sorted(savings.keys(), reverse=True):
            print("{0:3n}: {1:3n}".format(key, savings[key]))
            if key >= 100:
                res += savings[key]
        print(res, res/2)

    # elif part == '2':
    #     i_start = 0
    #     j_start = 0
    #     i_end = n_rows - 1
    #     j_end = n_cols - 1
    #     for iobstacle, line in enumerate(data):
    #         i = int(line.split(",")[0])
    #         j = int(line.split(",")[1])
    #         obstacle[i][j] = True
    #         grid = [[False for _ in range(n_cols)] for _ in range(n_rows)]
    #         area = bucket_fill(grid, obstacle, i_start, j_start, n_rows, n_cols)
    #         if area < n_rows * n_cols - (iobstacle + 1) and not grid[i_end][j_end]:
    #             break

    #     print("Result of part 2: {0},{1}".format(i, j))