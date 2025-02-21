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

def run_program_with_checks(instructions, computer, program):
    output = []
    while computer['pos'] < len(instructions):
        parse_instruction(instructions, computer, output)
        output_str = ",".join([str(x) for x in output])

        if len(output_str) > len(program):
            return False, output_str

        if output_str != program[0:len(output_str)]:
            return False, output_str

    return output_str == program, output_str

def parse_until_output(instructions, computer):
    output = []
    pos_min = computer['pos']
    pos_max = computer['pos']
    while computer['pos'] < len(instructions):
        if computer['pos'] + 1 > pos_max:
            pos_max = computer['pos'] + 1
        parse_instruction(instructions, computer, output)

        if len(output) > 0:
            break

    return output[0] if len(output)>0 else None, pos_max - pos_min + 1, computer['pos'] < len(instructions)

def get_computer_hash(computer):
    return (computer['A'], computer['B'], computer['C'], computer['pos'])

def run_program_with_cache(instructions, computer, program, map_state_to_instructions, map_state_instructions_to_state_output):
    output = []
    is_running = True
    instructions_str = "".join([str(x) for x in instructions])
    while is_running:
        needs_parse = True
        hash_computer = get_computer_hash(computer)
        if hash_computer in map_state_to_instructions:
            for saved_blocks in map_state_to_instructions[hash_computer]:
                if saved_blocks == instructions_str[computer['pos']:computer['pos']+len(saved_blocks)]:
                    computer = map_state_instructions_to_state_output[(hash_computer, saved_blocks)][0]
                    out = map_state_instructions_to_state_output[(hash_computer, saved_blocks)][1]
                    if out is None:
                        is_running = False
                    else:
                        output.append(out)
                    needs_parse = False
                    break

        if needs_parse:
            save_computer = computer.copy()
            hash_save_computer = get_computer_hash(save_computer)
            out, n_instructions, is_running = parse_until_output(instructions, computer)
            if is_running:
                output.append(out)
            instructions_block = instructions_str[save_computer['pos']:save_computer['pos']+n_instructions]
            if hash_save_computer not in map_state_to_instructions:
                map_state_to_instructions[hash_save_computer] = [instructions_block]
                map_state_instructions_to_state_output[(hash_save_computer, instructions_block)] = (computer, out)
            else:
                map_state_to_instructions[hash_save_computer].append(instructions_block)
                map_state_instructions_to_state_output[(hash_save_computer, instructions_block)].append((computer, out))

        output_str = ",".join([str(x) for x in output])
        if len(output_str) > len(program):
            return False, ",".join([str(x) for x in output])

        if output_str != program[0:len(output_str)]:
            return False, ",".join([str(x) for x in output])

    return output_str == program, output_str

def run_program_smart_with_cache(instructions, computer, program, cache):
    output = []
    counter = 0
    while computer['pos'] < len(instructions):
        A_input = computer['A']
        if A_input in cache:
            out, A_output = cache[A_input]
            computer['A'] = A_output
        else:
            out, _, _ = parse_until_output(instructions, computer)
            A_output = computer['A']
            cache[A_input] = [out, A_output]

        output.append(out)
        counter += 1
        if output[counter] != program[2*counter-1]:
            return False, output
        output_str = ",".join([str(x) for x in output])
        if len(output_str) > len(program):
            return False, output_str 

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
        i = 0
        found = False
        program = ",".join([str(x) for x in instructions])
        map_state_to_instructions = {}
        map_state_instructions_to_state_output = {}
        n_correct = 1
        while not found:
            computer = {'A' : i,
                        'B' : int(data[0][1].split(":")[1]),
                        'C' : int(data[0][2].split(":")[1]),
                        'pos' : 0}
            # found, output_str = run_program_with_cache(instructions, computer, program, map_state_to_instructions, map_state_instructions_to_state_output)
            found, output_str = run_program_with_checks(instructions, computer, program)

            # Print the trials that have some corerct numbers
            # print(i, " ", output_str, " ", program, program[0:2 * n_correct - 1], output_str == program[0:2 * n_correct - 1])
            print("{0:>10}   {1:32b}   {2:>20}".format(i, i, output_str))
            if (len(output_str) >= 2 * n_correct - 1):
                count = 0
                for pos, num in enumerate(output_str.split(',')):
                    if num == program[2 * pos]:
                        count += 1
                    else:
                        break
                if count == n_correct:
                    # print("{0:>10}   {1:32b}   {2:>20}    n_correct = {3}".format(i, i, output_str, n_correct))
                    n_correct += 1 # Comment to check for all occurrence with n_correct numbers, and uncomment to check for the first occurrence

            # Increment the trial
            if not found:
                i += 1

        result2 = i
        print("Result of part 2: ", result2)