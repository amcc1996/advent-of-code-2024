import os
import sys


sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def identify_keys_and_locks(data):
    keys_heights = []
    locks_heights = []

    n_rows = len(data[0])
    n_cols = len(data[0][0])

    for block in data:
        heights = []

        # Lock
        if block[0][0] == '#':
            for j in range(n_cols):
                count = 0
                for i in range(1, n_rows):
                    if block[i][j] == '#':
                        count += 1
                    else:
                        break

                heights.append(count)

            locks_heights.append(heights)

        # Lock
        if block[-1][0] == '#':
            for j in range(n_cols):
                count = 0
                for i in range(n_rows - 2, -1, -1):
                    if block[i][j] == '#':
                        count += 1
                    else:
                        break

                heights.append(count)

            keys_heights.append(heights)

    return keys_heights, locks_heights, n_rows, n_cols

def check_key_lock_pairs(key_heights, lock_heights, n_rows, n_cols):
    fit = True
    for j in range(n_cols):
        if key_heights[j] + lock_heights[j] > n_rows - 2:
            fit = False
            break

    return fit

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)

    if part == '1':
        res = 0
        keys_heights, locks_heights, n_rows, n_cols = identify_keys_and_locks(data)
        for key in keys_heights:
            for lock in locks_heights:
                if check_key_lock_pairs(key, lock, n_rows, n_cols):
                    res += 1

        print("Result of part 1: {0}".format(res))

    elif part == '2':
        res = 0
        print("Result of part 2: {0}".format(res))