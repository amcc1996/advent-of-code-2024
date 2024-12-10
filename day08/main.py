import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def parse_map(data):
    map_antena_pos = {}
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j] != '.':
                if data[i][j] not in map_antena_pos:
                    map_antena_pos[data[i][j]] = [(i,j)]
                else:
                    map_antena_pos[data[i][j]].append((i, j))

    return map_antena_pos

def compute_antinodes(x1, x2):
    tol = 1e-3
    dx = (x2[0] - x1[0], x2[1] - x1[1])
    x_sol = [[x1[i] + 1/3 * dx[i] for i in range(len(dx))],
             [x1[i] + 2/3 * dx[i] for i in range(len(dx))],
             [x1[i] - 1 * dx[i] for i in range(len(dx))],
             [x1[i] + 2 * dx[i] for i in range(len(dx))]]

    int_x_sol = []
    for i in range(len(x_sol)):
        if (abs(x_sol[i][0] - round(x_sol[i][0])) < tol) and (abs(x_sol[i][1] - round(x_sol[i][1])) < tol):
            int_x_sol.append((int(x_sol[i][0]), int(x_sol[i][1])))

    return int_x_sol

def process_frequency(freq, map_antena_pos, antinodes, n_rows, n_cols):
    for i in range(len(map_antena_pos[freq]) - 1):
        for j in range(i+1, len(map_antena_pos[freq])):
            sol = compute_antinodes(map_antena_pos[freq][i], map_antena_pos[freq][j])
            for x, y in sol:
                if 0 <= x < n_rows and 0 <= y < n_cols:
                    if (x,y) not in antinodes:
                        antinodes.append((int(x), int(y)))

def span_line_antinodes(x1, x2, n_rows, n_cols):
    tol = 1e-3
    dx = (x2[0] - x1[0], x2[1] - x1[1])
    maxdx = max([abs(y) for y in dx])
    dx_step = (dx[0] / maxdx, dx[1] / maxdx)
    int_x_sol = []
    # Span one side
    step = 0
    x_test = x1
    while x_test[0] >= -tol and x_test[0] <= n_rows - 1 + tol and x_test[1] >= -tol and x_test[1] <= n_cols - 1 + tol:
        if (abs(x_test[0] - round(x_test[0])) < tol) and (abs(x_test[1] - round(x_test[1])) < tol):
            int_x_sol.append((int(x_test[0]), int(x_test[1])))
        step += 1
        x_test = (x1[0] + step * dx_step[0], x1[1] + step * dx_step[1])

    # Span the other side
    step = -1
    x_test = (x1[0] + step * dx_step[0], x1[1] + step * dx_step[1])
    while x_test[0] >= -tol and x_test[0] <= n_rows - 1 + tol and x_test[1] >= -tol and x_test[1] <= n_cols - 1 + tol:
        if (abs(x_test[0] - round(x_test[0])) < tol) and (abs(x_test[1] - round(x_test[1])) < tol):
            int_x_sol.append((int(x_test[0]), int(x_test[1])))
        step -= 1
        x_test = (x1[0] + step * dx_step[0], x1[1] + step * dx_step[1])

    return int_x_sol

def process_frequency_part2(freq, map_antena_pos, antinodes, n_rows, n_cols):
    pairs_list = []
    freq_antinodes = []
    for i in range(len(map_antena_pos[freq]) - 1):
        for j in range(i+1, len(map_antena_pos[freq])):
            pairs_list.append((map_antena_pos[freq][i], map_antena_pos[freq][j]))

    for ipair in range(len(pairs_list)):
        x1 = pairs_list[ipair][0]
        x2 = pairs_list[ipair][1]
        candidates = span_line_antinodes(x1, x2, n_rows, n_cols)
        for node in candidates:
            if node not in antinodes:
                antinodes.append(node)


if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    verbose = False

    if part == '1':
        antinodes = []
        n_rows = len(data)
        n_cols = len(data[0])
        map_antena_pos = parse_map(data)
        for freq in map_antena_pos:
            process_frequency(freq, map_antena_pos, antinodes, len(data), len(data[0]))

        result1 = len(antinodes)
        if verbose:
            for x,y in antinodes:
                data[x] = data[x][0:y] + "#" + data[x][y+1:]

            for line in data:
                print(''.join(line))

        print("Result of part 1: ", result1)

    elif part == '2':
        antinodes = []
        n_rows = len(data)
        n_cols = len(data[0])
        map_antena_pos = parse_map(data)
        for freq in map_antena_pos:
            process_frequency_part2(freq, map_antena_pos, antinodes, len(data), len(data[0]))

        result2 = len(antinodes)
        if verbose:
            for x,y in antinodes:
                data[x] = data[x][0:y] + "#" + data[x][y+1:]

            for line in data:
                print(''.join(line))

        print("Result of part 2: ", result2)