import os
import sys

import re
import functools
import itertools
import copy

from collections import deque

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def convert_relative_pos_to_directions(i_start, j_start, i_end, j_end, keypad):
    horizontal_dir_string = ''
    if j_end > j_start:
        horizontal_dir_string += abs(j_end - j_start) * '>'
    elif j_end < j_start:
        horizontal_dir_string += abs(j_end - j_start) * '<'

    vertical_dir_string = ''
    if i_end > i_start:
        vertical_dir_string += abs(i_end - i_start) * 'v'
    elif i_end < i_start:
        vertical_dir_string += abs(i_end - i_start) * '^'

    if i_end == i_start:
        return [horizontal_dir_string]

    elif j_end == j_start:
        return [vertical_dir_string]

    else:
        dir_string_list = []
        path = []
        j_sign = 1 if j_end > j_start else -1
        for j in range(abs(j_end - j_start) + 1):
            path.append((i_start, j_start + j * j_sign))

        i_sign = 1 if i_end > i_start else -1
        for i in range(abs(i_end - i_start) + 1):
            path.append((i_start + i * i_sign, j_end))

        if not any([keypad[i][j] is None for i, j in path]):
            dir_string_list.append(horizontal_dir_string + vertical_dir_string)

        path = []
        i_sign = 1 if i_end > i_start else -1
        for i in range(abs(i_end - i_start) + 1):
            path.append((i_start + i * i_sign, j_start))

        j_sign = 1 if j_end > j_start else -1
        for j in range(abs(j_end - j_start) + 1):
            path.append((i_end, j_start + j * j_sign))

        if not any([keypad[i][j] is None for i, j in path]):
            dir_string_list.append(vertical_dir_string + horizontal_dir_string)

        return dir_string_list

def initialise_map_number_and_position_to_directions():
    numbers = [x for y in NUMERICAL_KEYPAD for x in y if x is not None]
    map_number_and_position_to_directions = {}
    for i_num in range(len(numbers)):
        map_number_and_position_to_directions[numbers[i_num]] = {}
        for j_num in range(len(numbers)):
            map_number_and_position_to_directions[numbers[i_num]][numbers[j_num]] = None

    for i in range(len(NUMERICAL_KEYPAD)):
        for j in range(len(NUMERICAL_KEYPAD[i])):
            if NUMERICAL_KEYPAD[i][j] is None:
                continue

            for k in range(len(NUMERICAL_KEYPAD)):
                for l in range(len(NUMERICAL_KEYPAD[k])):
                    if NUMERICAL_KEYPAD[k][l] is None:
                        continue

                    map_number_and_position_to_directions[NUMERICAL_KEYPAD[i][j]][NUMERICAL_KEYPAD[k][l]] = [x + 'A' for x in convert_relative_pos_to_directions(k, l, i, j, NUMERICAL_KEYPAD)]

    return map_number_and_position_to_directions

def initialise_map_direction_and_position_to_directions():
    directions = [x for y in DIRECTIONAL_KEYPAD for x in y if x is not None]
    map_direction_and_position_to_directions = {}
    for i_dir in range(len(directions)):
        map_direction_and_position_to_directions[directions[i_dir]] = {}
        for j_dir in range(len(directions)):
            map_direction_and_position_to_directions[directions[i_dir]][directions[j_dir]] = None

    for i in range(len(DIRECTIONAL_KEYPAD)):
        for j in range(len(NUMERICAL_KEYPAD[i])):
            if DIRECTIONAL_KEYPAD[i][j] is None:
                continue

            for k in range(len(DIRECTIONAL_KEYPAD)):
                for l in range(len(DIRECTIONAL_KEYPAD[k])):
                    if DIRECTIONAL_KEYPAD[k][l] is None:
                        continue

                    map_direction_and_position_to_directions[DIRECTIONAL_KEYPAD[i][j]][DIRECTIONAL_KEYPAD[k][l]] = [x + 'A' for x in convert_relative_pos_to_directions(k, l, i, j, DIRECTIONAL_KEYPAD)]

    return map_direction_and_position_to_directions


def parse_num_code(code, map_number_and_position_to_directions):
    sequence_list = ['']
    start_pos = 'A'
    for char in code:
        parsed_code = map_number_and_position_to_directions[char][start_pos]
        aux = []
        for sequence in sequence_list:
            for parsed in parsed_code:
                aux.append(sequence + parsed)
        sequence_list = [x for x in aux]
        start_pos = char

    return sequence_list

def parse_dir_code(code, map_direction_and_position_to_directions):
    sequence_list = ['']
    start_pos = 'A'
    for char in code:
        parsed_code = map_direction_and_position_to_directions[char][start_pos]
        aux = []
        for sequence in sequence_list:
            for parsed in parsed_code:
                aux.append(sequence + parsed)
        sequence_list = [x for x in aux]
        start_pos = char

    return sequence_list

