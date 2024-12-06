import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def find_xmas(i, j, last_i, last_j, word, data, n_rows, n_cols):
    if i < 0 or i >= n_rows or j < 0 or j >= n_cols:
        return 0

    elif len(word) == 4:
        return 0

    elif ('XMAS' == word + data[i][j]):
        return 1

    elif ('XMAS'.find(word + data[i][j])) == 0:
        res = 0
        word = word + data[i][j]
        for new_i in [i - 1, i, i + 1]:
            for new_j in [j - 1, j, j + 1]:
                if len(word) > 1:
                    di = new_i - i
                    dj = new_j - j
                    old_di = i - last_i
                    old_dj = j - last_j
                    if sign(di) == sign(old_di) and sign(dj) == sign(old_dj):
                        res += find_xmas(new_i, new_j, i, j, word, data, n_rows, n_cols)
                else:
                    res += find_xmas(new_i, new_j, i, j, word, data, n_rows, n_cols)


        return res

    else:
        return 0

def find_x_mas(i, j, data, n_rows, n_cols):
    if i < 1 or i >= n_rows - 1 or j < 1 or j >= n_cols - 1:
        return 0

    if data[i][j] != 'A':
        return 0

    else:
        corners = [[data[i-1][j-1], data[i-1][j+1]], [data[i+1][j-1], data[i+1][j+1]]]
        if any([x not in ['S', 'M'] for x in [y for z in corners for y in z]]):
            return 0
        if corners[0][0] != corners[1][1] and corners[0][1] != corners[1][0]:
            return 1
        else:
            return 0

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    if part == '1':
        result1 = 0
        n_rows = len(data)
        n_cols = len(data[0])
        for i in range(n_rows):
            for j in range(n_cols):
                result1 += find_xmas(i, j, None, None, '', data, n_rows, n_cols)

        print("Result of part 1: ", result1)

    elif part == '2':
        result2 = 0
        n_rows = len(data)
        n_cols = len(data[0])
        for i in range(n_rows):
            for j in range(n_cols):
                result2 += find_x_mas(i, j, data, n_rows, n_cols)

        print("Result of part 2: ", result2)