import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def transform_stone(x):
    if x == '0':
        return ['1']

    elif len(x) % 2 == 0:

        a = x[0:int(len(x)/2)]
        b = x[int(len(x)/2):]

        return [str(int(a)), str(int(b))]

    else:
        return [str(int(x) * 2024)]

def blink(stones):
    return [y for x in [transform_stone(stone) for stone in stones] for y in x]

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0][0].split(" ")

    if part == '1':
        stones = data
        for _ in range(25):
            stones = blink(stones)

        print("Result of part 1: ", len(stones))

    elif part == '2':
        stones = data
        for i in range(75):
            stones = blink(stones)

        print("Result of part 2: ", len(stones))