import sys

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
    data = f.readlines()

if part == '1':
    col1 = []
    col2 = []
    for line in data:
        line_split = line.split()
        col1.append(int(line.split()[0]))
        col2.append(int(line.split()[1]))

    col1.sort()
    col2.sort()
    result1 = sum(abs(x1 - x2) for x1, x2 in zip(col1, col2))
    print("Result of part 1: ", result1)

elif part == '2':
    col1 = []
    col2 = []
    for line in data:
        line_split = line.split()
        col1.append(int(line.split()[0]))
        col2.append(int(line.split()[1]))

    col1.sort()
    col2.sort()

    # for i in col1:
    #     for j in col2:
    #         if i == j:
    #             print(i)

    idx1 = 0
    idx2 = 0
    counter2 = 0
    result2 = 0
    while idx1 < len(col1) and idx2 < len(col2):
        print(col1[idx1], col2[idx2])
        if col1[idx1] == col2[idx2]:
            # move the pointer to the end of the repeated elements
            counter1 = 0
            repeated1 = True
            while (repeated1):
                if col1[idx1 + counter1] == col1[idx1]:
                    counter1 += 1
                else:
                    repeated1 = False

                if (idx1 + counter1) >= len(col1):
                    repeated1 = False

            # move the pointer to the end of the repeated elements
            counter2 = 0
            repeated2 = True
            while (repeated2):
                if col2[idx2 + counter2] == col2[idx2]:
                    counter2 += 1
                else:
                    repeated2 = False

                if (idx2 + counter2) >= len(col2):
                    repeated2 = False

            result2 += col1[idx1] * counter2 * counter1
            idx1 += counter1
            idx2 += counter2

        elif col1[idx1] < col2[idx2]:
            idx1 += 1
        else:
            idx2 += 1

    print("Result of part 2: ", result2)
