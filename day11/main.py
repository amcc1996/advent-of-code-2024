import os
import sys
from functools import lru_cache

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

def search(x, depth, stones_cache):
    if (x, depth) in stones_cache:
        return stones_cache[(x, depth)]

    else:
        if depth == 0:
            return 1
        else:
            if x == '0':
                res = search('1', depth - 1, stones_cache)
            elif len(x) % 2 == 0:
                a = str(int(x[0:int(len(x)/2)]))
                b = str(int(x[int(len(x)/2):]))
                res = search(a, depth - 1, stones_cache) + search(b, depth - 1, stones_cache)
            else:
                res = search(str(int(x) * 2024), depth - 1, stones_cache)

            stones_cache[(x, depth)] = res
            return res

@lru_cache(maxsize=32)
def search_with_cache(x, depth):
    if depth == 0:
        return 1
    else:
        if x == '0':
            res = search('1', depth - 1, stones_cache)
        elif len(x) % 2 == 0:
            a = str(int(x[0:int(len(x)/2)]))
            b = str(int(x[int(len(x)/2):]))
            res = search(a, depth - 1, stones_cache) + search(b, depth - 1, stones_cache)
        else:
            res = search(str(int(x) * 2024), depth - 1, stones_cache)

        return res

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
        stones_cache = {}
        n_blinks = 75

        print("Result of part 2        : ", sum(search(stone, n_blinks, stones_cache) for stone in stones))
        print("Result of part 2 (cache): ", sum(search_with_cache(stone, n_blinks) for stone in stones))