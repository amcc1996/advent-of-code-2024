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

def run_program_until_output(A, instructions):
    """
    This program runs the instructions until it finds an output.
    This is not general, and is based on a previous inspection of the input data, so that
    we know that the initial values of B and C registers do not matter, as they are overwritten
    by the program. In addiiton, the instruction position is initially set to 0, because the
    program is designed to repeat running from the beggining until it finds an output instruction.
    """
    output = []
    computer = {'A' : A,
                'B' : 0,
                'C' : 0,
                'pos' : 0}
    while computer['pos'] < len(instructions):
        parse_instruction(instructions, computer, output)
        if len(output) > 0:
            break

    return output[0], computer['A']

def run_program_with_cache_and_checks(A, instructions, program, cache):
    """
    This code si not general, and is based on a previous inspection of the input data.
    """
    output = []
    n_output = 0
    finished = False
    while not finished:
        if A in cache:
            out, A = cache[A]
        else:
            out, A = run_program_until_output(A, instructions)
            cache[A] = (out, A)

        if n_output >= len(instructions):
            finished = True

        elif out != instructions[n_output]:
            finished = True

        if A == 0:
            finished = True

        output.append(out)
        n_output += 1

    output_str = ",".join([str(x) for x in output])
    found = program == output_str

    return found, output_str

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
        A = 2**(3 * (len(instructions) - 1))
        A = 0
        found = False
        program = ",".join([str(x) for x in instructions])
        cache = {}
        count = 1
        while not found:
            found, output_str = run_program_with_cache_and_checks(A, instructions, program, cache)
            output_list = [int(x) for x in output_str.split(',')]
            if len(output_list) >= count:
                if (all(a==b for a, b in zip(output_list[0:count],instructions[0:count]))):
                    print("Count: ", count)
                    count += 1
                    print("{0:>10}   {1:32b}   {2:>20}".format(A, A, output_str))

            # Increment the trial
            if not found:
                A += 1
                # if i_digit == 2**n_digits_analysis - 1:
                #     i_digit = 0
                #     A = A_start * 2
                #     A_start = A
                # else:
                #     A += 1
                #     i_digit += 1

        result2 = A
        print("Result of part 2: ", result2)