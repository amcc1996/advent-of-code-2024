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

def find_wide_boxes(i, j, direction):
    i_next = i
    j_next = j
    wide_boxes = []
    blocked = False
    if direction in ['<', '>']:
        while warehouse[i_next][j_next] == ']' or warehouse[i_next][j_next] == '[':
            if warehouse[i_next][j_next] == '[':
                wide_boxes.append(((i_next, j_next), (i_next, j_next + 1)))

            i_next, j_next = new_pos(i_next, j_next, direction)


        if warehouse[i_next][j_next] == '#':
            blocked = True

    elif direction in ['v', '^']:
        if (warehouse[i_next][j_next] == '['):
            queue = [((i_next, j_next), (i_next, j_next + 1))]
        elif (warehouse[i_next][j_next] == ']'):
            queue = [((i_next, j_next - 1), (i_next, j_next))]

        while len(queue) > 0:
            (i_left, j_left), (i_right, j_right) = queue.pop(0)
            wide_boxes.append(((i_left, j_left), (i_right, j_right)))
            i_left, j_left = new_pos(i_left, j_left, direction)
            i_right, j_right = new_pos(i_right, j_right, direction)

            if (warehouse[i_left][j_left] == '['):
                box = ((i_left, j_left), (i_left, j_left+1))
                if (box not in queue):
                    queue.append(box)

            elif (warehouse[i_left][j_left] == ']'):
                box = ((i_left, j_left-1), (i_left, j_left))
                if (box not in queue):
                    queue.append(box)

            elif (warehouse[i_left][j_left] == '#'):
                blocked = True
                break

            if (warehouse[i_right][j_right] == '['):
                box = ((i_right, j_right), (i_right, j_right+1))
                if (box not in queue):
                    queue.append(box)

            elif (warehouse[i_right][j_right] == ']'):
                box = ((i_right, j_right-1), (i_right, j_right))
                if (box not in queue):
                    queue.append(box)

            elif (warehouse[i_right][j_right] == '#'):
                blocked = True
                break

    return wide_boxes, blocked

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

def move_robot_wide_boxes(i, j, move, wareshouse):
    i_new, j_new = new_pos(i, j, move)
    if wareshouse[i_new][j_new] == '.':
        wareshouse[i][j] = '.'
        wareshouse[i_new][j_new] = '@'

        return i_new, j_new

    elif warehouse[i_new][j_new] == '#':
        return i, j

    elif warehouse[i_new][j_new] == '[' or warehouse[i_new][j_new] == ']':
        wide_boxes, blocked = find_wide_boxes(i_new, j_new, move)
        if not blocked:
            new_boxes = []
            for box in wide_boxes:
                i_left, j_left = new_pos(box[0][0], box[0][1], move)
                i_right, j_right = new_pos(box[1][0], box[1][1], move)
                new_boxes.append(((i_left, j_left), (i_right, j_right)))

            for box in wide_boxes:
                warehouse[box[0][0]][box[0][1]] = '.'
                warehouse[box[1][0]][box[1][1]] = '.'

            for new_box in new_boxes:
                warehouse[new_box[0][0]][new_box[0][1]] = '['
                warehouse[new_box[1][0]][new_box[1][1]] = ']'

            warehouse[i][j] = '.'
            warehouse[i_new][j_new] = '@'

            return i_new, j_new

        else:
            return i, j

def compute_gps_coordinates(warehouse):
    res = 0
    for i in range(len(warehouse)):
        for j in range(len(warehouse[0])):
            if warehouse[i][j] == 'O' or warehouse[i][j] == '[':
                res += i * 100+ j

    return res

def print_warehouse(warehouse):
    for row in warehouse:
        print("".join(row))

def transform_warehouse(wareshouse):
    new_warehouse = []
    for i in range(len(wareshouse)):
        new_row = []
        for j in range(len(wareshouse[0])):
            if wareshouse[i][j] == '#':
                new_row.extend(['#', '#'])
            elif wareshouse[i][j] == 'O':
                new_row.extend(['[', ']'])
            elif wareshouse[i][j] == '.':
                new_row.extend(['.', '.'])
            elif wareshouse[i][j] == '@':
                new_row.extend(['@', '.'])

        new_warehouse.append(new_row)

    return new_warehouse

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
        warehouse = transform_warehouse(warehouse)
        for i in range(len(warehouse)):
            for j in range(len(warehouse[0])):
                if warehouse[i][j] == '@':
                    i_robot = i
                    j_robot = j
                    break

        result2 = 0
        for command in commands:
            # print(command)
            i_robot, j_robot = move_robot_wide_boxes(i_robot, j_robot, command, warehouse)
            # print_warehouse(warehouse)

        result2 = compute_gps_coordinates(warehouse)
        print("Result of part 2: ", result2)