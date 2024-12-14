import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def parse_input(line):
    line_split = line.split(    )
    x = [int(a) for a in line_split[0].split("=")[1].split(",")]
    v = [int(a) for a in line_split[1].split("=")[1].split(",")]
    return x, v

def move_robot(x, v, n_rows, n_cols):
    x_new = [0, 0]
    x_new[0] = (x[0] + v[0]) % n_cols
    x_new[1] = (x[1] + v[1]) % n_rows

    return x_new

def compute_safety_factor(x_robots, n_rows, n_cols):
    n_robots_quad = [0, 0, 0, 0]
    v_axis = int((n_cols-1)/2)
    h_axis = int((n_rows-1)/2)
    for x in x_robots:
        if x[0] < v_axis and x[1] < h_axis:
            n_robots_quad[0] += 1
        elif x[0] < v_axis and x[1] > h_axis:
            n_robots_quad[1] += 1
        elif x[0] > v_axis and x[1] < h_axis:
            n_robots_quad[2] += 1
        elif x[0] > v_axis and x[1] > h_axis:
            n_robots_quad[3] += 1

    return n_robots_quad[0] * n_robots_quad[1] * n_robots_quad[2] * n_robots_quad[3]

def print_robots(x_robots, n_rows, n_cols):
    grid = [[0 for j in range(n_cols)] for i in range(n_rows)]
    for x in x_robots:
        grid[x[1]][x[0]] += 1

    print(" ")
    for i in range(n_rows):
        print(grid[i])

def check_christmas_tree(x_robots, n_rows, n_cols):
    for x in x_robots:
        i_row = x[1]
        i_col = x[0]
        depth = 0
        n_robots = 0
        finished = False
        while i_col - depth >= 0 and i_col + depth < n_cols and i_row + depth < n_rows and not finished:
                for i in range(i_col - depth, i_col + depth + 1):
                    if all([[i,i_row + depth] in x_robots for i in range(i_col-depth, i_col+depth+1)]):
                        n_robots += (depth + 1)
                        depth += 1
                    else:
                        finished = True

    # This gave the correct answer but it was luck honestly
    return finished and n_robots > 1

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    verbose = False

    n_rows = 103
    n_cols = 101
    n_seconds = 100

    # # Test
    # n_cols = 11
    # n_rows = 7

    x_robots = []
    v_robots = []
    for line in data:
        x, v = parse_input(line)
        x_robots.append(x)
        v_robots.append(v)

    if part == '1':
        result1 = 0
        for i in range(n_seconds):
            for j in range(len(x_robots)):
                x_robots[j] = move_robot(x_robots[j], v_robots[j], n_rows, n_cols)

            if verbose:
                print_robots(x_robots, n_rows, n_cols)

        result1 = compute_safety_factor(x_robots, n_rows, n_cols)
        print("Result of part 1: ", result1)

    elif part == '2':
        result1 = 0
        i_seconds = 0
        while not check_christmas_tree(x_robots, n_rows, n_cols):
            print(i_seconds)
            for j in range(len(x_robots)):
                x_robots[j] = move_robot(x_robots[j], v_robots[j], n_rows, n_cols)

            i_seconds += 1
            if verbose:
                print_robots(x_robots, n_rows, n_cols)

        print("Result of part 2: ", i_seconds)