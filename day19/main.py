import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def find_possibilities(pos, design, towels, check=False):
    print(pos)
    if pos >= len(design):
        return 1

    res = 0
    for i in range(len(towels)):
        if design[pos:pos + len(towels[i])] == towels[i]:
            aux = find_possibilities(pos + len(towels[i]), design, towels)
            res += aux
            if check and aux > 0:
                break

    return res

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)

    towels = [x.strip() for x in data[0][0].split(",")]
    design_list = data[1]

    if part == '1':
        result1 = 0
        for design in design_list:
            print("Design: ", design)
            pos = 0
            n_combinations =  find_possibilities(pos, design, towels, check=True)
            if n_combinations > 0:
                result1 += 1

        print("Result of part 1: ", result1)

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