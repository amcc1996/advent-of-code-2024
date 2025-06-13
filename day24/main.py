import os
import sys

import math
from collections import deque
from itertools import combinations

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
    '''Parse the input data into input wires, gates, and a mapping of output wires to gate indices.

    Parameters
    ----------
    data : list of list of str
        The input data, where the first part contains input wires and the second part contains gates.

    Returns
    -------
    input_wires : dict[str, int]
        A dictionary mapping input wire names to their integer values.
    gates : list[tuple[str, str, function, str]]
        A list of tuples representing gates, where each tuple contains two input wires, an operation function, and an output wire.
    map_output_wire_to_gate : dict[str, int]
        A dictionary mapping output wire names to their corresponding gate indices.
    '''
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

def compute_number(wires, output_wires):
    '''Compute the integer value represented by the wires.

    It only requires the output wires starting with z.

    Parameters
    ----------
    wires : dict[str, int]
        A dictionary mapping wire names to their integer values.
    output_wires : list[str]
        A list of the output wires
    Returns
    -------
    int
        The computed integer value based on the wires.
    '''
    num = 0
    for wire in output_wires:
        bit_pos = int(wire[1:])
        num += 2 ** bit_pos * wires[wire]

    return num

def run_circuit(input_wires, output_wires, wires, gates, map_output_wire_to_gate, sol_sequence=None):
    '''Run the circuit with the given input wires and gates.

    Parameters
    ----------
    input_wires : dict[str, int]
        A dictionary mapping input wire names to their values.
    output_wires : list[str]
        A list of output wire names.
    wires : dict[str, int]
        A dictionary mapping wire names to their integer values.
    gates : list[tuple[str, str, function, str]]
        A list of tuples representing gates, where each tuple contains two input wires, an operation function, and an output wire.
    map_output_wire_to_gate : dict[str, int]
        A dictionary mapping output wire names to their corresponding gate indices.
    sol_sequence : list[str], optional
        A list of output wires in the order they should be computed. If provided, it will be used instead of computing the circuit normally.

    Returns
    -------
    int
        The computed integer value based on the output wires.
    list[str]
        A list of output wires in the order they were computed.
    bool
        A boolean indicating whether the circuit finished computing all output wires.
    '''
    queue = deque()
    for wire in wires:
        queue.append(wire)
        if wire in input_wires:
            wires[wire] = input_wires[wire]
        else:
            wires[wire] = None

    # If solution squence is available use it instead
    if sol_sequence is not None:
        for wire in sol_sequence:
            id_gate = map_output_wire_to_gate[wire]
            wire_input1, wire_input2, op, wire_output = gates[id_gate]
            wires[wire] = op(wires[wire_input1], wires[wire_input2])

        return compute_number(wires, output_wires), [], True

    sequence = []
    n_iter = 0
    cycling_counter = 0
    while queue:
        n_iter += 1
        wire = queue.popleft()
        if wires[wire] is None:
            id_gate = map_output_wire_to_gate[wire]
            wire_input1, wire_input2, op, wire_output = gates[id_gate]
            if (wires[wire_input1] is not None) and (wires[wire_input2] is not None):
                wires[wire] = op(wires[wire_input1], wires[wire_input2])
                sequence.append(wire_output)
                cycling_counter = 0
            else:
                queue.append(wire)
                cycling_counter += 1
                if cycling_counter > len(queue):
                    break
                continue

    finished = len(queue) == 0
    return compute_number(wires, output_wires) if finished else None, sequence, finished

def find_all_wires(input_wires, gates):
    '''Find all unique wires used in the circuit.

    Parameters
    ----------
    input_wires : dict[str, int]
        A dictionary mapping input wire names to their integer values.
    gates : list[tuple[str, str, function, str]]
        A list of tuples representing gates, where each tuple contains two input wires, an operation function, and an output wire.

    Returns
    -------
    list[str]
        A sorted list of all unique wire names used in the circuit.
    '''
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
    '''Extract output wires from the list of all wires. Output wires are those that start with 'z'.

    Parameters
    ----------
    all_wires : list[str]
        A sorted list of all unique wire names used in the circuit.

    Returns
    -------
    list[str]
        A sorted list of output wire names, which are those that start with 'z'.
    '''
    output_wires = []
    for wire in all_wires:
        if wire[0] == 'z':
            output_wires.append(wire)

    output_wires.sort(key=lambda x: int(x[1:]))

    return output_wires

