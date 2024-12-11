import os
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '../utils'))

from utils import get_input_filename, read_input_file

def defragment_block(id_defrag, pos_block, pos_start, files, empty):
    while files[pos_block] > 0:
        id_defrag.append(pos_block)
        files[pos_block] -= 1
        empty[pos_start] -= 1
        if empty[pos_start] == 0 and pos_block > pos_start + 1:
            while empty[pos_start] == 0:
                pos_start += 1
                id_defrag.extend([pos_start for _ in range(files[pos_start])])

    return pos_block, pos_start

def process_empty_space(id_defrag, id_defrag_end, pos_block, pos_start, files, empty):
    print("emtpy space ", pos_start, "  size : ", empty[pos_start])
    while empty[pos_start] > 0 and pos_block > pos_start:
        print("  block ", pos_block, "  size : ", files[pos_block])
        if (files[pos_block] < empty[pos_start]):
            id_defrag.extend([pos_block for _ in range(files[pos_block])])
            empty[pos_start] -= files[pos_block]
            files[pos_block] = 0
            pos_block -= 1
        else:
            pos_block -= 1
            id_defrag_end = [pos_block for _ in range(empty[pos_block])] + id_defrag_end

    return pos_block, pos_start

def compute_checksum(id_defrag):
    return sum(i * idx for idx, i in enumerate(id_defrag))

if __name__ == '__main__':
    filename, part = get_input_filename(os.path.dirname(__file__))
    data = read_input_file(filename)[0][0]
    files = [int(data[i]) for i in range(0,len(data),2)]
    empty = [int(data[i]) for i in range(1,len(data),2)]

    if part == '1':
        pos_start = 0
        pos_block = len(files) - 1
        id_defrag = [pos_start for _ in range(files[pos_start])]
        while pos_start < pos_block:
            pos_block, pos_start = defragment_block(id_defrag, pos_block, pos_start, files, empty)
            pos_block -= 1

        print("Result of part 1: ", compute_checksum(id_defrag))

    elif part == '2':
        pos_start = 0
        pos_block = len(files) - 1
        id_defrag = [pos_start for _ in range(files[pos_start])]
        id_defrag_end = []
        while pos_start < pos_block:
            pos_block, pos_start = process_empty_space(id_defrag, id_defrag_end, pos_block, pos_start, files, empty)
            pos_start += 1
            print(id_defrag)
            print(id_defrag_end)

        print(id_defrag_end, id_defrag)
        print("Result of part 2: ", compute_checksum(id_defrag + id_defrag_end))