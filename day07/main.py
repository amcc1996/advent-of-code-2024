import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def parse_operation(val, pos, nums, total):
    if pos == len(nums):
        return val == total

    elif val > total or nums[pos] > total:
        return False

    else:
        found_sum = parse_operation(val + nums[pos], pos + 1, nums, total)
        found_prod = parse_operation(val * nums[pos], pos + 1, nums, total)

        return found_sum or found_prod

def parse_operation_with_concatenation(val, pos, nums, total, pos_concat):
    if pos == len(nums):
        return val == total, pos_concat if val == total else []

    elif val > total or nums[pos] > total:
        return False, []

    else:
        found_sum, pos_concat = parse_operation_with_concatenation(val + nums[pos], pos + 1, nums, total, pos_concat)
        found_prod, pos_concat = parse_operation_with_concatenation(val * nums[pos], pos + 1, nums, total, pos_concat)
        found_concat, pos_concat = parse_operation_with_concatenation(int(str(val) + str(nums[pos])), pos + 1, nums, total, pos_concat)

        if found_concat:
            pos_concat.append(pos)

        return found_sum or found_prod or found_concat, pos_concat

def process_line(line, use_concat=False):
    line_split = line.split()
    total = int(line_split[0].split(':')[0])
    nums = [int(x) for x in line_split[1:]]
    if not use_concat:
        return parse_operation(nums[0], 1, nums, total), total
    else:
        found, pos_concat = parse_operation_with_concatenation(nums[0], 1, nums, total, [])
        return found, total

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    if part == '1':
        result1 = sum([x[1] for x in [process_line(line) for line in data] if x[0]])

        print("Result of part 1: ", result1)

    elif part == '2':
        result2 = sum([x[1] for x in [process_line(line, True) for line in data] if x[0]])

        print("Result of part 2: ", result2)