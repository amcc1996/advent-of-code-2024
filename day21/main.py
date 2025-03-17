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

    dir_string_list = []

    # Test vertical-horizontal
    failed_vertical_horizontal = False
    i_sign = 1 if i_end > i_start else -1
    for i in range(abs(i_end - i_start) + 1):
        failed_vertical_horizontal = failed_vertical_horizontal or keypad[i_start + i * i_sign][j_start] is None

    j_sign = 1 if j_end > j_start else -1
    for j in range(abs(j_end - j_start) + 1):
        failed_vertical_horizontal = failed_vertical_horizontal or keypad[i_end][j_start + j * j_sign] is None

    if not failed_vertical_horizontal:
        dir_string_list.append(vertical_dir_string + horizontal_dir_string)
        dir_string = dir_string_list[-1]

    # Test horizontal-vertical
    failed_horizontal_vertical = False
    j_sign = 1 if j_end > j_start else -1
    for j in range(abs(j_end - j_start) + 1):
        failed_horizontal_vertical = failed_horizontal_vertical or keypad[i_start][j_start + j * j_sign] is None

    i_sign = 1 if i_end > i_start else -1
    for i in range(abs(i_end - i_start) + 1):
        failed_horizontal_vertical = failed_horizontal_vertical or keypad[i_start + i * i_sign][j_end] is None

    if not failed_horizontal_vertical:
        dir_string_list.append(horizontal_dir_string + vertical_dir_string)
        dir_string = dir_string_list[-1]

    return dir_string

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

                    map_number_and_position_to_directions[NUMERICAL_KEYPAD[i][j]][NUMERICAL_KEYPAD[k][l]] = convert_relative_pos_to_directions(k, l, i, j, NUMERICAL_KEYPAD) + 'A'

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

                    map_direction_and_position_to_directions[DIRECTIONAL_KEYPAD[i][j]][DIRECTIONAL_KEYPAD[k][l]] = convert_relative_pos_to_directions(k, l, i, j, DIRECTIONAL_KEYPAD) + 'A'

    return map_direction_and_position_to_directions


def parse_num_code(code, map_number_and_position_to_directions):
    sequence = ''
    start_pos = 'A'
    for char in code:
        sequence += map_number_and_position_to_directions[char][start_pos]
        start_pos = char

    return sequence

def parse_dir_code(code, map_direction_and_position_to_directions):
    sequence = ''
    start_pos = 'A'
    for char in code:
        sequence += map_direction_and_position_to_directions[char][start_pos]
        start_pos = char

    return sequence

def compute_sequence_buttons(code, map_number_and_position_to_directions, map_direction_and_position_to_directions):
    print(" ")
    num_code = code
    print("Num code: {0}".format(num_code))
    dir_code_robot_1 = parse_num_code(num_code, map_number_and_position_to_directions)
    print("Dir code robot 1: {0}".format(dir_code_robot_1))
    dir_code_robot_2 = parse_dir_code(dir_code_robot_1, map_direction_and_position_to_directions)
    print("Dir code robot 2: {0}".format(dir_code_robot_2))
    dir_code_me = parse_dir_code(dir_code_robot_2, map_direction_and_position_to_directions)
    print("Dir code me: {0}".format(dir_code_me))

    return dir_code_me

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

    # elif part == '2':
    #     cheat_length = 20
    #     min_saving = 100
    #     distances, path = find_path_distance(i_start, j_start, i_end, j_end, maze, n_rows, n_cols)
    #     # print_path_distance(distances, maze)
    #     savings = compute_shortcut_savings(path, distances, n_rows, n_cols, cheat_length)
    #     res = count_savings_greater_than(savings, min_saving, verbose=True)

    #     print("Result of part 2: {0}".format(res))