def find_output_gate_dependency(output_wire, gates):
    '''For a given wire, find the indices of gates which it depends on.

    Parameters
    ----------
    output_wire : str
        The output wire for which to find the gate dependencies.
    gates : list[tuple[str, str, function, str]]
        A list of tuples representing gates, where each tuple contains two input wires, an operation function, and an output wire.

    Returns
    -------
    set[int]
        A set of indices of gates that the output wire depends on.
    '''
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

def check_bit_sum(i_bit, input_wires, output_wires, wires, gates, map_output_wire_to_gate):
    '''Check if the sum of two bits is correctly computed by the circuit.

    Parameters
    ----------
    i_bit : int
        The index of the bit to check (0-indexed).
    input_wires : dict[str, int]
        A dictionary mapping input wire names to their values.
    output_wires : list[str]
        A list of output wire names.
    wires : dict[str, int]
        A dictionary mapping wire names to their integer values.
    n_bits : int
        The total number of bits in the circuit.
    gates : list[tuple[str, str, function, str]]
        A list of tuples representing gates, where each tuple contains two input wires, an operation function, and an output wire.
    map_output_wire_to_gate : dict[str, int]
        A dictionary mapping output wire names to their corresponding gate indices.

    Returns
    -------
    bool
        True if the bit sum is correctly computed, False otherwise.
    '''
    if i_bit < 10:
        i_bit_str = '0' + str(i_bit)
    else:
        i_bit_str = str(i_bit)

    # x = 0, y = 0
    input_wires['x' + i_bit_str] = 0
    input_wires['y' + i_bit_str] = 0
    number, sequence, finished = run_circuit(input_wires, output_wires, wires, gates, map_output_wire_to_gate)
    if not finished:
        return False

    if number != 0:
        return False

    # x = 1, y = 0
    input_wires['x' + i_bit_str] = 1
    input_wires['y' + i_bit_str] = 0
    number, _, _ = run_circuit(input_wires, output_wires, wires, gates, map_output_wire_to_gate, sequence)
    if number != 2 ** i_bit:
        input_wires['x' + i_bit_str] = 0
        return False

    # x = 0, y = 1
    input_wires['x' + i_bit_str] = 0
    input_wires['y' + i_bit_str] = 1
    number, _, _ = run_circuit(input_wires, output_wires, wires, gates, map_output_wire_to_gate, sequence)
    if number != 2 ** i_bit:
        input_wires['y' + i_bit_str] = 0
        return False

    # x = 1, y = 1
    input_wires['x' + i_bit_str] = 1
    input_wires['y' + i_bit_str] = 1
    number, _, _ = run_circuit(input_wires, output_wires, wires, gates, map_output_wire_to_gate, sequence)
    if number != 2 ** (i_bit + 1):
        input_wires['x' + i_bit_str] = 0
        input_wires['y' + i_bit_str] = 0
        return True

    input_wires['x' + i_bit_str] = 0
    input_wires['y' + i_bit_str] = 0

    return True

def find_wrong_bits(n_bits, input_wires, output_wires, wires, gates, map_output_wire_to_gate):
    '''Find bits that are not correctly computed by the circuit.

    Parameters
    ----------
    n_bits : int
        The total number of bits in the circuit.
    input_wires : dict[str, int]
        A dictionary mapping input wire names to their values.
    output_wires : list[str]
        A list of output wire names.
    wires : dict[str, int]
        A dictionary mapping wire names to their integer values.
    gates : list[tuple[str, str, function, str]]
        A list of tuples representing gates, where each tuple contains two input wires, an operation function, and an output wire.
    map_output_wire_to_gate : dict[str, int]
        A dictionary mapping output wire names to their corresponding gate indices.

    Returns
    -------
    list[int]
        A sorted list of indices of bits that are not correctly computed by the circuit.
    '''
    wrong_bits = set()
    for i_bit in range(n_bits):
        if not check_bit_sum(i_bit, input_wires, output_wires, wires, gates, map_output_wire_to_gate):
            wrong_bits.add(i_bit)

    return sorted(wrong_bits)

