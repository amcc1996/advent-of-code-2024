import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    if part == '1':
        result1 = 0
        for line in data:
            line_split = [int(x) for x in line.split()]
            line_diff = [line_split[i + 1] - line_split[i] for i in range(len(line_split) - 1)]
            if all([x * y > 0 for x, y in zip(line_diff[0:-1], line_diff[1:])]):
                min_diff = min([abs(x) for x in line_diff])
                max_diff = max([abs(x) for x in line_diff])
                if min_diff >= 1 and max_diff <=3:
                    result1 += 1

        print("Result of part 1: ", result1)

    elif part == '2':
        result2 = 0
        for line in data:
            line_split = [int(x) for x in line.split()]
            line_diff = [line_split[i + 1] - line_split[i] for i in range(len(line_split) - 1)]
            signs = [x * y > 0 for x, y in zip(line_diff[0:-1], line_diff[1:])]
            min_diff = min([abs(x) for x in line_diff])
            max_diff = max([abs(x) for x in line_diff])
            if all(signs) and min_diff >= 1 and max_diff <=3:
                    result2 += 1

            else:
                count = 0
                for i in range(len(line_split)):
                    new_line_split = [line_split[j] for j in range(len(line_split)) if j != i]
                    new_line_diff = [new_line_split[j + 1] - new_line_split[j] for j in range(len(new_line_split) - 1)]
                    new_signs = [x * y > 0 for x, y in zip(new_line_diff[0:-1], new_line_diff[1:])]
                    new_min_diff = min([abs(x) for x in new_line_diff])
                    new_max_diff = max([abs(x) for x in new_line_diff])
                    if all(new_signs) and new_min_diff >= 1 and new_max_diff <=3:
                        result2 += 1
                        break

        print("Result of part 2: ", result2)