import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def split_computers(string):
    return string.split('-')[0], string.split('-')[1]

def build_computers(data):
    computers = []
    for line in data:
        computer1, computer2 = split_computers(line)
        computers.append((computer1, computer2))

    return computers

def find_computer_groups(computers):
    groups = {}
    for computer1, computer2 in computers:
        if computer1 not in groups:
            groups[computer1] = set()
        if computer2 not in groups:
            groups[computer2] = set()

        groups[computer1].add(computer1)
        groups[computer1].add(computer2)

        groups[computer2].add(computer1)
        groups[computer2].add(computer2)

    for computer in groups:
        groups[computer] = sorted(groups[computer])

    return groups

def count_groups_with_3_and_t(groups):
    groups_of_three = set()
    for computer in groups:
        for neighbour in groups[computer]:
            if (neighbour == computer):
                continue
            for other_neighbour in groups[neighbour]:
                if (other_neighbour == neighbour) or (other_neighbour == computer):
                    continue

                if (computer in groups[other_neighbour]):
                    groups_of_three.add(tuple(sorted((computer, neighbour, other_neighbour))))

    print("Groups of three:")
    for group in sorted(groups_of_three):
        print(group)

    count = 0
    for group in groups_of_three:
        for computer in group:
            if computer[0] == 't':
                # print(group)
                count += 1
                break

    return count

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    if part == '1':
        computers = build_computers(data)
        groups = find_computer_groups(computers)
        res = count_groups_with_3_and_t(groups)

        print("Result of part 1: {0}".format(res))

    elif part == '2':
        res = 0

        print("Result of part 2: {0}".format(res))