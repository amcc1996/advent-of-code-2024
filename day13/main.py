import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def compute_find_cheapest(x_A, y_A, x_B, y_B, x_prize, y_prize, n_max, price_A, price_B):
    cheapest = 0
    nA = 0
    nB = 0
    is_first = True
    for i_A in range(1, n_max+1):
        for i_B in range(1, n_max+1):
            if (i_A * x_A + i_B * x_B) == x_prize and (i_A * y_A + i_B * y_B) == y_prize:
                cost = i_A * price_A + i_B * price_B
                if cost < cheapest or is_first:
                    cheapest = cost
                    nA = i_A
                    nB = i_B
                    is_first = False

    return cheapest, nA, nB

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)

    x_A = []
    y_A = []
    x_B = []
    y_B = []
    x_prize = []
    y_prize = []
    for block in data:
        x_A.append(int(block[0].split()[2][2:-1]))
        y_A.append(int(block[0].split()[3][2:]))
        x_B.append(int(block[1].split()[2][2:-1]))
        y_B.append(int(block[1].split()[3][2:]))
        x_prize.append(int(block[2].split()[1][2:-1]))
        y_prize.append(int(block[2].split()[2][2:]))

    n_max = 100
    price_A = 3
    price_B = 1

    if part == '1':
        result1 = 0
        for i in range(len(x_A)):
            res, nA, nB = compute_find_cheapest(x_A[i], y_A[i], x_B[i], y_B[i], x_prize[i], y_prize[i], n_max, price_A, price_B)
            result1 += res

        print("Result of part 1: ", result1)

    elif part == '2':
        result2 = 0

        print("Result of part 2: ", result2)