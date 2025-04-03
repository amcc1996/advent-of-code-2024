import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def mix(secret_number, value):
    return secret_number ^ value

def prune(secret_number):
    return secret_number % 16777216

def generate_secret_number(initial_secret_number):
    secret_number = initial_secret_number
    secret_number = prune(mix(secret_number, 64 * secret_number))
    secret_number = prune(mix(secret_number, int(secret_number / 32)))
    secret_number = prune(mix(secret_number, 2048 * secret_number))

    return secret_number

def generate_nth_secret_numbers(initial_secret_number, n):
    secret_number = initial_secret_number
    for i in range(n):
        secret_number = generate_secret_number(secret_number)

    return secret_number

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    if part == '1':
        res = 0
        N = 2000
        for number in [int(x) for x in data]:
            secret_number = generate_nth_secret_numbers(number, N)
            print(number, secret_number)
            res += secret_number

        print("Result of part 1: {0}".format(res))

    # elif part == '2':
    #     # Debug
    #     # -----
    #     # dir_code = '<vA>^AAv<<A>>^AvA<^A>Av<<A>>^AvA^A' # Easy after two parse
    #     # dir_code = '>>vA^A' # Easy
    #     # dir_code = 'vAA<A>^A<A>A' # Easy after one parse
    #     # print("Dir code\n{0}".format(dir_code))
    #     # print("Dir code blocks")
    #     # print(convert_dir_code_to_blocks(dir_code))
    #     # print("Dir code parsed")
    #     # print(parse_dir_code(dir_code, map_direction_and_position_to_directions))
    #     # print("Dir code parsed blocks [0]")
    #     # print(convert_dir_code_to_blocks(parse_dir_code(dir_code, map_direction_and_position_to_directions)[0]))
    #     # print("Dir code parsed blocks dictionaries")
    #     # print(parse_dir_code_blocks(convert_dir_code_to_blocks(dir_code)))
    #     # print("Length of the original dir code blocks")
    #     # print(length_dir_code_block(convert_dir_code_to_blocks(dir_code)))
    #     # print("Length of the parsed dir code blocks")
    #     # print(dir_code)
    #     # print(convert_dir_code_to_blocks(dir_code))
    #     # print(length_dir_code_block(parse_dir_code_blocks(convert_dir_code_to_blocks(dir_code))[0]))
    #     # print(parse_dir_code_blocks(convert_dir_code_to_blocks(dir_code))[0])

    #     res = 0
    #     for code in data:
    #         # res += compute_minimal_complexity_part2_using_blocks_dfs(code, n_intermediate_pads=4)
    #         res += compute_minimal_complexity_part2_using_optimal_length_recursion(code, n_intermediate_pads=25)

    #     print("Result of part 2: {0}".format(res))