import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def adv(literal_operand, combo_operand, computer, output):
    computer['A'] = int(computer['A'] / 2 ** combo_operand)

def bxl(literal_operand, combo_operand, computer, output):
    computer['B'] = computer['B'] ^ literal_operand

def bst(literal_operand, combo_operand, computer, output):
    computer['B'] = combo_operand % 8

def jnz(literal_operand, combo_operand, computer, output):
    if computer['A'] != 0: computer['pos'] = literal_operand

def bxc(literal_operand, combo_operand, computer, output):
    computer['B'] = computer['B'] ^ computer['C']

def out(literal_operand, combo_operand, computer, output):
    output.append(combo_operand % 8)

def bdv(literal_operand, combo_operand, computer, output):
    computer['B'] = int(computer['A'] / 2 ** combo_operand)

def cdv(literal_operand, combo_operand, computer, output):
    computer['C'] = int(computer['A'] / 2 ** combo_operand)

OPCODE_FUNC_MAP = {0: adv, 1: bxl, 2: bst, 3: jnz, 4: bxc, 5: out, 6: bdv, 7: cdv}

def get_combo_operand(literal_operand, computer):
    if literal_operand >= 0 and literal_operand <= 3:
        return literal_operand

    elif literal_operand == 4:
        return computer['A']

    elif literal_operand == 5:
        return computer['B']

    elif literal_operand == 6:
        return computer['C']

    elif literal_operand == 7:
        return None

def parse_instruction(instructions, computer, output):
    pos = computer['pos']
    opcode = instructions[pos]
    literal_operand = instructions[pos + 1]
    combo_operand = get_combo_operand(literal_operand, computer)
    OPCODE_FUNC_MAP[opcode](literal_operand, combo_operand, computer, output)
    if not(opcode == 3 and pos != computer['pos']):
        computer["pos"] += 2

def run_program(instructions, computer):
    output = []
    while computer['pos'] < len(instructions):
        parse_instruction(instructions, computer, output)

    return ",".join([str(x) for x in output])

def run_program_with_checks(instructions, program, computer):
    output = []
    while computer['pos'] < len(instructions):
        parse_instruction(instructions, computer, output)
        min_len = min(len(instructions), len(output))
        if not(all([a == b for a, b in zip(output[0:min_len], instructions[0:min_len])])):
            return False, ",".join([str(x) for x in output])

        if len(output) > len(instructions):
            return False, ",".join([str(x) for x in output])

    output_str = ",".join([str(x) for x in output])

    return output_str == program, output_str

def run_program_part2_until_output(A):
    B = A % 8
    B = B ^ 5
    C = int(A / 2**B)
    B = B ^ C
    B = B ^ 6

    return B % 8

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)

    computer = {'A' : int(data[0][0].split(":")[1]),
                'B' : int(data[0][1].split(":")[1]),
                'C' : int(data[0][2].split(":")[1]),
                'pos' : 0}
    instructions = [int(x) for x in data[1][0].split(":")[1].split(",")]

    if part == '1':
        print("Result of part 1: ", run_program(instructions, computer))

    elif part == '2':
        program = ",".join([str(x) for x in instructions])
        n_parse_bits = 10 # number of bits to parse
        map_A_to_output = [run_program_part2_until_output(A) for A in range(2**n_parse_bits)]
        candidates = []
        n_bit_shift = 3
        for i in range(len(instructions)):
            if i == 0:
                for A, output in enumerate(map_A_to_output):
                    if output == instructions[i]:
                        candidates.append(A)
            else:
                new_candidates = []
                for j in range(2**n_bit_shift):
                    for A in candidates:
                        A_trial = A + (j << (n_parse_bits + (i-1) * n_bit_shift))
                        if map_A_to_output[A_trial >> (i * n_bit_shift)] == instructions[i]:
                            new_candidates.append(A_trial)

                candidates = [x for x in new_candidates]

        result2 = min(candidates)
        print("Result of part 2: ", result2)