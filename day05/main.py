import sys

def check_order(line, map_after_before, output_wrong_pair=False):
    entries = [int(x) for x in line.split(',')]
    for i, entry in enumerate(entries[:-1]):
        if entry not in map_after_before:
            continue
        else:
            for j, other_entry in enumerate(entries[i+1:]):
                if other_entry in map_after_before[entry]:
                    if output_wrong_pair:
                        return False, i, j+i+1
                    else:
                        return False

    if output_wrong_pair:
        return True, None, None
    else:
        return True

def fix_order(line, map_after_before):
    correct = False
    while not correct:
        correct, i, j = check_order(line, map_after_before, output_wrong_pair=True)
        if not correct:
            line_split = line.split(',')
            line_split[i], line_split[j] = line_split[j], line_split[i]
            line = ','.join(line_split)

    return line

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
    lines = f.read().splitlines()

map_before_after = {}
map_after_before = {}
ibreak = None
for i, line in enumerate(lines):
    if len(line) == 0:
        ibreak = i
        break

    line_split = [int(x) for x in line.split('|')]
    if line_split[0] in map_before_after:
        map_before_after[line_split[0]].append(line_split[1])
    else:
        map_before_after[line_split[0]] =[line_split[1]]

    if line_split[1] in map_after_before:
        map_after_before[line_split[1]].append(line_split[0])
    else:
        map_after_before[line_split[1]] =[line_split[0]]

data = lines[ibreak+1:]

if part == '1':
    result1 = 0
    for line in data:
        if check_order(line, map_after_before):
            result1 += int(line.split(',')[int(len(line.split(',')) / 2)])

    print("Result of part 1: ", result1)

elif part == '2':
    result2 = 0
    for line in data:
        if check_order(line, map_after_before):
            continue

        new_line = fix_order(line, map_after_before)
        result2 += int(new_line.split(',')[int(len(new_line.split(',')) / 2)])

    print("Result of part 2: ", result2)

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