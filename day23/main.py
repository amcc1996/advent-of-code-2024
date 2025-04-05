import os
import sys

import itertools

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

def compute_neighbours_array(computer, groups):
    array = [[False for _ in range(len(groups))] for _ in range(len(groups))]
    for i in range(len(groups[computer])):
        for j in range(len(groups[computer])):
            if groups[computer][j] in groups[groups[computer][i]]:
                array[i][j] = True

    return array

def compute_maximum_closed_group_around_node(computer, groups, visited, threshold=-float('inf')):
    found = False
    max_group = set()
    max_group_size = threshold
    neighbours_array = compute_neighbours_array(computer, groups)
    for i in range(len(neighbours_array)):
        j_list = [x for x in range(len(neighbours_array)) if neighbours_array[i][x]]
        for group_size in range(len(j_list) + 1, 0, -1):
            if group_size <= threshold:
                break

            for j_list_combination in itertools.combinations(j_list, group_size):
                group = set(groups[computer][x] for x in j_list_combination)
                if group in visited:
                    continue

                visited.add(tuple(sorted(group)))
                valid = True
                for ii in range(len(j_list_combination)):
                    for jj in range(len(j_list_combination)):
                        if not neighbours_array[j_list_combination[ii]][j_list_combination[jj]]:
                            valid = False
                            break

                if valid:
                    found = True
                    max_group = group
                    max_group_size = len(group)
                    break

        if found:
            break

    return max_group, max_group_size, found

def find_largest_group(groups):
    threshold = -float('inf')
    visited = set()
    largest_group = None
    largest_group_size = None
    for computer in groups:
        max_group, max_group_size, found = compute_maximum_closed_group_around_node(computer, groups, visited, threshold)
        if found:
            largest_group = max_group
            largest_group_size = max_group_size
            threshold = max_group_size

    return ",".join(sorted(largest_group))

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    if part == '1':
        computers = build_computers(data)
        groups = find_computer_groups(computers)
        res = count_groups_with_3_and_t(groups)

        print("Result of part 1: {0}".format(res))

    elif part == '2':
        computers = build_computers(data)
        groups = find_computer_groups(computers)
        res = find_largest_group(groups)

        print("Result of part 2: {0}".format(res))