def compute_sequence_buttons(code, map_number_and_position_to_directions, map_direction_and_position_to_directions):
    num_code = code
    dir_code_robot_1_list = parse_num_code(num_code, map_number_and_position_to_directions)
    dir_code_robot_2_list = []
    for dir_code_robot_1 in dir_code_robot_1_list:
        dir_code_robot_2 = parse_dir_code(dir_code_robot_1, map_direction_and_position_to_directions)
        dir_code_robot_2_list.extend(dir_code_robot_2)
    dir_code_me_list = []
    for dir_code_robot_2 in dir_code_robot_2_list:
        dir_code_me = parse_dir_code(dir_code_robot_2, map_direction_and_position_to_directions)
        dir_code_me_list.extend(dir_code_me)

    # Find the shortest code
    min_length = float('inf')
    for dir_code_me in dir_code_me_list:
        if len(dir_code_me) < min_length:
            min_length = len(dir_code_me)
            min_dir_code_me = dir_code_me

    return min_dir_code_me

def compute_sequence_buttons_part2(code, map_number_and_position_to_directions, map_direction_and_position_to_directions):
    """Impossible.
    """
    n_intermediate_robots = 2

    num_code = code
    dir_code_robot_1_list = parse_num_code(num_code, map_number_and_position_to_directions)

    dir_code_robot_i_input_list = [x for x in dir_code_robot_1_list]
    for i in range(n_intermediate_robots):
        dir_code_robot_i_output_list = []
        for dir_code_robot_i_input in dir_code_robot_i_input_list:
            dir_code_robot_i_output = parse_dir_code(dir_code_robot_i_input, map_direction_and_position_to_directions)
            dir_code_robot_i_output_list.extend(dir_code_robot_i_output)

        dir_code_robot_i_input_list = [x for x in dir_code_robot_i_output_list]
        print(len(dir_code_robot_i_output_list), len(dir_code_robot_i_output_list[0]))

    dir_code_me_list = []
    for dir_code_robot_2 in dir_code_robot_i_output_list:
        dir_code_me = parse_dir_code(dir_code_robot_2, map_direction_and_position_to_directions)
        dir_code_me_list.extend(dir_code_me)

    # Find the shortest code
    min_length = float('inf')
    for dir_code_me in dir_code_me_list:
        if len(dir_code_me) < min_length:
            min_length = len(dir_code_me)
            min_dir_code_me = dir_code_me

    return min_dir_code_me

def print_map(map):
    for key in map:
        print(key)
        for key2 in map[key]:
            print(" ", key2, map[key][key2])

def compute_complexity(code, sequence):
    return len(sequence) * int(code.split('A')[0])

def convert_dir_code_to_blocks(dir_code):
    """This function converts a direction code to a list of blocks ending in A.
    Powered by co-pilot.

    Returns the code in a dicitonary with keys the blocks and values the number of times
    they appear in the parsed code.
    """
    # Step 1: Split after each 'A' using negative lookbehind
    splits = [x for x in re.split(r'(?<=A)', dir_code) if x]

    # Step 2: Handle case where dir_code doesn't end in 'A'
    if not dir_code.endswith('A'):
        splits[-1] = splits[-1] + 'A'

    blocks = {}
    for split in splits:
        if split in blocks:
            blocks[split] += 1
        else:
            blocks[split] = 1

    return blocks

@functools.cache
def parse_dir_code_block_memoized(dir_code):
    """This code parses the direction code block with memoization. It is similar to before
    but now returns each parsed code as a list of blocks ending in A and not as a string.
    In addition, this function is only expeceted to be called with a block that ends in A
    with maximum length 5.

    It returns a list of dictionaries where each dictionary contains the blocks and the number
    of times they appear in the parsed code.
    """
    parsed_code_list = ['']
    start_pos = 'A'
    for char in dir_code:
        parsed_char_list = map_direction_and_position_to_directions[char][start_pos]
        aux = []
        for code in parsed_code_list:
            for parsed_char in parsed_char_list:
                aux.append(code + parsed_char)
        parsed_code_list = [x for x in aux]
        start_pos = char

    parsed_code_blocks = []
    for parsed_code in parsed_code_list:
        parsed_blocks = {}
        for block, n_repeat in convert_dir_code_to_blocks(parsed_code).items():
            if block in parsed_blocks:
                parsed_blocks[block] += n_repeat
            else:
                parsed_blocks[block] = n_repeat
        parsed_code_blocks.append(parsed_blocks)

    return parsed_code_blocks

def parse_dir_code_blocks(blocks):
    parsed_individual_blocks = []
    for block in blocks:
        aux = copy.deepcopy(parse_dir_code_block_memoized(block))
        for i in range(len(aux)):
            for key in aux[i]:
                aux[i][key] = aux[i][key] * blocks[block]

        parsed_individual_blocks.append(aux)

    parsed_blocks_list = []
    for combination in itertools.product(*parsed_individual_blocks):
        aux = {}
        for parsed_block in combination:
            for block in parsed_block:
                if block in aux:
                    aux[block] += parsed_block[block]
                else:
                    aux[block] = parsed_block[block]

        parsed_blocks_list.append(aux)

    return parsed_blocks_list

