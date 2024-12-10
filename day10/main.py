import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def walk(i, j, last_height, summit_list, data, n_rows, n_cols, count_paths=False):
    if i < 0 or i >= n_rows or j < 0 or j >= n_cols:
        return 0

    elif int(data[i][j]) - last_height != 1:
        return 0

    elif int(data[i][j]) == 9:
        if count_paths:
            return 1
        else:
            if (i,j) not in summit_list:
                summit_list.append((i,j))
                return 1
            else:
                return 0

    else:
        top_score    = walk(i-1, j, int(data[i][j]), summit_list, data, n_rows, n_cols, count_paths)
        bottom_score = walk(i+1, j, int(data[i][j]), summit_list, data, n_rows, n_cols, count_paths)
        left_score   = walk(i, j-1, int(data[i][j]), summit_list, data, n_rows, n_cols, count_paths)
        right_score  = walk(i, j+1, int(data[i][j]), summit_list, data, n_rows, n_cols, count_paths)

        return top_score + bottom_score + left_score + right_score

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    trailhead = []
    n_rows = len(data)
    n_cols = len(data[0])

    if part == '1':
        result1 = 0
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == '0':
                    trailhead.append((i,j))
                    summit_list = []
                    score = walk(i, j, -1, summit_list, data, n_rows, n_cols)
                    result1 += score

        print("Result of part 1: ", result1)

    elif part == '2':
        result2 = 0
        for i in range(len(data)):
            for j in range(len(data[i])):
                if data[i][j] == '0':
                    trailhead.append((i,j))
                    summit_list = []
                    score = walk(i, j, -1, summit_list, data, n_rows, n_cols, True)
                    result2 += score

        print("Result of part 2: ", result2)