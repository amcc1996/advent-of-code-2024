import sys

def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def find_xmas(i, j, last_i, last_j, word, data, n_rows, n_cols):
    if i < 0 or i >= n_rows or j < 0 or j >= n_cols:
        return 0

    elif len(word) == 4:
        return 0

    elif ('XMAS' == word + data[i][j]):
        return 1

    elif ('XMAS'.find(word + data[i][j])) == 0:
        res = 0
        word = word + data[i][j]
        for new_i in [i - 1, i, i + 1]:
            for new_j in [j - 1, j, j + 1]:
                if len(word) > 1:
                    di = new_i - i
                    dj = new_j - j
                    old_di = i - last_i
                    old_dj = j - last_j
                    if sign(di) == sign(old_di) and sign(dj) == sign(old_dj):
                        res += find_xmas(new_i, new_j, i, j, word, data, n_rows, n_cols)
                else:
                    res += find_xmas(new_i, new_j, i, j, word, data, n_rows, n_cols)


        return res

    else:
        return 0

def find_x_mas(i, j, data, n_rows, n_cols):
    if i < 1 or i >= n_rows - 1 or j < 1 or j >= n_cols - 1:
        return 0

    if data[i][j] != 'A':
        return 0

    else:
        corners = [[data[i-1][j-1], data[i-1][j+1]], [data[i+1][j-1], data[i+1][j+1]]]
        print(data[i][j])
        print(corners[0])
        print(corners[1])
        if any([x not in ['S', 'M'] for x in [y for z in corners for y in z]]):
            return 0
        if corners[0][0] != corners[1][1] and corners[0][1] != corners[1][0]:
            return 1
        else:
            return 0

DATAFILE = 'data.txt'
VALIDATION_PT1 = 'validation-part1.txt'
VALIDATION_PT2 = 'validation-part2.txt'

if len(sys.argv) < 2:
    print('Usage: python main.py <part> [v]')
    sys.exit(1)

part = sys.argv[1]
validation = False
if len(sys.argv) > 2:
    validation = (sys.argv[2] == 'v')

datafile = DATAFILE
if validation:
    if part == '1':
        datafile = VALIDATION_PT1
    else:
        datafile = VALIDATION_PT2

with open(datafile) as f:
    data = f.read().splitlines()

if part == '1':
    result1 = 0
    n_rows = len(data)
    n_cols = len(data[0])
    for i in range(n_rows):
        for j in range(n_cols):
            result1 += find_xmas(i, j, None, None, '', data, n_rows, n_cols)

    print("Result of part 1: ", result1)

elif part == '2':
    result2 = 0
    n_rows = len(data)
    n_cols = len(data[0])
    for i in range(n_rows):
        for j in range(n_cols):
            result2 += find_x_mas(i, j, data, n_rows, n_cols)

    print("Result of part 1: ", result2)

# elif part == '2':
#     result2 = 0
#     data =''.join(data)
#     for line in [data]:
#         mul_pos   = find_substring_pos(line, "mul(")
#         do_pos    = [-1] + find_substring_pos(line, "do()") + [len(line) + 2]
#         dont_pos  = [-2] + find_substring_pos(line, "don't()") + [len(line) + 1]
#         print(len(do_pos), len(dont_pos))
#         for pos in mul_pos:
#             aux_do = [pos - x for x in do_pos if x < pos]
#             last_do   = do_pos[aux_do.index(min(aux_do))]
#             aux_dont = [pos - x for x in dont_pos if x < pos]
#             last_dont = dont_pos[aux_dont.index(min(aux_dont))]
#             word_split = line[pos+len('mul('):].split(')')[0].split(',')
#             if word_split[0].isnumeric() and word_split[1].isnumeric() and len(word_split) == 2:
#                 if last_do > last_dont:
#                     result2 += int(word_split[0]) * int(word_split[1])

#     print("Result of part 2: ", result2)