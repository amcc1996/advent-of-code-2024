import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def defragment_block(id_defrag, pos_block, files, pos_files, empty, pos_empty):
    while files[pos_block] > 0:
        id_defrag.append(pos_block)
        files[pos_block] -= 1
        empty[pos_empty] -= 1
        if empty[pos_empty] == 0:
            pos_empty += 1
            if pos_files < pos_block:
                pos_files += 1
                id_defrag.extend([pos_files for _ in range(files[pos_files])])

    return pos_files, pos_empty

def compute_checksum(id_defrag):
    return sum(i * idx for idx, i in enumerate(id_defrag))

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0][0]

    if part == '1':
        files = [int(data[i]) for i in range(0,len(data),2)]
        empty = [int(data[i]) for i in range(1,len(data),2)]
        pos_files = 0
        pos_empty = 0
        pos_block = len(files) - 1
        id_defrag = [pos_files for _ in range(files[pos_files])]
        while pos_files < pos_block:
            pos_files, pos_empty = defragment_block(id_defrag, pos_block, files, pos_files, empty, pos_empty)
            pos_block -= 1
            print(" ")
            print(" ".join([str(i) for i in id_defrag]))

        # print(id_defrag)
        print("Result of part 1: ", compute_checksum(id_defrag))

    # elif part == '2':
    #     antinodes = []
    #     n_rows = len(data)
    #     n_cols = len(data[0])
    #     map_antena_pos = parse_map(data)
    #     for freq in map_antena_pos:
    #         process_frequency_part2(freq, map_antena_pos, antinodes, len(data), len(data[0]))

    #     result2 = len(antinodes)
    #     if verbose:
    #         for x,y in antinodes:
    #             data[x] = data[x][0:y] + "#" + data[x][y+1:]

    #         for line in data:
    #             print(''.join(line))

    #     print("Result of part 2: ", result2)