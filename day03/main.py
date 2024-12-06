import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0]

    def find_substring_pos(string, substring):
        list_pos = []
        start = 0
        pos = string[start:].find(substring)
        while pos != -1:
            list_pos.append(pos + start)
            start = pos + len(substring) + start
            pos = string[start:].find(substring)

        return list_pos

    if part == '1':
        result1 = 0
        for line in data:
            data_split = line.split('mul(')
            for word in data_split:
                word_split = word.split(')')[0].split(',')
                if word_split[0].isnumeric() and word_split[1].isnumeric() and len(word_split) == 2:
                    result1 += int(word_split[0]) * int(word_split[1])

        print("Result of part 1: ", result1)

    elif part == '2':
        result2 = 0
        data =''.join(data)
        for line in [data]:
            mul_pos   = find_substring_pos(line, "mul(")
            do_pos    = [-1] + find_substring_pos(line, "do()") + [len(line) + 2]
            dont_pos  = [-2] + find_substring_pos(line, "don't()") + [len(line) + 1]
            for pos in mul_pos:
                aux_do = [pos - x for x in do_pos if x < pos]
                last_do   = do_pos[aux_do.index(min(aux_do))]
                aux_dont = [pos - x for x in dont_pos if x < pos]
                last_dont = dont_pos[aux_dont.index(min(aux_dont))]
                word_split = line[pos+len('mul('):].split(')')[0].split(',')
                if word_split[0].isnumeric() and word_split[1].isnumeric() and len(word_split) == 2:
                    if last_do > last_dont:
                        result2 += int(word_split[0]) * int(word_split[1])

        print("Result of part 2: ", result2)