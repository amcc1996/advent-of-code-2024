import os
import sys

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
    n_intermediate_robots = 2

    num_code = code
    dir_code_robot_1_list = parse_num_code(num_code, map_number_and_position_to_directions)
    print(1, len(code))
    print(len(dir_code_robot_1_list), len(dir_code_robot_1_list[0]))

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
    print_map(map_number_and_position_to_directions)
    map_direction_and_position_to_directions = initialise_map_direction_and_position_to_directions()
    print_map(map_direction_and_position_to_directions)

    if part == '1':
        res = 0
        for code in data:
            sequence = compute_sequence_buttons(code, map_number_and_position_to_directions, map_direction_and_position_to_directions)
            res += compute_complexity(code, sequence)
            print("Code: {0}, Sequence: {1}, Length: {2}, Num: {3}".format(code, sequence, len(sequence), int(code.split('A')[0])))

        print("Result of part 1: {0}".format(res))

    elif part == '2':
        res = 0
        for code in data:
            sequence = compute_sequence_buttons_part2(code, map_number_and_position_to_directions, map_direction_and_position_to_directions)
            res += compute_complexity(code, sequence)
            print("Code: {0}, Sequence: {1}, Length: {2}, Num: {3}".format(code, sequence, len(sequence), int(code.split('A')[0])))

        print("Result of part 1: {0}".format(res))