def swap_wires(wire1, wire2, gates, map_output_wire_to_gate):
    '''Swap two wires in the circuit.

    Parameters
    ----------
    wire1 : str
        The first wire to swap.
    wire2 : str
        The second wire to swap.
    gates : list[tuple[str, str, function, str]]
        A list of tuples representing gates, where each tuple contains two input wires, an operation function, and an output wire.
    map_output_wire_to_gate : dict[str, int]
        A dictionary mapping output wire names to their corresponding gate indices.
    '''
    id_gate1 = map_output_wire_to_gate[wire1]
    id_gate2 = map_output_wire_to_gate[wire2]

    tmp_gate1 = gates[id_gate1]
    tmp_gate2 = gates[id_gate2]

    gates[id_gate1] = (tmp_gate1[0], tmp_gate1[1], tmp_gate1[2], wire2)
    gates[id_gate2] = (tmp_gate2[0], tmp_gate2[1], tmp_gate2[2], wire1)\

    map_output_wire_to_gate[wire1] = id_gate2
    map_output_wire_to_gate[wire2] = id_gate1

def find_swapped_wires(wrong_bits, n_bits, input_wires, output_wires, wires, gates, map_output_wire_to_gate, output_wires_dependency):
    '''Find the swapped wires.

    Parameters
    ----------
    wrong_bits : list[int]
        A sorted list of indices of bits that are not correctly computed by the circuit.
    n_bits : int
        The total number of bits in the circuit.
    input_wires : dict[str, int]
        A dictionary mapping input wire names to their values.
    output_wires : list[str]
        A list of output wire names.
    wires : dict[str, int]
        A dictionary mapping wire names to their integer values.
    gates : list[tuple[str, str, function, str]]
        A list of tuples representing gates, where each tuple contains two input wires, an operation function, and an output wire.
    map_output_wire_to_gate : dict[str, int]
        A dictionary mapping output wire names to their corresponding gate indices.
    output_wires_dependency : dict[str, list[str]]
        A dictionary mapping output wire names to a list of gate indices they depend on.
    '''
    candidates = set()
    for wrong_bit in wrong_bits:
        if wrong_bit < 10:
            i_bit_str = '0' + str(wrong_bit)
        else:
            i_bit_str = str(wrong_bit)

        output_wire = 'z' + i_bit_str
        for wire in output_wires_dependency[output_wire]:
            candidates.add(wire)

    candidates = sorted(candidates)

    # First find all swaps that solves the lowest bit
    swaps_that_solve_first_bit= []
    n_combinations = math.comb(len(candidates), 2)
    for i, (wire1, wire2) in enumerate(combinations(candidates, 2)):
        print(" {} of {}".format(i + 1, n_combinations))
        if wire1 == wire2:
            continue
        swap_wires(wire1, wire2, gates, map_output_wire_to_gate)
        wrong_bits_after_swap = find_wrong_bits(n_bits, input_wires, output_wires, wires, gates, map_output_wire_to_gate)
        min_wrong_bit_1 = min(wrong_bits_after_swap)
        if min_wrong_bit_1 > wrong_bits[0]:
            print("Found a swap that solves the first bit: {0} <-> {1}".format(wire1, wire2))
            swaps_that_solve_first_bit.append((wire1, wire2, min_wrong_bit_1))

        swap_wires(wire1, wire2, gates, map_output_wire_to_gate)

    print("Found {0} swaps that solve the first bit".format(len(swaps_that_solve_first_bit)))
    for wire1, wire2, _ in swaps_that_solve_first_bit:
        print("Swap {0} <-> {1}".format(wire1, wire2))

    swaps_that_solve_second_bit= []
    for wire1, wire2, min_wrong_bit_1 in swaps_that_solve_first_bit:
        for i, (wire3, wire4) in enumerate(combinations(candidates, 2)):
            print(" {} of {}".format(i + 1, n_combinations))
            used_wires = list(sorted(set((wire1, wire2) + (wire3, wire4))))
            if len(used_wires) != 4:
                continue
            swap_wires(wire1, wire2, gates, map_output_wire_to_gate)
            swap_wires(wire3, wire4, gates, map_output_wire_to_gate)
            wrong_bits_after_swap = find_wrong_bits(n_bits, input_wires, output_wires, wires, gates, map_output_wire_to_gate)
            min_wrong_bit_2 = min(wrong_bits_after_swap)
            if min_wrong_bit_2 >= min_wrong_bit_1:
                print("Found a swap that solves the first bit: {0} <-> {1}".format(wire3, wire4))
                swaps_that_solve_second_bit.append(((wire1, wire2, wire3, wire4, min_wrong_bit_2)))

            swap_wires(wire1, wire2, gates, map_output_wire_to_gate)
            swap_wires(wire3, wire4, gates, map_output_wire_to_gate)

    print("Found {0} swaps that solve the second bit".format(len(swaps_that_solve_second_bit)))
    for wire1, wire2 in swaps_that_solve_second_bit:
        print("Swap {0} <-> {1}  |  {2} <-> {3}".format(wire1, wire2, wire3, wire4))

    # for pair1, pair2, pair3, pair4 in combinations(swaps_that_solve_one_problem, 4):
    #     used_wires = list(sorted(set(pair1 + pair2 + pair3 + pair4)))
    #     if len(used_wires) != 8:
    #         continue

    #     swap_wires(pair1[0], pair1[1], gates, map_output_wire_to_gate)
    #     swap_wires(pair2[0], pair2[1], gates, map_output_wire_to_gate)
    #     swap_wires(pair3[0], pair3[1], gates, map_output_wire_to_gate)
    #     swap_wires(pair4[0], pair4[1], gates, map_output_wire_to_gate)
    #     wrong_bits_after_swap = find_wrong_bits(n_bits, input_wires, output_wires, wires, gates, map_output_wire_to_gate)
    #     if len(wrong_bits_after_swap) == 0:
    #         print("Found a solution with swaps:")
    #         print("Swap {0} <-> {1}".format(pair1[0], pair1[1]))
    #         print("Swap {0} <-> {1}".format(pair2[0], pair2[1]))
    #         print("Swap {0} <-> {1}".format(pair3[0], pair3[1]))
    #         print("Swap {0} <-> {1}".format(pair4[0], pair4[1]))
    #         print("Wrong bits after swap: {0} / {1}".format(len(wrong_bits_after_swap), len(wrong_bits)))
    #         print("Result: {0}".format(",".join(used_wires)))

    #     swap_wires(pair1[1], pair1[0], gates, map_output_wire_to_gate)
    #     swap_wires(pair2[1], pair2[0], gates, map_output_wire_to_gate)
    #     swap_wires(pair3[1], pair3[0], gates, map_output_wire_to_gate)
    #     swap_wires(pair4[1], pair4[0], gates, map_output_wire_to_gate)

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)
    input_wires, gates, map_output_wire_to_gate = parse_data(data)
    all_wires = find_all_wires(input_wires, gates)
    output_wires = extract_output_wires(all_wires)
    wires =  {x: None for x in all_wires}

    if part == '1':
       res, _, _ = run_circuit(input_wires, output_wires, wires, gates, map_output_wire_to_gate)

       print("Result of part 1: {0}".format(res))

    elif part == '2':
        for wire in input_wires:
            input_wires[wire] = 0

        n_bits = sum([1 for wire in input_wires if wire[0] == 'x'])
        output_wires_dependency_id = [find_output_gate_dependency(x, gates) for x in output_wires]
        output_wires_dependency = {}
        for output_wire, output_wire_dependency_id in zip(output_wires, output_wires_dependency_id):
            output_wires_dependency[output_wire] = [gates[x][3] for x in output_wire_dependency_id]

        wrong_bits = find_wrong_bits(n_bits, input_wires, output_wires, wires, gates, map_output_wire_to_gate)
        find_swapped_wires(wrong_bits, n_bits, input_wires, output_wires, wires, gates, map_output_wire_to_gate, output_wires_dependency)

    #     res = 0

    #     print("Result of part 2: {0}".format(res))