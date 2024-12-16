import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def new_pos(i, j, move):
    if move == 'v':
        return i + 1, j
    elif move == '^':
        return i - 1, j
    elif move == '>':
        return i, j + 1
    elif move == '<':
        return i, j - 1

def find_boxes(i, j, direction):
    i_next = i
    j_next = j
    boxes = []
    while warehouse[i_next][j_next] == 'O':
        boxes.append((i_next, j_next))
        i_next, j_next = new_pos(i_next, j_next, direction)

    return boxes

def move_robot(i, j, move, wareshouse):
    i_new, j_new = new_pos(i, j, move)
    if wareshouse[i_new][j_new] == '.':
        wareshouse[i][j] = '.'
        wareshouse[i_new][j_new] = '@'

        return i_new, j_new

    elif warehouse[i_new][j_new] == '#':
        return i, j

    elif warehouse[i_new][j_new] == 'O':
        boxes = find_boxes(i_new, j_new, move)
        i_end_new, j_end_new = new_pos(boxes[-1][0], boxes[-1][1], move)
        if warehouse[i_end_new][j_end_new] == '.':
            for box in boxes[::-1]:
                i_box_new, j_box_new = new_pos(box[0], box[1], move)
                warehouse[i_box_new][j_box_new] = 'O'
                warehouse[box[0]][box[1]] = '.'

            warehouse[i][j] = '.'
            warehouse[i_new][j_new] = '@'

            return i_new, j_new

        else:
            return i, j

def compute_gps_coordinates(warehouse):
    res = 0
    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            if warehouse[i][j] == 'O':
                res += i * 100+ j

    return res

def print_warehouse(warehouse):
    for row in warehouse:
        print("".join(row))

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)

    warehouse = [[y for y in x] for x in data[0]]
    commands = "".join(data[1])

    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            if warehouse[i][j] == '@':
                i_robot = i
                j_robot = j
                break

    if part == '1':
        result1 = 0
        for command in commands:
            i_robot, j_robot = move_robot(i_robot, j_robot, command, warehouse)

        result1 = compute_gps_coordinates(warehouse)
        print("Result of part 1: ", result1)

    elif part == '2':
        result2 = 0
        print("Result of part 2: ", result2)