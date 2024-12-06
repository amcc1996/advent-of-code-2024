import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def move(i, j, dir):
    if dir == 'l':
        return i, j - 1
    elif dir == 'u':
        return i - 1, j
    elif dir == 'r':
        return i, j + 1
    elif dir == 'd':
        return i + 1, j

def move_back(i, j, dir):
    if dir == 'l':
        return i, j + 1
    elif dir == 'u':
        return i + 1, j
    elif dir == 'r':
        return i, j - 1
    elif dir == 'd':
        return i - 1, j

def rotate_clockwise(dir):
    if dir == 'l':
        return 'u'
    elif dir == 'u':
        return 'r'
    elif dir == 'r':
        return 'd'
    elif dir == 'd':
        return 'l'

def walk_guard_recursive(i, j, dir, data, visited, n_rows, n_cols):
    # Exceeds recursion limit
    if i < 0 or i >= n_rows or j < 0 or j >= n_cols:
        for line in visited:
            print(''.join(line))
        return 0

    if data[i][j] != "#":
        if visited[i][j] == 'X':
            offset = 0
        else:
            visited[i][j] = 'X'
            offset = 1
        i, j = move(i, j, dir)
        return offset + walk_guard_recursive(i, j, dir, data, visited, n_rows, n_cols)

    else:
        i, j = move_back(i, j, dir)
        dir = rotate_clockwise(dir)
        return walk_guard_recursive(i, j, dir, data, visited, n_rows, n_cols)

def walk_guard(i, j, dir, data, n_rows, n_cols):
    i, j = move(i, j, dir)
    if i < 0 or i >= n_rows or j < 0 or j >= n_cols:
        return i, j, dir

    elif data[i][j] == "#":
        i, j = move_back(i, j, dir)
        dir = rotate_clockwise(dir)
        return walk_guard(i, j, dir, data, n_rows, n_cols)

    else:
        return i, j, dir

def find_guard_path(i_start, j_start, dir_start, data, n_rows, n_cols):
    visited = [[False for x in line] for line in data]
    visited_dir = [[[] for x in line] for line in data]
    visited_pos = []
    i = i_start
    j = j_start
    dir = dir_start
    count = 0
    while i >= 0 and i < n_rows and j >= 0 and j < n_cols:
        if not visited[i][j]:
            count = count + 1
            visited_pos.append((i, j))

        visited[i][j] = True
        if dir in visited_dir[i][j]:
            return count, visited_pos, True
        else:
            visited_dir[i][j].append(dir)
        i, j, dir = walk_guard(i, j, dir, data, n_rows, n_cols)

    return count, visited_pos, False

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    for line in data:
        if '^' in line:
            i_start, j_start = (data.index(line), line.index('^'))
            break

    n_rows = len(data)
    n_cols = len(data[0])
    visited = [[x for x in line] for line in data]

    if part == '1':
        result1, visited_pos, is_loop = find_guard_path(i_start, j_start, 'u', data, n_rows, n_cols)

        print("Result of part 1: ", result1)

    elif part == '2':
        result2 = 0
        _, visited_pos, _ = find_guard_path(i_start, j_start, 'u', data, n_rows, n_cols)
        for i, j in visited_pos:
            if data[i][j] != '^' and data[i][j] != '#' and data[i][j]:
                tmp = data[i][j]
                data[i] =  data[i][0:j] + "#" + data[i][j+1:]
                _, _, is_loop = find_guard_path(i_start, j_start, 'u', data, n_rows, n_cols)
                if is_loop:
                    result2 += 1

                data[i] = data[i][0:j] + tmp + data[i][j+1:]

        print("Result of part 2: ", result2)