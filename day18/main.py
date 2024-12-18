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
    while len(queue) > 0:
        i, j = queue.pop(0)
        visited[i][j] = True
        if i == i_end and j == j_end:
            break
        for i_next, j_next in [(i+1, j), (i-1, j), (i, j+1), (i, j-1)]:
            if i_next >= 0 and i_next < n_rows and j_next >= 0 and j_next < n_cols and not visited[i_next][j_next] and not obstacle[i_next][j_next]:
                if distances[i_next][j_next] > distances[i][j] + 1:
                    distances[i_next][j_next] = distances[i][j] + 1
                    prev[i_next][j_next] = (i, j)
                    queue.append((i_next, j_next))

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

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    n_rows = 71
    n_cols = 71

    # n_rows = 7
    # n_cols = 7

    obstacle = [[False for _ in range(n_cols)] for _ in range(n_rows)]
    if part == '1':
        # n_btyes = 12
        n_btyes = 1024
        for line in data[0:n_btyes]:
            i = int(line.split(",")[0])
            j = int(line.split(",")[1])
            obstacle[i][j] = True

        path, distance = find_path_dijkstra(0, 0, n_rows-1, n_cols-1, obstacle, n_rows, n_cols)
        print_grid(obstacle, path)
        print("Result of part 1: ", distance)

    # elif part == '2':
    #     i = 0
    #     found = False
    #     program = ",".join([str(x) for x in instructions])
    #     while not found:
    #         print(i)
    #         computer = {'A' : i,
    #                     'B' : int(data[0][1].split(":")[1]),
    #                     'C' : int(data[0][2].split(":")[1]),
    #                     'pos' : 0}
    #         found, output_str = run_program_with_checks(instructions, computer, program)
    #         i += 1

    #     result2 = i
    #     print("Result of part 2: ", result2)