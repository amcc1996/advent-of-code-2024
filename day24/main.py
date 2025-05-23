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

def find_all_wires(wires, gates):
    all_wires = set()
    for wire in wires:
        all_wires.add(wire)

    for gate in gates:
        wire_input1, wire_input2, op, wire_output = gate
        all_wires.add(wire_input1)
        all_wires.add(wire_input2)
        all_wires.add(wire_output)

    return all_wires

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

def check_bit_sum(i_bit, n_bits, gates):
    initial_wires = {}
    for i in range(n_bits):
        initial_wires['x' + str(i)] = 0
        initial_wires['y' + str(i)] = 0

    output_wire_1 = 'z' + str(i_bit)
    output_wire_2 = 'z' + str(i_bit + 1)

    # x = 0, y = 0
    wires = initial_wires.copy()
    run_circuit(initial_wires, gates)
    if not (wires[output_wire_1] == 0 and wires[output_wire_2] == 0):
        return False

    # x = 1, y = 0
    wires = initial_wires.copy()
    wires['x' + str(i_bit)] = 1
    run_circuit(initial_wires, gates)
    if not (wires[output_wire_1] == 1 and wires[output_wire_2] == 0):
        return False

    # x = 0, y = 1
    wires = initial_wires.copy()
    wires['y' + str(i_bit)] = 1
    run_circuit(initial_wires, gates)
    if not (wires[output_wire_1] == 1 and wires[output_wire_2] == 0):
        return False

    # x = 1, y = 1
    wires = initial_wires.copy()
    wires['x' + str(i_bit)] = 1
    wires['y' + str(i_bit)] = 1
    run_circuit(initial_wires, gates)
    if not (wires[output_wire_1] == 0 and wires[output_wire_2] == 1):
        return False

    return True

def find_wrong_bits(n_bits, gates):
    wrong_bits = set()
    for i_bit in range(n_bits):
        print("Checking bit {0}".format(i_bit))
        if not check_bit_sum(i_bit, n_bits, gates):
            wrong_bits.add(i_bit)

    return wrong_bits

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)
    wires, gates = parse_data(data)

    if part == '1':
        res = run_circuit(wires, gates)

        print("Result of part 1: {0}".format(res))

    elif part == '2':
        n_bits = sum([1 for wire in wires if wire[0] == 'x'])
        all_wires = find_all_wires(wires, gates)
        output_wires = extract_output_wires(all_wires)
        # print("Output wires: {0}".format(output_wires))
        output_wires_dependency_id = [find_output_gate_dependency(x, gates) for x in output_wires]
        # for output_wire, output_wire_dependency_id in zip(output_wires, output_wires_dependency_id):
        #     output_wire_dependency = [gates[x][3] for x in output_wire_dependency_id]
        #     print("Output wire {0} dependency: {1}".format(output_wire, output_wire_dependency))


        print(find_wrong_bits(n_bits, gates))

        res = 0

        print("Result of part 2: {0}".format(res))