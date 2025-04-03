import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

MAX_VALUE = 9

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

def generate_list_secret_numbers_and_diffs(initial_secret_number, n):
    secret_numbers_list = [initial_secret_number]
    old_secret_number = initial_secret_number
    diffs = []
    for i in range(n):
        new_secret_number = generate_secret_number(old_secret_number)
        diffs.append(new_secret_number % 10 - old_secret_number % 10)
        secret_numbers_list.append(new_secret_number)
        old_secret_number = new_secret_number

    return secret_numbers_list, diffs

def num2id(number):
    return number + MAX_VALUE

def id2num(id):
    return id - MAX_VALUE

def initialise_counting_array():
    count = []
    for _ in range(-MAX_VALUE, MAX_VALUE+1):
        aux_j_list = []
        for _ in range(-MAX_VALUE, MAX_VALUE+1):
            aux_k_list = []
            for _ in range(-MAX_VALUE, MAX_VALUE+1):
                aux_l_list = []
                for _ in range(-MAX_VALUE, MAX_VALUE+1):
                    aux_l_list.append(0)

                aux_k_list.append(aux_l_list)

            aux_j_list.append(aux_k_list)

        count.append(aux_j_list)

    return count

def reset_used_list(used_list):
    for i in range(len(used_list)):
        for j in range(len(used_list[i])):
            for k in range(len(used_list[i][j])):
                for l in range(len(used_list[i][j][k])):
                    used_list[i][j][k][l] = 0

    return used_list

def find_price(secret_number_list, diffs, price_list, used_list):
    for pos in range(len(diffs) - 3):
        num = secret_number_list[pos + 4] % 10
        i = diffs[pos]
        j = diffs[pos + 1]
        k = diffs[pos + 2]
        l = diffs[pos + 3]

        i_pos = num2id(i)
        j_pos = num2id(j)
        k_pos = num2id(k)
        l_pos = num2id(l)

        if (used_list[i_pos][j_pos][k_pos][l_pos] != 0):
            continue

        price_list[i_pos][j_pos][k_pos][l_pos] += num
        used_list[i_pos][j_pos][k_pos][l_pos] = 1

def compute_maximum_price(data, N):
    price_list = initialise_counting_array()
    used_list = initialise_counting_array()
    for number in data:
        print("Processing number: {0}".format(number))
        secret_numbers_list, diffs = generate_list_secret_numbers_and_diffs(number, N)
        find_price(secret_numbers_list, diffs, price_list, used_list)
        reset_used_list(used_list)

    max_price = -float('inf')
    max_i_pos = 0
    max_j_pos = 0
    max_k_pos = 0
    max_l_pos = 0
    for i_pos in range(len(price_list)):
        for j_pos in range(len(price_list[i_pos])):
            for k_pos in range(len(price_list[i_pos][j_pos])):
                for l_pos in range(len(price_list[i_pos][j_pos][k_pos])):
                    if price_list[i_pos][j_pos][k_pos][l_pos] > max_price:
                        max_price = price_list[i_pos][j_pos][k_pos][l_pos]
                        max_i_pos = i_pos
                        max_j_pos = j_pos
                        max_k_pos = k_pos
                        max_l_pos = l_pos

    max_i = id2num(max_i_pos)
    max_j = id2num(max_j_pos)
    max_k = id2num(max_k_pos)
    max_l = id2num(max_l_pos)

    # print("Maximum price: {0}".format(max_price))
    # print("Maximum sequence: {0}".format((max_i, max_j, max_k, max_l)))

    return max_price, (max_i, max_j, max_k, max_l)

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    if part == '1':
        res = 0
        N = 2000
        for number in [int(x) for x in data]:
            secret_number = generate_nth_secret_numbers(number, N)
            # print(number, secret_number)
            res += secret_number

        print("Result of part 1: {0}".format(res))

    elif part == '2':
        N = 2000
        max_price, max_sequence = compute_maximum_price([int(x) for x in data], N)

        print("Result of part 2: {0}".format(max_price))