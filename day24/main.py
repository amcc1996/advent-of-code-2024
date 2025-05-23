import os
import sys

from collections import deque

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
    input_wires = {}
    for line in data[0]:
        line_split = line.split(':')
        input_wires[line_split[0]] = int(line_split[1].strip())

    gates = []
    map_output_wire_to_gate = {}
    n_gates = 0
    for line in data[1]:
        line_split = line.split(' ')
        wire_input1 = line_split[0]
        op = MAP_OPERATIONS[line_split[1]]
        wire_input2 = line_split[2]
        wire_output = line_split[4]
        n_gates += 1
        gates.append((wire_input1, wire_input2, op, wire_output))
        map_output_wire_to_gate[wire_output] = n_gates - 1

    return input_wires, gates, map_output_wire_to_gate

def compute_number(wires):
    num = 0
    for wire in wires:
        if wire[0] == 'z':
            bit_pos = int(wire[1:])
            if wires[wire] == 1:
                num += 2 ** bit_pos

    return num

def run_circuit(input_wires, gates, map_output_wire_to_gate):
    queue = deque()
    wires_values = {}
    all_wires = find_all_wires(input_wires, gates)
    for wire in all_wires:
        queue.append(wire)
        if wire in input_wires:
            wires_values[wire] = input_wires[wire]
        else:
            wires_values[wire] = None

    n_iter = 0
    while queue:
        n_iter += 1
        wire = queue.popleft()
        if wires_values[wire] is None:
            id_gate = map_output_wire_to_gate[wire]
            wire_input1, wire_input2, op, wire_output = gates[id_gate]
            print("Processing gate {0}: {1} = {2}({3}, {4})".format(id_gate, wire_output, op.__name__, wire_input1, wire_input2))
            if (wires_values[wire_input1] is not None) and (wires_values[wire_input2] is not None):
                wires_values[wire] = op(wires_values[wire_input1], wires_values[wire_input2])
            else:
                queue.append(wire)
                continue

    return compute_number(wires_values)

def find_all_wires(input_wires, gates):
    all_wires = set()
    for wire in input_wires:
        all_wires.add(wire)

    for gate in gates:
        wire_input1, wire_input2, op, wire_output = gate
        all_wires.add(wire_input1)
        all_wires.add(wire_input2)
        all_wires.add(wire_output)

    return sorted(all_wires)

def extract_output_wires(all_wires):
    output_wires = []
    for wire in all_wires:
        if wire[0] == 'z':
            output_wires.append(wire)

    output_wires.sort(key=lambda x: int(x[1:]))

    return output_wires

def find_output_gate_dependency(output_wire, gates):
    output_gate_dependency_id = set()
    queue = set()
    queue.add(output_wire)
    while queue:
        wire = queue.pop()
        for i_gate, (wire_input1, wire_input2, op, wire_output) in enumerate(gates):
            if wire == wire_output:
                output_gate_dependency_id.add(i_gate)
                if wire_input1[0] not in ['x', 'y']:
                    queue.add(wire_input1)
                if wire_input2[0] not in ['x', 'y']:
                    queue.add(wire_input2)

                break

    return output_gate_dependency_id

def check_bit_sum(i_bit, n_bits, gates, map_output_wire_to_gate):
    initial_wires = {}
    if i_bit < 10:
        i_bit_str = '0' + str(i_bit)
    else:
        i_bit_str = str(i_bit)

    for i in range(n_bits):
        if i < 10:
            initial_wires['x0' + str(i)] = 0
            initial_wires['y0' + str(i)] = 0
        else:
            initial_wires['x' + str(i)] = 0
            initial_wires['y' + str(i)] = 0

    # x = 0, y = 0
    wires = initial_wires.copy()
    number = run_circuit(wires, gates, map_output_wire_to_gate)
    if number != 0:
        print("Error in bit {0}: case 1".format(i_bit))
        print(wires)
        print(number)
        return False

    # x = 1, y = 0
    wires = initial_wires.copy()
    wires['x' + i_bit_str] = 1
    number = run_circuit(wires, gates, map_output_wire_to_gate)
    if number != 2 ** i_bit:
        print("Error in bit {0}: case 2".format(i_bit))
        print(wires)
        print(number)
        return False

    # x = 0, y = 1
    wires = initial_wires.copy()
    wires['y' + i_bit_str] = 1
    number = run_circuit(wires, gates, map_output_wire_to_gate)
    if number != 2 ** i_bit:
        print("Error in bit {0}: case 3".format(i_bit))
        print(wires)
        print(number)
        return False

    # x = 1, y = 1
    wires = initial_wires.copy()
    wires['x' + i_bit_str] = 1
    wires['y' + i_bit_str] = 1
    number = run_circuit(wires, gates, map_output_wire_to_gate)
    if number != 2 ** (i_bit + 1):
        print("Error in bit {0}: case 4".format(i_bit))
        print(wires)
        print(number)
        return True

    return True

def find_wrong_bits(n_bits, gates, map_output_wire_to_gate):
    wrong_bits = set()
    for i_bit in range(n_bits):
        print("Checking bit {0}".format(i_bit))
        if not check_bit_sum(i_bit, n_bits, gates, map_output_wire_to_gate):
            wrong_bits.add(i_bit)

    return sorted(wrong_bits)

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)
    input_wires, gates, map_output_wire_to_gate = parse_data(data)

    if part == '1':
       res = run_circuit(input_wires, gates, map_output_wire_to_gate)

       print("Result of part 1: {0}".format(res))

    elif part == '2':
        n_bits = sum([1 for wire in input_wires if wire[0] == 'x'])
        all_wires = find_all_wires(input_wires, gates)
        output_wires = extract_output_wires(all_wires)
        print("Output wires: {0}".format(output_wires))
        output_wires_dependency_id = [find_output_gate_dependency(x, gates) for x in output_wires]
        for output_wire, output_wire_dependency_id in zip(output_wires, output_wires_dependency_id):
            output_wire_dependency = [gates[x][3] for x in output_wire_dependency_id]
            print("Output wire {0} dependency: {1}".format(output_wire, output_wire_dependency))


        print(find_wrong_bits(n_bits, gates, map_output_wire_to_gate))

    #     res = 0

    #     print("Result of part 2: {0}".format(res))