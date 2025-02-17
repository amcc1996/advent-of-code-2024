import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def find_possibilities(pos, design, towels, map_first_char_range, check=False):
    if pos >= len(design):
        return 1

    if design[pos] not in map_first_char_range:
        return 0

    start = map_first_char_range[design[pos]][0]
    end = map_first_char_range[design[pos]][1]

    res = 0
    for i in range(start, end + 1):
        if design[pos:pos + len(towels[i])] == towels[i]:
            aux = find_possibilities(pos + len(towels[i]), design, towels, map_first_char_range, check)
            res += aux
            if check and aux > 0:
                break

    return res

def find_possibilities_with_cache(pos, design, towels, map_first_char_range, cache):
    if pos >= len(design):
        return 1

    if design[pos] not in map_first_char_range:
        return 0

    if design[pos:] in cache:
        return cache[design[pos:]]

    start = map_first_char_range[design[pos]][0]
    end = map_first_char_range[design[pos]][1]

    res = 0
    for i in range(start, end + 1):
        if design[pos:pos + len(towels[i])] == towels[i]:
            aux = find_possibilities_with_cache(pos + len(towels[i]), design, towels, map_first_char_range, cache)
            res += aux

    cache[design[pos:]] = res
    return res

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)

    towels = [x.strip() for x in data[0][0].split(",")]
    towels.sort(key=lambda x: x[0], reverse=False)
    design_list = data[1]

    # Create a map between the first letter of the start and end of the section in the towels list
    map_first_char_range = {}
    for i, towel in enumerate(towels):
        if towel[0] not in map_first_char_range:
            map_first_char_range[towel[0]] = [i, i]
        else:
            map_first_char_range[towel[0]][1] = i

    if part == '1':
        result1 = 0
        for design in design_list:
            pos = 0
            n_combinations =  find_possibilities(pos, design, towels, map_first_char_range, check=True)
            if n_combinations > 0:
                result1 += 1

        print("Result of part 1: ", result1)

    elif part == '2':
        result2 = 0
        for design in design_list:
            pos = 0
            cache = {}
            n_combinations =  find_possibilities_with_cache(pos, design, towels, map_first_char_range, cache)
            print(n_combinations)
            result2 += n_combinations

        print("Result of part 2: ", result2)
