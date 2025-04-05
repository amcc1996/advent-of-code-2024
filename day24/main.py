import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def AND(a, b):
    return a & b

def OR(a, b):
    return a | b

def XOR(a, b):
    return a ^ b

MAP_OPERATIONS = {
    'AND': AND,
    'OR': OR,
    'XOR': XOR
}

def parse_data(data):
    wires = {}
    for line in data[0]:
        line_split = line.split(':')
        wires[line_split[0]] = int(line_split[1].strip())

    gates = []
    for line in data[1]:
        line_split = line.split(' ')
        wire_input1 = line_split[0]
        op = MAP_OPERATIONS[line_split[1]]
        wire_input2 = line_split[2]
        wire_output = line_split[4]
        gates.append((wire_input1, wire_input2, op, wire_output))

    return wires, gates

def compute_number(wires):
    num = 0
    for wire in wires:
        if wire[0] == 'z':
            bit_pos = int(wire[1:])
            if wires[wire] == 1:
                num += 2 ** bit_pos

    return num

def run_circuit(wires, gates):
    n_gates = len(gates)
    count = 0
    gate_done = [False] * n_gates
    while count < n_gates:
        for i in range(n_gates):
            wire_input1, wire_input2, op, wire_output = gates[i]
            if (wire_input1 in wires and wire_input2 in wires) and not gate_done[i]:
                wires[wire_output] = op(wires[wire_input1], wires[wire_input2])
                gate_done[i] = True
                count += 1

    return compute_number(wires)

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)
    wires, gates = parse_data(data)

    if part == '1':
        res = run_circuit(wires, gates)

        print("Result of part 1: {0}".format(res))

    # elif part == '2':
    #     computers = build_computers(data)
    #     groups = find_computer_groups(computers)
    #     res = find_largest_group(groups)

    #     print("Result of part 2: {0}".format(res))