def length_dir_code_block(blocks):
    total_length = 0
    for block, count in blocks.items():
        total_length += len(block) * count

    return total_length

def compute_minimal_complexity_part2_using_blocks_dfs(num_code, n_intermediate_pads=25):
    """Impossible.
    """
    num = int(code.split('A')[0])
    depth = 0

    dir_code_robot_1_list = parse_num_code(num_code, map_number_and_position_to_directions)
    dir_code_robot_1_list_blocks = [convert_dir_code_to_blocks(x) for x in dir_code_robot_1_list]

    queue = deque([(x, length_dir_code_block(x), depth) for x in dir_code_robot_1_list_blocks])
    min_length = float('inf')
    count = 0
    while queue:
        blocks, length, depth = queue.pop()
        count += 1
        print(count, depth)
        if depth == n_intermediate_pads:
            if length < min_length:
                min_length = length
            continue

        if length >= min_length:
            continue

        parsed_blocks = parse_dir_code_blocks(blocks)
        for parsed_block in parsed_blocks:
            queue.append((parsed_block, length_dir_code_block(parsed_block), depth + 1))

    print(num, min_length)
    return num * min_length

@functools.cache
def compute_shortest_length(dir_code, depth):
    parsed_code_blocks = parse_dir_code_block_memoized(dir_code)
    if depth == 1:
        return min([length_dir_code_block(x) for x in parsed_code_blocks])
    else:
        list_lengths = []
        for parsed_blocks in parsed_code_blocks:
            length = 0
            for block, count in parsed_blocks.items():
                length += count * compute_shortest_length(block, depth - 1)

            list_lengths.append(length)

        return min(list_lengths)

def compute_minimal_complexity_part2_using_optimal_length_recursion(num_code, n_intermediate_pads=25):
    """Impossible.
    """
    num = int(code.split('A')[0])
    depth = 0

    dir_code_robot_1_list = parse_num_code(num_code, map_number_and_position_to_directions)
    dir_code_robot_1_list_blocks = [convert_dir_code_to_blocks(x) for x in dir_code_robot_1_list]

    list_lengths = []
    for blocks in dir_code_robot_1_list_blocks:
        length = 0
        for block, count in blocks.items():
            length += count * compute_shortest_length(block, n_intermediate_pads)

        list_lengths.append(length)

    print(num, min(list_lengths))
    return num * min(list_lengths)

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    NUMERICAL_KEYPAD = [
        ['7', '8', '9'],
        ['4', '5', '6'],
        ['1', '2', '3'],
        [None, '0', 'A']
    ]

    DIRECTIONAL_KEYPAD = [
        [None, '^', 'A'],
        ['<', 'v', '>'],
    ]

    map_number_and_position_to_directions = initialise_map_number_and_position_to_directions()
    # print_map(map_number_and_position_to_directions)
    map_direction_and_position_to_directions = initialise_map_direction_and_position_to_directions()
    # print_map(map_direction_and_position_to_directions)

    if part == '1':
        res = 0
        for code in data:
            sequence = compute_sequence_buttons(code, map_number_and_position_to_directions, map_direction_and_position_to_directions)
            res += compute_complexity(code, sequence)
            print("Code: {0}, Sequence: {1}, Length: {2}, Num: {3}".format(code, sequence, len(sequence), int(code.split('A')[0])))

        print("Result of part 1: {0}".format(res))

    elif part == '2':
        # Debug
        # -----
        # dir_code = '<vA>^AAv<<A>>^AvA<^A>Av<<A>>^AvA^A' # Easy after two parse
        # dir_code = '>>vA^A' # Easy
        # dir_code = 'vAA<A>^A<A>A' # Easy after one parse
        # print("Dir code\n{0}".format(dir_code))
        # print("Dir code blocks")
        # print(convert_dir_code_to_blocks(dir_code))
        # print("Dir code parsed")
        # print(parse_dir_code(dir_code, map_direction_and_position_to_directions))
        # print("Dir code parsed blocks [0]")
        # print(convert_dir_code_to_blocks(parse_dir_code(dir_code, map_direction_and_position_to_directions)[0]))
        # print("Dir code parsed blocks dictionaries")
        # print(parse_dir_code_blocks(convert_dir_code_to_blocks(dir_code)))
        # print("Length of the original dir code blocks")
        # print(length_dir_code_block(convert_dir_code_to_blocks(dir_code)))
        # print("Length of the parsed dir code blocks")
        # print(dir_code)
        # print(convert_dir_code_to_blocks(dir_code))
        # print(length_dir_code_block(parse_dir_code_blocks(convert_dir_code_to_blocks(dir_code))[0]))
        # print(parse_dir_code_blocks(convert_dir_code_to_blocks(dir_code))[0])

        res = 0
        for code in data:
            # res += compute_minimal_complexity_part2_using_blocks_dfs(code, n_intermediate_pads=4)
            res += compute_minimal_complexity_part2_using_optimal_length_recursion(code, n_intermediate_pads=25)

        print("Result of part 2: {0}".format(res))