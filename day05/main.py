import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def check_order(line, map_after_before, output_wrong_pair=False):
    entries = [int(x) for x in line.split(',')]
    for i, entry in enumerate(entries[:-1]):
        if entry not in map_after_before:
            continue
        else:
            for j, other_entry in enumerate(entries[i+1:]):
                if other_entry in map_after_before[entry]:
                    if output_wrong_pair:
                        return False, i, j+i+1
                    else:
                        return False

    if output_wrong_pair:
        return True, None, None
    else:
        return True

def fix_order(line, map_after_before):
    correct = False
    while not correct:
        correct, i, j = check_order(line, map_after_before, output_wrong_pair=True)
        if not correct:
            line_split = line.split(',')
            line_split[i], line_split[j] = line_split[j], line_split[i]
            line = ','.join(line_split)

    return line

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)

    map_before_after = {}
    map_after_before = {}
    ibreak = None
    for i, line in enumerate(data[0]):
        line_split = [int(x) for x in line.split('|')]
        if line_split[0] in map_before_after:
            map_before_after[line_split[0]].append(line_split[1])
        else:
            map_before_after[line_split[0]] =[line_split[1]]

        if line_split[1] in map_after_before:
            map_after_before[line_split[1]].append(line_split[0])
        else:
            map_after_before[line_split[1]] =[line_split[0]]

    data = data[1]

    if part == '1':
        result1 = 0
        for line in data:
            if check_order(line, map_after_before):
                result1 += int(line.split(',')[int(len(line.split(',')) / 2)])

        print("Result of part 1: ", result1)

    elif part == '2':
        result2 = 0
        for line in data:
            if check_order(line, map_after_before):
                continue

            new_line = fix_order(line, map_after_before)
            result2 += int(new_line.split(',')[int(len(new_line.split(',')) / 2)])

        print("Result of part 2: ", result2)